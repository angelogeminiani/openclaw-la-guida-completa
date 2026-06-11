# Capitolo 2 — L'anatomia di un agente OpenClaw [★]

## Cosa imparerai

- Il modello mentale: l'agente come "dipendente digitale" con scrivania, badge, agenda e diario
- Gli **otto file di workspace** che OpenClaw carica all'avvio e che ruolo gioca ciascuno
- I **quattro strati di memoria**, e perché **heartbeat** e **cron** sono due cose diverse
- Il ciclo di vita di un task in **otto stadi**, raccontato anche con un esempio concreto
- Le regole di **sessione** e i **comandi di ispezione** di base

## Prerequisiti

Aver letto il [Capitolo 1](./01-cos-e-openclaw-e-perche-e-importante.md). Nessun prerequisito tecnico: basta mezz'ora.

## Contenuto principale

### Il modello mentale: un dipendente digitale, non un processo Unix

Il primo errore quando si apre la documentazione di OpenClaw è leggerla come un manuale di sistema: cercare il file di config, il binary, il demone. OpenClaw va invece ragionato come **un dipendente digitale** che vive sul tuo computer (o VPS, o Raspberry Pi), e l'analogia non è solo retorica: ti dice dove guardare quando qualcosa non va.

Il tuo agente ha **una scrivania**: il workspace, una cartella sul disco — `~/.openclaw/workspace/` per l'agente principale, `~/.openclaw/workspace-<nome>/` per gli agenti aggiuntivi. Ha un **badge**: nome, emoji e descrizione che lo rendono riconoscibile su Telegram, Slack o WhatsApp. Ha una **cassetta degli attrezzi**: le skill, ognuna documentata da un `SKILL.md`. Ha un'**agenda**: i cron job, che lui stesso può scrivere. Ha un **diario**: la memoria persistente, divisa in fogli giornalieri e note di lungo periodo. E ha un **cuore che batte**: l'heartbeat, un ping di sistema che lo sveglia anche quando nessuno gli ha scritto.

Quando l'agente "non risponde", il riflesso utile non è guardare i log di sistema, ma chiedersi quale dei sei elementi si è inceppato: workspace corrotto, `IDENTITY.md` ambiguo, skill senza permessi, cron non scritti, memoria piena o Gateway giù. La diagnostica del Capitolo 15 userà esattamente questa griglia.

### Workspace, agente, gateway: tre cose che non vanno confuse

Nel parlato della community questi tre termini si mescolano. Vale la pena tenerli separati fin da subito.

Il **Gateway** è uno e uno solo per macchina: il processo in background (lo lanci con `openclaw gateway start`) che apre i canali — Telegram, WhatsApp, Slack… — riceve i messaggi e li instrada. Senza Gateway acceso non c'è OpenClaw. Il suo control plane WebSocket interno (`ws://127.0.0.1:18789`) è il "centralino"; il Cap. 20 lo scopre nel dettaglio.

Gli **agenti** sono identità distinte, ognuna con il suo workspace. Un Gateway può servirne uno o dieci. `openclaw agents add <nome>` crea la cartella `~/.openclaw/workspace-<nome>/`, semina i file di partenza e insegna al Gateway a riconoscerlo nel routing.

Il **workspace** è la cartella fisica: file di identità, skill, cron, note di memoria, allegati. È versionabile con Git, copiabile da una macchina all'altra, ispezionabile con un editor di testo: chi vuole portare un agente da un Mac mini a un VPS sposta la cartella (e ridà le credenziali ai canali). È la conseguenza più potente di una scelta architetturale che il Cap. 20 esplora a fondo: **niente database, solo file**.

Una panoramica visuale:

```text
┌─────────────────────────────────────────────────────────┐
│            host (la tua macchina)                       │
│                                                         │
│  Telegram   WhatsApp    Slack      TUI                  │
│      │          │          │         │                  │
│      └──────────┴────┬─────┴─────────┘                  │
│                      ▼                                  │
│            ┌──────────────────┐                         │
│            │      Gateway     │  uno per host           │
│            │   (centralino)   │  ws://…:18789           │
│            └─────────┬────────┘                         │
│                      │                                  │
│                      ▼                                  │
│            ┌──────────────────┐                         │
│            │    agente × N    │  Polly, Finn, Max, …    │
│            │    (workspace)   │  (silos isolati)        │
│            ├──────────────────┤                         │
│            │ SOUL.md          │                         │
│            │ AGENTS.md        │                         │
│            │ IDENTITY.md      │                         │
│            │ USER.md          │                         │
│            │ TOOLS.md         │                         │
│            │ HEARTBEAT.md     │                         │
│            │ MEMORY.md        │                         │
│            │ memory/          │                         │
│            │ skills/          │                         │
│            │ cron/            │                         │
│            └─────────┬────────┘                         │
│                      ▼                                  │
│              [ LLM scelto ]   Claude, GPT, Nemotron, …  │
└─────────────────────────────────────────────────────────┘
```

Tre cose da notare. Primo, il Gateway è l'**unico punto di contatto con i canali**: nessun agente "parla" direttamente a Telegram. Secondo, ogni agente è un **silos**: i workspace non si vedono fra loro, e lo scambio passa da canali espliciti — `sessions_send` o una cartella condivisa configurata nel Gateway — mai dalla lettura del workspace altrui (Cap. 12). Terzo, ogni agente sceglie il **suo modello**: Polly può ragionare con Claude, Finn con Nemotron locale.

### Gli otto file che OpenClaw legge all'avvio

OpenClaw, all'avvio di una sessione, **carica automaticamente fino a otto file** dalla radice del workspace — alcuni sempre, altri secondo il contesto (MEMORY.md nelle sessioni dirette, HEARTBEAT.md quando il battito è rilevante). È bene memorizzarli.

I file sono `SOUL.md`, `AGENTS.md`, `USER.md`, `TOOLS.md`, `IDENTITY.md`, `HEARTBEAT.md`, `BOOTSTRAP.md`, `MEMORY.md`. Cinque sono di **identità**, due di **ciclo di vita**, uno è la **memoria di lungo periodo**.

Sul disco, una settimana dopo il primo avvio, il workspace tipico ha questa forma:

```text
~/.openclaw/workspace-polly/
├── SOUL.md          # personalità, tono, confini
├── AGENTS.md        # istruzioni operative
├── IDENTITY.md      # nome, emoji, vibe
├── USER.md          # dossier su di te (manuale)
├── TOOLS.md         # note operative sui tool
├── HEARTBEAT.md     # checklist battito (~30 min)
├── MEMORY.md        # memoria di lungo periodo
├── memory/          # note giornaliere
│   ├── 2026-05-05.md
│   ├── 2026-05-06.md   ← "ieri"
│   └── 2026-05-07.md   ← "oggi"
├── skills/          # cartelle con SKILL.md
│   ├── gog/
│   ├── summarize/
│   └── web-search/
├── cron/            # job programmati (yaml)
│   ├── morning-digest.yaml
│   └── meeting-prep.yaml
├── attachments/     # allegati dai canali
└── .openclaw/       # stato interno (cache, lock)
```

Quello che vedi qui è *tutto* ciò che esiste di un agente: niente database nascosti, niente stato nel cloud. Se cancelli la cartella, l'agente smette di esistere; se la copi altrove, riprende da dove l'avevi lasciato. Per questo **mettere il workspace sotto Git** è la cosa più utile della prima settimana (Cap. 15): ogni `git diff` ti racconta come l'agente sta cambiando.

**SOUL.md — la personalità.** Il file più impattante che esista: ogni risposta dell'agente passa attraverso il suo SOUL. Qui scrivi *come* parla, *cosa* fa volentieri, *cosa non deve mai fare*. Un SOUL.md generico produce un agente generico; uno scritto bene dà all'agente una voce. Esempio: `"Be witty and use understatement"` è personalità e sta qui; `"Always answer in under 200 words"` è una regola operativa e va in `AGENTS.md`. SOUL parla del *chi*, AGENTS del *come si lavora*.

