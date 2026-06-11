# Capitolo 5 — Installazione step-by-step [★]

## Cosa imparerai

- Preparare il computer in dieci minuti: account dedicato, Node 22.16+, prerequisiti giusti
- Scegliere fra `install.sh`, `npm`, sorgente e Docker, con le note per macOS, Linux e Windows/WSL2
- Generare la API key e navigare il wizard schermata per schermata, dopo il ban Anthropic del 4 aprile 2026
- Cosa scrive il wizard sul disco (stato vs workspace) e cosa aspettarti di spendere nei primi sette giorni
- Validare il setup con `openclaw doctor`, aggiornare, fare backup e disinstallare in sicurezza

## Prerequisiti

Aver letto il [Capitolo 3](./03-scegliere-dove-installare-openclaw.md) e scelto **dove** installare OpenClaw — Mac Mini dedicato, VPS, Raspberry Pi o cloud managed. Se hai letto anche il [Capitolo 4](./04-preparare-un-ambiente-sicuro-docker-sandbox.md), tieni a mente l'ordine giusto: il sandbox si applica **dopo** questa installazione. Prima installi, poi blindi.

Cosa devi avere a portata di mano: un account utente dedicato (mai il tuo profilo personale di lavoro) e dieci minuti di attenzione senza interruzioni. Una **Gmail dedicata** all'agente e **Chrome** servono solo se userai la skill `gog` o la browser automation: non sono obbligatori per installare. Il wizard fa quattro o cinque scelte importanti: sbagliarne una significa rifarlo da capo, o accorgersene una settimana dopo.

Verifica veloce, da incollare nel terminale prima dell'installazione:

```bash
node --version    # >= 22.16 (24 raccomandato)
git --version     # qualsiasi versione recente
curl --version    # qualsiasi versione recente
echo $SHELL       # /bin/zsh o /bin/bash
```

Se `node` manca o è vecchio, l'installer lo aggiunge per te, ma è più rapido (e più pulito) installarlo a mano prima.

## Contenuto principale

### TL;DR — installazione in dieci minuti

Se hai già un account dedicato e dieci minuti, questi sono i comandi essenziali; il resto del capitolo spiega cosa fanno davvero.

```bash
# 1. install OpenClaw (auto-detect OS);
#    the installer launches onboarding itself
curl -fsSL https://openclaw.ai/install.sh | bash

# 2. only if onboarding did NOT start by itself
openclaw onboard --install-daemon

# 3. verify everything is healthy
openclaw doctor
openclaw gateway status

# 4. open the local dashboard
openclaw dashboard
```

Quando l'ultimo comando apre `http://127.0.0.1:18789` e la chat funziona, l'installazione è andata a buon fine: da qui in poi è solo configurazione.

### Pre-work — i dieci minuti che ti risparmiano due ore

Prima di lanciare qualunque cosa, quattro mosse in quest'ordine.

**Account dedicato.** Crea un nuovo utente sul sistema — `openclaw`, `claw`, `agente` — e installa OpenClaw lì dentro. Su macOS: *Impostazioni di Sistema → Utenti e Gruppi → Aggiungi Account*; su Linux: `sudo adduser openclaw`; su Windows: *Impostazioni → Account → Famiglia e altri utenti*. Quando l'agente sbaglierà un comando — e accadrà — vorrai un perimetro che separi il suo errore dai tuoi file.

**Gmail dedicata (solo se userai la skill `gog`).** Registra un nuovo indirizzo Gmail per l'agente, *non* il tuo: identità separata significa nessuna confusione fra "l'ho mandata io" e "l'ha mandata lui", e revoca a singolo click.

**Chrome (solo per la browser automation).** OpenClaw guida tutti i browser, ma Chrome ha il binding più maturo (cookie store, DevTools protocol, profili separati). Se non farai navigare l'agente, salta il passo.

**Password manager pronto.** Crea una *vault* `OpenClaw` nel tuo password manager: ci salverai API key, token Telegram, token GitHub, eventuale password Gmail. **Nulla di tutto questo deve mai finire in chiaro in un file `.env` versionato.**

**(!) Attenzione:** non saltare l'account dedicato perché "tanto è la mia macchina": OpenClaw scrive in `~/.openclaw`, esegue cron e comandi shell.

### Quattro modi di installare — qual è il tuo

L'install ufficiale è uno script `bash` che fa il 95% del lavoro; le altre tre strade hanno ognuna un caso d'uso preciso.

