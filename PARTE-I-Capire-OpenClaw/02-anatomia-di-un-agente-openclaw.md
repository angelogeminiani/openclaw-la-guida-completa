# Capitolo 2 — L'anatomia di un agente OpenClaw [★]

## Cosa imparerai

- Il modello mentale: l'agente come "dipendente digitale" con scrivania, badge, agenda e diario
- Gli **otto file di workspace** che OpenClaw carica all'avvio e che ruolo gioca ciascuno
- Come funzionano **heartbeat** e **cron**, e perché sono due cose diverse
- I **quattro strati di memoria** e cosa va in quale strato
- Il ciclo di vita di un task in **otto stadi**, raccontato anche con un esempio concreto
- Le regole di **sessione** e isolamento per canale, gruppo e utente
- I **comandi di ispezione** di base per capire cosa sta facendo l'agente

## Prerequisiti

Aver letto il [Capitolo 1](./01-cos-e-openclaw-e-perche-e-importante.md). Nessun prerequisito tecnico: basta una mezz'ora e un blocco di carta per gli appunti.

## Contenuto principale

### Il modello mentale: un dipendente digitale, non un processo Unix

Il primo errore quando si apre la documentazione di OpenClaw è leggerla come si legge un manuale di sistema: cercare il file di config, il binary, il demone, le opzioni della CLI. È un riflesso comprensibile ma porta fuori strada. OpenClaw è progettato per essere ragionato come **un dipendente digitale** che vive sul tuo computer (o sul tuo VPS, o sul tuo Raspberry Pi), e l'analogia non è soltanto retorica: ti aiuta a capire dove guardare quando qualcosa non va.

Pensa così. Il tuo agente ha **una scrivania**: il workspace, una cartella sul disco — `~/.openclaw/workspace/` per l'agente principale, `~/.openclaw/workspace-<nome>/` per gli agenti aggiuntivi — dove vivono tutti i suoi file. Ha un **badge**: un'identità con un nome, un'emoji, una descrizione, che lo rende riconoscibile su Telegram, Slack o WhatsApp. Ha una **cassetta degli attrezzi**: le skill installate, ognuna documentata da un `SKILL.md` che gli spiega come usarla. Ha un'**agenda**: i cron job, scadenze ricorrenti che lui stesso può scrivere. Ha un **diario**: la memoria persistente, divisa in fogli giornalieri e in note di lungo periodo. E ha un **cuore che batte**: l'heartbeat, un ping di sistema che lo sveglia anche quando nessuno gli ha scritto.

Quando l'agente "non risponde", il primo riflesso utile non è guardare i log di sistema; è chiedersi quale dei sei elementi sopra non sta funzionando. Manca la scrivania (workspace corrotto)? Il badge è confuso (`IDENTITY.md` ambiguo)? La cassetta è chiusa (skill non installate o senza permessi)? L'agenda è vuota (cron non scritti)? Il diario è bloccato (memoria piena, contesto compattato)? Il cuore non batte (Gateway giù)? La diagnostica del Capitolo 15 rifletterà questa stessa griglia, e la userai più di una volta.

### Workspace, agente, gateway: tre cose che non vanno confuse

Nel parlato della community questi tre termini si mescolano. Vale la pena tenerli separati fin da subito.

Il **Gateway** è uno e uno solo per macchina: è il processo che gira in background (lo lanci con `openclaw gateway start`), apre i canali (Telegram, WhatsApp, Slack…), riceve i messaggi e li instrada. Senza Gateway acceso non c'è OpenClaw, anche se il tuo workspace è perfetto. Esiste un control plane WebSocket interno (`ws://127.0.0.1:18789`) che il Cap. 20 scopre nel dettaglio; per ora basta sapere che è il "centralino".

Gli **agenti** sono identità distinte, ognuna con il suo workspace. Un Gateway può servirne uno o dieci. Quando aggiungi un agente con `openclaw agents add <nome>`, viene creata una cartella `~/.openclaw/workspace-<nome>/`, vengono seminati alcuni file di partenza, e il Gateway impara a riconoscerlo nel routing dei canali.

Il **workspace** è la cartella fisica: lì dentro vivono i file di identità, le skill, i cron, le note di memoria, eventuali allegati. È versionabile con Git, copiabile da una macchina all'altra, ispezionabile con un editor di testo. È il punto in cui finisce ogni cosa che l'agente "sa di sé". Chi vuole portare un agente da un Mac mini a un VPS Hetzner non fa altro che spostare la cartella (e ridare le credenziali ai canali). È la conseguenza più potente di una scelta architetturale che il Cap. 20 esplora a fondo: **niente database, solo file**.

Una panoramica visuale aiuta a fissare i rapporti fra i tre concetti, prima di entrare nel dettaglio dei singoli pezzi:

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

Tre cose vale la pena notare in questo schema. Primo, il Gateway è l'**unico punto di contatto con i canali**: nessun agente "parla" direttamente a Telegram. Secondo, ogni agente è un **silos**: il workspace di Polly e quello di Finn (e di tutti gli altri) non si vedono fra loro, ed è questa la garanzia di isolamento. Quando due agenti devono davvero scambiarsi qualcosa, lo fanno attraverso canali espliciti — `sessions_send` o una cartella condivisa configurata nel Gateway — mai leggendo direttamente il workspace altrui: il meccanismo è spiegato nel Cap. 12. Terzo, ogni agente sceglie il **suo modello**: Polly può ragionare con Claude, Finn con Nemotron locale, e il Gateway è indifferente.

