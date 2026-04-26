# Changelog

All notable changes to HomeClaw will be documented here.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).
This project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] — 2026-04-24

### Added
- Initial public release.
- Wyoming <-> OpenClaw bridge (`skill/bridge.py`) with auto-reconnect and
  exponential backoff.
- LED feedback daemon for ReSpeaker USB 4-Mic Array APA102 ring
  (`led-feedback/homeclaw_led_feedback.py`).
- Six systemd units (openWakeWord, faster-whisper, piper, satellite,
  bridge, LED feedback).
- One-shot installer (`scripts/install-tier-b.sh`) for Bookworm 64-bit.
- Diagnostic script (`scripts/doctor.sh`) — 9 checks, color output.
- End-to-end latency benchmark (`scripts/benchmark.sh`).
- Weekly backup script (`scripts/backup.sh`) with rotation.
- ESPHome configuration for ESP32-S3-BOX-3 satellites (Tier C).
- SOUL.md, IDENTITY.md, TOOLS.md, AGENTS.md templates for the HomeClaw
  agent.
- Documentation: architecture, hardware BOM, wake-word training,
  Home Assistant integration, troubleshooting, speaker identification.

### Known limitations
- Only Italian language templates shipped (other languages welcome via PR).
- Speaker identification (`docs/speaker-id.md`) is documented but not
  yet wired into the bridge by default.
- Acoustic echo cancellation relies on ReSpeaker USB 4-Mic hardware AEC;
  software-only AEC for cheaper microphones is not yet implemented.