**Modo 1 — `install.sh` (consigliato a tutti).** Rileva OS e architettura, installa Node se manca, scarica l'eseguibile e avvia il wizard. È il default per macOS, Linux e (via WSL2) Windows.

```bash
curl -fsSL https://openclaw.ai/install.sh | bash
```

Su Windows in PowerShell l'equivalente è `iwr -useb https://openclaw.ai/install.ps1 | iex`.

**(i) Pro tip:** prima di pipare uno script in `bash` o `iex`, leggilo: `curl -O`, scorri il file, poi `bash install.sh`. Abitudine che vale per qualunque installer.

**Modo 2 — `npm` globale.** Se vuoi evitare lo script bash o sei dietro una rete che blocca i `curl | bash`:

```bash
npm install -g openclaw
openclaw onboard --install-daemon
```

Richiede Node 22.16+ e la global bin di `npm` nel `PATH` (vedi "Errori comuni").

**Modo 3 — Sorgente (per chi contribuisce o vuole leggersi il codice).** Clona `github.com/openclaw/openclaw`, poi `npm install && npm run build` e `npm link`. Utile per vedere il diff fra una release e la `main` o patchare al volo qualcosa per uso interno.

**Modo 4 — Docker / Compose (per ambienti isolati).** Se hai scelto il Livello 2 del Capitolo 4 (Gateway containerizzato), salti tutto questo capitolo e lanci:

```bash
git clone https://github.com/openclaw/openclaw.git
cd openclaw
./scripts/docker/setup.sh
```

Il setup monta `~/.openclaw` come volume (stato e, al suo interno, `workspace/`), espone la porta `18789` e parte; l'onboarding appare alla prima connessione alla dashboard.

### Dettagli per sistema operativo

Ogni piattaforma ha dettagli che, ignorati, costano un'oretta: vai diretto al paragrafo del tuo OS.

**macOS — Apple Silicon (M1/M2/M3/M4).** Lo script funziona out-of-the-box (binari *fat* arm64 + x86_64). Tre cose da sapere:

- Se hai **Homebrew**, installa Node prima: `brew install node@22`; lo script userà quello.
- L'installer crea `~/Library/LaunchAgents/ai.openclaw.gateway.plist`; lo gestisci con `launchctl list | grep openclaw`.
- Su M1/M2 di prima generazione può servire *Rosetta 2* per le skill con binari Intel: `softwareupdate --install-rosetta --agree-to-license`.

**macOS — Intel (Mac Mini 2018, MacBook Pro 2019).** Funziona, ma in regime "best effort". Fissa Node a 22.16 (non 24): qualche package nativo non è ancora aggiornato per Node 24 su Intel-Mac.

**Linux — Ubuntu/Debian.** L'installer cerca `apt` e installa `curl`, `git` e Node (via NodeSource) se mancano. Il daemon è una *user systemd unit* (`openclaw-gateway.service`); aggiungi `loginctl enable-linger <utente>` se deve partire anche senza login attivo (server headless).

**Linux — Fedora / RHEL / CentOS Stream.** Stesso flusso con `dnf` e NodeSource RPM. Su Fedora 40+ SELinux è in *enforcing*: se `openclaw doctor` lamenta `permission denied`, controlla i log con `sudo ausearch -m avc -ts recent`.

**Linux — Arch / Manjaro.** Più rapido di tutti:

```bash
sudo pacman -S nodejs npm
curl -fsSL https://openclaw.ai/install.sh | bash
```

Esiste anche un pacchetto AUR non ufficiale (`openclaw-bin`): controlla che maintainer e versione siano aggiornati prima di affidarti.

**Windows — WSL2 (consigliato).** In PowerShell:

```powershell
# install WSL2 with Ubuntu
wsl --install -d Ubuntu-22.04
```

Poi, dentro la shell Ubuntu di WSL, aggiorna (`sudo apt update && sudo apt upgrade -y`) e lancia l'installer Linux visto sopra. Specifiche di WSL: il filesystem dell'agente vive in `~/.openclaw` *dentro* WSL, non in `C:\Users\<tu>\.openclaw`; la dashboard è raggiungibile dal browser Windows su `http://localhost:18789` (port forwarding automatico); per il boot di Windows serve un task scheduler che lanci `wsl -d Ubuntu-22.04 -e openclaw gateway start`.

**Windows — PowerShell nativo (sconsigliato).** Lo script `install.ps1` esiste, ma molte skill assumono ambiente POSIX e si comportano in modo incoerente. Usalo solo se una policy aziendale ti vieta WSL2.

