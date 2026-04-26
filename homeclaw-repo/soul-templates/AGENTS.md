# HomeClaw — Operational Memory

*Long-lived operational context. Read at every session start. Update by
appending, never by rewriting old entries.*

---

## Hardware

- Host: Raspberry Pi 5 16GB, kernel 6.12, hostname `homeclaw-hub`
- NPU: Hailo-10H on AI HAT+ 2 (PCIe Gen 3)
- Mic: ReSpeaker USB 4-Mic Array (USB port 1, left)
- Speaker: JBL Go 3 (Bluetooth, MAC `XX:XX:XX:XX:XX:XX`)
- Power: 27W official supply
- Case: Argon One V3 with top lid vents

## Network

- Hub: 192.168.1.42 (static DHCP reservation)
- Home Assistant: 192.168.1.10 (homeassistant.local)
- Satellites (Tier C): 192.168.1.50 (cucina), 192.168.1.51 (camera)

## Cron jobs owned by HomeClaw

| Name | When | What |
|---|---|---|
| `morning-brief` | Mon–Fri 07:00 | Read calendar + weather if user is awake (HA presence). Silent on weekends unless user says good morning first. |
| `evening-wrap` | Daily 22:00 | Ask via Telegram: "need anything for tomorrow?". No voice. |
| `weekly-health-check` | Sat 10:00 | `openclaw doctor` + `openclaw security audit`. Telegram summary. |

## Personas in the house

Voice profiles trained for speaker identification (see `docs/speaker-id.md`):

- **Giacomo** (owner) — all commands allowed
- **Lucia** (partner) — all commands allowed, no sensitive-topic access
- **Pietro** (age 9) — commands routed to agent `Q` (educator), no purchases
- **Mia** (age 6) — commands routed to agent `Q` (educator), no purchases

If voice unrecognized: handle as Giacomo but refuse irreversible actions.

## Delegation map

When a command crosses into another agent's domain, delegate:

- *"Pietro, ripassa le tabelline"* → forward to `Q` agent
- *"Aggiungi al calendario"* → forward to `Polly`
- *"Prenota il treno domani"* → forward to `Polly` (confirm first)
- *"Cosa cucino stasera"* → handle locally (fun, no external skill)

## Logs and observability

- Bridge logs: `journalctl -u homeclaw-bridge`
- Wyoming logs: `journalctl -u wyoming-satellite -u wyoming-faster-whisper`
- Agent logs: `openclaw logs --agent HomeClaw`
- LED feedback: `journalctl -u homeclaw-led-feedback`
- Full trace: `./scripts/doctor.sh --verbose`

## Known quirks

- *(Add observations here as you discover them during use.)*
- Whisper occasionally hears "Ehi Claw" as "hey cloud" if ambient noise
  is high — ignore that transcript, wait for the next one.
- The JBL Go 3 takes ~1.5s to wake up from BT idle when the first TTS
  starts. Known limitation, not a HomeClaw bug.

## Update log

Append dated one-liners here when you change something meaningful.

- *2026-04-24*: Initial setup, Tier B.
- *2026-04-25*: Added "Ehi Claw" custom wake word.
- *2026-04-27*: Moved sensitive-topic rule before routing (SOUL §6).