### Gli otto file che OpenClaw legge all'avvio

OpenClaw, all'avvio di una sessione, **carica automaticamente otto file** se li trova nella radice del workspace. Non di più, non di meno. È bene memorizzarli: la maggior parte degli "errori da principiante" deriva dall'aver scritto qualcosa di importante in un file con un altro nome — di lì non viene letto a meno che tu non lo carichi a mano.

I file sono `SOUL.md`, `AGENTS.md`, `USER.md`, `TOOLS.md`, `IDENTITY.md`, `HEARTBEAT.md`, `BOOTSTRAP.md`, `MEMORY.md`. Cinque di questi sono di **identità** (chi è, come si comporta, cosa sa di te); due sono di **ciclo di vita** (come fa il primo avvio e cosa fa quando si sveglia); uno è la **memoria di lungo periodo**.

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
│   ├── 2026-05-05.md   ← "ieri"
│   ├── 2026-05-06.md   ← "oggi"
│   └── 2026-05-07.md
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

Quello che vedi qui è *tutto* ciò che esiste di un agente. Non c'è un database nascosto, non c'è un servizio cloud che tiene altro stato, non ci sono file binari proprietari. Se cancelli la cartella, l'agente smette di esistere; se la copi su un altro computer, riprende da dove l'avevi lasciato. La conseguenza pratica è importante: **mettere il workspace sotto Git** è la cosa più utile che puoi fare nella prima settimana — vedi il Cap. 15 per il workflow completo, ma il punto di partenza è banale: `cd ~/.openclaw/workspace-polly && git init && git add -A && git commit -m "polly day 0"`. Da quel momento ogni `git diff` ti racconta come l'agente sta cambiando nel tempo, e ogni `git log` è il diario delle sue evoluzioni.

**SOUL.md — la personalità.** È il file più impattante che esista. Ogni risposta dell'agente passa attraverso il suo SOUL. Qui scrivi *come* parla (formale o sciolto, breve o esteso, ironico o asciutto), *cosa* fa volentieri, *cosa non deve mai fare*, e con quale gerarchia di valori si muove. Un SOUL.md generico produce un agente generico; un SOUL.md scritto bene è la differenza fra un assistente anonimo e un collega con una voce. Un esempio: scrivere `"Be witty and use understatement"` qui dentro è una scelta di personalità; scrivere `"Always answer in under 200 words"` è invece una regola operativa, e va in `AGENTS.md`. La distinzione fra i due file è esattamente questa: SOUL parla del *chi*, AGENTS del *come si lavora*.

**AGENTS.md — il contratto di lavoro.** Le istruzioni operative, lette ad ogni risveglio. Cosa leggere prima di rispondere (ad esempio: "leggi USER.md, oggi e ieri in `memory/`, e MEMORY.md se presente"), in che ordine, con quali priorità. È qui che metti regole tipo: "se un'azione costa più di 50 centesimi, chiedi conferma prima di eseguirla", oppure "non scrivere mai email senza farmele leggere prima". Pensalo come al **mansionario** che daresti a un nuovo assunto.

**IDENTITY.md — il biglietto da visita.** Nome, emoji, vibe, descrizione breve. È la parte che vede chi entra in contatto con l'agente: chi sei, in che lingua di default rispondi, qual è il ruolo che ricopri. È più leggero di SOUL.md perché parla di *come l'agente appare* anziché di *come pensa*. Il framework risolve i campi con una catena di fallback (config globale → config per-agente → file di workspace), e quello che leggi sul canale è il risultato di quella risoluzione.

**USER.md — il dossier su di te.** Tutto ciò che l'agente deve ricordare di te in maniera *stabile*: nome, ruolo, città, fusi orari, preferenze ricorrenti, vincoli noti, persone che fanno parte della tua cerchia, gli account con cui lavori, i brand che usi. È la parte che mantieni *intenzionalmente* tu — e che resta ferma finché non la cambi. Una buona pratica del Cap. 7 è dedicarvi mezz'ora di onboarding e poi tornarci due o tre volte al mese.

**TOOLS.md — il manuale d'uso degli strumenti.** Note operative sull'ambiente: convenzioni di path sul tuo computer, alias del tuo shell, peculiarità del tuo sistema, comandi che vanno usati con cautela, adattatori configurati. Se installi una skill nuova e l'agente la usa male, è qui che vai a scrivere "quando usi `gog`, l'account di default è X, l'account di lavoro è Y, non confonderli mai".

**HEARTBEAT.md — la checklist del battito.** Se il file esiste, l'agente lo legge ad ogni heartbeat (di default ogni 30 minuti). È una *checklist piccola, stabile, sicura*: cosa controllare a intervalli regolari ("guarda se ci sono nuove email entro X criteri", "controlla che i cron di stamattina siano andati a buon fine", "verifica se è ora di mandare il digest"). Il consiglio operativo è di tenerla cortissima: tutto ciò che metti qui pesa sul costo di ogni battito, e i battiti sono molti in una giornata. Un esempio minimo che funziona bene nel primo mese:

```markdown
# Heartbeat checklist for Polly

Run silently every 30 minutes.
Reply "HEARTBEAT_OK" if nothing actionable.

1. Inbox: any emails from priority senders
   (see USER.md → priority_list)?
   If yes, summarize in one line and ping me on Telegram.
2. Calendar: is there a meeting starting in <30 min?
   If yes, run the "meeting-prep" skill and deliver
   the brief to Telegram.
3. Cron: did this morning's digest run successfully?
   If a cron failed, write a one-line report and ping me.
4. Otherwise: HEARTBEAT_OK.
```

Quando il battito scatta, l'agente legge questa checklist e — se nessuno dei criteri è scattato — risponde `HEARTBEAT_OK`, che il Gateway scarta in silenzio. Se invece c'è materia, agisce e ti scrive sul canale configurato. È la macchina che produce la sensazione, descritta nel Cap. 1, di "essere svegliato dall'agente al momento giusto".

**BOOTSTRAP.md — il rito del primo avvio.** Vive solo per pochi minuti. Al primo avvio dell'agente, OpenClaw scrive un BOOTSTRAP.md che guida una conversazione di onboarding (chi sei, come ti chiami, in che fuso orario sei, che canale preferisci…); le risposte vengono propagate in `IDENTITY.md`, `USER.md`, `SOUL.md`. Quando il rito è finito, OpenClaw cancella `BOOTSTRAP.md`. Se lo trovi ancora lì dopo settimane, vuol dire che il bootstrap non è andato a buon fine — vai al Cap. 7 a riavviarlo. Il rito ha anche due tetti da conoscere: i file di bootstrap vengono caricati fino a 150.000 caratteri complessivi, e nessun singolo file dovrebbe superare i 20.000.

**MEMORY.md — la memoria di lungo periodo.** Fatti durevoli, decisioni prese, preferenze emerse, vincoli che hai dichiarato in conversazione. È qui che l'agente accumula nel tempo ciò che USER.md non aveva previsto. La regola d'oro è semplice: **USER.md è ciò che tu metti deliberatamente; MEMORY.md è ciò che l'agente impara da solo**. Tenerli separati ti fa risparmiare ore di debug.

**(i) Pro tip:** la "regola degli 8 file" non è una formalità burocratica. Se scrivi una preferenza importante in un file con un nome diverso (per esempio `PREFERENCES.md` o `CONTEXT.md`), l'agente *non lo leggerà* a meno che una delle skill o un'istruzione esplicita in `AGENTS.md` glielo faccia caricare. È la causa numero uno dei "ma te l'avevo detto!" della prima settimana.

### Memoria: quattro strati che falliscono in modi diversi

OpenClaw non ha "una" memoria. Ne ha quattro, e capirne la geografia è ciò che fa la differenza fra un agente che dimentica tutto e uno che ricorda solo ciò che serve.

Il **primo strato** sono i **bootstrap files** appena descritti: caricati ad ogni inizio di sessione, danno all'agente la sua identità di base. Pesano in token, ma sono la spina dorsale: l'agente *deve* leggerli per essere sé stesso.

Il **secondo strato** è la **MEMORY.md**, che è l'archivio durevole dei fatti che vuoi sopravvivano alla singola conversazione. Caricata anche lei ad ogni inizio sessione DM (direct message: la chat 1:1 con te), è il posto giusto dove mettere "il mio chirurgo si chiama Y", "il prossimo viaggio è a Tokyo a luglio", "non chiamare mai mia madre prima delle 10".

Il **terzo strato** sono le **note giornaliere**, file in `memory/YYYY-MM-DD.md` con il contesto vivo della giornata: cosa è successo, cosa è in corso, cosa è da rifare. OpenClaw carica automaticamente la nota di oggi e quella di ieri, così l'agente ha una "finestra di lavoro" che copre il presente senza pesare sul contesto con un mese di storia. Questi file sono il tuo punto di osservazione preferito quando vuoi capire perché l'agente si è comportato in un certo modo: spesso la risposta è scritta lì.

Il **quarto strato** è l'**indice semantico** opzionale: un piccolo vettoriale costruito su MEMORY.md e sui file in `memory/`, che permette all'agente di trovare fatti rilevanti anche quando le parole della richiesta non coincidono con quelle scritte nei file. Non è obbligatorio, ma sui setup maturi diventa utile presto.

Quando l'agente "dimentica", la diagnosi parte da capire **quale strato ha fallito**. Se ha dimenticato il tuo nome, il problema è in USER.md o nei bootstrap files. Se ha dimenticato cosa avevate deciso ieri, è la nota giornaliera che non è stata letta o scritta. Se ha dimenticato un fatto durevole emerso due mesi fa, MEMORY.md non l'ha mai registrato. La distinzione è la base del Cap. 15.

**(!) Attenzione:** quando una sessione si avvicina al limite di contesto, OpenClaw esegue un *turno silenzioso* (con flag `NO_REPLY`, niente arriva al tuo canale) per ricordare al modello di salvare in memoria ciò che è importante prima della compattazione automatica. Se vedi nei log un'attività dell'agente che non corrisponde a nessun tuo messaggio, prima di allarmarti controlla se è quello.

### Heartbeat e cron: il cuore e l'agenda

Sono i due meccanismi temporali di OpenClaw, e si scambiano spesso a parole. Distinguerli è facile se tieni a mente che fanno cose diverse.