**(i) Pro tip:** qualunque sia l'OS, dopo l'installazione lancia `openclaw doctor`: i guasti più frequenti sono Node troppo vecchio su Linux, Windows senza WSL2 e macOS Intel con Node 24.

### Il wizard di onboarding, schermata per schermata

Subito dopo l'install, lo script chiama automaticamente `openclaw onboard --install-daemon`. Il flag registra il Gateway come servizio di sistema: partirà al boot e sopravviverà alla chiusura del terminale. Senza, gira solo finché tieni aperta la finestra — utile per testare, doloroso per usare davvero.

Il wizard mostra otto schermate. Le passiamo una a una.

**Schermata 1 — Avviso di sicurezza.** Un riassunto onesto di cosa OpenClaw può fare: leggere file, eseguire comandi, navigare la rete, mandare messaggi. Non è teatro: leggilo prima di accettare.

**Schermata 2 — Workspace.** Dove l'agente scriverà i suoi file. Il default `~/.openclaw/workspace` va bene per il 95% dei casi. Quello che metterai qui sarà *direttamente accessibile* dall'agente: niente segreti, niente roba personale.

**Schermata 3 — Modello LLM.** Il cuore della scelta. A maggio 2026 le opzioni mainstream sono tre.

| Modello | Provider | Quando sceglierlo |
|---|---|---|
| Claude Sonnet 4.6 | Anthropic | Default per agente generale |
| GPT-5.1 | OpenAI | Forte su codice e tool use |
| Gemini 2.5 Ultra | Google | Multimodale, finestra molto lunga |

La scelta non è irreversibile (`openclaw config set model <slug>`), ma cambiarla *spesso* costa: l'agente impara a "parlare" col modello iniziale. Scegli quello con cui pensi di restare almeno tre mesi.

**(i) Pro tip:** parti con Claude Sonnet 4.6 come unico default; il *router* multi-modello (Haiku per i task leggeri, Opus 4.6 come opzione premium) si configura in fase due, vedi Cap. 14. Un solo modello tiene il setup pulito.

**Schermata 4 — Autenticazione.** Qui c'è il bivio post-ban. Tre opzioni teoriche, una sola realmente sostenibile.

- **API key (consigliata).** Pay-as-you-go: paghi i token che consumi, nessun rischio di ToS violation. Incolla la key quando richiesta; viene salvata cifrata in `~/.openclaw/credentials/`.
- **Sottoscrizione ChatGPT Plus / Pro.** OpenAI ha "benedetto" GPT-5.1 via ChatGPT Pro ($200/mese, ~€185) per agenti come OpenClaw; conviene solo se prevedi un volume equivalente a $200+ al mese.
- **~~Sottoscrizione Claude Pro/Max~~ — bloccata.** Dal **4 aprile 2026** Anthropic ha sospeso l'uso di Claude Pro e Max con tool di terze parti, OpenClaw incluso: chi tenta vede `Unauthorized: subscription not allowed`. Per Claude l'unica via legittima è la **API key pay-as-you-go** (conti esatti nel Cap. 14).

**(!) Attenzione:** non lasciare la API key in chiaro in `~/.bashrc` o in un `.env` versionato: il wizard la cifra sotto `~/.openclaw/credentials/`, non spostarla. Su più macchine, chiavi separate e *credential proxy* del Capitolo 4.

#### Generare la API key — passo per passo per provider

Il wizard si aspetta che tu abbia già la chiave in tasca. Conta cinque minuti per provider.

**Anthropic (Claude Sonnet 4.6).** Il default del libro. Registrati su `console.anthropic.com` e aggiungi un metodo di pagamento in *Settings → Billing*: **senza billing non puoi generare key** (ricarica minima $5, ~€4,60). In *Settings → API keys* fai *Create Key* con un nome riconoscibile. **Copia la key adesso** — viene mostrata una sola volta — e salvala nel password manager. Infine imposta uno *spend limit* in *Settings → Limits*: $20 (~€18) al mese ti tiene al sicuro mentre prendi le misure.

**(!) Attenzione:** la sottoscrizione *Claude Pro/Max* (`claude.ai`) è una cosa diversa dall'API key (`console.anthropic.com`). La prima è bloccata per OpenClaw dal 4 aprile 2026, la seconda no. Se non vedi la voce *API keys*, sei sul sito sbagliato.

**OpenAI (GPT-5.1).** Flusso simile su `platform.openai.com`, con verifica del telefono e credito prepagato: *Add credit* minimo $5 (~€4,60), meglio con *auto-recharge* a $25 (~€23). Crea la chiave in *API keys*, copiala subito, e imposta un *Monthly budget* ($30, ~€28) in *Usage → Limits*.

