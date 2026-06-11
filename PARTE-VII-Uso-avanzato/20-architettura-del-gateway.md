# Capitolo 20 — L'architettura del Gateway [★★★]

## Cosa imparerai

- Il modello mentale del Gateway come *air traffic controller* e i cinque input vector dell'autonomia
- Il WebSocket control plane (`ws://127.0.0.1:18789`) e il modello di sessione visto dal Gateway
- La media pipeline (immagini, audio, video) e il Pi agent runtime (RPC, tool e block streaming)
- Le companion app: macOS, iOS/Android, Windows
- Live Canvas, A2UI e Lobster — il workflow shell, da non confondere con la mascotte

## Prerequisiti

Aver letto [Capitolo 2](../PARTE-I-Capire-OpenClaw/02-anatomia-di-un-agente-openclaw.md) e installato OpenClaw ([Capitolo 5](../PARTE-II-Installazione/05-installazione-step-by-step.md)). Conoscenza base di WebSocket e architetture client-server è utile ma non strettamente necessaria.

## Contenuto principale

### Il Gateway come kernel: il modello dell'air traffic controller

Per diciannove capitoli hai usato OpenClaw come si usa un'automobile: volante, pedali, cruscotto. Questo capitolo apre il cofano. E dentro non c'è "un programma che chatta": c'è un piccolo sistema operativo per agenti, e il suo kernel si chiama **Gateway**.

Il modello mentale più usato nella community è quello dell'**air traffic controller**, il controllore di volo. Gli aerei (i messaggi) arrivano da rotte diverse (i canali), ognuno deve atterrare sulla pista giusta (la sessione), nell'ordine giusto (la coda), e nessun pilota parla con un altro pilota — tutti parlano con la torre. Il Gateway è la torre: riceve ogni evento, decide chi se ne occupa, in quale sessione, con quale priorità, e dove va consegnata la risposta. Niente lo bypassa: non i messaggi Telegram, non l'heartbeat, non i cron, non le companion app. Quando nel Cap. 2 abbiamo detto che "senza Gateway acceso non c'è OpenClaw", era questa l'affermazione architetturale: i workspace sono lo *stato*, il Gateway è il *processo*.

Tecnicamente, il Gateway espone un **control plane** — il piano di controllo: l'interfaccia attraverso cui ogni componente del sistema riceve ordini e riporta eventi — come WebSocket locale su `ws://127.0.0.1:18789`. Sulla stessa porta, via HTTP, vivono anche la Control UI e il WebChat del Cap. 5: dashboard e control plane sono due facce dello stesso processo. La scelta di WebSocket non è estetica: a differenza di una API REST, la connessione è *bidirezionale e persistente*. Né il plugin Telegram né la companion app devono fare polling chiedendo ogni dieci secondi "ci sono novità?": tengono aperta una connessione e il Gateway *spinge* gli eventi quando accadono. È il motivo per cui una risposta dell'agente compare sul telefono nello stesso istante in cui compare nei log.

```yaml
# ~/.openclaw/config.yaml (excerpt)
gateway:
  host: 127.0.0.1   # loopback only, never 0.0.0.0
  port: 18789
```

L'autenticazione sul control plane passa dal token in `~/.openclaw/auth.token`: ogni client — plugin di canale, companion app, TUI — si presenta con quel token alla connessione. Tienilo a mente: tornerà nel case study di fine capitolo.

C'è una seconda decisione architetturale che il Cap. 2 aveva promesso di spiegare: **niente database, solo file**. Il Gateway non ha un PostgreSQL nascosto né un servizio cloud che tiene stato. Le sessioni sono file di trascrizione in `~/.openclaw/sessions/`, la configurazione è `config.yaml`, le credenziali stanno in `credentials/`, i log in `logs/`, e tutto ciò che l'agente sa vive nel suo workspace. Le conseguenze pratiche sono enormi: il backup è `tar` di una cartella, il debug è `less` su un file, la migrazione su un VPS è `rsync`. È una scelta che sacrifica eleganza da ingegneria enterprise in cambio di una proprietà che per un software *che vive a casa tua* vale di più: l'ispezionabilità totale.

**(i) Pro tip:** il modo più rapido per "vedere" il control plane al lavoro è tenere aperto `openclaw logs --follow` mentre scrivi al tuo agente da Telegram: evento inbound, risoluzione della sessione, chiamate ai tool e outbound scorrono in tempo reale. Dieci minuti di questo esercizio valgono più di qualunque diagramma.

