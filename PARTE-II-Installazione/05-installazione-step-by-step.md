# Capitolo 5 — Installazione step-by-step [★]

## Cosa imparerai

- Come preparare il computer in dieci minuti, senza dimenticare i quattro dettagli che fanno perdere mezza giornata
- Come scegliere fra `install.sh`, `npm`, sorgente e immagine Docker, e quando ognuna è la scelta giusta
- I dettagli specifici per macOS (Apple Silicon vs Intel), Linux (Ubuntu/Fedora/Arch) e Windows/WSL2
- Come generare passo per passo la API key su Anthropic, OpenAI e Google AI Studio (con i costi minimi di partenza)
- Come navigare il wizard di onboarding schermata per schermata, con il significato reale di ogni opzione
- Cosa succede dietro le quinte quando il wizard scrive `~/.openclaw/config.yaml` e `~/openclaw/workspace/`
- Cosa aspettarti di spendere nei primi sette giorni per profilo d'uso (leggero, moderato, intensivo)
- Come installare il Gateway come **daemon** (`--install-daemon`) e capire la differenza con la modalità foreground
- Come scegliere modello, autenticazione e canale **dopo il ban Anthropic del 4 aprile 2026**
- Come fare il "primo hatch", aprire la dashboard sulla porta `18789` e validare il setup con `openclaw doctor`
- Come usare lo script `verify-install.sh` per validare l'installazione in dieci secondi, ogni volta che serve
- Come aggiornare in sicurezza, fare backup di config e workspace, e disinstallare per ricominciare da capo
- Come scrivere i primi `IDENTITY.md` e `SOUL.md` direttamente dall'agente, in cinque minuti

## Prerequisiti

Aver letto il [Capitolo 3](./03-scegliere-dove-installare-openclaw.md) e scelto **dove** installare OpenClaw — Mac Mini dedicato, VPS, Raspberry Pi o cloud managed. Per un setup difensivo è caldamente consigliato anche il [Capitolo 4](./04-preparare-un-ambiente-sicuro-docker-sandbox.md): se hai pianificato il sandbox, questo capitolo si limita a passarti dentro.

Cosa devi avere a portata di mano prima di iniziare: un account utente dedicato (mai il tuo profilo personale di lavoro), una **Gmail dedicata** all'agente, **Chrome** installato (è il browser che OpenClaw guida meglio), e dieci minuti di attenzione senza interruzioni. Il wizard è lineare ma fa quattro o cinque scelte importanti: sbagliarne una significa rifarlo da capo o, peggio, accorgersene una settimana dopo.

Verifica veloce dei prerequisiti, da incollare nel terminale prima dell'installazione:

```bash
node --version    # >= 22.16 (24 raccomandato)
git --version     # qualsiasi versione recente
curl --version    # qualsiasi versione recente
echo $SHELL       # /bin/zsh o /bin/bash
```

Se `node` manca o è troppo vecchio, lo script di installazione lo aggiunge per te tramite `nvm` o pacchetto di sistema, ma è più rapido (e più pulito) installarlo a mano prima.

## Contenuto principale

### TL;DR — installazione in dieci minuti

Se hai già un account dedicato, una Gmail e dieci minuti, questi sono i comandi essenziali. Il resto del capitolo spiega *perché* ognuno di essi esiste e cosa fa davvero.

```bash
# 1. install OpenClaw (auto-detect OS)
curl -fsSL https://openclaw.ai/install.sh | bash

# 2. run the guided onboarding
openclaw onboard --install-daemon

# 3. verify everything is healthy
openclaw doctor
openclaw gateway status

# 4. open the local dashboard
openclaw dashboard
```

Quattro comandi. Quando l'ultimo apre il browser su `http://127.0.0.1:18789` e vedi la chat funzionante, l'installazione è andata a buon fine. Da qui in poi è solo configurazione.

### Pre-work — i dieci minuti che ti risparmiano due ore

Prima di lanciare qualunque cosa, prepara il terreno. Quattro mosse, in quest'ordine.

**Account dedicato.** Crea un nuovo utente sul sistema — `openclaw`, `claw`, `agente`, scegli tu — e installa OpenClaw lì dentro. Su macOS: *Impostazioni di Sistema → Utenti e Gruppi → Aggiungi Account*. Su Linux: `sudo adduser openclaw`. Su Windows: *Impostazioni → Account → Famiglia e altri utenti*. Mai installare l'agente sul tuo profilo personale: il giorno in cui sbaglierà un comando — e accadrà — vorrai un perimetro fisico che separi il suo errore dai tuoi file.

**Gmail dedicata.** Registra un nuovo indirizzo Gmail per l'agente, *non* il tuo. È l'identità con cui invierà email, autenticherà i servizi, riceverà notifiche di fatturazione. Tenerla separata significa due cose: nessuna confusione fra "l'ho mandata io" e "l'ha mandata lui", e revoca a singolo click quando vorrai disattivarlo.

**Chrome installato.** OpenClaw guida tutti i browser, ma Chrome è quello con il binding più maturo (cookie store, DevTools protocol, profili separati). Su Mac Mini dedicato è anche l'unico browser di cui avrai bisogno: lascia Safari per le tue cose personali sul laptop.

**Password manager pronto.** Apri 1Password, Bitwarden, KeePassXC — quello che usi — e crea una nuova *vault* o cartella chiamata `OpenClaw`. Nei prossimi venti minuti ci salverai: API key del modello, token Telegram, token GitHub, password Gmail, eventuali setup token. **Nulla di tutto questo deve mai finire in chiaro in un file `.env` versionato.**

**(!) Attenzione:** non saltare il passo dell'account dedicato perché "tanto è la mia macchina". OpenClaw scrive in `~/.openclaw`, esegue cron, può lanciare comandi shell. Mescolarlo con il tuo profilo significa che, fra un anno, non saprai più quali file `~/Documents` sono tuoi e quali sono cose che l'agente ha scaricato per qualche task dimenticato.

### Quattro modi di installare — qual è il tuo

L'install ufficiale è uno script `bash` che fa il 95% del lavoro. Ma esistono altre tre strade, e ognuna ha un caso d'uso preciso.

**Modo 1 — `install.sh` (consigliato a tutti).** Lo script ufficiale rileva sistema operativo e architettura, installa Node se manca, scarica l'eseguibile e avvia il wizard. È l'opzione predefinita per macOS, Linux e (via WSL2) Windows.