**AGENTS.md — il contratto di lavoro.** Le istruzioni operative, lette ad ogni risveglio: cosa leggere prima di rispondere, in che ordine, con quali priorità. È qui che metti regole tipo "se un'azione costa più di 50 centesimi, chiedi conferma". Il **mansionario** che daresti a un nuovo assunto.

**IDENTITY.md — il biglietto da visita.** Nome, emoji, vibe, descrizione breve: la parte che vede chi entra in contatto con l'agente. È più leggero di SOUL.md perché parla di *come l'agente appare*, non di *come pensa*.

**USER.md — il dossier su di te.** Ciò che l'agente deve ricordare di te in maniera *stabile*: nome, ruolo, città, fusi orari, preferenze ricorrenti, vincoli, persone della tua cerchia. È la parte che mantieni *intenzionalmente* tu (il Cap. 7 consiglia mezz'ora di onboarding, poi ritocchi mensili).

**TOOLS.md — il manuale d'uso degli strumenti.** Note operative in linguaggio naturale sull'ambiente: convenzioni di path, alias di shell, comandi da usare con cautela, adattatori configurati. Se installi una skill e l'agente la usa male, è qui che scrivi "quando usi `gog`, l'account di default è X, quello di lavoro è Y, non confonderli".

**HEARTBEAT.md — la checklist del battito.** Se il file esiste, l'agente lo legge ad ogni heartbeat (di default ogni 30 minuti). È una *checklist piccola, stabile, sicura*: cosa controllare a intervalli regolari. Tienila cortissima: tutto ciò che metti qui pesa sul costo di ogni battito, e i battiti sono molti in una giornata. Un esempio minimo che funziona bene nel primo mese:

```markdown
# Heartbeat checklist for Polly

Run silently every 30 minutes.
Reply "HEARTBEAT_OK" if nothing actionable.

1. Inbox: any emails from priority senders
   (see USER.md → priority_list)?
   If yes, summarize in one line and ping me.
2. Calendar: meeting starting in <30 min?
   If yes, run "meeting-prep" and deliver
   the brief to Telegram.
3. Otherwise: HEARTBEAT_OK.
```

Se nessun criterio scatta, l'agente risponde `HEARTBEAT_OK` e il Gateway lo scarta in silenzio; se c'è materia, agisce e ti scrive. È la macchina che produce la sensazione, descritta nel Cap. 1, di "essere svegliato dall'agente al momento giusto".

**BOOTSTRAP.md — il rito del primo avvio.** Vive solo per pochi minuti. Al primo avvio OpenClaw scrive un BOOTSTRAP.md che guida una conversazione di onboarding (chi sei, in che fuso orario sei, che canale preferisci…); le risposte vengono propagate in `IDENTITY.md`, `USER.md`, `SOUL.md`. Finito il rito, OpenClaw cancella `BOOTSTRAP.md`. Se lo trovi ancora lì dopo settimane, il bootstrap non è andato a buon fine — vai al Cap. 7 a riavviarlo. Due tetti da conoscere: i file di bootstrap vengono caricati fino a 150.000 caratteri complessivi, e nessun singolo file dovrebbe superare i 20.000.

**MEMORY.md — la memoria di lungo periodo.** Fatti durevoli, decisioni prese, preferenze emerse in conversazione: ciò che USER.md non aveva previsto. La regola d'oro: **USER.md è ciò che tu metti deliberatamente; MEMORY.md è ciò che l'agente impara da solo**. Tenerli separati ti risparmia ore di debug.

**(i) Pro tip:** la "regola degli 8 file" non è una formalità. Se scrivi una preferenza importante in un file con un altro nome (`PREFERENCES.md`, `CONTEXT.md`), l'agente *non lo leggerà* a meno che una skill o un'istruzione in `AGENTS.md` glielo faccia caricare. È la causa numero uno dei "ma te l'avevo detto!" della prima settimana.

### Memoria: quattro strati che falliscono in modi diversi