### I cinque input vector dell'autonomia

Se il Gateway è la torre di controllo, da quante rotte arrivano gli aerei? Cinque. La community li chiama gli **input vector dell'autonomia**: i cinque modi in cui un run dell'agente può cominciare — e solo uno richiede che tu stia facendo qualcosa.

| Vector | Chi lo origina |
|---|---|
| 1. Messaggi dai canali | tu, o chi può scriverti |
| 2. Heartbeat | il sistema, ogni 30 minuti |
| 3. Cron | l'agenda programmata |
| 4. Hook ed eventi | sistemi esterni (webhook) |
| 5. Agenti e nodes | il team e i tuoi device |

Il **primo vector** sono i messaggi dai canali: l'unico vector "umano in tempo reale", quello che un chatbot tradizionale possiede in esclusiva. Il **secondo** è l'heartbeat: il battito che ogni 30 minuti (default) sveglia l'agente e gli fa leggere `HEARTBEAT.md`. Il **terzo** sono i cron: appuntamenti espliciti, gestiti dal Gateway, che fanno partire un run a un orario preciso. Il **quarto** sono gli hook e gli eventi esterni: un webhook che scatta quando arriva un'email, un evento di sistema, una richiesta da un'integrazione — il mondo che bussa alla porta senza passare da una chat. Il **quinto** sono gli altri agenti e i nodes: un messaggio `sessions_send` da un collega di team (Cap. 12) o un evento da una companion app — la fotocamera del telefono, il comando vocale dalla menu bar.

Perché contare i vector è utile? Perché l'autonomia di un agente — quella sensazione, descritta nel Cap. 1, che "il lavoro succede da solo" — è esattamente la somma dei vector 2–5. Un assistente che reagisce solo al vector 1 è un chatbot; un agente con heartbeat ma senza cron sa accorgersi delle cose ma non sa darsi appuntamenti; un agente senza hook vive isolato dagli eventi del mondo. E, in direzione opposta: ogni vector è una porta d'ingresso, e ogni porta d'ingresso è superficie d'attacco — l'inventario dei rischi del Cap. 13 era, senza chiamarlo così, l'inventario dei cinque vector. Il Gateway li serializza tutti nello stesso punto: qualunque cosa entri, da qualunque rotta, diventa un evento sul control plane e si mette in coda nella sessione giusta. È questa serializzazione che rende il sistema osservabile: *un solo posto da guardare*.

### Sessioni: la geometria vista dal Gateway

Il Cap. 2 ha introdotto le sessioni dal punto di vista dell'agente; qui le guardiamo dal punto di vista di chi le crea e le smista. Per il Gateway, una sessione è una *lane*: una corsia con la sua storia, il suo stato, i suoi costi e la sua coda. La domanda a cui il Gateway risponde decine di volte al giorno — "questo evento, in quale lane va?" — dipende dal **session scope**, e i quattro valori possibili meritano uno scenario ciascuno.

**`main`** — una sola sessione globale per tutti i messaggi diretti. Scenario: sei l'unico essere umano che parla con l'agente. Tutto confluisce in un'unica storia continua, l'agente "si ricorda tutto" senza configurare nulla. Comodissimo finché è vero il presupposto: il giorno in cui tua moglie scrive all'agente dal suo Telegram, la sua conversazione e la tua si mescolano nella stessa memoria di lavoro. Per uso strettamente personale va bene; per tutto il resto no.

**`per-peer`** — una sessione per ogni interlocutore, su qualunque canale. Scenario: scrivi all'agente da Telegram la mattina e da WhatsApp la sera, e vuoi che sia *la stessa conversazione*. Il Gateway riconduce le due identità a te (serve la mappa in `USER.md`, vista nel Cap. 6) e usa una sola lane. Il prezzo: se la mappa è sbagliata, due persone diverse possono finire nella stessa sessione.