**Google (Gemini 2.5 Ultra).** Il più rapido: login su `aistudio.google.com`, *Get API key*, *Create API key*, copia e salva. Un dettaglio da non saltare: dal 19 giugno 2026 Google blocca le key *unrestricted* — fai *Edit* sulla key e abilita *Restrict to Gemini API*, o smetterà di funzionare. Free tier generoso ma con limiti rigidi sulle richieste al minuto.

**(i) Pro tip:** crea key *separate* per ogni installazione, non riusare la stessa fra Mac Mini, VPS e laptop. Quando una è compromessa, ruoti solo quella.

**Schermata 5 — Gateway.** Il wizard configura il **WebSocket control plane** — il cuore di OpenClaw. I default vanno lasciati come sono nel 99% dei casi.

| Parametro | Default | Nota |
|---|---|---|
| Bind address | `127.0.0.1` | Loopback only — nessuno dalla LAN |
| Porta | `18789` | Cambia solo se è già occupata |
| Auth mode | `token` | Token auto-generato salvato sotto `~/.openclaw/auth.token` |
| Tool policy | `strict` | Approvazione esplicita per azioni distruttive |
| Tailscale exposure | `disabled` | Abilitalo solo se sai cosa stai facendo |

Cambia il bind address in `0.0.0.0` *solo* se stai installando su un VPS con un firewall davanti, e anche allora: meglio Tailscale (vedi Cap. 19). Se cambi la porta, dovrai aprire la nuova nel firewall locale.

**Schermata 6 — Canale.** Il primo canale di messaggistica. Telegram è il default per ottime ragioni: setup di tre minuti, gruppi, mention gating nativo. Sceglilo anche se hai un caso d'uso enterprise: Slack o Teams si aggiungono dopo (le alternative sono nel [Capitolo 6](./06-configurare-telegram-e-altri-canali.md)). Oppure "Skip": potrai sempre lanciare `openclaw channels login --channel telegram` più tardi.

**Schermata 7 — Ricerca web.** Quattro opzioni, una precaricata.

- **Brave Search API** (precaricata). Da febbraio 2026 il free tier è $5 (~€4,60) di crediti gratuiti mensili — circa 1.000 query — poi a consumo. Per un agente personale bastano: sceglila per partire, nessuna chiave da inserire.
- **Exa.** Ricerca semantica, free tier generoso.
- **Perplexity API.** Risultati già "ragionati", più lenti e costosi.
- **Firecrawl.** Non è un motore di ricerca: è uno scraper, complemento e non sostituto.

Puoi anche saltare e installare dopo (`openclaw skills install brave-search`); lasciare Brave attiva è quasi sempre la mossa giusta.

**Schermata 8 — Skill iniziali e hook.** Il wizard propone skill consigliate: tienile *quasi tutte*. Le due indispensabili:

- **`gog`** — Gmail, Calendar, Drive in un solo bundle: trasforma OpenClaw da "chat con superpoteri" ad "assistente che sa cosa hai in calendario". L'OAuth con Google parte al primo accesso alla casella.
- **`summarize`** — riassunto di documenti, email, pagine web. Sembra banale, lo userai venti volte al giorno.

Il wizard offre anche di abilitare quattro **hook** di sistema:

| Hook | Cosa fa | Consiglio |
|---|---|---|
| `session-memory` | Salva il contesto a `/new` o `/reset` | **Sempre on** |
| `debug` | Tracce dettagliate quando un tool fallisce | On all'inizio |
| `cost-tracker` | Aggrega spesa per modello, sessione, agente | **Sempre on** |
| `context-optimizer` | Compatta il contesto vicino al limite | On — risparmia token |

`session-memory` fa la differenza fra "agente che dimentica tutto" e "agente che si ricorda chi sei": va sempre abilitato. Salva i ricordi in `~/.openclaw/workspace/memory/YYYY-MM-DD.md` — una nota per giorno, leggibile a occhio nudo.

### Cosa il wizard ha appena scritto sul tuo disco

Quando il wizard si chiude, il filesystem ha guadagnato un solo albero — `~/.openclaw/` — con due zone a responsabilità chiare. La confusione fra "stato" (la radice) e "workspace" (la sottocartella) è la fonte di errori più frequente delle prime settimane: ecco la mappa.