OpenClaw non ha "una" memoria: ne ha quattro, e capirne la geografia fa la differenza fra un agente che dimentica tutto e uno che ricorda solo ciò che serve.

Il **primo strato** sono i **bootstrap files** appena descritti: caricati ad ogni inizio di sessione, danno all'agente la sua identità di base. Pesano in token, ma sono la spina dorsale.

Il **secondo strato** è la **MEMORY.md**: l'archivio durevole dei fatti che devono sopravvivere alla singola conversazione, caricata ad ogni inizio sessione DM (la chat 1:1 con te). "Il mio chirurgo si chiama Y", "non chiamare mai mia madre prima delle 10".

Il **terzo strato** sono le **note giornaliere**, file in `memory/YYYY-MM-DD.md` con il contesto vivo della giornata. OpenClaw carica automaticamente la nota di oggi e quella di ieri: una "finestra di lavoro" sul presente, senza un mese di storia nel contesto. Quando vuoi capire perché l'agente ha fatto qualcosa, spesso la risposta è scritta lì.

Il **quarto strato** è l'**indice semantico** opzionale: un piccolo vettoriale costruito su MEMORY.md e sui file in `memory/`, che trova fatti rilevanti anche quando le parole della richiesta non coincidono con quelle nei file. Non obbligatorio, ma sui setup maturi diventa utile presto.

Quando l'agente "dimentica", la diagnosi parte da **quale strato ha fallito**: il tuo nome → USER.md o bootstrap files; le decisioni di ieri → nota giornaliera non letta o non scritta; un fatto di due mesi fa → MEMORY.md non l'ha mai registrato. La distinzione è la base del Cap. 15.

**(!) Attenzione:** quando una sessione si avvicina al limite di contesto, OpenClaw esegue un *turno silenzioso* (flag `NO_REPLY`, niente arriva al tuo canale) per ricordare al modello di salvare in memoria ciò che è importante prima della compattazione automatica. Se nei log vedi attività che non corrisponde a nessun tuo messaggio, probabilmente è quello.

### Heartbeat e cron: il cuore e l'agenda

Sono i due meccanismi temporali di OpenClaw, e si scambiano spesso a parole.

L'**heartbeat** è un battito *ricorrente di sistema*: di default ogni 30 minuti l'agente si sveglia, legge il suo `HEARTBEAT.md` e decide se c'è qualcosa di cui occuparsi. È ciò che gli permette di "esistere" anche quando nessuno gli ha scritto: la differenza essenziale rispetto a un chatbot. Per default gira nella sessione `main`, ma può essere isolato (`sessionTarget: "isolated"`): ogni battito parte da zero e costa una frazione di un battito ricco di contesto.

Il **cron** è un *appuntamento programmato esplicitamente*: "ogni mattina alle 7:00 mandami il digest", "fra venti minuti ricordami la chiamata". È il Gateway a tenere traccia dei cron, svegliare l'agente all'orario giusto e consegnare l'output sul canale configurato. Particolarità potente: i cron possono creare altri cron — il modo con cui un agente "impara la tua agenda" (Cap. 18).

La regola pratica: l'heartbeat è il *cuore*, il cron è l'*agenda*. "Ogni tanto, in modo opportunistico" sta nell'heartbeat; "a un orario preciso" sta nel cron. Se le code sono occupate l'heartbeat viene saltato e ritentato dopo: è un'eccezione gestita, non un errore.

### Sessioni: una geometria di isolamento

Una **sessione** è il contenitore in cui vive una conversazione: storia, stato, costi, modello in uso. La domanda interessante non è "cosa c'è dentro", ma "*quante* sessioni esistono e *come* sono separate". Dipende dal **session scope**, configurabile a livello di Gateway o di agente:

- **`main`** — una sessione globale per tutti i DM. Comodo per uso strettamente personale; pericoloso se l'agente parla con più persone.
- **`per-peer`** — una sessione per ogni mittente, indipendentemente dal canale: Telegram e WhatsApp finiscono nella stessa storia.
- **`per-channel-peer`** — una sessione per ogni mittente *su ogni canale*. È il default. La personalità è la stessa (SOUL.md è uno solo), ma le conversazioni non si contaminano.
- **`per-account-channel-peer`** — isolamento extra per account, utile per chi gestisce più tenant dallo stesso Gateway.

A questa geometria si sovrappone l'isolamento dei **gruppi**: una conversazione di gruppo è un'altra sessione ancora, separata dai DM. Nei gruppi entrano in gioco tre regolatori. Il **mention gating**: l'agente parte solo se menzionato (`@nome`) o se rispondi a un suo messaggio — senza, cercherebbe di rispondere a tutto il rumore del canale. I **reply tags**: etichette che legano correttamente i thread quando le conversazioni si intrecciano. Il **per-channel chunking**: ogni canale ha limiti diversi di lunghezza, e OpenClaw spezza la risposta rispettandoli senza mai rompere un blocco di codice a metà.

Due meccanismi di contorno, in breve. I messaggi di gruppo che non fanno scattare un run (perché nessuno ha menzionato l'agente) finiscono comunque in un **history buffer**, recuperabile se più tardi quel contesto serve. E quando arrivano messaggi mentre l'agente sta ancora lavorando, il comportamento dipende dal **queue mode**: `interrupt` taglia il run in corso, `steer` lo ricalibra senza fermarlo, `followup` accoda il messaggio come turno successivo, `collect` accumula tutto e lo tratta insieme a fine run. Per la maggior parte dei lettori il default va benissimo; il Cap. 20 copre le quattro modalità in dettaglio e i casi limite (gli agenti che gestiscono allarmi in tempo reale, per esempio, preferiscono `interrupt`).

### Il ciclo di vita di un task

Ricomponendo i pezzi, il viaggio di una richiesta — da quando scrivi a quando leggi la risposta — segue **otto stadi**.

1. **Inbound al canale.** Il plugin del canale traduce il payload nativo in un evento standard di OpenClaw.
2. **Routing al Gateway.** Il Gateway applica le regole di binding e seleziona l'agente.
3. **Risoluzione della sessione.** In base al session scope si trova (o si crea) la sessione corretta; le sessioni di gruppo applicano mention gating e reply tags.
4. **Assemblaggio del contesto.** Si caricano i bootstrap files, MEMORY.md, le note di oggi e ieri, eventualmente l'indice semantico.
5. **Ragionamento dell'LLM.** Il modello configurato decide cosa fare: rispondere, chiamare una skill, eseguire un tool, scrivere su disco, programmare un cron.
6. **Esecuzione delle azioni.** Skill invocate, tool eseguiti, comandi lanciati: ognuno con i suoi log e il suo costo.
7. **Outbound al canale.** Il risultato torna al Gateway, viene chunkato e consegnato; per i run da cron decide il `delivery channel` configurato.
8. **Aggiornamento della memoria.** A fine turno l'agente scrive ciò che merita di sopravvivere in MEMORY.md o nella nota giornaliera.

Ripetuto migliaia di volte al giorno fra heartbeat, cron e messaggi reali, questo ciclo costruisce la sensazione di "avere un dipendente". Ogni stadio è ispezionabile (`openclaw status`, log del Gateway, file della memoria) ed è un punto di intervento quando qualcosa non va.

#### Un esempio concreto: "Polly, prepara il brief per le 14:30"

Per ancorare gli otto stadi a qualcosa di tangibile, segui un singolo messaggio. Sono le 13:48. Scrivi su Telegram al tuo agente Polly: *"Prepara un brief sul cliente Rossi per la chiamata delle 14:30, due paragrafi."*

Il bot grammY trasforma il messaggio in un evento `MessageReceived` (stadio 1); il binding di config lo instrada all'agente `polly` (stadio 2). Lo scope è `per-channel-peer`: il Gateway riprende la sessione `(telegram, tuo_id, polly)`, che ha già 14 turni di storia (stadio 3).

Polly assembla il contesto (stadio 4): gli otto file canonici, più `memory/2026-05-06.md` (ieri) e `memory/2026-05-07.md` (oggi). In `MEMORY.md` trova: "Cliente Rossi — pricing in revisione, da non menzionare in pubblico". Tiene nota.

Il modello configurato (Claude Sonnet 4.6) decide il piano (stadio 5): due skill da chiamare, `crm-lookup` e `linkedin-recent`. Le invoca (stadio 6) e compone il brief, evitando il pricing per via della nota in `MEMORY.md`. La risposta — 187 parole, ben sotto i limiti di Telegram — viene consegnata in due messaggi, un paragrafo ciascuno (stadio 7). Infine Polly scrive nella nota di oggi: *"13:50 — preparato brief Rossi per 14:30; pricing volutamente omesso (vedi MEMORY.md)"* (stadio 8).

Tempo totale dall'invio alla risposta: ~6 secondi. Token spesi: ~3.500 in input (bootstrap + storia) + ~250 in output. Costo stimato: dell'ordine del centesimo. Il Cap. 14 trasforma questa contabilità in regole di budget esplicite.

### Canali: dove vive la conversazione

I **canali** sono i mezzi attraverso cui parli all'agente: ne esistono più di venti, ognuno con un plugin dedicato. I principali, con un consiglio d'uso.

**Telegram (grammY)** è il canale consigliato per iniziare: setup veloce con `@BotFather`, supporto a immagini, file, voce, gruppi — la base del Cap. 6. **WhatsApp (Baileys)** è il più naturale per uso personale e familiare, ma usa il protocollo non ufficiale di WhatsApp Web ed è il più sensibile a cambi lato Meta. **Slack** e **Discord** sono i canali da team: il primo per l'ufficio, il secondo per le community. **Signal** è la scelta per chi vuole privacy; per **iMessage**, dal 2026 il plugin nativo è il default e il vecchio ponte BlueBubbles è deprecato.

C'è poi l'arcipelago lungo — Teams, Matrix, Google Chat, LINE, IRC, Mattermost, Nostr, WeChat, QQ e altri — utile in casi specifici (WeChat e QQ per chi opera in Cina, Matrix per chi vuole un canale federato). E due interfacce locali: la **TUI**, la shell interattiva che vedi appena finita l'installazione, utile per il primo "hatch" e il debug; e il **WebChat**, una pagina web minimale servita dal Gateway.

La regola di scelta è banale: il canale giusto è *quello che già usi tutto il giorno*. Telegram è il consiglio del libro per l'onboarding perché ha l'attrito più basso, ma niente vieta di passare a WhatsApp dopo una settimana.

### Tool, skill, MCP: cosa sa fare l'agente

Le **skill** sono cartelle, ognuna con un `SKILL.md` che descrive cosa fa, quando usarla e come eseguirla. Il formato deriva dagli "AgentSkills" di Anthropic: YAML frontmatter, istruzioni in Markdown, eventuali script ausiliari. Quando un compito richiede una skill, l'agente la "scopre" leggendone il SKILL.md, la esegue e integra l'output nel ragionamento. Si installano da **ClawHub**, il registry pubblico, o da un repo Git, con `openclaw skills install <nome-o-url>`.

Accanto alle skill esistono i **tool nativi** del Gateway (filesystem, shell, web search di base) e i **server MCP** (Model Context Protocol), che espongono all'agente API e dati esterni in modo standardizzato. Per il livello di questo capitolo basta sapere che esistono tre porte di ingresso — skill, tool nativi, MCP — e che TOOLS.md è il posto dove dire all'agente come usarle bene.

**(!) Attenzione:** skill di terze parti significa codice di terze parti. La storia di **ClawHavoc** raccolta nel Cap. 13 — skill malevole sfuggite alla revisione e arrivate a workspace ignari — è successa davvero. Quando installi una skill, leggi il SKILL.md, controlla il repo e preferisci autori riconoscibili.

### Un agente o molti? L'idea del "team"

OpenClaw è pensato per il **multi-agente**: su un solo Gateway puoi avere un'assistente personale (Polly), un agente "famiglia" (Finn), un agente di marketing (Max), ognuno con SOUL, IDENTITY, MEMORY e cron diversi; il routing dei canali decide chi risponde a chi. I Capitoli 10–12 sono dedicati a questo, ma il principio serve subito: l'unità minima è *l'agente*, non *il sistema*. Se il tuo agente fa "troppe cose", il problema non è la capacità — è il mansionario sovraccarico. La risposta è quasi sempre **specializzare**: più agenti, ognuno con un SOUL.md mirato.

### Come ispezionare l'agente: i comandi che userai sempre

Ogni concetto di questo capitolo ha un comando di ispezione corrispondente. Non serve impararli a memoria oggi, ma la prima diagnosi di "perché non funziona?" passa quasi sempre da uno di questi.

```bash
# gateway up? canali connessi?
openclaw status
openclaw channels status

# agenti e loro config risolta
openclaw agents list
openclaw agents show polly

# sessioni attive; storia, modello, costi
openclaw sessions list
openclaw sessions show <session-id>

# skill installate e dettaglio
openclaw skills list
openclaw skills show <nome>

# cron programmati e stato del battito
openclaw cron list
openclaw heartbeat status

# workspace sul disco
ls -la ~/.openclaw/workspace-polly/
cat ~/.openclaw/workspace-polly/IDENTITY.md
```

Il pattern è sempre lo stesso: dalla salute del sistema (`status`) si scende al pezzo specifico e poi al file su disco. Il Cap. 15 espande questa griglia in un runbook diagnostico.

**(#) Debug:** se l'agente "non capisce" una preferenza che sei sicuro di aver dato: (1) `cat USER.md` e cercala letterale; (2) `grep -r "parola-chiave"` sul workspace, per vedere se è finita in un file non canonico; (3) `openclaw sessions show <session-id>` per controllare quali bootstrap files sono stati caricati. Nove volte su dieci il problema è al punto 2: la preferenza esiste, ma in un file che OpenClaw non legge.

**Prompt pronto:**
> "Apri il tuo workspace. Elenca i file nella radice e dimmi, per ognuno, se è uno degli otto canonici di OpenClaw e che ruolo gioca. Segnala canonici mancanti e file non canonici da spostare o caricare a mano."

**Prompt pronto:**
> "Riassumi chi sei in tre paragrafi: il primo dal tuo SOUL.md, il secondo da IDENTITY.md, il terzo da ciò che sai di me da USER.md e MEMORY.md. Indicami una cosa sbagliata o obsoleta che hai trovato."

**(i) Pro tip:** chiedere all'agente di **leggersi** ad alta voce — riassumere SOUL/IDENTITY/USER/MEMORY in linguaggio naturale — è la forma più semplice di manutenzione preventiva: fa emergere contraddizioni, regole stantie, preferenze invecchiate.

## Errori comuni e come risolverli

| Sintomo | Causa probabile | Fix |
|---------|-----------------|-----|
| L'agente "dimentica" cose importanti | Le note restano in conversazione, non sui file di memoria | Chiedi esplicitamente "salva questo in USER.md"; verifica che il file sia cambiato. |
| L'agente non risponde a un messaggio | Gateway giù o canale disconnesso (l'heartbeat non c'entra) | `openclaw status`, poi `openclaw channels status`. Se è il canale, riavvia quello. |
| Confondere SOUL, AGENTS e IDENTITY | Nomi simili, ruoli sovrapponibili | SOUL = personalità. AGENTS = istruzioni operative. IDENTITY = biglietto da visita. |
| BOOTSTRAP.md ancora lì dopo settimane | Bootstrap fallito al primo avvio | Vai al Cap. 7: rispondi alle domande nella TUI finché il file si auto-cancella. |
| "Regole" che non ricordi di aver scritto | Skill che ha modificato AGENTS.md | Cerca in AGENTS.md i marker tipo `<!-- skill:nome -->`; rimuovi e disinstalla se serve. |
| Risposte lente o costose | HEARTBEAT.md troppo lungo o note giornaliere enormi | HEARTBEAT.md sotto le 20 righe; archivia note vecchie con un cron di compaction (Cap. 18). |
| Conversazioni di gruppo che esplodono | Mention gating disattivato | Riattiva `mentionGating: true` per il canale di gruppo. |
| Una sessione "vede" cose di un'altra | Scope su `main` o `per-peer` invece di `per-channel-peer` | Cambia `session.scope`, riavvia, verifica con `openclaw sessions list`. |

## Checklist di fine capitolo

- [ ] So elencare gli **otto file** che OpenClaw legge all'avvio e cosa fa ciascuno
- [ ] So distinguere **SOUL.md** (personalità) da **AGENTS.md** (operatività) da **IDENTITY.md** (biglietto da visita)
- [ ] Conosco i **quattro strati di memoria** (bootstrap files, MEMORY.md, note giornaliere, indice semantico)
- [ ] So distinguere **heartbeat** (battito ricorrente, ~30 min) da **cron** (appuntamento programmato)
- [ ] Ho chiari gli **otto stadi del ciclo di vita di un task**
- [ ] Conosco i **session scope** e so che il default è `per-channel-peer`
- [ ] So cosa sono **mention gating**, **reply tags** e le **quattro queue mode** (interrupt, steer, followup, collect)
- [ ] So che **Gateway** è uno per macchina, **agenti** sono molti, **workspace** è una cartella di file ispezionabili
- [ ] Conosco i comandi di ispezione di base (`openclaw status`, `openclaw sessions list`, `openclaw cron list`)
- [ ] Ho capito perché **mettere il workspace sotto Git** è la prima cosa utile della prima settimana

## Link e risorse utili

- [Documentazione ufficiale](https://docs.openclaw.ai) — riferimento canonico per workspace, gateway, sessioni e memoria
- [Heartbeat — OpenClaw Docs](https://docs.openclaw.ai/gateway/heartbeat) — meccanica del battito e isolamento di sessione
- [Agent bootstrapping — OpenClaw Docs](https://docs.openclaw.ai/start/bootstrapping) — il primo avvio e la cancellazione di BOOTSTRAP.md
- [Architecture overview](https://github.com/openclaw/openclaw/blob/main/docs/concepts/architecture.md) — panoramica dei moduli
- [Memory concepts](https://github.com/openclaw/openclaw/blob/main/docs/concepts/memory.md) — i quattro strati di memoria spiegati nel codice
- [Messages and queue modes](https://docs.openclaw.ai/concepts/messages) — `interrupt` / `steer` / `followup` / `collect`
- [OpenClaw Workspace Files Explained](https://capodieci.medium.com/ai-agents-003-openclaw-workspace-files-explained-soul-md-agents-md-heartbeat-md-and-more-5bdfbee4827a) — Roberto Capodieci, marzo 2026
- [SOUL.md & Identity — Designing Your Agent's Personality](https://learnopenclaw.com/core-concepts/soul-md) — guida pratica alla scrittura di SOUL.md
- [OpenClaw Memory Masterclass](https://velvetshark.com/openclaw-memory-masterclass) — VelvetShark, deep-dive sulla memoria
- [Architecting the Agentic Future: OpenClaw vs NanoClaw vs NemoClaw](https://dev.to/mechcloud_academy/architecting-the-agentic-future-openclaw-vs-nanoclaw-vs-nvidias-nemoclaw-9f8) — confronto architetturale fra le tre famiglie
- [Repository GitHub](https://github.com/openclaw/openclaw) — il codice sorgente

Per l'elenco completo delle fonti del libro, vedi [Appendice E](../Appendici/E-risorse-e-link-utili.md).

---

[← Capitolo 1](./01-cos-e-openclaw-e-perche-e-importante.md)  ·  [Indice](../README.md)  ·  [Capitolo 3 →](../PARTE-II-Installazione/03-scegliere-dove-installare-openclaw.md)