```bash
curl -fsSL https://openclaw.ai/install.sh | bash
```

Su Windows in PowerShell la versione equivalente è:

```powershell
iwr -useb https://openclaw.ai/install.ps1 | iex
```

**(i) Pro tip:** prima di pipare uno script in `bash` o `iex`, leggilo. Sono ~200 righe e si capiscono. Salvalo con `curl -O https://openclaw.ai/install.sh`, scorrilo, poi lancia `bash install.sh`. È un'abitudine che vale per qualunque installer, non solo per OpenClaw.

**Modo 2 — `npm` globale.** Se vuoi evitare lo script bash o sei dietro una rete che blocca i `curl | bash`:

```bash
npm install -g openclaw
openclaw onboard --install-daemon
```

Funziona identico, ma richiede che tu abbia già Node 22.16+ installato e che `npm`'s global bin sia nel `PATH` (vedi la sezione "Errori comuni" se l'eseguibile `openclaw` non viene trovato).

**Modo 3 — Sorgente (per chi contribuisce o vuole leggersi il codice).** Clona il repo, builda, linka il binario:

```bash
git clone https://github.com/openclaw/openclaw.git
cd openclaw
npm install && npm run build
npm link
```

Utile in due casi: se vuoi vedere il diff fra una release e la `main`, e se hai bisogno di patchare al volo qualcosa per uso interno.

**Modo 4 — Docker / Compose (per ambienti isolati).** Se hai seguito il Capitolo 4 e hai scelto il Livello 2 (Gateway containerizzato), salti tutto questo capitolo e lanci:

```bash
git clone https://github.com/openclaw/openclaw.git
cd openclaw
./scripts/docker/setup.sh
```