```text
~/.openclaw/            ← "il motore" (stato)
├─ config.yaml
├─ credentials/   (encrypted)
├─ auth.token
├─ logs/
├─ sessions/
├─ channels/
└─ workspace/           ← "la scrivania"
   ├─ SOUL.md              (dell'agente)
   ├─ AGENTS.md
   ├─ IDENTITY.md
   ├─ USER.md
   ├─ TOOLS.md
   ├─ HEARTBEAT.md
   ├─ MEMORY.md
   ├─ BOOTSTRAP.md   (solo al primo avvio)
   ├─ memory/        (note giornaliere)
   ├─ skills/
   ├─ cron/
   └─ projects/
       └─ ... (your stuff)
```

In alto, **lo stato** — il *motore*. Config, credenziali cifrate, token, log, sessioni. È la parte "infrastrutturale" e contiene segreti: trattala come la cartella `.ssh`, mai in cloud non cifrato, mai in repo pubblici.

Dentro, **il workspace** — la *scrivania*. Sono i file `.md` che l'agente legge e scrive come se fossero documenti suoi. Qui puoi (anzi, *dovresti*) tenere un repo Git privato: ogni modifica all'identità o ai progetti diventa una commit, e in caso di guai torni indietro con `git checkout`. E poiché tutto vive sotto `~/.openclaw/`, **il backup è una cartella sola**.

Gli otto file nella radice del workspace sono i **bootstrap files** — gli unici che OpenClaw carica automaticamente all'avvio di ogni sessione. `BOOTSTRAP.md` è un caso a parte: è il **rito del primo avvio**. Lo crea OpenClaw stesso, guida la conversazione di onboarding, propaga le tue risposte in `IDENTITY.md`, `USER.md` e `SOUL.md`, poi si auto-cancella. Se settimane dopo lo trovi ancora lì, il bootstrap è fallito (ne riparliamo nel Cap. 7). `MEMORY.md` è la sintesi long-term della memoria. Tutti gli altri `.md` che metterai sotto `projects/` saranno disponibili all'agente *su richiesta*, non automaticamente: questo evita di saturare la finestra di contesto.

Cap aggregato: 150.000 caratteri totali fra tutti i bootstrap, 20.000 per singolo file. Sopra quei limiti, OpenClaw tronca silenziosamente. Se vedi comportamenti strani settimane dopo, controlla `/context list` dentro la TUI: ti dice cosa è entrato e cosa è stato troncato.

### Cosa aspettarti di spendere nei primi 7 giorni

La paura di spendere troppo, la prima settimana, è quasi sempre infondata: si spende poco perché si fa fatica a trovare cose utili da chiedere. Tre profili di riferimento su Claude Sonnet 4.6, da sessioni reali della community (marzo–maggio 2026): Esploratore = "voglio capire cos'è" (5–10 sessioni brevi al giorno); Quotidiano = digest, email, calendario (15–30); Intensivo = coding, ricerca e cron (50+).

| Profilo | Costo 7 giorni |
|---|---|
| Esploratore | $0,50–$1,50 |
| Quotidiano | $4–$10 |
| Intensivo | $20–$45 |

> **Nota di cambio** — cambio di riferimento: $1 ≈ €0,92. Il profilo "Quotidiano" spende quindi ~€3,70–9,20 a settimana.

I numeri assumono *cache prompt* abilitato (default in OpenClaw 2026.x). Con GPT-5.1 i costi salgono di circa il 30% sul ragionamento puro; con Gemini 2.5 Ultra scendono di circa il 20% sui task multimodali. La sottoscrizione ChatGPT Pro ($200/mese, ~€185) conviene solo oltre i ~250.000 token al giorno, che è già "intensivo serio".

**(i) Pro tip:** la prima settimana, a fine giornata lancia `openclaw cost report --since today`: il numero ti rassicura — o ti avvisa, se un cron impazzito brucia token nella notte. Tabella completa e strategie nel [Capitolo 14](../PARTE-V-Sicurezza-costi/14-gestire-i-costi-senza-sorprese.md).

### Daemon o foreground — capire la differenza

Se hai usato `--install-daemon`, il Gateway è già un servizio:

```bash
openclaw gateway status   # is it running?
openclaw gateway stop     # stop the service
openclaw gateway restart  # apply config changes
```

Per i log in tempo reale: `openclaw logs --follow`. Se invece hai installato senza `--install-daemon`, il Gateway gira solo finché tieni aperto il terminale; `openclaw gateway --install-daemon` lo promuove a servizio dopo il fatto (LaunchAgent su macOS, user unit systemd su Linux, Service Control Manager su Windows).

