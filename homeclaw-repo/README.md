# HomeClaw — Alexa Locale con Raspberry Pi 5 e OpenClaw

> Codice e configurazioni del capitolo extra del libro *OpenClaw: Guida Completa*.

HomeClaw è un assistente vocale completamente locale basato su [OpenClaw](https://openclaw.ai),
il [Wyoming Protocol](https://github.com/rhasspy/wyoming) di Home Assistant, e l'ecosistema
open-source per speech (Whisper + Piper + openWakeWord). Gira su Raspberry Pi 5, con o senza
acceleratore AI Hailo-10H, e ti permette di sostituire Alexa o Google Home con qualcosa che
rispetta la tua privacy e che puoi estendere come vuoi.

Per la teoria, l'architettura e la discussione completa, leggi il **Capitolo Extra** del libro.
Questo repo è la parte pratica: codice, systemd service, configurazioni.

---

## Struttura del repo

```
homeclaw-repo/
├── skill/                  # La skill OpenClaw 'homeclaw-bridge' (Python)
├── systemd/                # 6 unit file pronti da copiare in /etc/systemd/system/
├── led-feedback/           # Script di feedback visuale sui LED APA102
├── soul-templates/         # Template SOUL.md / IDENTITY.md / TOOLS.md / AGENTS.md
├── scripts/                # install-tier-b.sh, doctor.sh, benchmark.sh
├── esphome/                # Configurazione ESPHome per satelliti ESP32-S3 (Tier C)
└── docs/                   # Documentazione approfondita
```

---

## Tre tier di installazione

- **Tier A — Mono-stanza minimalista (€130)**: Pi 5 + microfono USB + altoparlante. Tutto su CPU.
- **Tier B — Mono-stanza produzione (€380)**: Pi 5 16GB + AI HAT+ 2 Hailo-10H + ReSpeaker USB 4-Mic.
- **Tier C — Multi-stanza (€550+)**: Hub Tier B + satelliti ESP32-S3-BOX-3 o Pi Zero 2 W in ogni stanza.

---

## Quickstart Tier B

```bash
# 1. Flash Raspberry Pi OS Bookworm 64-bit, abilita SSH, connetti via ssh.

# 2. Clona questo repo.
git clone https://github.com/tuo-account/homeclaw-repo.git
cd homeclaw-repo

# 3. Installa driver Hailo seguendo la guida ufficiale.
# https://www.raspberrypi.com/documentation/computers/ai.html
# Verifica con:
hailortcli fw-control identify
# Deve mostrare: Device Architecture: HAILO10H

# 4. Installa Wyoming stack + OpenClaw + bridge con lo script one-shot.
sudo ./scripts/install-tier-b.sh

# 5. Configura OpenClaw: crea l'agente HomeClaw e bindalo al canale 'voice'.
openclaw agents add HomeClaw
openclaw skills install ./skill
openclaw agents bind HomeClaw --channel voice --via homeclaw-bridge

# 6. Copia il template SOUL.md nel workspace dell'agente e personalizzalo.
cp soul-templates/*.md ~/.openclaw/homeclaw-workspace/

# 7. Abilita e avvia tutti i systemd service.
sudo cp systemd/*.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable --now \
    wyoming-openwakeword \
    wyoming-faster-whisper \
    wyoming-piper \
    wyoming-satellite \
    homeclaw-bridge \
    homeclaw-led-feedback

# 8. Test end-to-end.
./scripts/benchmark.sh
# Deve mostrare latenza media <2.5 secondi.

# 9. Prova il comando base.
# Di' "Ehi Claw, che ore sono?" e aspetta la risposta vocale.
```

Se qualcosa non funziona, lancia `./scripts/doctor.sh` per una diagnostica automatica.

---

## Requisiti software

- Raspberry Pi OS Bookworm **64-bit** (32-bit non supportato)
- Python 3.11+ (preinstallato su Bookworm)
- Node.js 22+ (installato da OpenClaw)
- OpenClaw 1.x con il Gateway WebSocket attivo su `ws://127.0.0.1:18789`
- Home Assistant opzionale per integrazione smart home

---

## Hardware testato

| Componente | Modello testato | Note |
|---|---|---|
| SBC | Raspberry Pi 5 16GB | 8GB funziona solo senza LLM locale |
| NPU | Raspberry Pi AI HAT+ 2 (Hailo-10H) | Opzionale; senza NPU Whisper small impiega 2+ s |
| Microfono | ReSpeaker USB 4-Mic Array (Seeed 107100001) | AEC hardware, LED APA102 integrati |
| Altoparlante | JBL Go 3 (BT) o Anker Soundcore USB | BT richiede disable power-save |
| Alimentatore | Ufficiale USB-C 27W | **Non** 15W: causa throttling |
| Satellite | ESP32-S3-BOX-3 | ESPHome 2026.4+ |

Dettagli BOM e link di acquisto in [`docs/hardware-bom.md`](docs/hardware-bom.md).

---

## Licenza

MIT. Vedi `LICENSE`.

---

## Contribuire

Issue e PR benvenute. Prima di aprire una PR:
- Per bug: allega output di `./scripts/doctor.sh`
- Per feature: discuti su GitHub Issues prima di aprire la PR
- Stile Python: commenti in inglese, metodi privati con `_` iniziale, divisori con commento

---

## Community

- Canale Discord OpenClaw, stanza `#homeclaw`
- Hashtag `#HomeClaw` e `#LobsterLamp` su X
- Tutorial video sulla playlist *How I AI* YouTube
