---
name: homeclaw-bridge
version: 1.0.0
description: >
  Bridge between the Wyoming Protocol (local voice stack on the Raspberry Pi)
  and the OpenClaw Gateway. Connects to wyoming-satellite as a TCP client on
  port 10700, receives ASR transcripts, forwards them as user messages to the
  HomeClaw agent on the 'voice' channel, strips Markdown from agent responses,
  and sends synthesize events back for Piper TTS playback.
author: HomeClaw Contributors
license: MIT
entry_point: bridge.py
runtime: python3.11
permissions:
  - network.connect: 127.0.0.1:10700   # wyoming-satellite
  - network.connect: 127.0.0.1:18789   # openclaw gateway
  - agent.send: HomeClaw
  - agent.receive: HomeClaw
config:
  satellite_uri:
    type: string
    default: tcp://127.0.0.1:10700
    description: Wyoming satellite endpoint
  tts_voice:
    type: string
    default: it_IT-paola-medium
    description: Piper voice model name (see wyoming-piper --list-voices)
  agent_name:
    type: string
    default: HomeClaw
    description: OpenClaw agent this bridge drives
  response_timeout_seconds:
    type: float
    default: 8.0
    description: Max wait for an agent response before giving up
  silent_ok_marker:
    type: string
    default: "[SILENT_OK]"
    description: >
      If the agent's response is exactly this marker, the bridge will NOT send
      a TTS synthesize event. The LED feedback (green pulse) acts as the only
      confirmation. Used for trivial commands like 'timer 5 minuti' or 'accendi
      la luce' where speaking the confirmation would be noise.
---

# HomeClaw Bridge

When a transcript arrives from the satellite, forward it as a user message
to the HomeClaw agent on the `voice` channel. When the agent responds:

1. Strip Markdown (asterisks, backticks, link syntax, bullet dashes, etc.)
   because the TTS engine reads them literally otherwise
2. If the cleaned response equals `[SILENT_OK]`, do not synthesize audio;
   the LED feedback is the only confirmation
3. Otherwise send a Wyoming `synthesize` event to the satellite so Piper
   can generate speech and play it back

If the agent does not respond within `response_timeout_seconds`, send a
short synthesize event saying "non riesco a raggiungere il mio cervello,
riprova tra un momento" so the user knows something is wrong.

Each satellite (Tier C multi-room setup) opens a TCP connection with a
distinct `peer` name (e.g. `homeclaw-cucina`, `homeclaw-camera`). The bridge
passes this peer name along to the agent so that room-aware responses
become possible.
