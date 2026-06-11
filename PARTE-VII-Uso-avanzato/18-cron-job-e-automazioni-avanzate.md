# Capitolo 18 — Cron job e automazioni avanzate [★★★]

## Cosa imparerai

- L'anatomia di un cron job in OpenClaw
- Pattern temporali e trigger
- Cron ricorsivi: cron che creano altri cron
- Debugging dei cron

## Prerequisiti

Aver già attivato almeno un workflow ricorrente ([Capitolo 8](../PARTE-III-Primo-mese/08-dieci-workflow-pronti-all-uso.md)). Familiarità con la sintassi cron è utile ma non obbligatoria: OpenClaw accetta anche linguaggio naturale.

## Contenuto principale

### 18.1 Le 6:32 di Claire

Torniamo per un momento alla scena con cui si apre il [Capitolo 11](../PARTE-IV-Multi-agente/11-progettare-il-tuo-team-di-agenti.md): una mattina di febbraio 2026, alle 6:32, Claire Vo riceve su Telegram il digest di Polly — le email che contano, i meeting già preparati, l'allenamento del figlio alle 17. Lei non ha chiesto niente. Nel Capitolo 11 quella scena serviva a raccontare il *team*; qui scendiamo in sala macchine e guardiamo l'ingranaggio che l'ha prodotta: un cron job. Un'espressione di cinque campi, una timezone, un prompt e un canale di consegna. Tutto qui — e proprio perché è così poco, è il punto del libro dove la differenza fra "configurato bene" e "configurato quasi bene" si misura in euro e in figuracce.

Questo capitolo è la versione lunga della promessa fatta nel Capitolo 2: i cron sono l'*agenda* dell'agente, e un agente può imparare la tua agenda da solo. Vedremo la sintassi vera dei comandi, i quattro archetipi temporali che coprono il 90% dei casi, le pipeline di job dipendenti, i meta-cron (cron che creano cron) con i loro salvagenti, e il debugging. In chiusura, due storie della community: una da $2.000 e una da $177.417.

### 18.2 La mappa dell'automazione: sei meccanismi, uno scheduler

"Automazione" in OpenClaw non vuol dire una cosa sola. La documentazione ufficiale distingue sei meccanismi, e confonderli è la prima causa di automazioni che scattano due volte, o mai:

- **Heartbeat** — il battito ricorrente di sistema (default ogni 30 minuti): l'agente si sveglia, legge `HEARTBEAT.md`, decide se c'è materia. Opportunistico per natura: se la coda è occupata, salta e ritenta. È il *cuore* del Capitolo 2.
- **Cron** — l'appuntamento programmato esplicitamente: orario preciso, garanzia di esecuzione, storico dei run. È l'*agenda*, ed è il protagonista di questo capitolo.
- **Hook (trigger a evento)** — non guarda l'orologio: scatta quando succede qualcosa *fuori* (una richiesta HTTP, una nuova email via Gmail PubSub). Ne riparliamo fra un attimo, perché la differenza con i cron è concettuale, non solo tecnica.
- **Background task** — un lavoro lungo lanciato da una conversazione ("fallo in background e avvisami quando hai finito"), che gira senza bloccare la chat. Ogni esecuzione di cron, peraltro, viene registrata proprio come background task: è lì che vive lo storico.
- **Task flow** — una sequenza dichiarata di passi con dipendenze, quando il lavoro è "prima A, poi B se A riesce".
- **Standing order** — l'istruzione permanente in linguaggio naturale scritta nei file di workspace ("ogni volta che arriva una fattura, archiviala in `~/Documents/fatture/`"): non ha un orario suo, viene onorata dall'agente quando heartbeat, cron o conversazioni la rendono pertinente.

La tabella decisionale, in breve:

| Vuoi… | Strumento |
|-------|-----------|
| qualcosa a un orario preciso | cron |
| controlli "ogni tanto" | heartbeat |
| reagire a un evento esterno | hook |
| lavoro lungo, chat libera | background task |
| più passi con dipendenze | task flow |
| una regola sempre valida | standing order |

