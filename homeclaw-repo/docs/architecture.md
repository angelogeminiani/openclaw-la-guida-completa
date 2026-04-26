# HomeClaw architecture

This document explains how the pieces of HomeClaw fit together: the
processes, the protocols, and the data flow for a single voice command.

---

## High-level picture

```
                        ┌──── HUB (Raspberry Pi 5) ──────────────────┐
                        │                                            │
  microphone ──audio──▶ │ wyoming-satellite ─event─▶ homeclaw-bridge │
  speaker   ◀──audio─── │       ▲                         │          │
                        │       │                         │          │
                        │ wyoming-openwakeword            │          │
                        │ wyoming-faster-whisper          ▼          │
                        │ wyoming-piper           openclaw-gateway   │
                        │                               │            │
                        │                        HomeClaw agent      │
                        │                        (via OpenClaw)      │
                        └────────────────────────────────┼───────────┘
                                                         │
                                                         ▼
                                   Home Assistant, Google (gog), Telegram, etc.
```

Five long-running processes:

1. **wyoming-satellite** — owns the audio devices. Captures microphone,
   streams PCM to openWakeWord for trigger, then to Whisper for ASR, then
   sends results as Wyoming events.
2. **wyoming-openwakeword** — wake word recognizer (ok_nabu / ehi_claw).
3. **wyoming-faster-whisper** — speech-to-text.
4. **wyoming-piper** — text-to-speech.
5. **homeclaw-bridge** — the glue we own. Reads transcripts from the
   satellite, talks to the OpenClaw gateway, pipes replies back to Piper.

All five run as user services under systemd. The bridge holds state of
which peer (room) the current conversation is coming from.

---

## The Wyoming protocol, in 3 minutes

Wyoming is a tiny TCP/JSON protocol invented by Home Assistant. One event
per line, JSON. Example:

```
{"type": "transcript", "data": {"text": "accendi la luce del salotto"}}
{"type": "synthesize", "data": {"text": "Fatto.", "voice": {"name": "it_IT-paola-medium"}}}
```

Events relevant for HomeClaw:

| Event | Direction | Meaning |
|---|---|---|
| `describe` | client → server | "tell me what you can do" |
| `info` | server → client | capabilities response (includes satellite name) |
| `detection` | satellite → bridge | wake word just fired |
| `transcript` | whisper → satellite → bridge | finalized ASR text |
| `synthesize` | bridge → piper → satellite | request to speak text |
| `audio-start`, `audio-chunk`, `audio-stop` | between processes | raw PCM stream |
| `error` | any → any | something broke |

The satellite is effectively a multiplexer: one TCP port (10700) accepts
connections from both the bridge and the LED feedback daemon, and emits
the full event stream to both.

---

## The OpenClaw side

The bridge talks to the OpenClaw Gateway over a local WebSocket at
`ws://127.0.0.1:18789`. Protocol (simplified):

### Client → server

```json
{
  "type": "agent.send_message",
  "correlation_id": "9a8f...",
  "agent": "HomeClaw",
  "channel": "voice",
  "peer": "homeclaw-cucina",
  "content": {"text": "accendi la luce del salotto"}
}
```

### Server → client

Zero or more interim events (`agent.typing`, `tool.call`, `tool.result`)
followed by exactly one terminal event:

```json
{
  "type": "agent.reply",
  "correlation_id": "9a8f...",
  "agent": "HomeClaw",
  "model": "claude-sonnet-4-6",
  "session_id": "sess_abc",
  "content": {"text": "Fatto."}
}
```

Or, on failure:

```json
{
  "type": "agent.error",
  "correlation_id": "9a8f...",
  "error": "tool 'home-assistant' timeout"
}
```

The bridge correlates requests and responses via `correlation_id`. Since
a voice session is single-speaker-at-a-time, the bridge serializes
requests with an `asyncio.Lock()` — this is defensive, not strictly
necessary on a well-behaved audio pipeline.

---

## The lifecycle of a single command

Wall-clock timings measured on Tier B (Pi 5 + Hailo-10H + ReSpeaker USB).

```
t=+0ms      wyoming-satellite streams mic PCM to openWakeWord continuously
t=+200ms    openWakeWord emits `detection` event ('ehi_claw')
t=+210ms    satellite sends `detection` to all connected clients (bridge, LED)
t=+210ms    LED feedback: ring pulses blue
t=+220ms    satellite starts recording command, streams to Whisper
t=+2200ms   user stops talking, VAD declares end of speech
t=+2250ms   Whisper returns Transcript("accendi la luce del salotto")
t=+2260ms   satellite forwards transcript to bridge
t=+2260ms   bridge sends agent.send_message to OpenClaw gateway
t=+2270ms   LED feedback: ring turns amber (thinking)
t=+3400ms   HomeClaw agent decides: call home-assistant skill
t=+3500ms   skill invokes HA REST API: light.turn_on
t=+3600ms   HA returns 200 OK
t=+3650ms   agent returns AgentReply("[SILENT_OK]")
t=+3650ms   bridge sees SILENT_OK marker — does NOT call Piper
t=+3650ms   LED feedback: ring turns green (speaking), then off
```

Total perceived latency: ~1.45 seconds, because no TTS was needed. For a
reply that needs speaking (e.g. weather query), add ~300–500 ms for Piper
to generate the first audio chunk.

---

## Failure modes and fallbacks

- **Satellite crash** → bridge reconnects with exponential backoff, LED
  daemon also reconnects. No user-visible effect beyond a gap in service.
- **Whisper crash** → satellite reports `error`, LED flashes red. Next
  command triggers the normal path, which fails again until whisper
  restarts (systemd auto-restarts).
- **OpenClaw gateway unreachable** → bridge timeout hits 8 seconds,
  bridge sends a "Non riesco a raggiungere il mio cervello" TTS message.
- **Cloud LLM unreachable** but local Nemotron is up → agent config
  routes to local model automatically (OpenClaw feature).
- **Power loss mid-command** → on reboot, all services come up via
  systemd. No persistent state corruption possible (all state is in
  OpenClaw workspace, backed by regular file writes).

---

## Security model

- Each service runs as the `pi` user, never root.
- Systemd hardening applied: `ProtectSystem=strict`, `NoNewPrivileges=true`,
  restricted writable paths.
- All TCP ports used (10200, 10300, 10400, 10700, 18789) bind to localhost
  or LAN only — never exposed on the WAN.
- If you need remote access, use Tailscale (see Capitolo 19 of the book).
- API keys for cloud LLMs live in `~/.openclaw/.env` with mode 0600.
- Sensitive voice recordings (debug) go to `/home/pi/homeclaw-debug` with
  mode 0700. Consider disabling debug recording in production.

---

## Scaling to multi-room (Tier C)

Each satellite (ESP32-S3 or Pi Zero 2 W) opens its own TCP connection to
the hub's `homeclaw-bridge`. The `Info` event at handshake time tells the
bridge which room this satellite represents (`homeclaw-cucina`,
`homeclaw-camera`, etc.).

That `peer` name is passed along to the agent as the `peer` field of every
`agent.send_message`. The HomeClaw SOUL.md teaches the agent to interpret
peer names as locations:

> "When the peer is `homeclaw-cucina` and the user says 'accendi la
> luce' without specifying where, assume the user means the kitchen."

This is how room-aware commands work in HomeClaw without any per-room
configuration on the agent side.