**(i) Pro tip:** promuovi a daemon solo dopo aver verificato la configurazione in foreground: un servizio mal configurato che parte al boot si scopre tre giorni dopo.

### Il primo "hatch" — la nascita dell'agente

Finito il wizard, lancia:

```bash
openclaw
```

Si apre la **TUI** — Terminal User Interface — con l'iconico lobster ASCII art e un prompt di chat. Il "primo hatch" è la nascita dell'agente: legge i bootstrap files vuoti, capisce che non ha identità e ti chiede di presentarti. Questa conversazione *configura tutto il resto*: da quanto gli dici nascono `IDENTITY.md` e (su tua richiesta) `SOUL.md`. Niente di irreversibile, ma una buona presentazione risparmia un'ora di tweaking dopo.

In parallelo, `openclaw dashboard` apre `http://127.0.0.1:18789` con la **Control UI**: chat, log live, stato del Gateway, costi accumulati, skill, canali, audit log. È più comoda della TUI per l'uso quotidiano; la TUI resta il modo più rapido per il debug in tempo reale.

### Verifica finale — i comandi essenziali e `verify-install.sh`

Ogni volta che qualcosa "non sembra giusto", riparti da questi comandi. Coprono il 90% dei casi.

```bash
# 1. is the CLI installed?
openclaw --version

# 2. is the gateway running?
openclaw gateway status

# 3. config sanity check (+ --fix for safe repairs)
openclaw doctor

# 4. is the dashboard reachable?
curl -fsS --max-time 3 \
  http://127.0.0.1:18789/health

# 5. follow logs in real time
openclaw logs --follow
```

`openclaw doctor` esegue una dozzina di check (Node, Gateway, token di auth, workspace, config YAML, bootstrap files, provider, scadenze OAuth). Lancialo dopo *ogni* `openclaw update`: molte release cambiano lo schema del `config.yaml`. La variante `--fix` applica le migrazioni automatiche e ripara i warning sicuri; non tocca nulla che richieda intervento umano (nuove API key, riautenticazione OAuth).

Uno script che li orchestra e dà un *verdetto unico* — `verify-install.sh` — è più pratico per passare l'installazione a qualcun altro o rivalidare dopo ogni update. Non scriverlo a mano: fallo generare all'agente, poi salvalo (`chmod +x`) nei dotfiles versionati.

**Prompt pronto — fai generare lo script all'agente stesso:**

> "Genera uno script bash chiamato `verify-install.sh` che esegua sette controlli sull'installazione OpenClaw: (1) `openclaw` nel PATH, (2) versione Node confrontata con il minimo 22.16 (fallisci se inferiore), (3) gateway running, (4) dashboard raggiungibile su `127.0.0.1:18789`, (5) `openclaw doctor` senza errori (warning ammessi), (6) almeno un canale collegato (warning se zero), (7) presenza non vuota di `IDENTITY.md` e `SOUL.md` in `~/.openclaw/workspace/`. Output a colori, exit 0 se tutto verde, 1 al primo rosso."

**(i) Pro tip:** mettilo in cron settimanale insieme al rebuild del sandbox (Cap. 4): ricevi una notifica solo quando qualcosa torna *rosso*.

### Update, backup e disinstallazione

OpenClaw rilascia una minor ogni 2–3 settimane e una major ogni 2–3 mesi. Tre operazioni ricorrenti, ognuna con la sua piccola disciplina.

**Aggiornare in sicurezza.** Il comando è semplice; il problema è che le major possono cambiare lo schema del `config.yaml`.

```bash
# 1. snapshot before updating
openclaw backup create \
  --output ~/Backups \
  --include-workspace

# 2. update
openclaw update

# 3. validate the new state
openclaw doctor --fix
bash ~/dotfiles/verify-install.sh
```

Il flag `--include-workspace` aggiunge all'archivio anche la "scrivania" (di default c'è solo lo stato del motore). Il `doctor --fix` cattura gli `schema mismatch`; lo script segnala rotture non ovvie. Prima di un major leggi *sempre* il changelog: contano solo i tag `[breaking]` e `[security]`.

**Backup periodico.** Lo stesso `backup create` con `--rotate 8` produce archivi `.tar.gz` settimanali tenendo gli ultimi otto: dentro ci sono `config.yaml`, `credentials/` cifrate, `auth.token`, `sessions/`, `channels/` e — con `--include-workspace` — anche `workspace/`. Per il restore: `openclaw backup restore <archivio>`.

**(i) Pro tip:** schedula il backup in un cron settimanale (es. domenica alle 03:00). Non aspettare il guasto per scoprire che non hai un punto di ripristino.