**Cron contro trigger a evento.** Il cron risponde alla domanda "*quando* deve succedere?"; il trigger a evento risponde a "*cosa* deve farlo succedere?". Se il fatto scatenante è il tempo (le 7:00, ogni venerdì), è un cron. Se è un evento del mondo (un ordine sul tuo e-commerce, un'email del commercialista), forzarlo dentro un cron significa fare *polling*: un job ogni cinque minuti che controlla "è successo qualcosa?" — e paga un'inferenza anche quando la risposta è no, 288 volte al giorno. Per questi casi il Gateway espone endpoint webhook autenticati. Un sistema esterno può svegliare l'agente così:

```bash
curl -X POST http://127.0.0.1:18789/hooks/wake \
  -H "Authorization: Bearer <hook-token>" \
  -H "Content-Type: application/json" \
  -d '{"text":"New order received","mode":"now"}'
```

Nessun orologio: l'agente dorme gratis finché il mondo non bussa. La regola pratica: **cron per il tempo, hook per gli eventi, heartbeat per l'opportunismo**. Quando nel resto del capitolo vedrai l'archetipo "on-event", ricordati che spesso il modo giusto di implementarlo non è un cron.

**(!) Attenzione:** gli endpoint hook vanno tenuti dietro loopback, tailnet o reverse proxy fidato, con un token dedicato (mai riusare il token del Gateway). Un hook esposto su internet senza autenticazione è un citofono che chiunque può suonare — e dall'altra parte c'è un agente che esegue.

### 18.3 Anatomia di un cron job

Il libro finora ti ha fatto *leggere* i cron (`openclaw cron list`) e spegnerli (`openclaw cron disable <id>`). È ora di crearli da CLI. Il comando è `openclaw cron add` (con l'alias `cron create`), e questo è l'esempio completo da cui partire — il digest mattutino di Claire, con espressione, timezone, modello economico e consegna:

```bash
openclaw cron add \
  --name "morning-digest" \
  --cron "0 7 * * *" \
  --tz "Europe/Rome" \
  --session isolated \
  --message "Read inbox and calendar for the day. \
Send a 5-bullet digest, one line each, sorted \
by priority. If nothing relevant: 'Free day.'" \
  --model "claude-haiku-4-5" \
  --announce --channel telegram
```

Smontiamolo pezzo per pezzo, perché ogni flag è una decisione.

**Lo schedule.** Tre forme possibili: `--at` per il colpo singolo (un timestamp ISO oppure un relativo come `20m`; aggiungi `--delete-after-run` perché il job si cancelli da solo dopo il successo), `--every` per l'intervallo fisso (`--every 1h`), `--cron` per l'espressione classica a cinque campi: minuto, ora, giorno del mese, mese, giorno della settimana. `0 7 * * *` = ogni giorno alle 7:00; `0 18 * * 5` = venerdì alle 18:00.

**La timezone è obbligatoria** — non per la CLI, che senza `--tz` accetta comunque il job, ma per la tua sanità mentale. Senza timezone esplicita i timestamp vengono trattati come UTC e le espressioni seguono l'orologio della macchina che ospita il Gateway: il giorno in cui sposti l'agente dal Mac mini a un VPS di Francoforte, o il giorno del cambio dell'ora legale, il digest delle 7:00 arriva alle 6:00, alle 8:00 o mai (il Capitolo 15 ha già raccontato questo guasto dal lato della diagnosi). Scrivi `--tz "Europe/Rome"` su ogni job, sempre, anche quando "tanto il server è in Italia".

**Il tipo di sessione** decide quanto contesto — e quindi quanti token — ogni esecuzione si porta dietro:

- `--session main`: il job inietta un evento di sistema nella sessione principale, tipicamente con `--system-event` e `--wake now`. Giusto per promemoria brevi che devono *interrompere*.
- `--session isolated`: ogni run parte da una sessione pulita, fa il suo lavoro, muore. È la scelta di default per report e faccende ricorrenti: costa una frazione di un run carico di storia. Richiede `--message` (il prompt del job).
- `--session session:<nome>`: sessione persistente con memoria fra un run e l'altro — la vedremo nelle pipeline.

**Il budget massimo di esecuzione.** Un cron è spesa ricorrente per definizione, e va messo a dieta *alla creazione*, non dopo la bolletta. Le leve sono quattro. La prima è il **modello**: `--model` assegna al job un modello diverso da quello di default dell'agente — Haiku per i task ripetitivi, Sonnet 4.6 per il lavoro vero, Opus 4.6 solo dove serve ragionamento profondo (è la stessa logica di routing del Capitolo 14). La seconda è il **timeout**: il campo `timeoutSeconds` del job tronca i run che non finiscono, e un run troncato è anche un run che smette di consumare. La terza sono i **retry**, limitati per configurazione (sotto, nei salvagenti). La quarta è il **max-iterations**: un tetto al numero di cicli che un job può concatenare. Attenzione alla semantica: per un cron normale il concetto non serve (un run = un'esecuzione); diventa vitale per i *meta-cron* della sezione 18.6, dove "iterazione" significa "un cron che crea un altro cron". Lì `max-iterations` è il contatore — scritto nelle istruzioni del job e tracciato in un file di memoria — oltre il quale la catena si ferma da sola.

**La consegna.** `--announce --channel telegram` fa recapitare il testo finale sul canale; con `--to` scegli il destinatario esplicito (un gruppo, un topic). In alternativa `--webhook <url>` spedisce il risultato a un endpoint HTTP, per le integrazioni macchina-a-macchina. Senza nulla, il run lavora in silenzio — utile, ma è anche la causa del classico "il cron risulta `ok` ma non mi arriva niente".

Il ciclo di vita si governa con quattro comandi gemelli di quelli che già conosci:

```bash
# inspect one job, with resolved delivery route
openclaw cron show <id>

# change the prompt or the model
openclaw cron edit <id> --message "New prompt" \
  --model "claude-sonnet-4-6"

# force a test run now and wait for the result
openclaw cron run <id> --wait

# delete the job
openclaw cron remove <id>
```

**(i) Pro tip:** il modo più rapido di creare un cron resta il linguaggio naturale: scrivi all'agente "ogni mattina alle 7 (ora di Roma) mandami il digest" e sarà lui a chiamare lo scheduler con i flag giusti. Funziona perché l'agente ha i tool cron fra le sue capacità. Il motivo per cui questo capitolo ti mostra comunque la CLI è che *tu* devi saper verificare cosa ha creato: `openclaw cron show <id>` dopo ogni cron "dettato a voce" è l'abitudine che distingue il power user.

C'è infine un tranello di sintassi che merita il suo paragrafo, perché produce cron che scattano sei volte al mese invece di una. Quando compili **sia** il giorno del mese **sia** il giorno della settimana, il parser (croner, che segue la semantica Vixie) li combina in **OR**, non in AND:

```text
# Intended: 9:00 on the 15th, only if Monday
# Actual: every 15th OR every Monday (union)
0 9 15 * 1
```

Se vuoi davvero la congiunzione, programma su un solo campo e fai verificare l'altro alle istruzioni del job ("run only if today is Monday, otherwise reply NO_REPLY").

### 18.4 I quattro archetipi temporali

Guarda i cron di chiunque abbia un setup maturo — il team di Claire, il business di Nat Eliason, la Polly di questo libro — e troverai sempre le stesse quattro famiglie. La giornata-tipo del Capitolo 1 era, senza dirlo, un catalogo di archetipi: il digest delle 7:00, il ping pre-meeting delle 12:30, la bozza serale. Eccoli con orari e contenuti tipici.

**Il mattutino (6:30–8:00).** Il digest: email, calendario, priorità. È il "hello world" dei cron e l'hai già costruito nel Capitolo 8. Caratteristiche: `isolated`, modello economico, output corto e *finito* ("se non c'è nulla: 'Giornata libera'"). L'errore tipico è farlo crescere: quando il digest supera le dieci righe, nessuno lo legge più ed è ora di dividerlo.

**Il serale (21:00–23:00).** Il wrap-up: la nota di memoria del giorno (il run delle 22:00 che hai visto nella contabilità di Polly nel Capitolo 14), il riepilogo di cosa è rimasto aperto, la preparazione del giorno dopo. È l'archetipo più sottovalutato: un buon serale rende migliore il mattutino, perché la nota di ieri è esattamente ciò che l'agente carica al risveglio.

**Il settimanale (venerdì pomeriggio o domenica sera).** Report, audit, manutenzione. Qui vivono i due job promessi dai capitoli precedenti. Il primo è l'auto-ispezione del Capitolo 15: domenica, l'agente controlla i propri cron, le skill e la memoria, e ti manda un rapporto di una riga. Il secondo è la **compaction della memoria** promessa dal Capitolo 2: le note giornaliere si accumulano, e dopo qualche settimana pesano su ogni risveglio. Il job che le tiene in ordine:

```bash
openclaw cron add \
  --name "memory-compaction" \
  --cron "30 22 * * 0" \
  --tz "Europe/Rome" \
  --session isolated \
  --message "Read files in memory/ older than 14 \
days. Merge durable facts into MEMORY.md, move \
the processed notes to memory/archive/, report \
in one line what changed." \
  --announce --channel telegram
```

Domenica 22:30, dopo il serale: prima si scrive la nota del giorno, poi si archivia il passato. L'ordine non è un vezzo — è la prima, microscopica *pipeline*.

**L'on-event.** Nuova iscrizione alla newsletter, nuovo ordine, nuova menzione del brand. Come detto nella sezione 18.2: se esiste un evento tecnico (webhook, Gmail PubSub), usa un hook e lascia dormire lo scheduler; il cron-che-fa-polling è l'ultima spiaggia, da riservare alle fonti che non sanno bussare — e con frequenze oneste (ogni ora, non ogni cinque minuti) e modello minimo.

### 18.5 Pipeline: cron con dipendenze

Prima o poi un job singolo non basta: il report del venerdì richiede *raccolta* dei dati, poi *sintesi*, poi *invio*. Tre modi di costruirlo, in ordine crescente di accoppiamento.

**Il passaggio di file.** Il modo più robusto e più unix: il job A scrive un file nel workspace, il job B — schedulato dopo, con margine — lo legge. `report-collect` alle 17:00 produce `memory/report-raw.md`; `report-send` alle 17:40 lo trova, lo sintetizza e lo manda. Le istruzioni di B devono coprire il fallimento di A: "se il file non esiste o è più vecchio di 2 ore, avvisami invece di inventare". Il margine fra i due orari è il tuo ammortizzatore; il file è il contratto.

**La sessione condivisa.** Per i lavori che devono *ricordare* i passi precedenti, `--session session:<nome>` dà a più job (o a più run dello stesso job) una sessione persistente con memoria comune. È il meccanismo giusto per lo standup quotidiano che si costruisce sul riassunto di ieri, o per la pipeline editoriale in cui il job del lunedì propone i temi e quello del martedì sviluppa il tema scelto. Il prezzo è il contesto che cresce: una sessione condivisa va periodicamente ripulita, o diventa il cron più costoso del tuo parco.

**L'orchestratore.** Quando i passi sono tanti e condizionali, conviene rovesciare il disegno: *un solo* cron che fa da direttore d'orchestra e delega i passi a subagent o a un task flow ("raccogli; se ci sono dati nuovi, sintetizza; se la sintesi supera X, chiedi conferma prima di inviare"). Un punto di schedulazione, un punto di fallimento, un solo posto dove guardare i log. La regola di buon senso: due o tre job collegati via file vanno benissimo; alla quarta dipendenza, passa all'orchestratore.

**(#) Debug:** in una pipeline che zoppica, il colpevole si trova interrogando lo storico run per run: `openclaw cron runs --id <jobId> --limit 20` mostra esiti e durate di ogni esecuzione del job. Se A risulta `ok` ma B non trova mai il file, guarda le *durate*: un A che finisce alle 17:39 per un B delle 17:40 non è una dipendenza, è una roulette.

### 18.6 Meta-cron: cron che creano altri cron

Ed eccoci al contenuto più originale del modello OpenClaw, promesso fin dal Capitolo 2: **i cron possono creare altri cron**. L'agente ha accesso allo scheduler come a qualunque altro tool; quindi un job può, come parte del proprio lavoro, programmare job futuri. È il meccanismo con cui un agente "impara la tua agenda".

L'esempio quotidiano è già nella giornata-tipo del Capitolo 1: il ping delle 12:30 sul cliente del meeting delle 14:30. Non c'è nessun job fisso "alle 12:30": c'è un mattutino che, oltre al digest, legge il calendario e semina promemoria one-shot:

```text
Part of morning-digest instructions:
For each external meeting today, create a
one-shot cron 30 minutes before it (--at,
--delete-after-run) that checks the guest's
public channels and sends me a 3-line brief.
```

I job one-shot creati con `--delete-after-run` si cancellano da soli dopo l'esecuzione: la sera lo scheduler è pulito, e domattina il mattutino riseminerà. Questo è il meta-cron "sicuro": figli a vita breve, numero limitato dal calendario stesso.

Il meta-cron *ricorsivo* — un job ricorrente che crea altri job ricorrenti — è un'altra categoria di rischio, perché senza freni la popolazione di cron può solo crescere. L'esempio canonico, monitoraggio competitor, scritto per esteso e **con stop-condition**:

```text
watch-competitors (Mondays 08:00 Europe/Rome):
1. Read memory/competitors.md.
2. Search the web for new competitors
   in our niche (max 2 new per week).
3. For each new competitor found:
   - append it to memory/competitors.md
   - create cron "watch-<name>": daily
     07:30, isolated, Haiku, checks their
     site/socials, reports changes only
   - create a one-shot cron at +14 days
     that REMOVES "watch-<name>" unless
     marked "keep" in memory/competitors.md
4. STOP-CONDITIONS (check before creating):
   - run "cron list": if 5 or more
     "watch-*" jobs exist, create nothing,
     report "watch budget full" instead
   - if "watch-<name>" already exists,
     skip it (never create duplicates)
```

Nota la struttura: ogni figlio nasce **già con la propria morte programmata** (il one-shot che lo rimuove a 14 giorni), e il padre verifica il censimento **prima** di creare, non dopo. Il `max-iterations` della sezione 18.3 è esattamente questo: "5 or more watch-* jobs → create nothing".

I **tre salvagenti** che ogni meta-cron deve indossare, sempre:

1. **Budget.** Ogni figlio ha modello economico, `timeoutSeconds`, e un tetto di popolazione (il contatore qui sopra). Il padre ha un orario a bassa frequenza: un meta-cron che gira ogni cinque minuti è un generatore di incidenti.
2. **Idempotenza.** Eseguire il padre due volte non deve produrre due figli. I nomi (`--name "watch-acme"`) sono la chiave: prima di creare, il job controlla `cron list` e salta ciò che esiste già. Lo stesso vale per te: dare nomi parlanti ai cron è ciò che rende possibile il controllo.
3. **Retry limitati.** I tentativi su errore sono già limitati dalla configurazione del Gateway — e così devono restare:

```yaml
cron:
  enabled: true
  maxConcurrentRuns: 8
  retry:
    maxAttempts: 3
    # backoff in ms: 1, 2, then 5 minutes
    backoffMs: [60000, 120000, 300000]
```

Tre tentativi con backoff crescente per gli errori transitori (rate limit, rete, server); gli errori permanenti disabilitano il job invece di insistere. Se ti viene la tentazione di alzare `maxAttempts` "per sicurezza", rileggi la prima storia della sezione 18.8.

**(!) Attenzione:** un meta-cron senza stop-condition non è un'automazione avanzata: è una bomba a orologeria con la miccia accesa a tua insaputa. La checklist minima prima di attivarne uno: tetto di popolazione scritto nelle istruzioni, figli con auto-rimozione, nomi univoci, modello economico sui figli, e un cron di audit (sezione 18.7) che ti avvisa se il conteggio cresce. Se manca anche uno solo di questi pezzi, il meta-cron non va in produzione.

### 18.7 Debugging: la scala dei comandi

Quando un cron si comporta male, la diagnosi segue la stessa logica del Capitolo 15: dal generale al particolare. La scala completa:

```bash
openclaw status
openclaw gateway status
openclaw cron status
openclaw cron list
openclaw cron runs --id <jobId> --limit 20
openclaw logs --follow
openclaw doctor
```

`openclaw cron list` resta il colpo d'occhio: job, schedule, timezone, ultima esecuzione. Le due colonne da guardare sono `last run` (un job sano è stato eseguito di recente) e la timezone (un job sano ce l'ha esplicita). `openclaw cron runs --id <jobId>` apre lo storico: esiti, durate, errori — è qui che si distingue il job che non scatta dal job che scatta e fallisce, due malattie con cure opposte. Per il test attivo, `openclaw cron run <jobId> --wait` forza l'esecuzione adesso e aspetta l'esito (exit code 0 solo se `ok`); la variante `--due` esegue solo se il job era effettivamente in scadenza — utile per capire se il problema è lo schedule o il contenuto.

E poi c'è il tecnico interno: l'agente stesso, che i propri cron li può ispezionare. Il dialogo del Capitolo 15 vale come modello:

> **Tu:** Il digest di stamattina non è arrivato. Ispeziona i tuoi cron e dimmi cosa è successo.
>
> **Polly:** Ho controllato. Il cron `morning-digest` esiste ed è attivo, ma l'ultima esecuzione risale a 3 giorni fa. Lo schedule è `30 7 * * *` senza timezone esplicita: col passaggio all'ora legale potrebbe essere il problema. Vuoi che aggiunga `Europe/Rome` e faccia un test?

L'evoluzione naturale è rendere l'ispezione *lei stessa* un cron: l'audit settimanale promesso nel Capitolo 15 — "controlla i tuoi cron, segnala quelli che non scattano da più di 48 ore, conta i `watch-*`, somma i costi" — chiude il cerchio. I cron sorvegliano il lavoro; un cron sorveglia i cron.

**(i) Pro tip:** i cron ricorrenti allo scoccare dell'ora esatta vengono leggermente sparpagliati dallo scheduler (fino a 5 minuti) per evitare picchi di carico. Se il tuo digest "delle 7:00" arriva alle 7:03, non è rotto. Quando il minuto esatto conta davvero, crea il job con `--exact`.

### 18.8 Due storie per chiudere

**La war story dei $2.000.** Circola nei thread della community fin dai giorni del ban di Anthropic, raccontata da chi l'ha vissuta come monito (i dettagli variano nei racconti; la meccanica è sempre la stessa, ed è quella che conta). Un freelance attiva un meta-cron di monitoraggio mercato sul suo agente di marketing: ogni ora, su Opus, e — convinto di fare la cosa prudente — alza i retry "per non perdere nessun run". Niente nomi univoci, niente censimento prima di creare: a ogni esecuzione il padre crea figli duplicati, e i figli falliti ritentano in coda. La popolazione di cron cresce in silenzio per giorni, ognuno paga un'inferenza su modello premium, e nessun audit guarda il contatore. Il weekend lungo fa il resto: lunedì mattina la dashboard del provider segna circa **$2.000 (~€1.840)**. La parte istruttiva è che *ogni singolo anello* della catena è uno dei tre salvagenti della sezione 18.6, mancato: nessuna idempotenza, retry gonfiati, nessun budget, nessun tetto di popolazione. Il fix, a posteriori, fu umiliante nella sua semplicità: `openclaw cron list`, una strage di `openclaw cron remove`, e il meta-cron riscritto con le stop-condition — venti minuti di lavoro che, fatti prima, sarebbero costati zero.

**Il contrappunto.** Gli stessi ingranaggi, montati con disciplina, sono la spina dorsale del caso più citato della community: il business "che si gestisce da solo" di Nat Eliason, già incontrato nel Capitolo 8 — quello arrivato a **$177.417 (~€163.000)** di ricavi raccontati nelle interviste di inizio 2026. Spogliato del titolo a effetto, è un parco di cron fatto degli archetipi di questo capitolo: mattutini che preparano la pipeline editoriale, serali che chiudono la contabilità della giornata, settimanali che fanno audit di costi e qualità, e pochissimi meta-cron, tutti con tetti espliciti. La differenza fra le due storie non è il talento e nemmeno il modello: è che nella seconda ogni job ha un nome, un budget, una timezone e qualcuno — umano o cron — che lo controlla una volta a settimana.

**Prompt pronto:**
> "Voglio creare un cron che [descrivi: es. "ogni mattina alle 7:00 (Europe/Rome) mi mandi su Telegram un riassunto delle email importanti del giorno e dei meeting"]. Aiutami a: (1) scrivere l'espressione cron con timezone esplicito, (2) decidere se è un cron singolo o un pipeline di task dipendenti, (3) impostare un budget massimo di esecuzione per evitare costi a sorpresa, (4) testarlo con un primo run forzato e verificare il log."

## Errori comuni e come risolverli

**Sintomo:** il cron non scatta.
Causa: timezone non specificato (default UTC) o cron syntax errato.
Fix: aggiungere timezone esplicito (es. `Europe/Rome`); validare l'espressione cron con un parser online.

**Sintomo:** il cron scatta due volte di seguito.
Causa: due cron sovrapposti per errore o cron + heartbeat che si pestano i piedi.
Fix: `openclaw cron list` per verificare; eliminare il duplicato con `openclaw cron remove <id>`.

**Sintomo:** il cron scatta cinque o sei volte al mese invece di una.
Causa: giorno del mese e giorno della settimana entrambi valorizzati: il parser li combina in OR, non in AND.
Fix: programmare su un solo campo e far verificare l'altro alle istruzioni del job.

**Sintomo:** il run risulta `ok` ma sul canale non arriva nulla.
Causa: nessuna modalità di consegna configurata, target mancante, o run che risponde solo `NO_REPLY`.
Fix: `openclaw cron show <id>` per vedere la rotta di consegna risolta; aggiungere `--announce --channel telegram` (ed eventualmente `--to`).

**Sintomo:** meta-cron crea cron infiniti.
Causa: nessun budget o stop-condition.
Fix: aggiungere `max-iterations` o una stop-condition (data, contatore, file flag).

**Sintomo:** il cron ha un costo mensile inaspettato.
Causa: frequenza troppo alta o modello costoso usato per ogni esecuzione.
Fix: ridurre frequenza, usare modelli più economici per task ripetitivi (`openclaw cron edit <id> --model …`).

## Checklist di fine capitolo

- [ ] Almeno un cron mattutino funzionante e verificato per 3 giorni
- [ ] Timezone esplicito su tutti i cron
- [ ] So creare, modificare e cancellare un job da CLI (`cron add|edit|remove`) e forzare un test (`cron run <id> --wait`)
- [ ] Nessuna espressione con giorno del mese e giorno della settimana valorizzati insieme
- [ ] Budget di iterazioni e stop-condition impostati per i meta-cron
- [ ] Ogni cron ricorrente ha un nome parlante e un modello proporzionato al task
- [ ] Log dei cron riveduti almeno una volta a settimana
- [ ] Ho un cron "audit" che mi avvisa se la spesa supera la soglia

## Link e risorse utili

- [Documentazione ufficiale](https://docs.openclaw.ai) — reference della sintassi cron e dei comandi `openclaw cron`
- [Heartbeat — documentazione ufficiale](https://docs.openclaw.ai/gateway/heartbeat) — il confine fra battito e agenda
- [The Complete Guide to Building Your Personal AI Agent](https://www.lennysnewsletter.com/p/openclaw-the-complete-guide-to-building) — la guida di Claire Vo, con i cron del suo team
- [Use OpenClaw to Build a Business That Runs Itself](https://creatoreconomy.so/p/use-openclaw-to-build-a-business-that-runs-itself-nat-eliason) — esempi di automazioni ricorrenti per un business reale

Per l'elenco completo delle fonti del libro, vedi [Appendice E](../Appendici/E-risorse-e-link-utili.md).

---

[← Capitolo 17](./17-creare-skill-personalizzate.md)  ·  [Indice](../README.md)  ·  [Capitolo 19 →](./19-deploy-su-vps-e-infrastruttura-cloud.md)
