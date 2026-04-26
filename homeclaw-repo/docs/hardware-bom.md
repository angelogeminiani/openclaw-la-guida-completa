# Hardware Bill of Materials (BOM)

All prices indicative, EU market, April 2026. Links point to trusted
resellers; shop around.

## Tier A — Mono-room minimal (€130 total)

| # | Item | Model | EU reseller | Price |
|---|---|---|---|---|
| 1 | SBC | Raspberry Pi 5 8GB | Kubii / PiShop / Amazon EU | €75 |
| 2 | PSU | Official RPi 27W USB-C | same | €14 |
| 3 | microSD | SanDisk Extreme 64GB A2 U3 | Amazon EU | €12 |
| 4 | Cooling | Official active cooler | Kubii / PiShop | €5 |
| 5 | Microphone | Generic USB lavalier or Fifine K669 | Amazon EU | €15 |
| 6 | Speaker | Cheap USB-powered PC speakers | Amazon EU | €10 |
| 7 | Case | Flirc or official case | Kubii / PiShop | €10 |

Recycle at home: microSD, speaker, case. Realistic Tier A: **~€105** if
you already have a speaker.

---

## Tier B — Production (€360 total)

| # | Item | Model | EU reseller | Price |
|---|---|---|---|---|
| 1 | SBC | Raspberry Pi 5 **16GB** | Kubii | €95 |
| 2 | NPU | Raspberry Pi AI HAT+ 2 (Hailo-10H) | Kubii | €110 |
| 3 | PSU | Official RPi 27W USB-C | same | €14 |
| 4 | microSD | SanDisk Extreme 128GB A2 U3 | Amazon EU | €20 |
| 5 | Cooling | Official active cooler (must fit under HAT) | Kubii | €5 |
| 6 | Microphone | ReSpeaker USB 4-Mic Array (Seeed 107100001) | Seeed / Mouser | €75 |
| 7 | Speaker | JBL Go 3 (BT) or Anker Soundcore USB | Amazon EU | €40 |
| 8 | Case | Argon One V3 Pi 5 (with HAT compatibility) | Argon40 / Amazon | €30 |

Realistic Tier B: **€389**. Can shave €15–20 by picking a cheaper case.

### Why these parts, specifically

- **Pi 5 16GB, not 8GB.** Running Nemotron-3B locally with 89%-accuracy
  Whisper small + OpenClaw runtime uses ~6–10 GB RAM under load. 8 GB
  works only if you rely exclusively on cloud LLMs.
- **AI HAT+ 2, not the older AI HAT+.** The Hailo-10H on HAT+ 2 supports
  int4 LLMs; the Hailo-8 on the older HAT does vision only. HAT+ 2 is
  €110 new, old HAT is €60 used — but with the old HAT you can't run
  LLMs locally, just accelerate Whisper.
- **27W official PSU, not 15W.** Non-official or underspec PSUs cause
  USB throttling — your ReSpeaker will disconnect randomly. This is the
  #1 reason for "unreliable audio" complaints.
- **ReSpeaker USB 4-Mic Array, not ReSpeaker 2-Mic HAT.** The USB version
  has the XMOS XVF3510 chip which does hardware AEC and beamforming. The
  GPIO HAT version has no AEC and its drivers are broken on Pi 5 kernel
  6.x (as of April 2026). USB just works.
- **JBL Go 3 or similar.** Any Bluetooth speaker works; go is compact and
  battery-powered is a plus. USB speakers are more reliable for
  always-on setups but lack portability.
- **Argon One V3.** Metal case with active cooling, HAT cutouts, full GPIO
  access. Alternatives: FLIRC (silent but no HAT room), 3D-printed (see
  community Discord `#hardware-builds`).

---

## Tier C — Per-satellite add-ons

### Option 1 — ESP32-S3-BOX-3 (€65 per room)

| # | Item | Model | Reseller | Price |
|---|---|---|---|---|
| 1 | Satellite | Espressif ESP32-S3-BOX-3 | Mouser / Digi-Key / Pimoroni | €60 |
| 2 | USB-C cable | 3ft for power | anywhere | €5 |

Already has: dual microphone, speaker, 2.4" touch screen, RGB LED.

### Option 2 — Raspberry Pi Zero 2 W (€75 per room)

| # | Item | Model | Reseller | Price |
|---|---|---|---|---|
| 1 | SBC | Raspberry Pi Zero 2 W | Kubii | €20 |
| 2 | PSU | RPi micro-USB 2.5A | Kubii | €8 |
| 3 | microSD | 32GB A1 | Amazon EU | €7 |
| 4 | Mic HAT | Seeed ReSpeaker 2-Mic Pi HAT | Seeed | €15 |
| 5 | Speaker | Small JST 3W speaker | Seeed | €7 |
| 6 | Case | 3D-print | community files | €3 |
| 7 | Cables | jumper/Grove | Seeed | €2 |

---

## Optional but nice

| Item | Purpose | Price |
|---|---|---|
| NVMe M.2 HAT + 256GB SSD | Faster storage than microSD | €40 + €30 |
| UPS HAT (Waveshare) | Ride through brief power blips | €40 |
| Temperature sensor (BME280) | Talk to HomeClaw about room climate | €6 |
| 3D printer filament for lobster case | The aesthetic | €25 |

---

## Anti-shopping list (do NOT buy these)

- **USB-A to USB-B audio cables** — the Pi 5 has only USB-A/USB-C; many
  pro mics use USB-B and you end up juggling adapters. Stick to
  USB-C microphones or ones with built-in USB-A cable (ReSpeaker USB).
- **Alexa Echo Dots as satellites** — no, they can't be repurposed.
- **Arduino Uno / Nano / Mega** — not powerful enough for any voice
  processing. See the chapter's "Perché non Arduino" section.
- **Passive microphones (analog 3.5mm)** — Pi 5 has no analog audio input.
- **Unbranded Hailo knockoffs** — the Hailo toolchain requires firmware
  signed by Hailo. Clones won't load models.
