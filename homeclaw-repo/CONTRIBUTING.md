# Contributing to HomeClaw

Thanks for your interest. HomeClaw is community-maintained and any
improvement — from a typo fix to a new satellite platform — is welcome.

## Ground rules

- **Safety first.** HomeClaw runs on a computer with network access and
  microphone access. Any PR that introduces new capabilities must
  explicitly discuss the security implications in the PR description.
- **Honest about limitations.** If your change works 90% of the time,
  say so in the docs. Over-promising breaks trust.
- **Italian and English.** Docs primarily in Italian (it's an
  Italian-first project), but code comments, variable names, log
  messages, and commit messages in English. This makes the code
  searchable across the broader OSS world.

## Code style

- **Python**: PEP 8 via `ruff`. Commands in English. Private methods
  prefixed with `_` (underscore) and lowercase. Section separators
  with comments (see existing files for the style — `// c t r`,
  `// p r i v a t e`, etc., adapted for Python as `# c t r`).
- **Bash**: `set -euo pipefail` at the top. Functions over one-liners.
  Quote variable expansions. Use `readonly` for constants.
- **YAML (ESPHome)**: 2-space indent. Comments explain non-obvious
  values (pin assignments, substitution keys).

## Before opening a PR

1. Run `./scripts/doctor.sh` on a fresh install to confirm nothing
   regressed.
2. If changing the bridge or LED feedback, run `./scripts/benchmark.sh`
   and include before/after latency numbers in the PR description.
3. Update relevant docs in `docs/`.
4. Add your change to a new line in `CHANGELOG.md` (create it if missing).

## Adding a new satellite platform

We welcome new satellite platforms (M5Stack, ESPHome variants, other
SBCs). PR checklist:
- Config file in `esphome/` (if applicable) or a new directory for the
  platform.
- A short `docs/satellite-<platform>.md` explaining hardware, flash
  procedure, and any quirks.
- Updated `docs/hardware-bom.md` with the new option.
- Tested with at least one end-to-end voice turn (show the
  `benchmark.sh` output).

## Adding a new language

Right now HomeClaw is tuned for Italian (Whisper `--language it`,
Piper `it_IT-paola-medium`, SOUL.md in Italian). Adding another language:
1. New Piper voice download instructions in `docs/hardware-bom.md`.
2. Translated SOUL.md template in `soul-templates/SOUL.<lang>.md`.
3. Wake word training notes for phonetic gotchas in the target language.

## Reporting issues

When opening an issue, include:
- Output of `./scripts/doctor.sh --verbose`
- Tier (A / B / C), hardware list
- Whisper model, Piper voice, LLM in use
- Minimum reproducible steps
- Relevant log excerpts (sanitize secrets)

## Discord

Most real-time conversation happens on the OpenClaw Discord, channel
`#homeclaw`. Join there first if you're unsure whether something is a
bug, a feature request, or a misconfiguration.