**`per-channel-peer`** — una sessione per ogni coppia interlocutore+canale. È il **default consigliato**, ed è il motivo per cui nello stadio 3 del ciclo di vita (Cap. 2) la sessione si chiamava `(telegram, tuo_id, polly)`. Scenario: su Telegram fai brainstorming privato, su Slack chiedi cose di lavoro. Le due conversazioni non si contaminano, e un collega che legge le risposte su Slack non riceverà mai un riferimento al brainstorming. La personalità resta una (il SOUL.md è lo stesso); le *storie* sono separate. Se vuoi che convergano, la *session unification* del Cap. 6 (`sessions.unification`) esiste apposta — ma è una scelta esplicita, non il default.

**`per-account-channel-peer`** — aggiunge la dimensione account. Scenario: un consulente gestisce dallo stesso Gateway due bot Telegram, uno per cliente. Lo stesso interlocutore che scrive a entrambi i bot genera due sessioni distinte: i due "tenant" non condividono nulla, nemmeno per errore.

Sopra questa geometria il Gateway applica tre regolatori già incontrati. Primo: l'**isolamento dei gruppi** — ogni gruppo Telegram/Slack/Discord è una lane a sé, mai mescolata con i DM. Secondo: gli **activation mode** — nei gruppi l'agente parte solo se menzionato (`mention`, il default: il mention gating del Cap. 2), sempre (`always`, da usare con grande cautela) o mai (`never`, lane di solo ascolto che alimenta il history buffer senza far partire run). Terzo: i **queue mode** — `interrupt`, `steer`, `followup`, `collect` — che decidono cosa succede quando un messaggio arriva durante un run; la guida alla scelta è nel Cap. 2.

Resta un ultimo concetto, il **reply-back**: la regola per cui l'output di un run torna, di default, al canale da cui è arrivato l'input. Se scrivi da Telegram, la risposta esce su Telegram; nessun cross-posting automatico. E per i run *senza* origine umana — un cron, un heartbeat che ha trovato materia? Lì non esiste un "canale di provenienza", e per questo ogni cron dichiara il suo *delivery channel* (Cap. 18). Una percentuale sorprendente dei "il cron è girato ma non mi è arrivato niente" si riduce a questo: il run è andato a buon fine, ma nessuno aveva detto al Gateway dove consegnare il risultato.

### La media pipeline: cosa succede quando mandi un vocale

Un messaggio di testo è un evento leggero; una foto, un vocale o un video no. Per gestirli il Gateway ha una **media pipeline**: la catena che trasforma un blob binario in qualcosa che un modello linguistico può capire.

Quando mandi un vocale a Polly su Telegram, succede questo. Il plugin del canale scarica il file e lo registra come allegato; il Gateway applica i **size cap** — i limiti dimensionali per tipo di media: un'immagine oltre soglia viene ridimensionata, un file oltre il limite viene rifiutato con un messaggio cortese invece di esplodere a metà pipeline. Poi scatta la **trascrizione automatica**: l'audio passa a un motore speech-to-text — Whisper in locale se installato, altrimenti il provider STT cloud configurato — e il testo entra nel contesto del run *come se lo avessi scritto*, con l'audio originale disponibile come allegato. Per i video la pipeline estrae ciò che il modello sa gestire (la traccia audio da trascrivere e, con i modelli multimodali, i frame); per le immagini verifica se il modello dell'agente ha capacità di visione e, in caso contrario, degrada con grazia descrivendo l'allegato.