L'**heartbeat** è un battito *ricorrente di sistema*: di default ogni 30 minuti, l'agente si sveglia, legge il suo `HEARTBEAT.md`, decide se c'è qualcosa di cui occuparsi e — se non c'è nulla — risponde un laconico `HEARTBEAT_OK` che il Gateway scarta in silenzio. È il meccanismo che permette all'agente di "esistere" anche quando nessuno gli ha scritto: la differenza essenziale rispetto a un chatbot. L'heartbeat gira nella sessione `main` dell'agente per default, ma può essere configurato in modo *isolato* (`sessionTarget: "isolated"`), così ogni battito parte da zero senza la storia conversazionale precedente. Nei setup maturi questa è una scelta di costo importante: un battito isolato vale una frazione di un battito ricco di contesto.

Il **cron** è invece un *appuntamento programmato esplicitamente*: "ogni mattina alle 7:00 mandami il digest", "ogni venerdì alle 17:00 prepara il report", "fra venti minuti ricordami la chiamata". È il Gateway a tenere traccia dei cron, a far svegliare l'agente all'orario giusto, e — se serve — a consegnare l'output su un canale specifico. Una particolarità potente: i cron possono creare altri cron. È il modo con cui un agente "impara la tua agenda", come vedremo nel Cap. 18.

La regola pratica per non confondersi: l'heartbeat è il *cuore*, il cron è l'*agenda*. Se vuoi qualcosa "ogni tanto, in modo opportunistico", sta nell'heartbeat; se vuoi qualcosa "a un orario preciso", sta nel cron. Si possono pestare i piedi a vicenda — se la coda principale, la lane di sessione, la lane cron o un cron attivo sono occupati, l'heartbeat viene saltato e ritentato dopo: è un'eccezione gestita, non un errore — ma è raro che vada storto.

### Sessioni: una geometria di isolamento

Una **sessione**, in OpenClaw, è il contenitore in cui vive una conversazione: storia, stato, costi, modello in uso, livello di "thinking", parametri di attivazione. La domanda interessante non è "cosa c'è in una sessione" (le sessioni sono semplici), ma "*quante* sessioni esistono e *come* sono separate fra loro".

La risposta dipende dal **session scope**, configurabile a livello di Gateway o di agente. Quattro opzioni in pratica:

- **`main`** — una sessione globale per tutti i DM. Tutto ciò che ti scrivono confluisce nella stessa storia, indipendentemente dalla persona o dal canale. Comodo per uso strettamente personale; pericoloso se l'agente parla con più persone.
- **`per-peer`** — una sessione per ogni mittente, indipendentemente dal canale. Se ti scrivo da Telegram e poi da WhatsApp, finiamo nella stessa sessione.
- **`per-channel-peer`** — una sessione per ogni mittente *su ogni canale*. È il default consigliato. Se ti scrivo da Telegram, parliamo lì; se ti scrivo da WhatsApp, è un'altra storia. La personalità dell'agente è la stessa (SOUL.md è uno solo), ma le conversazioni non si contaminano.
- **`per-account-channel-peer`** — aggiunge un livello extra di isolamento per account, utile per chi gestisce più tenant o più clienti dallo stesso Gateway.

A questa geometria si sovrappone l'isolamento dei **gruppi**: una conversazione di gruppo su Slack, Discord o Telegram è un'altra sessione ancora, separata dai DM. Nei gruppi entrano in gioco tre regolatori che vale la pena conoscere:

**Mention gating.** L'agente parte solo quando viene menzionato (`@nome`) o quando rispondi direttamente a un suo messaggio. Senza mention gating, l'agente leggerebbe tutto il rumore del canale e — peggio — cercherebbe di rispondere a tutto.

**Reply tags.** Le risposte dell'agente nei gruppi includono tag che permettono di legare correttamente i thread, in modo che lui stesso sappia "a chi" sta rispondendo quando le conversazioni si intrecciano.

**Per-channel chunking.** Ogni canale ha limiti diversi sulla lunghezza dei messaggi (Telegram, Slack, WhatsApp non sono uguali). OpenClaw spezza la risposta in chunk rispettando questi limiti, e — fatto cruciale — *non spezza mai un blocco di codice*: quando un fenced code block è troppo lungo, lo chiude e lo riapre attraverso il taglio per non rompere il rendering Markdown.

Esiste anche un meccanismo di **history buffer** per i messaggi *pending-only*: i messaggi di gruppo che non hanno fatto scattare un run (ad esempio perché non sono stati menzionati) vengono comunque tenuti in un buffer, così se più tardi il contesto serve l'agente lo recupera senza scartare nulla.

### Queue modes: cosa succede se mentre lavora ne arrivano altri

Quando stai parlando con il tuo agente e gli arrivano messaggi mentre lui sta ancora pensando, il comportamento dipende dal **queue mode**. Le modalità principali — `interrupt`, `steer`, `followup`, `collect`, più le varianti `backlog` — corrispondono a tre filosofie:

- **`interrupt`** — il nuovo messaggio interrompe il run in corso, l'agente smette di pensare al precedente e ricomincia dal nuovo. È la modalità giusta quando vuoi cambiare idea velocemente.
- **`steer`** — il nuovo messaggio modifica il run in corso senza interromperlo: l'agente "ricalibra" tenendo conto di entrambi.
- **`followup`** — il nuovo messaggio aspetta che il precedente finisca, e poi parte come turno successivo. È la modalità più conservativa.
- **`collect`** — i nuovi messaggi si accumulano in un buffer e vengono trattati insieme appena il run corrente termina.

Per la maggior parte dei lettori del libro, il default `followup` o `collect` è quello giusto: evita di tagliare a metà ragionamenti complessi e mantiene un'esperienza prevedibile. Il Cap. 15 entra nei dettagli di come scegliere il modo per i casi limite (per esempio, gli agenti che gestiscono allarmi in tempo reale preferiscono `interrupt`).

Per fissare i termini inglesi di queste due sezioni:

| Termine | In parole semplici |
|---|---|
| session scope | quante sessioni, e come separate |
| peer | il singolo interlocutore |
| mention gating | parte solo se menzionato |
| reply tag | etichetta che lega i thread |
| chunking | risposta spezzata per il canale |
| queue mode | gestione dei messaggi in arrivo |

### Il ciclo di vita di un task

Ricomponendo i pezzi, il viaggio di una richiesta — dal momento in cui scrivi al tuo agente al momento in cui leggi la risposta — segue **otto stadi**.

1. **Inbound al canale.** Il messaggio arriva su Telegram, WhatsApp, Slack, ecc. Il plugin del canale traduce il payload nativo in un evento standard di OpenClaw.
2. **Routing al Gateway.** Il Gateway riceve l'evento, applica le regole di binding (quale agente serve quale canale) e seleziona l'agente.
3. **Risoluzione della sessione.** In base al session scope si trova (o si crea) la sessione corretta: main, per-peer, per-channel-peer, gruppo. Le sessioni di gruppo applicano mention gating e reply tags.
4. **Assemblaggio del contesto.** Si caricano i bootstrap files (SOUL, AGENTS, USER, TOOLS, IDENTITY, HEARTBEAT se rilevante), MEMORY.md, le note di oggi e ieri, eventualmente l'indice semantico.
5. **Ragionamento dell'LLM.** Il modello configurato per l'agente (Claude, GPT, Gemini, Nemotron, locale) elabora la richiesta e decide cosa fare: rispondere direttamente, chiamare una skill, eseguire un tool, fare una ricerca web, scrivere su disco, programmare un cron.
6. **Esecuzione delle azioni.** Le skill vengono invocate, i tool eseguiti, i comandi shell lanciati. Ogni esecuzione ha i suoi log, le sue uscite, il suo costo.
7. **Outbound al canale.** Il risultato torna al Gateway, viene chunkato secondo i limiti del canale, e consegnato. Se il run è scattato da cron, il `delivery channel` configurato decide dove arriva.
8. **Aggiornamento della memoria.** A fine turno, e con maggior intensità verso la fine della finestra di contesto, l'agente scrive ciò che merita di sopravvivere in MEMORY.md o nella nota giornaliera.

Questo ciclo è quello che, ripetuto migliaia di volte al giorno fra heartbeat, cron e messaggi reali, costruisce la sensazione di "avere un dipendente". Ognuno degli otto stadi è ispezionabile (`openclaw status`, log del Gateway, file della memoria), e ognuno è un punto di intervento quando qualcosa non va.

#### Un esempio concreto: "Polly, prepara il brief per le 14:30"

Per ancorare gli otto stadi a qualcosa di tangibile, segui un singolo messaggio dall'inizio alla fine. Sono le 13:48. Apri Telegram e scrivi al tuo agente Polly: *"Prepara un brief sul cliente Rossi per la chiamata delle 14:30, due paragrafi."*

**Stadio 1 — Inbound al canale.** Il bot grammY collegato al tuo Telegram riceve il messaggio in pochi millisecondi e lo trasforma in un evento standard `MessageReceived` con metadati (chat_id, user_id, timestamp, testo).

**Stadio 2 — Routing al Gateway.** L'evento arriva al Gateway sul control plane WebSocket. Il binding di config dice che la chat 1:1 con il tuo user_id è instradata all'agente `polly`.

**Stadio 3 — Risoluzione della sessione.** Lo `session.scope` è `per-channel-peer`. Il Gateway cerca la sessione `(telegram, tuo_id, polly)`: esiste, ha 14 turni di storia. La riprende.