**Disinstallare per ricominciare da capo.** A volte è la mossa più rapida. Tre passi, in ordine:

```bash
# 1. stop the daemon and remove the service
openclaw gateway uninstall

# 2. keep a copy of the workspace (optional)
cp -r ~/.openclaw/workspace \
  ~/openclaw-archive-$(date +%F)

# 3. remove state, config AND workspace
#    (DANGER: secrets + agent files)
rm -rf "${OPENCLAW_STATE_DIR:-$HOME/.openclaw}"
```

**(!) Attenzione:** il passo 3 cancella le API key cifrate: usa l'occasione per *ruotarle* sui pannelli dei provider. E poiché il workspace vive *dentro* `~/.openclaw/`, lo stesso comando distrugge anche `IDENTITY.md`, `SOUL.md`, memorie e progetti: non saltare il passo 2 se vuoi tenerne una copia.

Se `gateway uninstall` non ha rimosso il servizio, togli a mano il LaunchAgent (macOS) o la user unit systemd (Linux). Poi puoi rilanciare l'installer pulito, riprendendo dalla sezione "TL;DR".

Quando qualcosa si rompe, l'ordine di diagnosi è sempre lo stesso: `openclaw --version` (problema di PATH?), `openclaw gateway status` (fermo? porta occupata?), `openclaw doctor` (Node, config, auth), `openclaw logs --follow`. Se sei ancora perso, incolla il `config.yaml` a un coding agent: funziona sorprendentemente bene per trovare typo, indentazioni sbagliate e chiavi obsolete.

## Prompt pronti all'uso

I tre prompt che usi nei primi cinque minuti di vita dell'agente. Copia, incolla, adatta al tuo nome.

**Prompt 1 — La presentazione iniziale (scrive `IDENTITY.md`):**

> "Ciao! Sono [tuo nome]. Lavoro come [ruolo, breve] e le mie sfide quotidiane sono: [tre o quattro bullet]. Voglio che tu sia il mio assistente personale. Il tuo nome è [nome agente — es. Polly, Max, Sage]. Sei [tre aggettivi: es. preciso, asciutto, ironico]. Scrivi tu il tuo `IDENTITY.md` partendo da queste informazioni. Mostrami il contenuto prima di salvarlo."

**Prompt 2 — Definire personalità e confini (`SOUL.md`):**

> "Adesso scrivi il tuo `SOUL.md`. Deve contenere: (1) tono di voce; (2) cosa fai sempre; (3) cosa non fai mai — confini etici e operativi; (4) come gestisci l'incertezza — quando chiedi conferma e quando agisci da solo. Massimo 600 parole. Mostrami la bozza prima di salvarla."

**Prompt 3 — Test di salute end-to-end:**

> "Esegui un self-test: (a) leggi `IDENTITY.md` e dimmi chi sei in due frasi; (b) controlla che `gog` sia configurato e dimmi quanti messaggi non letti ho; (c) verifica il canale Telegram e mandami un messaggio di prova; (d) cerca sul web 'OpenClaw release notes' e riassumi in tre righe; (e) dimmi quanti token hai consumato in questa conversazione. Output in lista."

