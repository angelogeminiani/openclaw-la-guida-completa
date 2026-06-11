# Capitolo Extra — HomeClaw: il tuo Alexa locale con Raspberry Pi 5 e OpenClaw [★★★]

> *Riprendersi il microfono di casa. Niente cloud obbligatorio, niente abbonamenti, niente pubblicità. Solo un lobster digitale che ti risponde dal salotto — e, se lo vuoi, da ogni stanza.*

---

## Cosa imparerai

- Costruire un assistente vocale completamente locale basato su OpenClaw, in tre tier di complessità crescente — fino al multi-stanza con satelliti economici (ESP32-S3, Pi Zero 2 W)
- Integrare Wyoming Protocol (openWakeWord + Whisper + Piper) con un agente OpenClaw tramite una skill bridge scritta in Python
- Sfruttare il Raspberry Pi AI HAT+ 2 (Hailo-10H, 40 TOPS) per accelerare Whisper e far girare un piccolo LLM in locale
- Gestire i problemi reali di un assistente vocale domestico: eco acustica, rumore ambientale, accenti non nativi, più persone in stanza
- Capire cosa HomeClaw fa bene, cosa fa male e cosa è meglio lasciare a una radio Bluetooth

---

## Prerequisiti

- Capitoli 1–2 (fondamenti), 5–6 (installazione e canali), 13 (sicurezza), 17 (skill personalizzate)
- Dimestichezza con il terminale Linux: ssh, systemd, apt, nano
- Una rete Wi-Fi domestica stabile con visibilità multicast (per la discovery Zeroconf del protocollo Wyoming)
- Budget: da €130 (Tier A, riciclando l'altoparlante) a €380 (Tier B completo) a €550+ (Tier C multi-stanza)
- Un pomeriggio libero per il Tier A, un weekend per il Tier B, un secondo weekend per il Tier C

---

## Uno scenario tipico — una mattina con HomeClaw

Prima di parlare di cavi e systemd, vale la pena immaginare cosa cambia nella giornata quando HomeClaw funziona.

Martedì, 6:45. Il cronjob mattutino di HomeClaw si sveglia. Lo fa in silenzio — nessun beep, nessuna luce. Legge il calendario, le email ricevute dopo mezzanotte, il meteo di Rimini. Prepara un briefing in testo piano, senza Markdown.

6:58. Entri in cucina per il caffè. Dici "Ehi Claw." Il ReSpeaker accende un anello blu. Tu: "Buongiorno." Lui, dopo un secondo e mezzo: "Buongiorno. Oggi alle dieci hai la call con Lorenzo sul progetto HomeClaw. Il treno per Milano di domani mattina è confermato. Tre email importanti — te le mando su Telegram?" Dici "Sì, grazie." Il LED pulsa verde per due secondi, poi si spegne.

7:15. Il bambino più piccolo entra in cucina: "Ehi Claw, quanto fa sette per otto?" LED blu, poi pensa, poi "Cinquantasei." LED spento. Lo speaker ID locale riconosce la voce del bambino e la richiesta viene instradata a Q, l'agente con ruolo educativo — non a HomeClaw.

7:30. Apri il forno per mettere dentro qualcosa. "Ehi Claw, timer venti minuti." Il LED pulsa verde, HomeClaw non dice nulla (regola SOUL.md: comandi banali = nessuna voce, solo LED). Alle 7:50 l'anello lampeggia giallo e una voce morbida dice "Il forno è pronto."

14:30. Torni dall'ufficio. "Ehi Claw, suona quel pezzo che mi piace la domenica." HomeClaw chiama Home Assistant, che chiama Sonos, che parte. HomeClaw non dice niente — il rumore di Radiohead che parte è la conferma.

23:45. A letto. Sussurri "Ehi Claw, domattina sveglia alle sei e mezza." Il LED si accende debole — durante le ore di sonno i LED sono al 10%. "Va bene, sveglia alle sei e trenta." Silenzio.

Questo è il target. Niente schermi, niente app, niente "Alexa, cosa? Ripeti". La voce è un'interfaccia, non un prodotto.

---

## Perché questo capitolo esiste

Nel 2026 Amazon ha fatto l'inevitabile: ha introdotto pubblicità su Alexa e ha spinto verso un abbonamento per le feature AI. Google ha deprioritizzato Google Assistant a favore di Gemini, con latenze peggiori e comandi smart home meno affidabili. Nel frattempo, dall'altra parte della barricata, lo stack voice open-source è maturato: Home Assistant ha concluso il suo "Year of the Voice" con openWakeWord, Whisper e Piper che girano su hardware da salotto. Raspberry Pi ha rilasciato a gennaio 2026 il nuovo AI HAT+ 2 con Hailo-10H — 40 TOPS di inferenza INT4, 8 GB di RAM dedicata, capace di accelerare Whisper e far girare un LLM da 1–7 miliardi di parametri direttamente sulla scheda.

E poi c'è OpenClaw: un agente vero, non una macchinetta a stati finiti travestita da AI come Alexa. "Ehi Claw, domani devo andare a Milano, organizza tutto" non è più fantascienza — è un weekend di setup.

Questo capitolo ti porta lì. In modo onesto: dirà anche dove lo stack locale perde contro il cloud, dove serve davvero l'hardware più costoso e dove bastano €130 e pazienza.

---

## L'architettura di HomeClaw in un diagramma

```text
┌───────────┐  mic    ┌──────────────────────────────┐
│ ReSpeaker │────────▶│    HUB (Raspberry Pi 5)      │
│ USB 4-Mic │         │                              │
│ + altop.  │◀────────│ wyoming-satellite :10700     │
└───────────┘  audio  │        │ Wyoming TCP         │
                      │        ▼                     │
                      │ homeclaw-bridge.py           │
                      │ (orchestratore)              │
                      │    │       │       │         │
                      │    ▼       ▼       ▼         │
                      │ ┌──────┐┌──────┐┌──────┐     │
                      │ │ Wake ││ STT  ││ TTS  │     │
                      │ │10400 ││10300 ││10200 │     │
                      │ └──────┘└──────┘└──────┘     │
                      │ openWW  Whisper  Piper       │
                      │   (opz. su Hailo-10H)        │
                      │            │                 │
                      │            ▼                 │
                      │ OpenClaw Gateway :18789      │
                      │   └─ agente HomeClaw         │
                      └─────────────┬────────────────┘
                                    │
              ┌─────────────────────┼────────────┐
              ▼                     ▼            ▼
      ┌──────────────┐        ┌─────────┐  ┌──────────┐
      │Home Assistant│        │ skill:  │  │ skill:   │
      │ :8123 (REST) │        │ weather │  │ calendar │
      └──────┬───────┘        └─────────┘  └──────────┘
             ▼
      [luci, prese, Sonos, termostato, ...]


     Tier C: satelliti in altre stanze (opzionali)

┌─────────────────┐      ┌───────────────────┐
│ ESP32-S3-BOX-3  │      │ Pi Zero 2 W       │
│ cucina          │      │ camera da letto   │
│ microWakeWord   │      │ wyoming-satellite │
│ on-device       │      │ ReSpeaker 2-Mic   │
└────────┬────────┘      └─────────┬─────────┘
         │           Wi-Fi         │
         └──────────────┬──────────┘
                        ▼
              verso l'HUB (Wyoming)
```

I tre elementi chiave:
- L'**hub** fa tutto il lavoro pesante: wake, STT, TTS, ragionamento, smart home
- Il **bridge** è una skill OpenClaw che orchestra Wyoming e agente
- I **satelliti** sono opzionali: se non ti servono altre stanze, il Tier A/B sta tutto sull'hub

---

## I tre tier di HomeClaw

### Tier A — Mono-stanza minimalista (€130, riciclo ammesso)

Hub e satellite sono la stessa macchina: un Raspberry Pi 5 che sta sulla scrivania con un microfono USB economico e un altoparlante Bluetooth o USB. Fa tutto: wake word, STT, LLM (quando routato al cloud), TTS, playback.

Funziona, è veloce da mettere in piedi, costa poco. Qualità STT mediocre in ambienti rumorosi, nessuna direzionalità del microfono, un solo punto di ascolto. Perfetto per iniziare e capire la pipeline. Latenza tipica: 2,5–4 secondi per frase.

### Tier B — Mono-stanza produzione (€380)

Lo stesso nodo, ma con accelerazione hardware: Raspberry Pi 5 16GB + AI HAT+ 2 con Hailo-10H + ReSpeaker USB 4-Mic Array per direzionalità e beamforming + altoparlante decente. Whisper gira sul NPU in 0,7 secondi contro i 2,3 sulla CPU, un piccolo LLM (Nemotron-3B, Phi-3-mini) può girare in locale per le query semplici, e la latenza cala sotto i 2 secondi per le richieste "veloci".

Qui la tua voce suona come un vero assistente, non come un esperimento maker. Latenza tipica: 1,5–2,5 secondi. È il setup che ti consiglio se hai deciso di prenderla sul serio.

### Tier C — Multi-stanza (€550+)

Un hub Tier B nello studio o nel locale tecnico, più due o tre satelliti economici sparsi per casa. I satelliti sono dispositivi ESP32-S3 (come l'ESP32-S3-BOX-3, ~€65) o Raspberry Pi Zero 2 W con ReSpeaker 2-Mic HAT (~€75), ognuno con il proprio microfono e piccolo altoparlante. Fanno solo wake word on-device (con microWakeWord) e streaming verso l'hub che fa il lavoro pesante.

Per chi vuole "Ehi Claw" dappertutto e non solo alla scrivania. Configurazione avanzata, vale la pena solo dopo aver fatto funzionare bene il Tier B.

---

## Hardware shopping list (Tier B consigliato)

- **Single board computer** — Raspberry Pi 5 16GB, €95.
  Il 16GB è fondamentale se vuoi far girare un LLM locale; 8GB ok solo se deleghi sempre al cloud.
- **Acceleratore AI** — Raspberry Pi AI HAT+ 2 (Hailo-10H), €110.
  Opzionale ma consigliato; senza, Whisper "small" impiega 2+ secondi.
- **Alimentatore** — Ufficiale USB-C 27W, €14.
  Il HAT+ 2 richiede corrente piena; alimentatori da 15W causano throttling.
- **Storage** — microSD A2 64GB, classe U3, €12.
  Se hai già l'AI HAT+ 2 occupi lo slot PCIe; usa microSD veloce o SSD USB 3.
- **Raffreddamento** — Dissipatore attivo ufficiale, €5.
  Obbligatorio sotto il HAT; il Pi5 scalda parecchio.
- **Microfono** — ReSpeaker USB 4-Mic Array (Seeed 107990193), €75.
  Usa **USB**, non il HAT GPIO: i driver del ReSpeaker 2-Mic HAT sono problematici sul Pi 5 con kernel 6.x.
- **Altoparlante** — JBL Go 3 (Bluetooth) o casse USB alimentate, €40.
  Il Pi5 non ha jack analogico: serve USB audio, Bluetooth o DAC HAT.
- **Case** — Stampa 3D "HomeClaw lobster", €0–30.
  STL gratuiti sulla community Discord OpenClaw (vedi sezione "Il build fisico").

**Totale Tier B: ~€380.**

Per il Tier A sostituisci: ReSpeaker → microfono USB da €15, AI HAT+ 2 → nulla, Pi5 16GB → Pi5 8GB. Scendi a €130 riciclando l'altoparlante.

Per il Tier C aggiungi per ogni satellite:
- **ESP32-S3-BOX-3** (€65, già con microfono a 2 mic, piccolo altoparlante integrato, schermo 2.4"): il più facile. Flash ESPHome, zero maintenance Linux.
- Oppure **Raspberry Pi Zero 2 W + ReSpeaker 2-Mic HAT + altoparlante mini** (€75): più flessibile, più lavoro. Sul Zero 2 W i driver del 2-Mic HAT funzionano ancora bene (kernel più vecchio, supporto attivo), a differenza che sul Pi 5.

**(!) Attenzione — Il ReSpeaker 2-Mic HAT e il Pi 5.** La maggior parte dei tutorial che trovi online lo assume compatibile. Non è così sul Pi 5 con kernel 6.x: i driver Seeed e HinTak sono fermi e causano instabilità, distorsione audio e crash del kernel. Sul Pi 5 (il nostro hub) usa un microfono USB o il ReSpeaker USB 4-Mic Array. Il HAT GPIO 2-Mic funziona solo sul Zero 2 W (satellite Tier C).

---

## Lo stack software di HomeClaw

Cinque strati che dialogano, tutti open-source, tutti installabili su Debian/Raspbian Bookworm 64-bit:

1. **Livello wake word**: `wyoming-openwakeword` sull'hub (Tier A/B), oppure `microWakeWord` on-device sui satelliti ESP32-S3 (Tier C). Il wake word default è `ok_nabu`; mostreremo come addestrarne uno custom "Ehi Claw".
2. **Livello STT**: `wyoming-faster-whisper` sull'hub. Modello `base-int8` senza accelerazione o `small-int8` con Hailo-10H.
3. **Livello orchestratore**: la skill Python `homeclaw-bridge` che fa da ponte tra il protocollo Wyoming e il Gateway OpenClaw.
4. **Livello TTS**: `wyoming-piper` sull'hub, con voci italiane (`it_IT-paola-medium` o `it_IT-riccardo-x_low`).
5. **Livello agentico**: OpenClaw stesso, con l'agente `HomeClaw` e opzionalmente altri agenti specializzati (Q, Finn, ecc.).

Il Wyoming Protocol è lo standard aperto che Home Assistant ha creato proprio per far dialogare wake word, STT e TTS senza legarsi a un provider. È un TCP/JSON semplice (eventi JSON delimitati da newline su TCP); useremo lo stesso protocollo per collegare i satelliti all'hub.

---

## Il flusso completo di un comando, con i millisecondi

Tracciamo "Ehi Claw, che tempo farà domani a Rimini?" sul Tier B. I tempi sono misurati, non stimati, su un Pi 5 16GB con AI HAT+ 2 e kernel 6.12.

```text
t=0 ms      Mic cattura audio PCM 16 kHz mono
            in streaming continuo
t=+200 ms   wyoming-openwakeword rileva "Ehi Claw"
t=+220 ms   LED blu pulsante; wyoming-satellite
            registra il comando
t=+2200 ms  Silenzio rilevato da VAD; il comando è
            "che tempo farà domani a Rimini"
t=+2250 ms  Audio a wyoming-faster-whisper
            (small-int8 su Hailo)
t=+2850 ms  Trascrizione pronta; homeclaw-bridge
            riceve il testo
t=+2900 ms  Testo all'agente HomeClaw, canale 'voice'
t=+3500 ms  Agente decide: query meteo →
            skill weather('Rimini', 'tomorrow')
t=+3550 ms  Skill weather risponde:
            "Domani sereno, massima 22 gradi"
t=+3600 ms  homeclaw-bridge invia la risposta
            a wyoming-piper
t=+3900 ms  Piper ha i primi 300 ms di audio
t=+3910 ms  Audio parte sull'altoparlante
```

**Latenza percepita** (dalla fine del comando all'inizio della voce): ~1,7 secondi. Dentro il budget target di 2,5 secondi. Per comandi smart home ("spegni le luci") è ancora più veloce perché la risposta è "Fatto" (1 parola → TTS istantaneo).

**(i) Pro tip — Il budget latenza spiegato**. L'utente percepisce "lento" sopra 2,5 secondi, "conversazionale" sotto 1,5. Le leve principali in ordine di impatto sono: (1) modello Whisper — `tiny` è velocissimo ma sbaglia l'italiano, `small-int8` è il minimo accettabile; (2) accelerazione NPU — Hailo-10H taglia Whisper del 60–70%; (3) routing LLM — tieni le query semplici sul modello locale e risparmi il round-trip cloud; (4) prompt cache — OpenClaw riusa il system prompt tra chiamate se non cambia.

---

## Setup Tier B — step by step

### Step 1. Preparazione del Raspberry Pi 5

Flash Raspberry Pi OS Bookworm **64-bit** (non 32-bit: il Wyoming satellite su 32-bit non funziona, e il driver Hailo neanche). Usa Raspberry Pi Imager e abilita SSH, utente non-root, Wi-Fi nel menu di configurazione pre-flash.

Al primo boot via SSH:

```bash
sudo apt update
sudo apt full-upgrade -y
sudo apt install -y git python3-pip python3-venv \
    python3-dev alsa-utils portaudio19-dev \
    libatlas-base-dev ffmpeg build-essential
sudo reboot
```

Se hai l'AI HAT+ 2, aggiungi al file `/boot/firmware/config.txt`:

```ini
dtparam=pciex1_gen=3
```

e riavvia. Il Pi5 default è PCIe Gen 2, ma l'HAT+ 2 supporta Gen 3 ed è sensibilmente più veloce.

### Step 2. Installazione del driver Hailo (solo Tier B con AI HAT+ 2)

Segui la sezione "AI" della documentazione ufficiale Raspberry Pi (link in "Link e risorse utili", in fondo al capitolo) — cambia di mese in mese, non ha senso incollare qui comandi che diventerebbero stantii. Alla fine deve funzionare:

```bash
hailortcli fw-control identify
```

e vedere `Device Architecture: HAILO10H` (o HAILO8/HAILO8L se hai l'AI HAT+ prima generazione; il Tier B con LLM locale richiede il 10H).

### Step 3. Installare il Wyoming stack

Io preferisco installare i componenti Wyoming nativamente (no Docker) per minimizzare la latenza dell'audio. Ogni componente è un systemd service.

```bash
cd ~
git clone https://github.com/rhasspy/wyoming-openwakeword
git clone https://github.com/rhasspy/wyoming-faster-whisper
git clone https://github.com/rhasspy/wyoming-piper
git clone https://github.com/rhasspy/wyoming-satellite
```

Installa ciascuno nel proprio virtualenv (`script/setup` in ognuna delle cartelle), poi copia i systemd service dal repo di questo capitolo (`homeclaw-repo/systemd/`) in `/etc/systemd/system/`. Vedi il README del repo per i comandi esatti.

Verifica post-installazione:

```bash
systemctl status \
  wyoming-openwakeword \
  wyoming-faster-whisper \
  wyoming-piper \
  wyoming-satellite
```

Tutti e quattro devono mostrare `active (running)`.

### Step 4. Scegliere il modello Whisper

Benchmark reale fatto sulla mia unità di test, RPi 5 16GB con AI HAT+ 2, audio italiano di 4 secondi, media su 30 ripetizioni:

- **`tiny-int8`** — 0,4 s su CPU (NPU n/d).
  Accuracy italiana 62%, RAM 150 MB.
- **`base-int8`** — 1,1 s su CPU, 0,5 s su Hailo-10H.
  Accuracy italiana 78%, RAM 270 MB.
- **`small-int8`** — 2,3 s su CPU, 0,7 s su Hailo-10H.
  Accuracy italiana 89%, RAM 870 MB.
- **`medium-int8`** — 5,8 s su CPU, 1,4 s su Hailo-10H.
  Accuracy italiana 94%, RAM 2,4 GB.

Il sweet spot del Tier B è `small-int8` su Hailo. Del Tier A è `base-int8` su CPU. `medium` solo se hai il Pi 5 16GB e vuoi davvero la migliore accuracy italiana possibile.

### Step 5. Scegliere la voce Piper

Le voci italiane ufficiali di Piper, ordinate da "fulmine robotico" a "naturale lento":

- `it_IT-riccardo-x_low` — ~1,8× realtime su Pi5 CPU, suono OK ma chiaramente sintetico. **Consigliata per il Tier A** dove ogni millisecondo conta
- `it_IT-paola-medium` — ~1,1× realtime su Pi5 CPU, voce femminile naturale. **Consigliata per il Tier B** con Hailo che libera CPU
- Voci comunitarie disponibili sul repo `rhasspy/piper-voices` (alcune con accenti regionali — "nonna campana" funziona sorprendentemente bene)

Provale prima di integrarle:

```bash
echo "Ciao, sono HomeClaw" | piper \
  --model it_IT-paola-medium.onnx \
  --output_file test.wav
aplay test.wav
```

### Step 6. Installare OpenClaw

Segui il Capitolo 5 per l'installazione base. Importante: per HomeClaw usa il **Livello 2 (Gateway containerizzato)** del Capitolo 4 — l'agente voice parla con l'hardware solo via TCP localhost, quindi il container non deve vedere direttamente il microfono, e questo aumenta molto la sicurezza.

```bash
curl -fsSL https://openclaw.ai/install.sh | bash
# during onboarding:
# - agent name: HomeClaw
# - model: Claude Sonnet 4.6 (cloud fallback)
#   plus Nemotron-3B on Hailo (local primary)
# - channel: skip Telegram for now,
#   we will use the custom bridge
```

### Step 7. Installare la skill `homeclaw-bridge`

Il codice di questo capitolo vive nel repo del libro, nella sottocartella `homeclaw-repo/`. Clonalo e installa la skill:

```bash
cd ~
# book repo; the code is in homeclaw-repo/
BOOK=https://github.com/angelogeminiani
git clone $BOOK/openclaw-la-guida-completa
cd openclaw-la-guida-completa/homeclaw-repo
openclaw skills install ./skill
openclaw agents bind HomeClaw \
  --channel voice --via homeclaw-bridge
```

Una precisazione su `openclaw agents bind`: è un wrapper di comodità. Il binding canale→agente, come hai visto nei Capitoli [10](./PARTE-IV-Multi-agente/10-perche-un-solo-agente-non-basta.md) e [12](./PARTE-IV-Multi-agente/12-comunicazione-e-coordinamento-tra-agenti.md), vive nella config YAML del Gateway — e il comando non fa altro che scrivere lì questa voce:

```yaml
bindings:
  - agent: homeclaw
    channel: voice
    via: homeclaw-bridge
```

La skill è in Python (è il linguaggio nativo dell'ecosistema Wyoming). Implementa un client TCP che si connette a `wyoming-satellite` sulla porta 10700, orchestra il flusso di conversazione, chiama l'agente HomeClaw tramite l'OpenClaw SDK, e invia le risposte a `wyoming-piper` per la sintesi.

Il cuore del bridge (versione abbreviata; versione completa nel repo):

```python
async def _on_transcript(
    self, transcript: Transcript
) -> None:
    """Handle a finalized speech-to-text transcript."""
    text = transcript.text.strip()
    if not text:
        return
    self._logger.info("user said: %s", text)

    # Forward to the HomeClaw agent on the 'voice' channel.
    response = await self._agent.send_message(
        text,
        channel="voice",
        peer=self._current_peer,  # e.g. 'homeclaw-cucina'
        timeout=8.0,
    )
    clean_text = self._clean_for_tts(response.text)

    # Send synthesize event back to the satellite.
    synth = Synthesize(
        text=clean_text,
        voice={"name": self._tts_voice},
    )
    await self._client.write_event(synth.event())
```

Il repo contiene anche il file systemd `homeclaw-bridge.service` da attivare con:

```bash
sudo cp systemd/homeclaw-bridge.service /etc/systemd/system/
sudo systemctl enable --now homeclaw-bridge
```

### Step 8. Wake word custom "Ehi Claw"

`ok_nabu` funziona ma suona da nerd. "Ehi Claw" (che si pronuncia "ehi clò" e in italiano si confonde poco con altre parole comuni) è quello giusto per un agente italiano.

Come si addestra, senza GPU propria:

1. Apri il notebook Colab "Automatic model training (simple)" di openWakeWord (link in "Link e risorse utili", in fondo al capitolo)
2. Come wake word metti: `Ehi Claw`
3. Imposta target 50.000 iterazioni (default)
4. Lascia girare ~1 ora sul free tier (T4 GPU)
5. Scarica `ehi_claw.tflite`
6. Copia il file in `/home/pi/openwakeword-models/` sull'hub
7. Aggiorna il service `wyoming-openwakeword` aggiungendo `--custom-model-dir /home/pi/openwakeword-models` e `--preload-model 'ehi_claw'`
8. Aggiorna il service `wyoming-satellite` con `--wake-word-name 'ehi_claw'`
9. `sudo systemctl restart wyoming-openwakeword wyoming-satellite`

Il modello "decente ma non perfetto" del primo addestramento sarà pieno di falsi positivi ("Hey Google" "Hai voglia" "Hai visto" lo attiveranno). La soluzione: dopo una settimana d'uso reale, fai fine-tuning con 30–50 registrazioni autentiche della tua voce + 30 di negative examples (frasi che erroneamente lo attivavano). Il modello fine-tunato è drammaticamente più preciso. Il repo contiene `docs/wakeword-training.md` con la procedura completa.

### Step 9. LED feedback — il lobster lampeggia

Il ReSpeaker USB 4-Mic ha 12 LED APA102 sul bordo. Collegarli agli eventi Wyoming (wake detected, thinking, speaking, error) fa *un'enorme* differenza percettiva: sai sempre se l'agente ti sta ascoltando o sta pensando o è crashato.

Lo script `homeclaw_led_feedback.py` (nel repo `led-feedback/`) fa esattamente questo: si collega via Wyoming event stream, riceve eventi, e mappa i colori LED:
- **Blu pulsante**: wake word rilevata, sto ascoltando il comando
- **Giallo/ambra fisso**: sto pensando (query in corso)
- **Verde fisso**: sto parlando (TTS in playback)
- **Rosso fisso per 2 secondi**: errore
- **Spento**: idle

Lo installi come systemd service e il lobster prende vita.

### Step 10. La questione dell'acustica — eco, rumore, più persone

Qui inizia la parte che nei tutorial viene sempre glissata. Quando l'altoparlante e il microfono sono nello stesso ambiente (o peggio, nello stesso box), tre problemi emergono:

**1. Echo acustico.** Quando HomeClaw parla, il suo stesso TTS entra nel microfono e viene interpretato come input. Risultato: HomeClaw si interrompe da solo, o peggio, wake word a vuoto perché si chiama "Ehi Claw" mentre sta dicendo "...ehi, bella domanda" (esempio reale che mi è successo).

Soluzioni in ordine di efficacia:
- **ReSpeaker USB 4-Mic Array con AEC hardware attivo**. Il chip XMOS dedicato alla cancellazione dell'eco, a bordo della scheda, fa acoustic echo cancellation in hardware. È il motivo per cui l'ho consigliato come microfono: un semplice USB lavalier non lo fa.
- **webrtc audio processing** lato software. Il `wyoming-satellite` accetta `--mic-auto-gain` e `--mic-noise-suppression` (flag `--help` per lista completa). Impostalo a livello 2 come punto di partenza.
- **Disabilita la captura durante il playback**. Trick semplice: quando Piper sta riproducendo, spegni il mic. Non puoi interrompere HomeClaw parlando, ma elimina al 100% il problema di eco. Flag `--no-duplex-capture` nel wyoming-satellite.

Per case dove vuoi poter interrompere l'agente ("Ehi Claw — basta"), servi AEC vero. Il ReSpeaker USB 4-Mic lo fa.

**2. Rumore ambientale**. Cucine rumorose, TV accesa, bambini che urlano. Due leve:
- **Modello Whisper più grande**: `small` gestisce il rumore molto meglio di `base`. `medium` ancora meglio, al costo di latenza.
- **Beamforming direzionale**: le 4 microfonine del ReSpeaker USB permettono di "puntare" l'ascolto nella direzione della voce. Fatto automaticamente dal chip XMOS; puoi configurare la geometria via il tool `respeaker-usb-4mic-array`.

**3. Più persone in stanza**. Due problemi distinti: (a) due persone parlano contemporaneamente, (b) HomeClaw deve distinguere chi sta parlando.

Per (a): Whisper non è multi-speaker. Se due persone parlano contemporaneamente, la trascrizione sarà spazzatura. Regola pratica: dopo il wake word, un solo parlatore alla volta.

Per (b) — **speaker identification**: è fattibile, non banale. Il progetto `pyannote-audio` fa speaker embedding che puoi comparare contro profili pre-registrati. Nel repo c'è `docs/speaker-id.md` con una procedura per training di 3 profili (tu + altre 2 persone di casa). Latenza aggiunta: ~200 ms. Precisione: 85–92% dopo 5 minuti di training per profilo. È quello che permette a Q di rispondere ai bambini e a HomeClaw di rispondere a te.

---

## Cosa HomeClaw non fa bene (essere onesti)

Non è Alexa-ma-locale: ha buchi. Elencarli è onesto e salva una settimana di frustrazioni.

**Musica e streaming**. Piper è per voce parlata, non cantata. Per "suonami X", HomeClaw deve delegare a un sistema esterno (Spotify tramite Home Assistant, Music Assistant, Sonos, ecc.). Puro stack locale = niente musica.

**Trascrizione continua e conversazione multi-turn naturale**. Whisper fa trascrizione "a batch", non streaming vero. Tra la fine del tuo comando e la risposta c'è sempre pausa. Le conversazioni a ping-pong lunghe stancano. HomeClaw è bravissimo a "un comando, una risposta"; è meno bravo a "parliamone".

**Interruzione dell'agente mentre parla**. Senza AEC vero (quindi senza ReSpeaker USB 4-Mic) non puoi dire "basta" a HomeClaw che sta parlando. Anche con AEC è fragile in presenza di rumore.

**Accenti forti, dialetti, voci di bambini**. Whisper è addestrato principalmente su italiano standard. Voci con accento siciliano forte, romagnolo stretto, bambini sotto i 6 anni: accuracy crolla al 60–70%. Fine-tuning con tuoi audio migliora molto.

**Rispondere a stimoli non verbali**. Alexa si accende con battito di mani in alcuni setup. HomeClaw no, per scelta: tutto passa dalla wake word. Niente hotkey fisiche, niente motion trigger. Volendo si aggiunge, ma non è incluso.

**Query che richiedono conoscenza profonda in locale**. Nemotron-3B non sa chi ha vinto lo scudetto del 1984. Se sei in modalità air-gapped e fai domande di cultura generale, la qualità è da "piccolo bambino curioso ma male informato". Routing al cloud per quelle query, sempre.

**Failover graceful quando internet va giù**. Se sei configurato con cloud LLM e la connessione si interrompe, il bridge si blocca in timeout di 8 secondi per query. HomeClaw risponde "non riesco a raggiungere il mio cervello". Gestibile — il Tier B con Nemotron locale fa da fallback automatico — ma richiede configurazione esplicita nel SOUL.md (vedi sezione successiva).

---

## Prompt pronto — il SOUL.md di HomeClaw

HomeClaw ha esigenze diverse da un agente Telegram. Le risposte devono essere brevissime (un TTS di 30 secondi stanca), senza Markdown, senza elenchi puntati, e devono essere robuste all'ambiguità del parlato. Ecco un SOUL.md di partenza. La versione completa è nel repo, in `soul-templates/SOUL.md` — attenzione: i template del repo sono **in inglese** (convenzione del progetto), quindi traduci o adatta le regole qui sotto se vuoi un SOUL.md italiano come questo:

> "Sei HomeClaw, un assistente vocale locale che vive su un Raspberry Pi nel salotto. Le tue risposte vengono lette ad alta voce da un sintetizzatore vocale. Regole non negoziabili:
>
> - **Brevità.** Rispondi in massimo 2 frasi, 30 parole totali. Per liste di più di 3 elementi di' 'ci sono cinque cose, te le mando su Telegram' e invia un messaggio.
> - **No Markdown.** Mai asterischi, mai trattini-elenco, mai simboli (%, €, °). Scrivi a parole: 'venti per cento', 'venticinque euro', 'ventidue gradi'. Esempio da non fare: 'temperatura **22°C**'. Esempio da fare: 'ventidue gradi'.
> - **Chiarifica una volta sola.** Se il comando è ambiguo, fai UNA domanda di chiarimento brevissima. Mai più di una.
> - **Conferma silenziosa per comandi banali.** Per 'timer N minuti', 'accendi la luce', 'spegni la sveglia' → NON parlare, risposta `[SILENT_OK]` e il LED verde fa da conferma. Parola = costo d'attenzione; non sprecarla.
> - **Smart home**: usa la skill `home-assistant`. Rispondi solo 'Fatto' o 'Non ho trovato [nome]'.
> - **Routing modello**: meteo/orari/math/controllo casa → Nemotron-3B locale. Brainstorming/email/coding/ricerca → Claude Sonnet. Topic sensibili (password, medici, finanze) → SEMPRE locale, MAI cloud.
> - **Privacy**: le query con keyword ['password', 'banca', 'diagnosi', 'medicina', nomi dei familiari minori] non escono mai dall'hub. Se non puoi rispondere in locale di' 'questa è meglio che la guardi tu' e mandala su Telegram.
> - **Conferma esplicita per azioni irreversibili**: inviare email, fare acquisti, cancellare eventi, modificare il budget di casa → chiedi 'confermo HomeClaw' esplicitamente. Se la conferma non arriva in 10 secondi, abortisci silenziosamente.
> - **Modalità notte**: tra le 22:00 e le 7:00, voce più bassa, LED al 10%, risposte ancora più brevi, niente notifiche proattive."

**(i) Pro tip.** Il SOUL.md evolve. La prima settimana lo rileggi e lo modifichi ogni sera basandoti su cosa non ha funzionato. Esempio reale: ho dovuto aggiungere "NON leggere mai URL ad alta voce, sostituiscili con 'apri il link che ti ho mandato su Telegram'" dopo che HomeClaw mi ha letto `https://www.repubblica.it/politica/2026/04/22/news/...` letter-by-letter per 40 secondi.

**Prompt pronto — la prima conversazione con HomeClaw dopo l'installazione:**

> "Ciao HomeClaw, sei sveglio per la prima volta. Leggi il tuo SOUL.md e riassumilo in 2 frasi. Poi dimmi tre cose che sai fare e tre cose che non farai mai. Stai per essere messo al centro della mia casa, voglio essere sicuro di aver capito come ti comporti."

---

## Home Assistant: il vero moltiplicatore

OpenClaw e Home Assistant sono complementari: Home Assistant è il migliore al mondo a **parlare con dispositivi** (Zigbee, Z-Wave, Matter, Hue, Shelly, Sonos, termostati, solare, auto elettriche — 2000+ integrazioni). OpenClaw è il migliore al mondo a **ragionare sui bisogni**. Farli dialogare moltiplica entrambi.

### Architettura del bridge HA ↔ HomeClaw

Tre modi, in ordine di crescente potenza:

**Modalità 1 — Home Assistant come fornitore di dispositivi (consigliata)**
- Home Assistant rimane il padrone dei dispositivi, controllato da dashboard, timer, automazioni sue
- OpenClaw HomeClaw ha una skill `home-assistant` che chiama `POST /api/services/{domain}/{service}` con un long-lived access token
- "Ehi Claw, accendi la luce del salotto" → HomeClaw capisce intent → skill chiama `light.turn_on` con `area: 'salotto'`
- HA fa il lavoro, conferma, HomeClaw risponde "Fatto"
- Vantaggio: separazione pulita, Home Assistant UI continua a funzionare per il partner non tecnico, OpenClaw aggiunge solo la voce AI sopra

**Modalità 2 — Home Assistant come conversation agent**
- Usi il wyoming-satellite direttamente con HA (non con il nostro bridge)
- HA ha la sua "Assist" pipeline: wake → STT → intent parser → TTS
- Configuri un custom component HA che routa le query a OpenClaw invece che al parser built-in
- Più lavoro, più integrato, richiede scrivere un `custom_components/openclaw_conversation/` per HA

**Modalità 3 — Ibrida**
- Primary wake "Ehi Claw" → HomeClaw (conversazione ricca)
- Secondary wake "Hey Home" → HA Assist (controllo rapido smart home, zero latency LLM)
- Due pipeline parallele sullo stesso hardware

Personalmente consiglio **Modalità 1**. È semplice, robusta, e mantiene HA come padrone delle automazioni "mission critical" (sveglia, termostato, allarme) dove non vuoi che un LLM decida cose strane.

### Esempio concreto di skill `home-assistant`

Nel repo: `docs/home-assistant-integration.md`. In sintesi:

```python
# Inside skill/home-assistant/handler.py
async def light_control(
    area: str, action: str, brightness: int = None
):
    """Control a Home Assistant light via REST API."""
    service = "turn_on" if action == "on" else "turn_off"
    body = {"area_id": area}
    if brightness is not None:
        body["brightness_pct"] = brightness
    path = f"/api/services/light/{service}"
    return await _ha_post(path, body)
```

Con questo, HomeClaw può rispondere a:
- "Accendi le luci del salotto" → `light_control('salotto', 'on')`
- "Luci della camera al 30 per cento" → `light_control('camera', 'on', brightness=30)`
- "Spegni tutto" → loop su tutte le aree

### Awareness contestuale: "HomeClaw sa dove sei"

Con il Tier C multi-stanza, ogni satellite ha un nome (`homeclaw-cucina`, `homeclaw-studio`). Il bridge passa questo nome come `peer` all'agente. Nel SOUL.md aggiungi:

> "Quando ricevi un messaggio dal peer `homeclaw-cucina` e l'utente dice 'accendi la luce' senza specificare dove, assumi che voglia dire 'la luce della cucina'. Conferma silenziosamente."

Questo è il tipo di intelligenza che Alexa non ha. Per Alexa, "accendi la luce" richiede sempre il nome della stanza.

---

## La prima settimana con HomeClaw

Installare è il 20% del lavoro. Domarlo è l'80%. Ecco una tabella di marcia per i primi 7 giorni:

**Giorno 1 — Prima conversazione**. Chiedi solo cose facili: "Che ore sono", "Meteo oggi", "Timer 5 minuti". Scopo: verificare che latenza, STT, TTS, LED, playback funzionino end-to-end. Se non funziona qualcosa, sistemalo ora, prima di aggiungere complessità.

**Giorno 2 — Tuning del SOUL.md**. Leggi le trascrizioni della giornata (`openclaw logs --agent HomeClaw | grep transcript`). Per ogni risposta insoddisfacente, chiediti: è colpa di STT (parole sbagliate), del SOUL (regola mancante), o dell'agente (ragionamento scadente)? Modifica SOUL.md di conseguenza.

**Giorno 3 — Falsi positivi wake word**. Tieni un log: quante volte "Ehi Claw" si è attivato senza che tu parlassi? Se più di 2/ora, fai fine-tuning del wake word con 30 registrazioni tue + 20 negative (TV, radio, silenzio).

**Giorno 4 — Integra UN dispositivo smart home reale**. Una lampada. Solo una. Configura Home Assistant per controllarla, crea la skill `home-assistant`, testa "Ehi Claw, accendi la lampada". Quando funziona bene per un dispositivo, la scalata a dieci è banale.

**Giorno 5 — Cron mattutino e serale**. Aggiungi due cron OpenClaw: alle 7:00 un digest vocale (solo se la camera è "sveglia" — Home Assistant sa se le persone sono in casa), alle 22:00 un wrap-up con domande "serve qualcosa per domani?". Se il mattino suona invadente, passa al silenzio: il briefing va solo su Telegram, HomeClaw parla solo se chiamato.

**Giorno 6 — Aggiungi un agente specializzato**. Es: Q (educativo) per i bambini, con speaker ID che lo attiva quando una voce giovane pronuncia "Ehi Claw". Testa con tuoi figli.

**Giorno 7 — Misura onestamente**. Quante volte HomeClaw ha aiutato? Quante ha fallito? Quanto costano le API nel periodo (`openclaw cost report --since 7d`)? Quanto Alexa ti sarebbe costata in abbonamento? Decidi: continui, migliori, o torni indietro. È un progetto serio solo se lo metti alla prova.

---

## Il build fisico — dalla cassetta Amazon al lobster lamp

Un Raspberry Pi 5 + AI HAT+ 2 + ReSpeaker USB + altoparlante JBL sulla scrivania funziona ma è *brutto*. E se HomeClaw deve stare nel salotto, brutto è veto del partner. Tre livelli di build fisico, in ordine di impegno:

**Livello 1 — Case commerciale**. Argon One V3 per Pi 5 + AI HAT+ 2 (€30, metallo, ventilazione attiva, GPIO accessibili). Metti il Pi nel case, il ReSpeaker e il JBL accanto. È ordinato, si può mettere su una mensola. Totale tempo: 20 minuti.

**Livello 2 — Stampa 3D "HomeClaw desk companion"**. File STL sul Discord OpenClaw (canale `#hardware-builds`, cartella `homeclaw/desk-v3/`). Include: alloggiamento Pi + HAT, foro per ReSpeaker, anello diffusore per LED, altoparlante USB piccolo integrato (consiglio: Anker Soundcore mini, €25). Totale budget: ~€40 in plastica, ~6 ore di stampa. Risultato: qualcosa che sembra un Echo ma rosso-astice.

**Livello 3 — Il "Lobster Lamp"**. Il build del cuore, iconico della community. Una lampada da tavolo in cui l'astice stampato in 3D è la lampada stessa: le LED del ReSpeaker si vedono attraverso la corazza traslucida, il microfono è nelle "antenne", l'altoparlante nella base. Primo build di @pablito_gamma (video su YouTube), poi iterato dalla community. File STL multi-parte, richiede una Bambu A1 o stampante FDM con 4 colori. Tempo totale: un weekend di stampa + montaggio. Risultato: vince tutti gli amici quando vengono a cena.

Indipendentemente dal livello, tre regole d'oro del build fisico:

1. **Ventilazione**. Il Pi 5 + HAT+ 2 sotto carico (inferenza LLM continua) scalda. Servono prese d'aria o ventola, senza eccezioni. Un case sigillato causa throttling e crash termici.
2. **Accessibilità del pulsante mute**. Il ReSpeaker USB ha un tasto fisico che disabilita il microfono. Il tasto DEVE essere accessibile senza aprire il case. Privacy = fisica, non solo software.
3. **LED visibili da distanza**. Se il LED è nascosto dentro una feritoia, il feedback visuale è inutile. Sii generoso con l'area LED visibile.

---

## Modalità air-gapped — zero cloud

Se vuoi zero dipendenza dal cloud (privacy paranoica, cabina di montagna, ufficio compliance-sensitive), il Tier B lo permette. Ecco cosa cambia:

- **LLM**: solo Nemotron-3B-Instruct o Phi-3-mini tramite `hailo-ollama` sul Hailo-10H. Latenza 0,6–1,5 s, qualità "buona per comandi casalinghi e query brevi", scarsa per knowledge avanzata
- **STT**: Whisper small locale (già è così nel setup base)
- **TTS**: Piper locale (già è così nel setup base)
- **Ricerca web**: disabilitata, o via `searxng` locale che instrada su motori pubblici senza lasciare la tua identità
- **Network rules**: iptables che bloccano tutto l'outbound eccetto Wi-Fi LAN + NTP + mirror apt/GitHub per gli aggiornamenti
- **Canali di comunicazione**: solo il canale voce + Matrix self-hosted (nel Capitolo 6 è elencato)

Cosa perdi: Opus/Sonnet non rispondono più su temi complessi. Per "qual è la storia del Partenone?" avrai la risposta di un modello da 3 miliardi di parametri, che *sa molto meno* di uno da 500 miliardi. Per "accendi la luce", "che ore sono", "aggiungi latte alla lista della spesa", "leggimi le ultime 3 email": nessuna differenza percepibile.

Io personalmente faccio un compromesso: cloud abilitato ma con regola SOUL.md chiara che le query contenenti keyword sensibili (nomi dei bambini, medici, finanze, password) restano locali. Compromesso pragmatico.

---

## Tier C in breve — satelliti multi-stanza

Per portare "Ehi Claw" in cucina e camera da letto non serve un altro Pi5 per ogni stanza. Due opzioni:

**Opzione 1 — ESP32-S3-BOX-3 (€65/stanza)**. Flash ESPHome con la configurazione `voice-assistant`. Il box fa microWakeWord on-device, streama al Gateway Wyoming dell'hub, riproduce l'audio di risposta. Ha anche uno schermetto dove puoi mostrare informazioni visive (meteo, timer, notifica email). Zero manutenzione Linux — è un firmware.

Il file `esphome/satellite-esp32s3-box3.yaml` nel repo contiene una configurazione testata. Flash con `esphome run satellite-esp32s3-box3.yaml` dopo aver collegato il box via USB-C.

**Opzione 2 — Raspberry Pi Zero 2 W + ReSpeaker 2-Mic HAT + altoparlante (€75/stanza)**. Più flessibile, più lavoro: Pi OS 64-bit sul Zero 2 W + wyoming-satellite locale + wake word leggero. Sul Zero 2 W il 2-Mic HAT funziona bene. Audio migliore dell'ESP32-S3 grazie al codec WM8960. Ma devi gestire un altro Linux.

Il Gateway OpenClaw non cambia — le skill vedono ogni satellite come un peer del canale `voice` con un nome diverso (`homeclaw-studio`, `homeclaw-cucina`, `homeclaw-camera`). Puoi far sapere all'agente dove si trova ogni peer nel file `~/.openclaw/workspace-homeclaw/peers.yaml`. Nota: `peers.yaml` **non è incluso nel repo** — crealo a mano con questo contenuto:

```yaml
peers:
  homeclaw-studio:
    room: studio
    area_id: studio
  homeclaw-cucina:
    room: cucina
    area_id: cucina
  homeclaw-camera:
    room: camera da letto
    area_id: camera
    quiet_hours: "22:00-07:00"
```

Con `quiet_hours` la camera da letto usa volume e dettaglio ridotti di notte, senza altre regole. Piccole cose che cambiano l'esperienza.

---

## Perché non Arduino (e perché ESP32-S3 sì)

- **Arduino Uno/Nano/Mega**: non ci provare. 8–16 MHz, niente DSP, niente Wi-Fi di serie. Al massimo keyword spotting molto limitato con Edge Impulse. Nessuna speranza di ASR generica.
- **Arduino Nicla Voice**: ha un DSP Syntiant NDP120 ottimo per wake word, ma non fa ASR generica. Potrebbe sostituire l'ESP32-S3 come satellite, ma costa €90 — più dell'ESP32-S3-BOX-3 che ha già schermo + altoparlante + touch. Non vale.
- **Arduino Portenta X8**: è praticamente un mini-PC (Cortex-A53 + Yocto Linux). Potrebbe girare Whisper.cpp, ma costa €250. A quel prezzo compri un Pi5 e sei più libero.
- **ESP32-S3** (Seeed XIAO ESP32-S3 Sense, M5Stack ATOM Echo, Espressif ESP32-S3-BOX-3): il vero "Arduino per voice" nel 2026. Si programma con Arduino IDE o ESPHome, ha Wi-Fi, microfono I2S, abbastanza potenza per microWakeWord on-device, costa €13–65.

In breve: l'HUB vuole una macchina full-OS (Raspberry Pi 5). I SATELLITI vogliono un microcontrollore connesso economico (ESP32-S3). Arduino classico sta in mezzo: troppo debole per l'hub, troppo ingombrante/costoso per i satelliti rispetto all'ESP32.

---

## Confronto costi a 3 anni

- **Alexa Echo Dot gen 5** — hardware €55; servizi €0–60/anno (Prime/Alexa+); totale 3 anni: €55–235.
  Privacy: cloud USA. Estendibilità: bassa.
- **Google Nest Mini** — hardware €60; servizi €0/anno, ma pubblicità in arrivo; totale 3 anni: ~€60.
  Privacy: cloud USA. Estendibilità: media.
- **HomeClaw Tier A** — hardware €130; servizi €30–60/anno (API + elettricità); totale 3 anni: €220–310.
  Privacy: locale ibrido. Estendibilità: alta.
- **HomeClaw Tier B** — hardware €380; servizi €30–120/anno (API + elettricità); totale 3 anni: €470–740.
  Privacy: locale ibrido. Estendibilità: altissima.
- **HomeClaw Tier B air-gapped** — hardware €380; servizi €12/anno (solo elettricità); totale 3 anni: €416.
  Privacy: totale. Estendibilità: altissima.
- **HomeClaw Tier C 3 stanze** — hardware €550; servizi €50–150/anno; totale 3 anni: €700–1000.
  Privacy: locale ibrido. Estendibilità: altissima.

Il Tier B non vince sul prezzo contro Echo Dot. Vince su tre cose che Echo Dot non vende: sai cosa fa, puoi estenderlo a piacere, nessuno scorre nei tuoi comandi per targettizzare pubblicità.

---

## Diagnosi rapida — l'albero da tenere accanto all'hub

**(#) Debug:** quando qualcosa non funziona, parti da qui. Questo albero porta al problema nel 90% dei casi; per i dettagli di ogni ramo, vedi la sezione "Errori comuni e come risolverli" subito sotto.

```text
L'agente non risponde?
├─ LED acceso quando dici "Ehi Claw"?
│  ├─ NO → wake word non rileva:
│  │      mic (arecord/aplay), servizio
│  │      openwakeword, threshold 0.4
│  └─ SÌ → segui la catena
│         whisper → bridge → agente
│         (journalctl + openclaw logs)
├─ Latenza > 4 secondi?
│  ├─ Tier A → resta su base-int8
│  ├─ Tier B → hailortcli identify
│  ├─ RAM → free -h (swap in uso?)
│  └─ Rete → iperf3 verso l'hub
├─ Falsi positivi wake word?
│  └─ fine-tuning con audio reali
├─ Audio distorto o rotto?
│  └─ alimentatore 27W, arecord -L,
│     Bluetooth power-save, HDMI
└─ Il TTS legge i simboli?
   └─ SOUL.md + _clean_for_tts()
```

---

## Errori comuni e come risolverli

- **Sintomo:** dici "Ehi Claw" e il LED non si accende mai.
  Causa: la wake word non viene rilevata — microfono muto, servizio fermo o threshold troppo severo.
  Fix: registra e riascolta con `arecord` e `aplay`; controlla `systemctl status wyoming-openwakeword`; prova `--threshold 0.4` (più sensibile); se la wake word è custom, fai fine-tuning del modello.

- **Sintomo:** il LED pulsa blu, ma la risposta non arriva mai.
  Causa: la catena STT → bridge → agente è interrotta in uno dei tre anelli.
  Fix: seguila nell'ordine: `journalctl -u wyoming-faster-whisper -f` (l'STT lavora?), `journalctl -u homeclaw-bridge -f` (il bridge riceve?), `openclaw logs --follow` (l'agente risponde?).

- **Sintomo:** latenza sopra i 4 secondi.
  Causa: modello Whisper troppo pesante per l'hardware, NPU non attiva, RAM esaurita o Wi-Fi instabile.
  Fix: sul Tier A resta su `base-int8` (non `small`); sul Tier B verifica il NPU con `hailortcli fw-control identify`; controlla lo swap con `free -h` (se è in uso, serve il Pi 5 16GB o un modello più piccolo); misura la rete con `iperf3` verso l'hub e sotto i 50 Mbps passa a Ethernet.

- **Sintomo:** la wake word si attiva da sola, più di 2 volte l'ora.
  Causa: modello addestrato solo su voci sintetiche; TV o radio che "parlano" all'agente.
  Fix: fine-tuning con 30–50 registrazioni reali della tua voce più negative examples, comprese le voci che lo ingannano (procedura in `docs/wakeword-training.md` del repo); con la TV accesa alza il threshold a 0,6 o stringi il VAD.

- **Sintomo:** audio distorto, ReSpeaker che sparisce, Bluetooth che si sgancia ogni 10 secondi.
  Causa: alimentatore sottodimensionato (15 W = throttling USB) o power-save del modulo Bluetooth.
  Fix: usa l'alimentatore ufficiale da 27W; verifica con `arecord -L` che compaia `ArrayUAC10`; aggiungi `Disable=Handsfree,FakePlayer` in `/etc/bluetooth/main.conf` e riavvia `bluetoothd` — o passa a un altoparlante USB, più affidabile per l'always-on; se l'audio HDMI interferisce, `dtparam=audio=off` in `/boot/firmware/config.txt`.

- **Sintomo:** il TTS legge asterischi e simboli letter-by-letter.
  Causa: l'agente risponde in Markdown.
  Fix: prima aggiorna il SOUL.md con esempi concreti ("non dire *importante* ma 'importante'"), poi verifica che il bridge applichi `_clean_for_tts()` alla risposta.

- **Sintomo:** il driver Hailo crasha dopo `apt full-upgrade`.
  Causa: kernel aggiornato senza driver Hailo corrispondente.
  Fix: `sudo apt-mark hold raspberrypi-kernel raspberrypi-kernel-headers` finché Hailo non rilascia il driver per il kernel nuovo, poi reinstalla il driver.

- **Sintomo:** HomeClaw risponde in inglese anche se parli italiano.
  Causa: l'auto-detect della lingua di Whisper sbaglia sulle frasi corte.
  Fix: verifica che il flag `--language it` sia presente nel service `wyoming-faster-whisper` (nei service file del repo c'è già; se l'hai scritto a mano, aggiungilo); nel SOUL.md: "Rispondi sempre in italiano, a meno che il comando non sia esplicitamente in un'altra lingua."

- **Sintomo:** "Ehi Claw" riconosciuto, ma il comando successivo trascritto male o troncato.
  Causa: finestra di silenzio prima della trascrizione troppo aggressiva.
  Fix: nel satellite aumenta `--vad-threshold 0.3` (più permissivo sul silenzio) e `--max-recording-seconds 15`.

---

## Il codice di questo capitolo

Tutto il materiale di questo capitolo — il bridge Python completo, i systemd service, lo script LED feedback, i template SOUL.md, la configurazione ESPHome per satelliti, gli script di installazione e diagnostica — è nel repo del libro:

```text
homeclaw-repo/
├── README.md             # guida end-to-end
├── LICENSE               # MIT
├── CHANGELOG.md
├── CONTRIBUTING.md
├── skill/
│   ├── SKILL.md          # definizione skill
│   ├── bridge.py         # Wyoming <-> OpenClaw
│   ├── openclaw_client.py
│   └── requirements.txt
├── systemd/              # 6 service da copiare
│   ├── wyoming-openwakeword.service
│   ├── wyoming-faster-whisper.service
│   ├── wyoming-piper.service
│   ├── wyoming-satellite.service
│   ├── homeclaw-bridge.service
│   └── homeclaw-led-feedback.service
├── led-feedback/
│   ├── homeclaw_led_feedback.py
│   ├── requirements.txt
│   └── README.md
├── soul-templates/       # template (in inglese)
│   ├── SOUL.md
│   ├── IDENTITY.md
│   ├── TOOLS.md
│   └── AGENTS.md
├── scripts/
│   ├── install-tier-b.sh # installer Tier B
│   ├── doctor.sh         # diagnostica
│   ├── backup.sh         # backup config
│   └── benchmark.sh      # latenza end-to-end
├── esphome/
│   ├── satellite-esp32s3-box3.yaml
│   └── secrets.yaml.example
└── docs/
    ├── architecture.md       # protocol flow
    ├── hardware-bom.md       # BOM verificata
    ├── wakeword-training.md  # "Ehi Claw"
    ├── home-assistant-integration.md
    ├── speaker-id.md         # profili voce
    └── troubleshooting.md    # manuale esteso
```

Licenza MIT. Clona, fork, migliora, contribuisci — è open-source come OpenClaw stesso.

---

## Checklist di fine capitolo

- [ ] Raspberry Pi 5 (16GB se vuoi LLM locale) con Pi OS Bookworm 64-bit attivo
- [ ] AI HAT+ 2 con Hailo-10H riconosciuto (`hailortcli fw-control identify`) — se Tier B
- [ ] Microfono USB o ReSpeaker USB 4-Mic visto da `arecord -L`
- [ ] Altoparlante (USB o BT) visto da `aplay -L`
- [ ] Quattro systemd service attivi: `wyoming-openwakeword`, `wyoming-faster-whisper`, `wyoming-piper`, `wyoming-satellite`
- [ ] OpenClaw Gateway containerizzato (Livello 2 del Cap. 4) in esecuzione
- [ ] Agente `HomeClaw` creato con `openclaw agents add HomeClaw`
- [ ] Skill `homeclaw-bridge` installata e bindata al canale `voice`
- [ ] Service `homeclaw-bridge` systemd attivo
- [ ] SOUL.md di HomeClaw scritto con le regole "brevità + no-Markdown + privacy + conferme"
- [ ] (Tier B) Wake word custom "Ehi Claw" addestrato, deployato e testato per falsi positivi per 24 ore
- [ ] (Tier B) Script LED feedback attivo, il lobster lampeggia quando ascolta, pensa, parla, sbaglia
- [ ] AEC verificato: parlare a HomeClaw mentre HomeClaw parla non lo confonde
- [ ] (Opzionale) Home Assistant connesso, almeno 1 dispositivo smart home comandabile a voce
- [ ] (Tier C) Almeno 1 satellite ESP32-S3 o Pi Zero 2 W funzionante, con nome stanza
- [ ] (Tier C) Peers.yaml configurato con `area_id` e `quiet_hours` per ogni stanza
- [ ] Interruttore fisico di mute del microfono accessibile senza aprire il case
- [ ] Test end-to-end: "Ehi Claw, che ore sono?" risponde in <2,5 secondi
- [ ] Test edge-case: "Ehi Claw, leggi la mia ultima email" → riassunto di 2 frasi + dettagli su Telegram
- [ ] Prima settimana completata: SOUL.md rivisto almeno 3 volte, wake word fine-tuned
- [ ] Backup della cartella `.openclaw/` + immagine microSD su disco esterno
- [ ] `openclaw cost report` controllato: rientri nel budget stimato

---

## Cosa provare dopo

Il Capitolo 17 (skill personalizzate) ti dà i mattoni per aggiungere a HomeClaw comandi specifici della tua casa: una skill `lista-spesa` che sincronizza con Todoist, una `ricette` che legge i libri di cucina digitalizzati in Obsidian, una `bimbi` che fa domande-indovinelli quando senti la voce dei bambini. Il Capitolo 18 (cron avanzati) permette abitudini vocali proattive: "Ogni mattina alle 7:15 saluta buongiorno e leggi il meteo se sta per piovere, solo se c'è qualcuno sveglio in casa."

Il Capitolo 12 (comunicazione e coordinamento tra agenti) si sposa con il Tier C in modo interessante: HomeClaw come agente voice "front-end" e, dietro, Polly per gli orari, Max per il marketing, Q per le domande dei bambini, Finn per la famiglia. HomeClaw sente la voce, capisce di chi è il dominio, e delega. Il lobster non è solo — ha un team.

E quando, tra un anno, vorrai far rispondere HomeClaw con il tono di tua madre che ti chiama a pranzo, troverai che Piper permette di clonare voci con 30 minuti di registrazioni autentiche e un Google Colab. Ma quella è un'altra storia, e forse un altro capitolo.

---

## Link e risorse utili

- [Componenti Wyoming di Rhasspy](https://github.com/rhasspy) — i repo `wyoming-satellite`, `wyoming-openwakeword`, `wyoming-faster-whisper`, `wyoming-piper`
- [Documentazione Raspberry Pi — sezione AI](https://www.raspberrypi.com/documentation/computers/ai.html) — installazione del driver Hailo per l'AI HAT+ 2 (Step 2)
- [openWakeWord — notebook Colab "Automatic model training (simple)"](https://colab.research.google.com/github/dscripka/openWakeWord/blob/main/notebooks/automatic_model_training_simple.ipynb) — addestramento della wake word custom senza GPU propria (Step 8)
- [Piper voices](https://github.com/rhasspy/piper-voices) — voci italiane ufficiali e comunitarie per il TTS
- [Home Assistant — Voice control](https://www.home-assistant.io/voice_control/) — il "Year of the Voice" e la pipeline Assist
- [Home Assistant — REST API](https://developers.home-assistant.io/docs/api/rest/) — gli endpoint usati dalla skill `home-assistant`
- [pyannote-audio](https://github.com/pyannote/pyannote-audio) — speaker embedding per lo speaker ID
- [ESPHome — Voice assistant](https://esphome.io/components/voice_assistant.html) — configurazione dei satelliti ESP32-S3 (Tier C)
- [Seeed ReSpeaker USB 4-Mic Array](https://wiki.seeedstudio.com/ReSpeaker_Mic_Array_v2.0/) — documentazione di microfono, AEC hardware e beamforming
- Discord OpenClaw, canale `#hardware-builds` — file STL dei case stampati in 3D (sezione "Il build fisico")

Per l'elenco completo delle fonti del libro, vedi [Appendice E](./Appendici/E-risorse-e-link-utili.md).

---

*Capitolo extra scritto il 24 aprile 2026. Lo stack open-source voice evolve rapidamente; verifica versioni di `wyoming-*` e driver Hailo prima di iniziare. Benchmark eseguiti su Raspberry Pi 5 16GB con AI HAT+ 2 e kernel 6.12, ReSpeaker USB 4-Mic Array, Piper `it_IT-paola-medium`. Codice completo e MIT-licensed nel repo del libro, cartella `homeclaw-repo/`.*

---

[← Capitolo 22](./PARTE-VIII-Visione-futuro/22-futuro-del-lavoro-con-gli-agenti.md)  ·  [Indice](./README.md)  ·  [Appendici →](./Appendici/A-glossario.md)