Il setup script monta `~/.openclaw` (config) e `~/openclaw/workspace` (file dell'agente) come volumi, espone la porta `18789`, e parte. L'onboarding viene mostrato la prima volta che ti colleghi alla dashboard.

### Dettagli per sistema operativo

L'installer si comporta in modo simile su tutte le piattaforme, ma ognuna ha tre o quattro dettagli che, se li ignori, ti fanno perdere un'oretta. Vai diretto al paragrafo del tuo OS.

**macOS — Apple Silicon (M1/M2/M3/M4).** Lo script funziona out-of-the-box su Apple Silicon: i binari vengono distribuiti come *fat binary* arm64 + x86_64. Tre cose da sapere:

- Se hai **Homebrew**, installa Node prima dell'installer: `brew install node@22`. Lo script userà quello senza scaricare nulla.
- L'installer crea un'entry in `~/Library/LaunchAgents/ai.openclaw.gateway.plist`. La gestisci con `launchctl list | grep openclaw`.
- Su M1/M2 di prima generazione (Ventura 13.4 e precedenti) può servire abilitare *Rosetta 2* per alcune skill che dipendono ancora da binari Intel: `softwareupdate --install-rosetta --agree-to-license`.

**macOS — Intel (Mac Mini 2018, MacBook Pro 2019).** Funziona ma è in fase di "best effort": Apple ha deprecato il supporto a partire da macOS 16. Se sei ancora su un Intel, fissa Node a 22.16 (non 24): qualche package nativo non è ancora aggiornato per Node 24 su Intel-Mac.

**Linux — Ubuntu/Debian.** L'installer cerca `apt`, installa `curl`, `git`, e Node via NodeSource se manca:

```bash
# pre-install Node from NodeSource
curl -fsSL https://deb.nodesource.com/setup_22.x \
  | sudo -E bash -
sudo apt-get install -y nodejs

# now run the OpenClaw installer
curl -fsSL https://openclaw.ai/install.sh | bash
```

Il daemon viene installato come *user systemd unit* in `~/.config/systemd/user/openclaw-gateway.service`. Dopo `systemctl --user enable --now openclaw-gateway` aggiungi `loginctl enable-linger <utente>` se vuoi che parta anche senza login attivo (utile sui server headless).

**Linux — Fedora / RHEL / CentOS Stream.** Sostituisci `apt` con `dnf`:

```bash
curl -fsSL https://rpm.nodesource.com/setup_22.x \
  | sudo bash -
sudo dnf install -y nodejs
curl -fsSL https://openclaw.ai/install.sh | bash
```

Su Fedora 40+ il SELinux è in *enforcing* di default: se `openclaw doctor` lamenta `permission denied` su socket o porte, controlla i log con `sudo ausearch -m avc -ts recent` e, se necessario, applica un `setsebool -P openclaw_can_network 1`.

**Linux — Arch / Manjaro.** Più rapido di tutti:

```bash
sudo pacman -S nodejs npm
curl -fsSL https://openclaw.ai/install.sh | bash
```

Esiste anche un pacchetto AUR non ufficiale (`openclaw-bin`): comodo, ma controlla che il maintainer sia attivo e la versione recente prima di affidarti.

**Windows — WSL2 (consigliato).** Installa Ubuntu 22.04 o 24.04 dal Microsoft Store, aggiorna, e dentro WSL lancia l'installer Linux:

```powershell
# in PowerShell, install WSL2
wsl --install -d Ubuntu-22.04
```

```bash
# inside the WSL2 Ubuntu shell
sudo apt update && sudo apt upgrade -y
curl -fsSL https://openclaw.ai/install.sh | bash
```

Tre cose specifiche di WSL: il filesystem dell'agente vive in `~/.openclaw` *dentro* WSL, non in `C:\Users\<tu>\.openclaw` (Windows). La dashboard è raggiungibile da Windows browser su `http://localhost:18789` grazie al port forwarding automatico di WSL2. Per far partire il Gateway al boot di Windows, aggiungi un task scheduler che lanci `wsl -d Ubuntu-22.04 -e openclaw gateway start` allo *startup*.

**Windows — PowerShell nativo (sconsigliato per uso quotidiano).** Funziona, ma molte skill assumono ambiente POSIX e si comportano in modo incoerente. Lo script PowerShell esiste:

```powershell
iwr -useb https://openclaw.ai/install.ps1 | iex
```

Usalo solo se hai un vincolo di policy aziendale che non permette WSL2.

**(i) Pro tip:** indipendentemente dall'OS, dopo l'installazione lancia `openclaw doctor`. È l'unica certezza che il setup specifico per il tuo sistema sia andato bene. I "non funziona ma non so perché" che vedo più spesso sono Linux con Node troppo vecchio, Windows senza WSL2, e macOS Intel con Node 24.

### Il wizard di onboarding, schermata per schermata

Subito dopo l'install, lo script chiama automaticamente `openclaw onboard --install-daemon`. Il flag `--install-daemon` registra il Gateway come servizio di sistema (launchd su macOS, systemd su Linux, Service Control Manager su Windows): partirà al boot e sopravviverà alla chiusura del terminale. Senza di esso, il Gateway gira solo finché tieni aperta la finestra — utile per testare, doloroso per usare davvero.

Il wizard mostra otto schermate. Le passiamo una a una.

**Schermata 1 — Avviso di sicurezza.** Una pagina di testo con un riassunto onesto di cosa OpenClaw può fare al tuo computer: leggere file, eseguire comandi, navigare la rete, mandare messaggi. Non è teatro: leggila davvero. Il pulsante "accetto" abilita l'installazione del daemon.

**Schermata 2 — Workspace.** Dove l'agente scriverà i suoi file. Il default `~/openclaw/workspace` va bene per il 95% dei casi. Se hai un disco esterno dedicato o un volume cifrato, puntalo lì. Quello che metterai in questa cartella sarà *direttamente accessibile* dall'agente: niente segreti, niente roba personale.

**Schermata 3 — Modello LLM.** Il cuore della scelta. A maggio 2026 le opzioni mainstream sono tre.

| Modello | Provider | Quando sceglierlo |
|---|---|---|
| Claude Opus 4.6 | Anthropic | Default per agente generale |
| Codex 5.4 | OpenAI | Forte su codice e tool use |
| Gemini 2.5 Ultra | Google | Multimodale, finestra molto lunga |

La scelta non è irreversibile: puoi cambiarla con `openclaw config set model <slug>` in qualunque momento. Ma cambiarla *spesso* costa, perché ogni modello ha i suoi token quirks e l'agente impara a "parlare" col modello iniziale. Scegli quello con cui pensi di restare almeno tre mesi.

**(i) Pro tip:** se vuoi giocare in modalità "modello leggero per task semplici, modello forte per quelli difficili", scegli ora Claude Opus 4.6 come default e configura un *router* in fase due (vedi Cap. 14, sezione "Strategie di ottimizzazione costi"). Cominciare con un solo modello tiene il setup pulito.

**Schermata 4 — Autenticazione.** Qui c'è il bivio post-ban. Tre opzioni teoriche, una sola realmente sostenibile.

- **API key (consigliata, unica opzione affidabile).** Vai su `console.anthropic.com`, `platform.openai.com` o `aistudio.google.com` e genera una chiave. Pay-as-you-go: paghi i token che consumi. Incolla la key quando il wizard te la chiede; viene salvata cifrata in `~/.openclaw/credentials/`. Nessun rischio di ToS violation.
- **Sottoscrizione ChatGPT Plus / Pro.** OpenAI ha esplicitamente "benedetto" l'uso di Codex 5.4 via account ChatGPT Pro ($200/mese) per agenti come OpenClaw. Conviene se prevedi un volume di token equivalente a $200+ al mese: sotto, l'API key paga di meno.
- **~~Sottoscrizione Claude Pro/Max~~ — bloccata.** Dal **4 aprile 2026** Anthropic ha sospeso l'uso di Claude Pro e Max con tool di terze parti, OpenClaw incluso. Chi tenta vedrà un errore `Anthropic API key invalid` o `Unauthorized: subscription not allowed for third-party agents`. Unica via legittima oggi: API key o, in alternativa, "extra usage" pay-as-you-go aggiunto sopra alla sottoscrizione (vedi Cap. 14 per i conti esatti).

**(!) Attenzione:** non lasciare la API key in chiaro in `~/.bashrc` o in un file `.env` versionato. Il wizard la cifra automaticamente sotto `~/.openclaw/credentials/`; non spostarla. Se devi condividere l'installazione fra più macchine, ruota le chiavi su ognuna e usa il *credential proxy* del Capitolo 4.

#### Generare la API key — passo per passo per provider

Il wizard si aspetta che tu abbia già la chiave in tasca. I tre provider mainstream hanno flussi simili ma non identici. Conta cinque minuti per ognuno.

**Anthropic (Claude Opus 4.6).** È il provider che il libro usa come default.

1. Vai su `console.anthropic.com` e fai *Sign up* o *Continue with Google*. Verifica l'email.
2. Apri *Settings → Billing* (sidebar sinistra) e aggiungi un metodo di pagamento. **Senza billing non puoi generare key.** Il minimo di ricarica è $5; per partire è sufficiente.
3. Vai su *Settings → API keys* (oppure direttamente `console.anthropic.com/settings/keys`).
4. Click *Create Key*, dai un nome riconoscibile (es. `openclaw-mac-mini`), conferma.
5. **Copia la key adesso.** Anthropic la mostra una sola volta. Salvala nel password manager con tag `anthropic-api`.
6. Imposta un *spend limit* mensile in *Settings → Limits*. Per partire, $20 al mese ti tengono al sicuro mentre prendi le misure.

**(!) Attenzione:** la sottoscrizione *Claude Pro/Max* (`claude.ai`) è una cosa diversa dall'API key (`console.anthropic.com`). La prima è bloccata da OpenClaw dal 4 aprile 2026, la seconda no. Se non vedi la voce *API keys* in sidebar, sei sul sito sbagliato: vai su `console.anthropic.com`, non su `claude.ai`.

**OpenAI (Codex 5.4, GPT-5).** Il flusso è simile ma con due passaggi extra (verifica telefono, ricarica prepagata).

1. Vai su `platform.openai.com`, fai *Sign in with Google* o crea l'account. Verifica email **e numero di telefono** (OpenAI lo richiede).
2. Apri *Settings → Organization → Billing* (`platform.openai.com/settings/organization/billing/overview`) e *Add credit*. Minimo $5. Suggerito: abilita *auto-recharge* a $25 quando il credito scende sotto $5, così non ti ferma a metà task.
3. Apri *API keys* (`platform.openai.com/api-keys`).
4. *Create new secret key*, nome descrittivo (`openclaw-prod`), permessi *All*, *Create*.
5. **Copia la key subito.** Stesso vincolo di Anthropic: viene mostrata una volta sola.
6. Vai su *Usage → Limits* e imposta un *Monthly budget*. $30/mese è un buon punto di partenza.

**Google (Gemini 2.5 Ultra).** Il più rapido dei tre, ma con un dettaglio di sicurezza da non saltare.

1. Vai su `aistudio.google.com`, login con account Google.
2. Click *Get API key* in sidebar (o `aistudio.google.com/app/apikey`).
3. *Create API key*, nome descrittivo (`openclaw-personal`), conferma.
4. Copia la key e salvala. Google la mostra anche dopo, ma non contarci.
5. **Importante (cambio del 2026):** dal 19 giugno 2026 Google blocca le key *unrestricted*. Vai sulla key appena creata, click *Edit*, abilita *Restrict to Gemini API*. Senza questa restrizione la key smetterà di funzionare nelle prossime release.
6. Imposta un *Monthly budget* in Google Cloud Console se prevedi uso intensivo; il piano free è generoso ma ha limiti rigidi sulle richieste/minuto.

**Tabella riassuntiva dei costi minimi per partire:**

| Provider | Min. ricarica | Setup tempo | Note |
|---|---|---|---|
| Anthropic | $5 | ~5 min | Spend limit consigliato $20/mese |
| OpenAI | $5 | ~7 min | Auto-recharge $25, limite $30 |
| Google | gratis | ~3 min | Free tier ampio; restrict obbligatorio dal 19 giu 2026 |

**(i) Pro tip:** crea key *separate* per ogni installazione, non riusare la stessa fra Mac Mini, VPS e laptop. Quando una compromessa, ruoti solo quella.

**Schermata 5 — Gateway.** Qui il wizard configura il **WebSocket control plane** — il cuore di OpenClaw. I default sono ragionevoli per uso locale e li lasci come sono nel 99% dei casi.

| Parametro | Default | Nota |
|---|---|---|
| Bind address | `127.0.0.1` | Loopback only — nessuno dalla LAN |
| Porta | `18789` | Cambia solo se è già occupata |
| Auth mode | `token` | Token auto-generato salvato sotto `~/.openclaw/auth.token` |
| Tool policy | `strict` | Approvazione esplicita per azioni distruttive |
| Tailscale exposure | `disabled` | Abilitalo solo se sai cosa stai facendo |

Cambia il bind address in `0.0.0.0` *solo* se stai installando su un VPS con un firewall davanti, e anche allora: meglio Tailscale (vedi Cap. 19). Se cambi la porta, ricordati che dovrai aprire la nuova nella tua firewall locale.

**Schermata 6 — Canale.** Il wizard ti chiede di scegliere il primo canale di messaggistica. Telegram è il default e per ottime ragioni: setup di tre minuti, gruppi, mention gating nativo, app eccellente su tutte le piattaforme. Le altre opzioni (WhatsApp, Slack, Discord, Signal, iMessage) sono coperte in dettaglio nel [Capitolo 6](./06-configurare-telegram-e-altri-canali.md). Per ora: scegli Telegram, anche se hai un caso d'uso enterprise. Aggiungerai Slack o Teams dopo, in due minuti, quando saprai che il resto funziona.

Se non vuoi configurare alcun canale ora, scegli "Skip" — potrai sempre lanciare `openclaw channels add` più tardi.

**Schermata 7 — Ricerca web.** Quattro opzioni, una precaricata.

- **Brave Search API** (precaricata, gratis fino a 2.000 query/mese). Sceglila per partire. Nessuna chiave da inserire.
- **Exa.** Ricerca semantica eccellente per task di "trova-mi-cose-tipo-questa". Generosa nel free tier.
- **Perplexity API.** Risultati già "ragionati", più lenti, più costosi. Utile per ricerche di sintesi.
- **Firecrawl.** Non è motore di ricerca: è scraper. Utile come complemento, non come sostituto.

Puoi anche saltare e configurarle dopo con `openclaw skills add brave-search` (o equivalente). Lasciare Brave attiva di default è quasi sempre la mossa giusta.

**Schermata 8 — Skill iniziali e hook.** Il wizard propone un set di skill consigliate: tienile *quasi tutte*. Le due indispensabili per partire bene:

- **`gog`** — Gmail, Calendar, Drive in un solo bundle. È quello che trasforma OpenClaw da "chat con superpoteri" a "assistente che sa cosa hai in calendario". L'autenticazione OAuth con Google avviene la prima volta che l'agente prova a leggere la tua casella.
- **`summarize`** — riassunto di documenti, email, pagine web. Sembra banale, lo userai venti volte al giorno.

Il wizard offre anche di abilitare quattro **hook** di sistema:

| Hook | Cosa fa | Consiglio |
|---|---|---|
| `session-memory` | Salva il contesto a `/new` o `/reset` | **Sempre on** |
| `debug` | Cattura tracce dettagliate quando un tool fallisce | On in fase di apprendimento |
| `cost-tracker` | Aggrega spesa per modello, sessione, agente | **Sempre on** |
| `context-optimizer` | Compatta il contesto quando si avvicina al limite | On — risparmia token |

`session-memory` è il singolo hook che fa la differenza fra "agente che dimentica tutto a ogni sessione" e "agente che si ricorda chi sei". Va sempre abilitato. Salva i ricordi in `~/.openclaw/workspace/memory/YYYY-MM-DD-HHMM.md`, leggibili a occhio nudo.

### Cosa il wizard ha appena scritto sul tuo disco

Quando il wizard si chiude, il filesystem ha guadagnato due alberi separati con responsabilità chiare. Visualizziamoli con una mappa, perché la confusione fra "stato" (`.openclaw`) e "workspace" (`openclaw`) è la singola fonte di errori più frequente nelle prime settimane.

```text
            ┌─────────────────────────────┐
            │      Home directory         │
            │      (~/, %USERPROFILE%)    │
            └──────────────┬──────────────┘
                           │
            ┌──────────────┴──────────────┐
            │                             │
   ┌────────▼─────────┐         ┌─────────▼──────────┐
   │   ~/.openclaw    │         │    ~/openclaw      │
   │   "il motore"    │         │   "la scrivania"   │
   │  (state dir)     │         │  (workspace dir)   │
   └────────┬─────────┘         └─────────┬──────────┘
            │                             │
   ├─ config.yaml                ├─ workspace/
   ├─ credentials/  (encrypted)  │   ├─ SOUL.md
   ├─ auth.token                 │   ├─ IDENTITY.md
   ├─ logs/                      │   ├─ AGENTS.md
   ├─ sessions/                  │   ├─ TOOLS.md
   ├─ channels/                  │   ├─ USER.md
   └─ workspace/memory/          │   ├─ HEARTBEAT.md
       (session snapshots)       │   ├─ BOOTSTRAP.md (opt)
                                 │   └─ MEMORY.md (opt)
                                 └─ projects/
                                     └─ ... (your stuff)
```

A sinistra, **lo stato** — il *motore*. Config, credenziali cifrate, token, log, sessioni, snapshot di memoria. È la parte "infrastrutturale" e contiene segreti: trattala come la cartella `.ssh`, mai in cloud non cifrato, mai versionata in repo pubblici.

A destra, **il workspace** — la *scrivania*. Sono i file `.md` che l'agente legge e scrive come se fossero documenti suoi. Qui puoi (anzi, *dovresti*) tenere un repo Git privato: ogni modifica all'identità o ai progetti diventa una commit, e in caso di guai torni indietro con un `git checkout`.

I sette/otto file nella radice del workspace sono i **bootstrap files** — gli unici che OpenClaw carica automaticamente all'avvio di ogni sessione. `BOOTSTRAP.md` (override personalizzato) e `MEMORY.md` (sintesi long-term) sono opzionali ma utili. Tutti gli altri `.md` che metterai sotto `projects/` saranno disponibili all'agente *su richiesta*, non automaticamente: questo evita di saturare la finestra di contesto.

Cap aggregato: 150.000 caratteri totali fra tutti i bootstrap, 20.000 per singolo file. Sopra quei limiti, OpenClaw tronca silenziosamente. Se vedi comportamenti strani settimane dopo, controlla `/context list` dentro la TUI: ti dice cosa è entrato e cosa è stato troncato.

### Cosa aspettarti di spendere nei primi 7 giorni

Quasi tutti, la prima settimana, hanno paura di spendere troppo. La realtà è quasi sempre l'opposto: si spende poco perché si fa fatica a trovare cose utili da chiedere. Tre profili di riferimento, misurati su Claude Opus 4.6 con cache prompt attivo, basati su sessioni reali raccontate dalla community fra marzo e maggio 2026.

| Profilo | Tipico utente | Sessioni/giorno | Token/sessione | Costo 7 giorni |
|---|---|---|---|---|
| Esploratore | "voglio capire cos'è" | 5–10 | ~3k | $0,50–$1,50 |
| Quotidiano | digest, email, calendario | 15–30 | ~8k | $4–$10 |
| Intensivo | coding + ricerca + cron | 50+ | ~20k | $20–$45 |

I numeri assumono *cache prompt* abilitato (default in OpenClaw 2026.x) e modello Opus. Se usi Codex 5.4 i costi salgono di circa il 30% per task di ragionamento puro; se usi Gemini 2.5 Ultra scendono di circa il 20% sui task multimodali. Se invece sei sulla sottoscrizione ChatGPT Pro ($200/mese), il costo è fisso indipendentemente dal volume — conviene quando superi le ~250.000 token al giorno, che è già "intensivo serio".

**(i) Pro tip:** la prima settimana, abilita `cost-tracker` (lo hai fatto nel wizard) e a fine giornata lancia `openclaw cost report --since today`. Il numero ti rassicura — o ti avvisa, se hai un cron impazzito che brucia token nella notte.

Sui costi, il [Capitolo 14](../PARTE-V-Sicurezza-costi/14-gestire-i-costi-senza-sorprese.md) ha la tabella completa per dodici mesi e le strategie di ottimizzazione (router multi-modello, cache aggressive, batching).

### Daemon o foreground — capire la differenza

Se hai usato `--install-daemon`, il Gateway è già un servizio. Lo controlli con tre comandi:

```bash
openclaw gateway status   # is it running?
openclaw gateway stop     # stop the service
openclaw gateway restart  # apply config changes
```

Per leggere i log in tempo reale (utile in fase di troubleshooting):

```bash
openclaw logs --follow
```

Se invece hai installato senza `--install-daemon`, il Gateway gira solo finché tieni aperto il terminale. Per promuoverlo a servizio dopo il fatto:

```bash
openclaw gateway --install-daemon
```

Su macOS questo crea `~/Library/LaunchAgents/ai.openclaw.gateway.plist`; su Linux installa `~/.config/systemd/user/openclaw-gateway.service` e fa un `systemctl --user enable --now`. Su Windows registra un servizio gestito dal Service Control Manager.

**(i) Pro tip:** usa `openclaw gateway --install-daemon` solo dopo aver verificato che la configurazione funzioni in foreground. Avere un servizio di sistema che parte al boot ma è mal configurato significa scoprire l'errore tre giorni dopo, quando ti chiederai perché l'agente non risponde.

### Il primo "hatch" — la nascita dell'agente

Finito il wizard, lancia:

```bash
openclaw
```

Si apre la **TUI** — Terminal User Interface — con l'iconico lobster ASCII art e un prompt di chat. Il "primo hatch" è la prima volta che l'agente "nasce": legge i bootstrap files vuoti, capisce che non ha ancora identità, e ti chiede di presentarti.

Questa prima conversazione è importante perché *configura tutto il resto*. L'agente userà quanto gli dici per scrivere `IDENTITY.md` e (su tua richiesta) `SOUL.md`. Niente di irreversibile: puoi modificarli a mano in qualunque momento. Ma partire da una buona presentazione risparmia un'ora di tweaking dopo.

In parallelo alla TUI, apri la dashboard nel browser:

```bash
openclaw dashboard
```

Si apre `http://127.0.0.1:18789` con la **Control UI**: chat, log live, stato del Gateway, costi accumulati, lista skill, lista canali, audit log. È più comoda della TUI per uso quotidiano; la TUI resta il modo più rapido per debug in tempo reale.

### Verifica finale — cinque comandi che devi conoscere

Ogni volta che qualcosa "non sembra giusto", riparti da questi cinque comandi. Coprono il 90% dei casi.

```bash
# 1. is the CLI installed?
openclaw --version

# 2. is the gateway running?
openclaw gateway status

# 3. config sanity check
openclaw doctor

# 4. apply safe fixes if doctor flagged any
openclaw doctor --fix

# 5. follow logs in real time
openclaw logs --follow
```

`openclaw doctor` esegue una dozzina di check: versione di Node, stato del Gateway, validità del token di auth, scrivibilità del workspace, validità della config YAML, presenza dei bootstrap files, raggiungibilità dei provider configurati, certificati TLS, scadenza dei token OAuth. Run dopo *ogni* `openclaw update`: una percentuale non trascurabile delle release introduce schema changes nel `config.yaml`.

`openclaw doctor --fix` rimuove chiavi di config invalide, applica migrazioni automatiche dello schema e ripara i warning sicuri. Non tocca nulla che richieda intervento umano (nuove API key, riautenticazione OAuth).

### Lo script `verify-install.sh`

I cinque comandi della sezione precedente sono comodi a memoria, ma uno script che li orchestra e ti dà un *verdetto unico* è più pratico per due cose: passare l'installazione a qualcun altro (pair setup, onboarding di un collega) e validare in dieci secondi dopo ogni `openclaw update`. Lo script che segue va salvato come `verify-install.sh`, reso eseguibile (`chmod +x`), e tenuto nella cartella dei dotfiles versionata.

```bash
#!/usr/bin/env bash
# verify-install.sh — fast OpenClaw health check
# Exits 0 if green, 1 at first red.

set -u
RED=$'\e[31m'; GRN=$'\e[32m'
YEL=$'\e[33m'; OFF=$'\e[0m'

ok()  { echo "${GRN}OK${OFF}  $1"; }
bad() { echo "${RED}FAIL${OFF} $1"; exit 1; }
warn(){ echo "${YEL}WARN${OFF} $1"; }

# 1. CLI present and recent
command -v openclaw >/dev/null \
  || bad "openclaw not in PATH"
VER=$(openclaw --version 2>/dev/null \
  | head -1)
ok "CLI installed: $VER"

# 2. Node version >= 22.16
NODE=$(node --version 2>/dev/null \
  | sed 's/v//')
[ -n "$NODE" ] || bad "Node not found"
ok "Node version: v$NODE"

# 3. Gateway running
openclaw gateway status \
  2>/dev/null | grep -qi running \
  || bad "gateway is not running"
ok "Gateway: running"

# 4. Dashboard reachable on 18789
curl -fsS -o /dev/null \
  --max-time 3 \
  http://127.0.0.1:18789/health \
  || bad "dashboard unreachable"
ok "Dashboard: 127.0.0.1:18789 reachable"

# 5. Doctor clean (no errors)
DOC=$(openclaw doctor 2>&1)
echo "$DOC" | grep -qi 'error' \
  && bad "doctor reports errors"
echo "$DOC" | grep -qi 'warn' \
  && warn "doctor has warnings"
ok "Doctor: clean"

# 6. At least one channel connected
CHN=$(openclaw channels status \
  2>/dev/null \
  | grep -c -i connected)
[ "$CHN" -ge 1 ] \
  || warn "no channel connected yet"
[ "$CHN" -ge 1 ] && \
  ok "Channels: $CHN connected"

# 7. Bootstrap files present
WS="$HOME/openclaw/workspace"
for f in IDENTITY.md SOUL.md; do
  [ -s "$WS/$f" ] \
    || warn "$f missing or empty"
done
ok "Bootstrap files: checked"

echo ""
echo "${GRN}All green.${OFF} Setup is healthy."
```

Lanciato dopo l'installazione, il risultato atteso è una pila di `OK` verdi e l'ultima riga "All green". Un `WARN` su canali o bootstrap files non blocca: vuol dire solo che hai ancora due cose da finire (collegare un canale, scrivere `IDENTITY.md`/`SOUL.md` con i prompt della sezione successiva).

**(i) Pro tip:** mettilo in cron settimanale insieme al rebuild del sandbox (Cap. 4): ricevi una notifica solo quando qualcosa torna *rosso*, e dormi tranquillo nel frattempo.

```bash
# Linux — every Monday at 09:00
0 9 * * 1 ~/dotfiles/verify-install.sh \
  || echo "OpenClaw broke" \
     | mail -s "[!] OpenClaw" tu@email
```

**Prompt pronto — fai generare lo script all'agente stesso:**

> "Genera uno script bash chiamato `verify-install.sh` che esegua sette controlli sull'installazione OpenClaw: (1) `openclaw` nel PATH, (2) Node ≥ 22.16, (3) gateway running, (4) dashboard raggiungibile su `127.0.0.1:18789`, (5) `openclaw doctor` senza errori (warning ammessi), (6) almeno un canale collegato (warning se zero), (7) presenza non vuota di `IDENTITY.md` e `SOUL.md` in `~/openclaw/workspace/`. Output a colori, exit 0 se tutto verde, 1 al primo rosso."

### Update, backup e disinstallazione

L'installazione non è un atto unico: OpenClaw rilascia una versione minore ogni 2–3 settimane e una major ogni 2–3 mesi. Tre operazioni che dovrai fare nel tempo, ognuna con la sua piccola disciplina.

**Aggiornare in sicurezza.** Il comando è semplice; il problema è che le major release possono cambiare lo schema del `config.yaml`.

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

Il flag `--include-workspace` aggiunge i file della "scrivania" all'archivio (di default il backup contiene solo lo stato). Il `doctor --fix` post-update cattura i `schema mismatch` automaticamente. Lo script verifica che dopo l'update non ti sia rotto qualcosa di non ovvio (canale disconnesso, hook spento).

Leggi *sempre* il changelog prima di un major. Cerca le righe con tag `[breaking]` e `[security]`: sono le sole che ti faranno cambiare config a mano.

**Backup periodico.** OpenClaw ha un comando dedicato che produce un archivio `.tar.gz` versionato nel tempo:

```bash
# weekly backup, keeps last 8 archives
openclaw backup create \
  --output ~/Backups \
  --include-workspace \
  --rotate 8
```

Il file risultante è `openclaw-backup-YYYYMMDD-HHMM.tar.gz` e contiene: `config.yaml`, `credentials/` (cifrate, non in chiaro), `auth.token`, `sessions/`, `channels/`, e — se hai messo `--include-workspace` — anche `~/openclaw/workspace/`. Per restore in caso di disastro:

```bash
openclaw backup restore \
  ~/Backups/openclaw-backup-2026-05-13-0900.tar.gz
```

**(i) Pro tip:** schedula il backup in cron settimanale. Non aspettare il guasto per scoprire che non hai un punto di ripristino.

```bash
# Linux — every Sunday at 03:00
0 3 * * 0 openclaw backup create \
  --output ~/Backups \
  --include-workspace \
  --rotate 8
```

**Disinstallare per ricominciare da capo.** A volte è la mossa più rapida quando le cose si sono accumulate male. Tre passi, in ordine:

```bash
# 1. stop the daemon and remove the service
openclaw gateway uninstall

# 2. remove state and config (DANGER: secrets)
rm -rf "${OPENCLAW_STATE_DIR:-$HOME/.openclaw}"

# 3. remove the workspace if you really want
rm -rf ~/openclaw/workspace
```

**(!) Attenzione:** il passo 2 cancella le API key cifrate. Se le hai salvate solo lì, dopo non le recuperi più: usa l'occasione per *ruotarle* sui pannelli dei provider, in modo che eventuali copie sparse non valgano più. Il passo 3 distrugge `IDENTITY.md`, `SOUL.md`, memorie e progetti: prima di lanciarlo, valuta se vuoi tenerne almeno una copia (`cp -r ~/openclaw/workspace ~/openclaw-archive-$(date +%F)`).

Su macOS ricordati anche di rimuovere il LaunchAgent se non l'ha fatto `gateway uninstall`:

```bash
launchctl unload \
  ~/Library/LaunchAgents/ai.openclaw.gateway.plist
rm ~/Library/LaunchAgents/ai.openclaw.gateway.plist
```

Su Linux con systemd:

```bash
systemctl --user disable --now \
  openclaw-gateway.service
rm ~/.config/systemd/user/openclaw-gateway.service
```

A questo punto puoi rilanciare l'installer pulito da capo, riprendendo dalla sezione "TL;DR" all'inizio di questo capitolo.

### Mini-decision tree — "qualcosa non funziona"

Quando un'installazione si rompe, segui questo albero in ordine. Risolve l'80% dei casi senza googlare.

```text
1. openclaw --version
   └── command not found? → PATH problem
       (npm global bin not in PATH)

2. openclaw gateway status
   └── stopped? → openclaw gateway restart
   └── port in use? → change in config.yaml

3. openclaw doctor
   └── Node too old? → install Node 22.16+
   └── invalid config? → openclaw doctor --fix
   └── auth invalid? → re-run wizard auth step

4. openclaw logs --follow
   └── still confused? → ask Claude Code:
       "read ~/.openclaw/config.yaml and tell me
        what's wrong"
```

L'ultima riga non è una battuta: incollare il config a Claude Code o a un altro coding agent funziona sorprendentemente bene per individuare typo, indentazioni sbagliate, chiavi obsolete.

## Prompt pronti all'uso

I tre prompt che usi nei primi cinque minuti di vita dell'agente. Copia, incolla, adatta al tuo nome.

**Prompt 1 — La presentazione iniziale (scrive `IDENTITY.md`):**

> "Ciao! Sono [tuo nome]. Lavoro come [ruolo, breve] e le mie sfide quotidiane sono: [tre o quattro bullet]. Voglio che tu sia il mio assistente personale. Il tuo nome è [nome agente — es. Polly, Max, Sage]. Sei [tre aggettivi: es. preciso, asciutto, ironico]. Scrivi tu il tuo `IDENTITY.md` partendo da queste informazioni. Mostrami il contenuto prima di salvarlo, così posso correggere."

**Prompt 2 — Definire personalità e confini (`SOUL.md`):**

> "Adesso scrivi il tuo `SOUL.md`. Deve contenere: (1) tono di voce — come parli con me; (2) cosa fai sempre — abitudini positive; (3) cosa non fai mai — confini etici e operativi; (4) come gestisci l'incertezza — quando chiedi conferma e quando agisci da solo. Lunghezza massima 600 parole. Mostrami la bozza prima di salvarla."

**Prompt 3 — Test di salute end-to-end:**

> "Esegui un self-test: (a) leggi `IDENTITY.md` e dimmi chi sei in due frasi; (b) controlla che `gog` sia configurato e dimmi quanti messaggi non letti ho in inbox; (c) verifica che il canale Telegram sia collegato e mandami un messaggio di prova; (d) fai una ricerca web per 'OpenClaw release notes' e riassumi in tre righe; (e) dimmi quanti token hai consumato finora in questa conversazione. Output in formato lista."

**(#) Debug:** se il prompt 3 fallisce su uno qualunque dei punti, *non* andare avanti con altri setup. Risolvilo prima. Una pila di configurazioni sopra una base rotta produce solo confusione.

## Errori comuni e come risolverli

| Sintomo | Causa probabile | Fix |
|---|---|---|
| Lo script `curl … install.sh` fallisce | Rete dietro proxy aziendale o certificate pinning | Scaricare lo script (`curl -O`), ispezionarlo, lanciarlo manualmente con `bash install.sh`. |
| `openclaw: command not found` dopo `npm install -g` | `npm` global bin non in `PATH` | Aggiungi `export PATH="$(npm bin -g):$PATH"` a `~/.zshrc` o `~/.bashrc`, riapri il terminale. |
| `Node version too old` | Sistema con Node < 22.16 | Installa Node 24 (raccomandato) o 22 LTS via `nvm install 22 && nvm use 22`. |
| Errore `Anthropic API key invalid` o `subscription not allowed` | Tentativo di usare Claude Pro/Max bloccata dal 4 aprile 2026 | Generare una API key da `console.anthropic.com` e usarla. Vedi Cap. 14 per le alternative al ban. |
| La TUI non parte dopo l'installazione | Terminale non TTY (es. SSH senza `-t`) | Lanciare in un vero terminale o aggiungere `-t` allo `ssh`. |
| Onboarding completo ma `openclaw gateway status` dice "stopped" | Il Gateway non è stato avviato come daemon | `openclaw gateway --install-daemon` oppure `openclaw gateway start` per la sessione corrente. |
| Porta `18789` già in uso | Altro processo (o un'altra istanza OpenClaw) la sta tenendo | `lsof -i :18789` per identificare il processo; cambiare porta in `~/.openclaw/config.yaml`. |
| Dashboard si apre ma chat non risponde | Token di auth scaduto o regenerato dal Gateway | `cat ~/.openclaw/auth.token` per leggere quello attuale, ricaricare la dashboard. |
| `openclaw doctor` segnala "schema mismatch" | `config.yaml` di una versione precedente | `openclaw doctor --fix` per migrazione automatica; se fallisce, rinominare `config.yaml.bak` e rifare il wizard. |
| OAuth Google fallisce sul setup `gog` | Browser non aperto, redirect URI bloccato | Lanciare `openclaw skills configure gog` con Chrome aperto come browser di default. |
| Spese Anthropic salite all'improvviso | Hook `cost-tracker` disabilitato, agente in loop | `openclaw cost report --since 24h`; se vedi un cron bug, fermalo con `openclaw cron list && openclaw cron disable <id>`. |

## Checklist di fine capitolo

- [ ] Account utente dedicato e Gmail dedicata creati
- [ ] Node.js 22.16+ (idealmente 24) verificato con `node --version`
- [ ] Specifiche del mio OS lette (macOS / Linux / Windows-WSL2)
- [ ] OpenClaw installato senza errori (`openclaw --version` risponde)
- [ ] API key generata sul provider scelto, con spend limit mensile impostato
- [ ] Wizard di onboarding completato, daemon installato (`openclaw gateway status` = running)
- [ ] Modello LLM configurato con **API key valida** (NON sottoscrizione Claude)
- [ ] Almeno un canale collegato (`openclaw channels status` lo conferma)
- [ ] Skill `gog` e `summarize` installate; Brave Search attivo per la ricerca web
- [ ] Hook `session-memory` e `cost-tracker` attivi
- [ ] Primo "hatch" completato e l'agente risponde nella TUI
- [ ] Dashboard accessibile su `http://127.0.0.1:18789`
- [ ] `openclaw doctor` esce senza warning
- [ ] Script `verify-install.sh` salvato nei dotfiles, prima esecuzione "All green"
- [ ] `IDENTITY.md` e `SOUL.md` scritti con i Prompt 1 e 2
- [ ] Self-test (Prompt 3) superato su tutti e cinque i punti
- [ ] Backup settimanale schedulato in cron (`openclaw backup create --rotate 8`)
- [ ] API key, token Telegram, password Gmail salvati nel password manager
- [ ] Letto e annotato dove sta il file `config.yaml` per ritrovarlo dopo un `openclaw update`

## Link e risorse utili

- [Onboarding overview — documentazione ufficiale](https://docs.openclaw.ai/start/onboarding-overview) — cosa fa il wizard, opzioni avanzate
- [Onboarding wizard (CLI) — docs.openclaw.ai](https://docs.openclaw.ai/start/wizard) — reference dei flag e delle schermate
- [Getting started — docs.openclaw.ai](https://docs.openclaw.ai/start/getting-started) — quickstart ufficiale
- [Node.js requirements — docs.openclaw.ai](https://docs.openclaw.ai/install/node) — versioni supportate e troubleshooting
- [Hooks — docs.openclaw.ai](https://docs.openclaw.ai/cli/hooks) — reference completa di session-memory, cost-tracker e altri
- [General troubleshooting — docs.openclaw.ai](https://docs.openclaw.ai/help/troubleshooting) — guida ufficiale agli errori comuni
- [How to install OpenClaw without getting banned](https://www.shareuhack.com/en/posts/openclaw-setup-tutorial-2026) — tutorial aggiornato post-ban Anthropic
- [Anthropic provider docs (OpenClaw)](https://docs.openclaw.ai/providers/anthropic) — come configurare la chiave API Anthropic dopo il 4 aprile 2026
- [OpenClaw Setup Guide 2026: Install, Configure & Connect in 15 Min](https://www.verdent.ai/guides/openclaw-setup-guide-from-zero-to-ai-assistant) — walkthrough con screenshot
- [How to Run OpenClaw: Terminal, Daemon, TUI & Cloud](https://dextralabs.com/blog/how-to-run-openclaw/) — confronto delle modalità di esecuzione
- [OpenClaw Memory Files: AGENTS.md, IDENTITY.md, SOUL.md & More](https://openclaw-setup.me/blog/openclaw-internals/openclaw-memory-files/) — anatomia dei bootstrap files
- [OpenClaw Memory Masterclass — VelvetShark](https://velvetshark.com/openclaw-memory-masterclass) — guida completa alla memoria persistente
- [What Does `openclaw doctor --fix` Do?](https://www.stack-junkie.com/blog/openclaw-doctor-command) — ogni warning del doctor spiegato
- [openclaw on npm](https://www.npmjs.com/package/openclaw) — pacchetto ufficiale, changelog versioni
- [Uninstall — docs.openclaw.ai](https://docs.openclaw.ai/install/uninstall) — procedura ufficiale di rimozione
- [OpenClaw Backup Guide — LumaDock](https://lumadock.com/tutorials/openclaw-backup-export-settings-memory) — backup di stato, config, memoria
- [OpenClaw Complete Uninstall Guide (All Platforms)](https://gist.github.com/bewithdhanu/a5b960ef4a9550afa4a27020eeea1b85) — gist con i passi per ogni OS
- [Anthropic API keys — console.anthropic.com](https://console.anthropic.com/settings/keys) — pannello per generare la chiave Claude
- [How to Get Your Claude (Anthropic) API Key — Apideck](https://www.apideck.com/blog/how-to-get-your-claude-anthropic-api-key) — guida visuale passo-passo
- [OpenAI API keys — platform.openai.com](https://platform.openai.com/api-keys) — pannello per generare la chiave OpenAI
- [OpenAI API Quick Start (2026) — DEV Community](https://dev.to/abdul_qadir/openai-api-quick-start-2026-account-api-key-and-billing-setup-9b8) — account, key e billing in cinque minuti
- [Google AI Studio API key — aistudio.google.com](https://aistudio.google.com/app/apikey) — pannello per generare la chiave Gemini
- [Using Gemini API keys — ai.google.dev](https://ai.google.dev/gemini-api/docs/api-key) — restrizioni obbligatorie dal 19 giugno 2026

Per l'elenco completo delle fonti del libro, vedi [Appendice E](../Appendici/E-risorse-e-link-utili.md).

---

[← Capitolo 4](./04-preparare-un-ambiente-sicuro-docker-sandbox.md)  ·  [Indice](../README.md)  ·  [Capitolo 6 →](./06-configurare-telegram-e-altri-canali.md)