L'ultimo anello è il **lifecycle**: dove vivono questi file e per quanto. Gli allegati delle conversazioni finiscono nella cartella `attachments/` del workspace dell'agente — l'hai vista nell'albero del Cap. 2 — mentre i file intermedi della pipeline (l'audio convertito, i frame estratti) sono temporanei e vengono ripuliti. La distinzione conta per la privacy: quel vocale in cui detti il numero della carta resta scritto, trascritto, dentro la sessione e nel workspace. La pipeline è comoda al punto da far dimenticare che *tutto ciò che mandi diventa testo persistente da qualche parte* — il Cap. 13 lo diceva in generale, qui vedi il meccanismo esatto.

**(#) Debug:** se i vocali non vengono trascritti, la diagnosi segue la pipeline nell'ordine: il file è arrivato? (guarda `attachments/`); è sotto il size cap? (guarda i log); il motore STT esiste? (`pip show openai-whisper` o la config del provider). Nove volte su dieci è il terzo anello: l'installazione era nata senza Whisper e nessuno se n'era accorto perché nessuno aveva mai mandato un vocale.

### Il Pi agent runtime: RPC, tool streaming, block streaming

Arriviamo al pezzo che ragiona. Quando il Gateway decide che un evento deve produrre un run, non "chiama una funzione": avvia (o riusa) un processo separato, il **Pi agent runtime**, e gli parla. Pi è il loop agentico vero e proprio — *prompt → ragionamento → tool → risultato → ragionamento* — ed è un progetto distinto: deriva da **pi**, l'agente minimale open-source di Mario Zechner che Steinberger adottò ai tempi di Clawdbot. Il nome è rimasto come dichiarazione di intenti: come la costante matematica, è piccolo, stabile, e finisce dappertutto. Il Gateway sa tutto di canali e sessioni e niente di LLM; Pi sa tutto di LLM e niente di Telegram. La divisione è netta: puoi cambiare modello senza toccare i canali e aggiungere canali senza toccare il ragionamento.

I due processi comunicano in modalità **RPC** — Remote Procedure Call: il Gateway non importa Pi come libreria, gli manda *richieste strutturate* (JSON su stdin/stdout) e riceve risposte ed eventi, come un client parla a un server. Sembra un dettaglio implementativo; è invece la proprietà che rende possibile metà delle cose viste nel libro. Un processo separato può girare **dentro il sandbox** (il perimetro Docker del Cap. 4) mentre il Gateway resta fuori a fare da torre; può essere ucciso a metà run senza tirare giù i canali; può usare un modello diverso per ogni agente. E, soprattutto, espone un'interfaccia che altri possono implementare: è il punto di aggancio per le integrazioni avanzate.

Dentro questa conversazione RPC scorrono due flussi che la documentazione nomina di continuo. Il **tool streaming** è il flusso degli eventi tool: quando Pi esegue un comando shell o una skill, il Gateway riceve in tempo reale "tool partito", l'output man mano che viene prodotto, "tool finito, exit code 0". È ciò che permette alla Control UI di mostrarti *cosa sta facendo* l'agente mentre lo fa, invece di un cursore che lampeggia per trenta secondi. Il **block streaming** è il flusso della risposta: il modello non consegna un testo monolitico a fine run, ma blocchi tipizzati — testo, codice, tool-use — che il Gateway può iniziare a inoltrare al canale prima che il run sia concluso. Quando vedi la risposta di Polly "crescere" a pezzi su Telegram, con il blocco di codice che arriva intero e mai spezzato a metà (il per-channel chunking del Cap. 2), stai guardando il block streaming attraversare tutta la catena: modello → Pi → Gateway → canale.

### Il viaggio di un messaggio, versione integrale

Il Cap. 2 ha raccontato gli otto stadi del ciclo di vita dal punto di vista dell'agente. Ora che hai tutti i pezzi — control plane, vector, lane, pipeline, runtime — puoi rifare il viaggio dal punto di vista dell'architettura, che è quello che serve quando qualcosa si rompe.

```text
Telegram ──► plugin canale
               │  evento normalizzato + media
               ▼
        Gateway  ws://127.0.0.1:18789
               │  binding ──► agente
               │  scope  ──► lane di sessione
               ▼
        coda della lane (queue mode)
               │  contesto assemblato
               ▼
        Pi runtime (RPC, nel sandbox)
               │  tool streaming ◄─► skill/shell
               │  block streaming
               ▼
        Gateway ──► chunking ──► Telegram
               │
               ▼
        sessione + memoria su file
```

In prosa: il plugin del canale normalizza il payload nativo in un evento standard e lo consegna al control plane, con gli eventuali media già passati per la pipeline. Il Gateway applica il binding (quale agente serve questo canale — nello YAML del Gateway, Cap. 12), risolve la lane secondo lo scope, accoda rispettando il queue mode. Quando la lane è libera, assembla il contesto — gli otto file, la memoria, le note di ieri e di oggi — e fa partire il run sul Pi runtime via RPC. Pi ragiona, chiama tool e skill (tool streaming), produce la risposta a blocchi (block streaming); il Gateway chunka secondo i limiti del canale e consegna in reply-back. Infine lo stato si deposita: la trascrizione in `~/.openclaw/sessions/`, la memoria nel workspace. File, non database — fino in fondo.

La resa diagnostica è immediata: ogni segmento ha il suo sintomo. Messaggio mai arrivato? Plugin del canale (`openclaw channels status`). Arrivato ma nessun run? Binding o activation mode. Run in attesa? Queue mode e lane occupata. Run lento sui tool? Tool streaming nei log. Risposta troncata? Chunking del canale. Il viaggio del messaggio è la spina dorsale del Cap. 15: adesso sai *perché* quella diagnostica funziona.

**Prompt pronto:**
> "Spiegami l'architettura interna di te stesso, partendo dal Gateway. Voglio capire: (1) come funziona il control plane WebSocket su `127.0.0.1:18789`, (2) cosa succede quando arriva un messaggio Telegram (sequence diagram a parole), (3) come usi sessioni e queue mode quando ho più finestre aperte in parallelo, (4) la differenza tra il runtime RPC che esegui tu e una skill standard. Massimo un paragrafo per punto."

### Companion app: la torre di controllo in tasca

Tutto ciò che si connette al control plane è un client come gli altri: le **companion app** sono client privilegiati che portano il Gateway dove i canali di messaggistica non arrivano.

**macOS — la menu bar app.** Vive nella barra dei menu con una connessione WebSocket permanente al Gateway. Le tre funzioni che la fanno amare: **Voice Wake** (una wake word locale: pronunci il nome dell'agente e detti senza toccare la tastiera), il **push-to-talk** (un tasto premuto, parli, rilasci — il vocale entra nella media pipeline come da qualunque canale), e il **WebChat** in finestra con i tool di debug accanto: stato delle sessioni, eventi del control plane in tempo reale. Per chi sviluppa skill è il posto più comodo da cui guardare il tool streaming.

**iOS e Android — i nodes.** Le app mobili non sono "un altro canale di chat": si registrano sul Gateway come **nodes**, dispositivi che oltre a portare la conversazione *espongono capacità* — fotocamera, posizione, notifiche push, microfono. L'agente può chiederti una foto del documento da archiviare, e tu puoi dettargli un task dal parcheggio. Il pairing avviene dalla Control UI; la connessione resta WebSocket, identica a quella di ogni altro client. Il caso d'uso che convince tutti: il Gateway gira su un VPS (Cap. 19), tu sei in treno, e la companion app è il filo diretto — via Tailscale, senza porte aperte — con la tua torre di controllo.

**Windows — System Tray e PowerToys.** Sul fronte Windows l'equivalente è la app di System Tray, costruita sopra una shared library riusabile da altre integrazioni, più l'estensione per la **PowerToys Command Palette**: l'agente invocabile dalla palette di sistema, senza aprire nessuna chat. È il segnale più chiaro della direzione di marcia: l'agente non come app che apri, ma come capacità ambientale del sistema operativo.

### Live Canvas e A2UI: quando la risposta non è testo

C'è una classe di risposte per cui il testo è il formato sbagliato: "com'è andata la settimana di spese?" merita un grafico, "scegli fra queste tre opzioni di volo" merita tre card con un bottone. **A2UI** — Agent-to-UI — è la risposta di OpenClaw: un protocollo con cui l'agente, invece di restituire parole, restituisce una *descrizione dichiarativa di interfaccia* (componenti, layout, dati) che il Gateway renderizza su una superficie web locale. Il **Live Canvas** è quella superficie: una pagina servita dal Gateway — sorella della Control UI — su cui l'agente crea e *modifica in tempo reale* l'interfaccia mentre la conversazione prosegue.

L'esempio che rende l'idea: chiedi a Polly il quadro delle spese del mese. Sul canale arriva il riassunto in due frasi; sul canvas, una tabella per categoria con un filtro per periodo. Scrivi "togli gli abbonamenti e confronta con aprile": la tabella *cambia*, senza ricaricare nulla — l'agente ha spinto un aggiornamento A2UI sulla stessa connessione WebSocket dei messaggi. Il passo da "l'agente usa le interfacce" a "l'agente *fabbrica* le interfacce" è il più grande cambio di paradigma UI dai tempi del touch.

**(!) Attenzione:** a maggio 2026 Canvas e A2UI sono la parte più giovane dello stack: nomi di configurazione e perimetro delle funzioni cambiano fra release. Prima di costruirci sopra, verifica sulla documentazione ufficiale (sezione Canvas/A2UI) lo stato della feature nella tua versione — `openclaw --version` alla mano.

### Lobster: il workflow shell (no, non la mascotte)

Chiariamo subito l'omonimia che confonde chiunque entri nella community: la mascotte di OpenClaw è *il lobster*, l'aragosta che fa il "molt". **Lobster**, maiuscolo e senza articolo, è un'altra cosa: il **workflow shell** di OpenClaw — un linguaggio di pipeline per comporre skill e tool in automazioni deterministiche.

Il problema che risolve è sottile ma reale. Un agente LLM è bravissimo a *decidere* cosa fare e pessimo a *ripetere* la stessa procedura cento volte in modo identico: ogni run ri-ragiona da capo, con costi in token e una varianza che in produzione non vuoi. Lobster ribalta il rapporto: la procedura la scrivi una volta, come pipeline **tipizzata** — ogni passo dichiara cosa accetta e cosa emette, e la shell rifiuta in partenza un passo che produce testo incollato a uno che si aspetta un elenco di eventi — e **composabile**: le pipeline si concatenano come i comandi Unix con la pipe. Concettualmente:

```text
calendar.today
  | filter: external_attendees
  | brief: two_paragraphs
  | approve              # human gate
  | send: telegram
```

(Sintassi illustrativa: l'esatta è nella documentazione ufficiale.) Il passo `approve` è la firma del progetto: un *human gate* tipizzato, il punto in cui la pipeline si ferma e aspetta il tuo sì — la versione strutturata della regola "chiedi conferma prima di inviare" che nel Cap. 7 scrivevi in prosa dentro `AGENTS.md`. Ed è tutto **local-first**: le pipeline sono file nel workspace, versionabili con Git, eseguibili senza servizi esterni.

La divisione del lavoro diventa allora elegante: l'LLM per ciò che richiede giudizio, Lobster per ciò che richiede affidabilità. La mossa da power user è usare il primo per scrivere il secondo — far *generare* all'agente la pipeline di un processo che ormai fate sempre uguale, e da lì in poi eseguire la pipeline, non il ragionamento.

**Prompt pronto:**
> "Guarda i task ricorrenti delle ultime due settimane (cerca nelle note di memoria). Individua il più ripetitivo e proponimi una pipeline Lobster che lo automatizzi: passi tipizzati, un human gate prima di ogni azione esterna, e una nota su cosa resta fuori perché richiede giudizio."

### Case study: ClawJacked, ovvero perché l'architettura è sicurezza

Chiudiamo con le due storie che hanno insegnato alla community, a sue spese, tutto il capitolo.

La prima è un aneddoto diventato proverbiale: **"Molty mostra la home directory"**. Primi tempi, era Clawdbot e l'agente di default si chiamava Molty. In un gruppo Telegram con l'agente configurato per rispondere a tutti — activation mode `always` — un partecipante scrive, per scherzo: "Molty, cosa c'è nella home del tuo padrone?". E Molty, servizievole, esegue `ls ~` e incolla l'elenco in chat: `Documents`, `Projects`, i nomi delle cartelle dei clienti, tutto. Lo screenshot fece il giro della community. Nessun exploit, nessun bug: ogni componente aveva fatto il suo dovere. Il problema era la *composizione* — sessione di gruppo, attivazione senza gating, tool filesystem — e la lezione attraversa tutto il capitolo: in un sistema di agenti la sicurezza non vive nei componenti, vive nella geometria con cui li componi.

La seconda storia è la **CVE-2026-25253**, che la community chiama **ClawJacked** — già incrociata nei Cap. 3 e 4, ma solo adesso hai gli strumenti per capirla davvero. Gennaio 2026: viene documentato che un'istanza non patchata, con il control plane raggiungibile dall'esterno, poteva essere compromessa in meno di 90 secondi se l'agente leggeva una singola pagina web ostile. Riletta con la mappa di questo capitolo, è una lezione di architettura applicata. Primo ingrediente: un Gateway in ascolto su `0.0.0.0` invece che su `127.0.0.1` — di solito per pigrizia, "così lo raggiungo dal portatile" — che trasforma la torre di controllo in un servizio pubblico. Secondo: la pagina ostile come prompt injection, cioè il quarto e il primo input vector usati come cavallo di Troia. Terzo: il control plane che, per design, *può tutto* — è il kernel — e quindi, una volta raggiunto, consegna tutto. La risposta del progetto seguì la diagnosi: patch nelle release `2026.1.x`, binding su loopback come default rigido, token di autenticazione obbligatorio sul control plane, e il sandbox promosso da "consigliato" a "predefinito" (è il momento, raccontato nel Cap. 4, in cui la documentazione cambiò linguaggio).

**(!) Attenzione:** la porta `18789` non va *mai* esposta su internet, nemmeno "solo per un test". Per raggiungere il Gateway da fuori casa la strada giusta è una rete privata (Tailscale, Cap. 19) o un tunnel autenticato. Verifica ora: `lsof -i :18789` deve mostrare il bind su `127.0.0.1`, non su `*` o `0.0.0.0`.

Il filo che lega le due storie è lo stesso del capitolo: il Gateway è il punto in cui tutto converge — vector, sessioni, media, runtime, app, interfacce. È la sua forza architetturale ed è, per la stessa ragione, il punto da difendere meglio. Capire come è fatto non è curiosità da ingegneri: è la differenza fra usare un sistema autonomo e *governarlo*.

## Errori comuni e come risolverli

**Sintomo:** il WebSocket si disconnette ogni minuto.
Causa: timeout di un proxy o load balancer troppo basso.
Fix: aumentare il timeout (es. nginx
`proxy_read_timeout 3600s`) o abilitare keep-alive.

**Sintomo:** la companion app iOS/Android non si connette.
Causa: il firewall del router blocca il traffico in ingresso.
Fix: Tailscale risolve senza port forwarding;
in alternativa, port forwarding sul router.

**Sintomo:** la trascrizione audio fallisce.
Causa: media pipeline senza Whisper né provider STT remoto.
Fix: installare Whisper
(`pip install openai-whisper`) o configurare uno STT cloud.

**Sintomo:** Live Canvas/A2UI non renderizza.
Causa: Gateway troppo vecchio o feature non abilitata
nella tua build.
Fix: `openclaw update`, poi verificare nella
documentazione ufficiale (sezione Canvas/A2UI) come
abilitarla nella versione installata.

**Sintomo:** nei gruppi l'agente risponde a tutto (o a niente).
Causa: activation mode su `always` (o `never`)
invece che su `mention`.
Fix: riportare il gruppo al mention gating e provare
con un messaggio senza menzione.

**Sintomo:** il cron gira ma sul canale non arriva nulla.
Causa: run senza origine umana e senza delivery channel,
quindi il reply-back non sa dove consegnare.
Fix: dichiarare il canale di consegna nel cron (Cap. 18).

## Checklist di fine capitolo

- [ ] Capisco il ruolo del Gateway come control plane
- [ ] Verificato che il Gateway gira su `ws://127.0.0.1:18789` (default)
- [ ] Conosco i 5 input vector dell'autonomia
- [ ] So spiegare in due frasi cos'è una "session" e quali tipi esistono
- [ ] Conosco almeno una companion app (macOS/iOS/Android/Windows)
- [ ] So seguire il viaggio di un messaggio segmento per segmento
- [ ] So distinguere Lobster (workflow shell) dalla mascotte del progetto
- [ ] Ho verificato con `lsof -i :18789` che il control plane ascolta solo su loopback

## Link e risorse utili

- [Documentazione ufficiale](https://docs.openclaw.ai) — reference del WebSocket control plane e del Pi agent runtime
- [Repository GitHub](https://github.com/openclaw/openclaw) — codice sorgente del Gateway
- [Architecting the Agentic Future](https://dev.to/mechcloud_academy/architecting-the-agentic-future-openclaw-vs-nanoclaw-vs-nvidias-nemoclaw-9f8) — inquadramento architetturale
- [Architecture overview](https://github.com/openclaw/openclaw/blob/main/docs/concepts/architecture.md) — i moduli (Gateway, agenti, skill, sessioni) nella documentazione del repo
- [Messages and queue modes](https://docs.openclaw.ai/concepts/messages) — reference ufficiale di code e modalità di attivazione
- [Sandboxing](https://docs.openclaw.ai/gateway/sandboxing) — il perimetro di esecuzione del runtime

Per l'elenco completo delle fonti del libro, vedi [Appendice E](../Appendici/E-risorse-e-link-utili.md).

---

[← Capitolo 19](./19-deploy-su-vps-e-infrastruttura-cloud.md)  ·  [Indice](../README.md)  ·  [Capitolo 21 →](../PARTE-VIII-Visione-futuro/21-ecosistema-openclaw.md)