**Stadio 4 — Assemblaggio del contesto.** Polly carica `SOUL.md`, `AGENTS.md`, `IDENTITY.md`, `USER.md`, `TOOLS.md`, `HEARTBEAT.md` (perché c'è), `MEMORY.md`. Carica `memory/2026-05-06.md` (ieri) e `memory/2026-05-07.md` (oggi). In `MEMORY.md` trova: "Cliente Rossi — pricing in revisione, da non menzionare in pubblico". Tiene nota.

**Stadio 5 — Ragionamento dell'LLM.** Il modello configurato (Claude Sonnet 4.6) decide il piano: cercare il contatto Rossi nel CRM, leggere l'ultimo scambio email, leggere l'ultimo post LinkedIn pubblicato, ricomporre due paragrafi. Il piano richiede di chiamare due skill: `crm-lookup` e `linkedin-recent`.

**Stadio 6 — Esecuzione delle azioni.** Polly invoca `crm-lookup{cliente: "Rossi"}` (~1.2s). Poi `linkedin-recent{handle: "rossi-mario"}` (~2.8s). Poi compone il brief, evitando di toccare il pricing per via della nota in `MEMORY.md`.

**Stadio 7 — Outbound al canale.** La risposta è di 187 parole, ben sotto il limite di Telegram. Polly la chunka in due messaggi separati per leggibilità (un paragrafo ciascuno) e li consegna alla chat `telegram://<tuo_id>`.

**Stadio 8 — Aggiornamento della memoria.** Polly scrive nella nota di oggi: *"13:50 — preparato brief Rossi per 14:30; pricing volutamente omesso (vedi MEMORY.md)"*. La nota è disponibile alla prossima sessione, e per il prossimo heartbeat che la legga fra le note di "ieri" domani mattina.

Tempo totale dall'invio alla risposta: ~6 secondi. Token spesi: ~3.500 in input (bootstrap + storia) + ~250 in output. Costo stimato sul tuo provider: dell'ordine del centesimo. Il Cap. 14 trasforma questa contabilità in regole di budget esplicite.

### Canali: dove vive la conversazione

I **canali** sono i mezzi attraverso cui parli all'agente. Ne esistono ad oggi più di venti, ognuno con un plug-in dedicato e un protocollo proprio. Senza pretendere di essere esaustivi, vale la pena vederne i sette principali con un consiglio d'uso.

**Telegram (grammY).** Il canale consigliato per iniziare. Setup veloce con `@BotFather`, supporto a immagini, file, voce, gruppi, messaggi formattati. È quello che useremo come base nel Cap. 6.

**WhatsApp (Baileys).** Il più "naturale" per uso personale e familiare. La libreria Baileys parla il protocollo non ufficiale di WhatsApp Web; richiede di tenere il telefono online e di scansionare un QR. Funziona bene ma è il canale più sensibile a cambi lato Meta.

**Slack (Bolt) e Discord (discord.js).** I canali da team. Slack per uso lavorativo "office", Discord per community e team più informali. Entrambi gestiscono bene gruppi, mention gating e thread.

**Signal (signal-cli) e iMessage (plugin nativo).** I canali per chi vuole privacy (Signal) o per chi vive nell'ecosistema Apple (iMessage). Dal 2026 il plugin nativo iMessage è il default; il vecchio ponte BlueBubbles è deprecato.

**Microsoft Teams, Matrix, Google Chat, Feishu, LINE, IRC, Mattermost, Nextcloud Talk, Nostr, Synology Chat, Tlon, Twitch, Zalo, WeChat, QQ, WebChat.** L'arcipelago lungo, utile in casi specifici. WeChat e QQ sono particolarmente importanti per chi opera in Cina; Matrix per chi vuole un canale federato; Nostr per chi vive nell'ecosistema crittografico decentralizzato.

**TUI (Terminal UI).** Non è un canale "di rete", ma è la prima interfaccia che vedi appena finita l'installazione: una shell interattiva da cui puoi parlare all'agente direttamente sul terminale. Utile per il primo "hatch" e per il debug.

**WebChat.** Una pagina web minimale che il Gateway può servire localmente (o dietro un tunnel come Tailscale). Comodo per quando sei al computer e non vuoi cambiare app.

La regola di scelta è banale: il canale giusto è *quello che già usi tutto il giorno*. Non costringerti a installare una nuova app per parlare al tuo agente. Telegram come "canale di onboarding" è il consiglio del libro perché ha l'attrito più basso; ma niente impedisce di passare a WhatsApp dopo una settimana se ti stai più comodo lì.

### Tool, skill, MCP: cosa sa fare l'agente

Le **skill** sono cartelle, ognuna con un `SKILL.md` dentro che descrive cosa fa, quando usarla e come eseguirla. Il formato deriva dagli "AgentSkills" di Anthropic: YAML frontmatter (nome, descrizione, parole chiave) seguito da istruzioni in Markdown e — se serve — script ausiliari. Quando l'agente decide che un compito richiede una skill, la "scopre" leggendone il SKILL.md, la esegue e integra l'output nel suo ragionamento.

Le skill si installano da **ClawHub**, il registry pubblico, oppure da un repo Git arbitrario. Il comando classico è `openclaw skills install <nome-o-url>`: la CLI scarica il pacchetto, valida il manifest, lo registra nel workspace dell'agente. Da quel momento la skill è disponibile e l'agente può scegliere di usarla quando opportuno.

Accanto alle skill esistono i **tool nativi** del Gateway (filesystem, shell, web search di base, calendario interno) e i **server MCP** (Model Context Protocol) che permettono di esporre all'agente API e dati di sistemi esterni in modo standardizzato. Per il livello base di questo capitolo basta sapere che esistono tre porte di ingresso — skill, tool nativi, MCP — e che TOOLS.md è il posto giusto dove dire all'agente come usarle bene.

**(!) Attenzione:** Skill di terze parti significa codice di terze parti. La storia di **ClawHavoc** raccolta nel Cap. 13 — skill malevole sfuggite alla revisione e arrivate a workspace ignari — non è uno spauracchio: è successo davvero. Quando installi una skill, leggi il SKILL.md, controlla il repo, e — ai primi tempi — preferisci skill mantenute dalla community ufficiale o da autori riconoscibili.

### Un agente o molti? L'idea del "team"

OpenClaw è pensato per il **multi-agente**: nulla impedisce di avere su un solo Gateway una assistente personale (Polly), un agente "famiglia" (Finn), un agente di marketing (Max). Ognuno con SOUL, IDENTITY, MEMORY e cron diversi. Le sessioni e i workspace sono isolati, il routing dei canali decide chi risponde a chi.

I Capitoli 10–12 sono dedicati a questo, ma è utile saperlo già da subito: l'unità minima di OpenClaw è *l'agente*, non *il sistema*. Se ti accorgi che il tuo agente fa "troppe cose" (gestisce posta, codice, casa, finanze, bambini), il problema non è che è poco capace — è che ha un mansionario sovraccarico. La risposta è quasi sempre **specializzare**: dividere il lavoro fra più agenti, ognuno con un SOUL.md mirato.

### Come ispezionare l'agente: i comandi che userai sempre

Ogni concetto descritto in questo capitolo ha un comando di ispezione corrispondente. Non serve impararli a memoria oggi, ma vale la pena vederli tutti insieme almeno una volta: la prima diagnosi di "perché non funziona?" passa quasi sempre da uno di questi.

```bash
# === Salute generale del Gateway e dei canali ===

# gateway up? canali connessi?
openclaw status

# dettaglio per canale (telegram, whatsapp, …)
openclaw channels status


# === Inventario degli agenti ===

# quali agenti esistono e su quale workspace puntano
openclaw agents list

# config risolta dell'agente "polly"
openclaw agents show polly


# === Sessioni in corso ===

# tutte le sessioni attive
openclaw sessions list

# storia, modello, costi, stato di una sessione
openclaw sessions show <session-id>


# === Skill installate ===

# nome, versione, fonte di ogni skill
openclaw skills list

# cosa fa una skill, quando si attiva, quali comandi espone
openclaw skills show <nome>


# === Cron e heartbeat ===

# job programmati e prossima esecuzione
openclaw cron list

# ultimo battito, prossimo, modalità di sessione
openclaw heartbeat status


# === Workspace sul disco (utile anche solo con ls) ===

# i file canonici e la cartella memory/
ls -la ~/.openclaw/workspace-polly/

# ispezionare un file di identità
cat ~/.openclaw/workspace-polly/IDENTITY.md

# storia delle modifiche, se sotto Git
git -C ~/.openclaw/workspace-polly/ log --oneline -10
```

Il pattern è sempre lo stesso: dalla salute del sistema (`status`) si scende verso il pezzo specifico (canale, agente, sessione, skill, cron) e poi al file su disco. Il Cap. 15 espande questa griglia in un vero e proprio runbook diagnostico.

**(#) Debug:** se l'agente "non capisce" una preferenza che tu sei sicuro di aver dato, esegui questa sequenza prima di qualsiasi altra cosa: (1) `cat USER.md` e cerca la preferenza letterale; (2) `grep -r "parola-chiave" ~/.openclaw/workspace-polly/` per vedere se è finita in un file diverso da quelli canonici; (3) `openclaw sessions show <session-id>` per controllare quali bootstrap files sono stati effettivamente caricati nell'ultimo turno. Nove volte su dieci il problema è alla riga 2: la preferenza esiste, ma è in un file con un nome che OpenClaw non legge.

**Prompt pronto:**
> "Apri il tuo workspace. Elenca i file presenti nella radice e dimmi, per ognuno, se è uno degli otto file canonici di OpenClaw e che ruolo gioca. Segnala se manca qualcuno dei canonici e se ce ne sono di non canonici che vorresti che spostassi o caricassi a mano."

**Prompt pronto:**
> "Fammi un riassunto di chi sei in tre paragrafi: il primo dal tuo SOUL.md, il secondo dal tuo IDENTITY.md, il terzo da ciò che sai di me leggendo USER.md e MEMORY.md. Indicami una cosa sbagliata o obsoleta che hai trovato."

**(i) Pro tip:** un esercizio molto utile della prima settimana è chiedere all'agente di **leggersi** ad alta voce. Lo costringe a riassumere SOUL/IDENTITY/USER/MEMORY in linguaggio naturale, e tu ne approfitti per individuare contraddizioni, regole stantie, preferenze invecchiate. È la forma più semplice di manutenzione preventiva.

## Errori comuni e come risolverli

| Sintomo | Causa probabile | Fix |
|---------|-----------------|-----|
| L'agente "dimentica" cose importanti | Le note finiscono in conversazione, non vengono salvate sui file di identità o di memoria | Chiedi esplicitamente "salva questo in USER.md" o "aggiungi questa regola al SOUL.md"; verifica che il file sia stato modificato. |
| L'agente non risponde a un messaggio recente | Heartbeat non ancora scattato (default ~30 min), Gateway giù, o canale disconnesso | `openclaw status` per il Gateway, `openclaw channels status` per i canali. Se il problema è il canale, riavvia quello, non tutto. |
| Confondere SOUL.md, AGENTS.md e IDENTITY.md | Nomi simili, ruoli sovrapponibili | SOUL = personalità e confini (chi è). AGENTS = istruzioni operative (come lavora). IDENTITY = biglietto da visita (nome, emoji, vibe). |
| Il BOOTSTRAP.md è ancora lì dopo settimane | Il rito di bootstrap non è andato a buon fine al primo avvio | Vai al Cap. 7: la procedura prevede di rispondere alle domande dentro la TUI fino a quando il file viene cancellato automaticamente. |
| L'agente ha "regole" che non ricordi di aver scritto | Skill installata che ha modificato AGENTS.md o ha aggiunto istruzioni ai bootstrap files | Apri AGENTS.md e cerca i blocchi aggiunti dalle skill (di solito hanno marker tipo `<!-- skill:nome -->`). Rimuovi ciò che non vuoi e disinstalla la skill se necessario. |
| Risposte estremamente lente o costose | HEARTBEAT.md troppo lungo, oppure note giornaliere enormi caricate ad ogni turno | Tieni HEARTBEAT.md sotto le 20 righe; archivia note vecchie con un cron settimanale di "compaction" (vedi Cap. 18). |
| Conversazioni di gruppo che esplodono | Mention gating disattivato | Riattiva `mention_gating: true` per il canale di gruppo o aggiungi reply tags più stringenti. |
| Una sessione "vede" cose di un'altra sessione | Session scope su `main` o `per-peer` quando volevi `per-channel-peer` | Cambia `session.scope` nella config del Gateway o dell'agente, riavvia, verifica con `openclaw sessions list`. |

## Checklist di fine capitolo

- [ ] So elencare gli **otto file** che OpenClaw legge all'avvio e cosa fa ciascuno
- [ ] So distinguere **SOUL.md** (personalità) da **AGENTS.md** (operatività) da **IDENTITY.md** (biglietto da visita)
- [ ] Conosco i **quattro strati di memoria** (bootstrap files, MEMORY.md, note giornaliere, indice semantico)
- [ ] So distinguere **heartbeat** (battito ricorrente, ~30 min) da **cron** (appuntamento programmato)
- [ ] Ho chiari gli **otto stadi del ciclo di vita di un task** (inbound → routing → sessione → contesto → ragionamento → esecuzione → outbound → memoria)
- [ ] Conosco i **session scope** (main, per-peer, per-channel-peer, per-account-channel-peer) e quale è il default consigliato
- [ ] So cosa sono **mention gating**, **reply tags** e **chunking per canale** nei gruppi
- [ ] Conosco le **quattro queue mode** (interrupt, steer, followup, collect) e quando ciascuna è appropriata
- [ ] So che **Gateway** è uno per macchina, **agenti** sono molti, **workspace** è una cartella di file ispezionabili
- [ ] Saprei descrivere a voce un albero tipico di workspace dopo una settimana di uso
- [ ] Conosco i comandi di ispezione di base (`openclaw status`, `openclaw sessions list`, `openclaw cron list`) e cosa restituiscono
- [ ] Ho capito perché **mettere il workspace sotto Git** è la prima cosa utile da fare nella prima settimana

## Link e risorse utili

- [Documentazione ufficiale](https://docs.openclaw.ai) — riferimento canonico per file di workspace, gateway, sessioni e memoria
- [Heartbeat — OpenClaw Docs](https://docs.openclaw.ai/gateway/heartbeat) — meccanica esatta del battito, isolamento di sessione, soglie
- [Agent bootstrapping — OpenClaw Docs](https://docs.openclaw.ai/start/bootstrapping) — il primo avvio, la creazione dei file canonici, la cancellazione di BOOTSTRAP.md
- [Architecture overview](https://github.com/openclaw/openclaw/blob/main/docs/concepts/architecture.md) — panoramica dei moduli (Gateway, agenti, skill, sessioni)
- [Memory concepts](https://github.com/openclaw/openclaw/blob/main/docs/concepts/memory.md) — i quattro strati di memoria spiegati nel codice
- [Messages and queue modes](https://docs.openclaw.ai/concepts/messages) — `interrupt` / `steer` / `followup` / `collect` e i loro effetti
- [OpenClaw Workspace Files Explained](https://capodieci.medium.com/ai-agents-003-openclaw-workspace-files-explained-soul-md-agents-md-heartbeat-md-and-more-5bdfbee4827a) — Roberto Capodieci, Marzo 2026, panoramica didattica degli otto file
- [SOUL.md & Identity — Designing Your Agent's Personality](https://learnopenclaw.com/core-concepts/soul-md) — guida pratica alla scrittura di SOUL.md
- [OpenClaw Memory Masterclass](https://velvetshark.com/openclaw-memory-masterclass) — VelvetShark, deep-dive sulla memoria che sopravvive
- [Architecting the Agentic Future: OpenClaw vs NanoClaw vs NemoClaw](https://dev.to/mechcloud_academy/architecting-the-agentic-future-openclaw-vs-nanoclaw-vs-nvidias-nemoclaw-9f8) — confronto architetturale fra le tre famiglie
- [Repository GitHub](https://github.com/openclaw/openclaw) — codice sorgente per chi vuole guardare sotto il cofano

Per l'elenco completo delle fonti del libro, vedi [Appendice E](../Appendici/E-risorse-e-link-utili.md).

---

[← Capitolo 1](./01-cos-e-openclaw-e-perche-e-importante.md)  ·  [Indice](../README.md)  ·  [Capitolo 3 →](../PARTE-II-Installazione/03-scegliere-dove-installare-openclaw.md)