**(#) Debug:** se il prompt 3 fallisce su un punto qualunque, *non* andare avanti: una pila di configurazioni sopra una base rotta produce solo confusione.

## Errori comuni e come risolverli

**Sintomo:** lo script `curl … install.sh` fallisce.
Causa: proxy aziendale o certificate pinning.
Fix: scarica con `curl -O`, ispeziona, lancia
`bash install.sh`.

**Sintomo:** `openclaw: command not found` dopo
`npm install -g`.
Causa: `npm` global bin non in `PATH`.
Fix: aggiungi
`export PATH="$(npm prefix -g)/bin:$PATH"` a `~/.zshrc`,
riapri il terminale.

**Sintomo:** `Node version too old`.
Causa: Node < 22.16.
Fix: installa Node 24 (raccomandato) o 22.16+ via
`nvm install 22.16 && nvm use 22.16`.

**Sintomo:** `Anthropic API key invalid` o
`subscription not allowed`.
Causa: Claude Pro/Max bloccata dal 4 aprile 2026.
Fix: genera una API key da `console.anthropic.com`. Vedi
Cap. 14.

**Sintomo:** `openclaw gateway status` dice "stopped".
Causa: Gateway non avviato come daemon.
Fix: `openclaw gateway --install-daemon` oppure
`openclaw gateway start`.

**Sintomo:** porta `18789` già in uso.
Causa: altro processo la sta tenendo.
Fix: `lsof -i :18789`; cambia porta in
`~/.openclaw/config.yaml`.

**Sintomo:** `openclaw doctor` segnala "schema mismatch".
Causa: `config.yaml` di una versione precedente.
Fix: `openclaw doctor --fix`; se fallisce, rinomina la
config e rifai il wizard.

**Sintomo:** OAuth Google fallisce sul setup `gog`.
Causa: browser non aperto, redirect URI bloccato.
Fix: `openclaw skills configure gog` con Chrome come
browser di default.

**Sintomo:** spese salite all'improvviso.
Causa: `cost-tracker` spento, agente in loop.
Fix: `openclaw cost report --since 24h`; ferma il cron
con `openclaw cron list && openclaw cron disable <id>`.

## Checklist di fine capitolo

- [ ] Account utente dedicato creato (Gmail dedicata solo se userai `gog`)
- [ ] Node.js 22.16+ (idealmente 24) verificato con `node --version`
- [ ] OpenClaw installato senza errori (`openclaw --version` risponde)
- [ ] API key generata con spend limit mensile (NON sottoscrizione Claude)
- [ ] Wizard completato, daemon installato (`openclaw gateway status` = running)
- [ ] Almeno un canale collegato (`openclaw channels status` lo conferma)
- [ ] Skill `gog` e `summarize` installate; Brave Search attivo
- [ ] Hook `session-memory` e `cost-tracker` attivi
- [ ] Primo "hatch" completato; dashboard su `http://127.0.0.1:18789`
- [ ] `openclaw doctor` esce senza warning
- [ ] `verify-install.sh` generato dall'agente, prima esecuzione "All green"
- [ ] `IDENTITY.md` e `SOUL.md` scritti (Prompt 1 e 2); self-test (Prompt 3) superato
- [ ] Backup settimanale in cron; tutti i segreti nel password manager

## Link e risorse utili

- [Onboarding overview — docs.openclaw.ai](https://docs.openclaw.ai/start/onboarding-overview) — cosa fa il wizard
- [Onboarding wizard (CLI) — docs.openclaw.ai](https://docs.openclaw.ai/start/wizard) — flag e schermate
- [Getting started — docs.openclaw.ai](https://docs.openclaw.ai/start/getting-started) — quickstart ufficiale
- [Node.js requirements — docs.openclaw.ai](https://docs.openclaw.ai/install/node) — versioni supportate
- [Hooks — docs.openclaw.ai](https://docs.openclaw.ai/cli/hooks) — session-memory, cost-tracker e altri
- [General troubleshooting — docs.openclaw.ai](https://docs.openclaw.ai/help/troubleshooting) — errori comuni
- [How to install OpenClaw without getting banned](https://www.shareuhack.com/en/posts/openclaw-setup-tutorial-2026) — tutorial post-ban Anthropic
- [Anthropic provider docs (OpenClaw)](https://docs.openclaw.ai/providers/anthropic) — la chiave API Anthropic dopo il 4 aprile 2026
- [OpenClaw Memory Files: AGENTS.md, IDENTITY.md, SOUL.md & More](https://openclaw-setup.me/blog/openclaw-internals/openclaw-memory-files/) — anatomia dei bootstrap files
- [openclaw on npm](https://www.npmjs.com/package/openclaw) — pacchetto ufficiale, changelog
- [Uninstall — docs.openclaw.ai](https://docs.openclaw.ai/install/uninstall) — rimozione ufficiale
- [OpenClaw Backup Guide — LumaDock](https://lumadock.com/tutorials/openclaw-backup-export-settings-memory) — backup di stato, config, memoria
- [Anthropic API keys — console.anthropic.com](https://console.anthropic.com/settings/keys) — chiave Claude
- [OpenAI API keys — platform.openai.com](https://platform.openai.com/api-keys) — chiave OpenAI
- [Google AI Studio API key — aistudio.google.com](https://aistudio.google.com/app/apikey) — chiave Gemini
- [Using Gemini API keys — ai.google.dev](https://ai.google.dev/gemini-api/docs/api-key) — restrizioni dal 19 giugno 2026

Per l'elenco completo delle fonti del libro, vedi [Appendice E](../Appendici/E-risorse-e-link-utili.md).

---

[← Capitolo 4](./04-preparare-un-ambiente-sicuro-docker-sandbox.md)  ·  [Indice](../README.md)  ·  [Capitolo 6 →](./06-configurare-telegram-e-altri-canali.md)
