# Capitolo 12 — Comunicazione e coordinamento tra agenti [★★★]

## Cosa imparerai

- L'architettura multi-agente: workspace, binding, routing
- Pattern di collaborazione su progetti condivisi
- Gestire conflitti e sovrapposizioni di competenza
- Pattern di escalation: quando un agente chiede aiuto a un altro

## Prerequisiti

Avere almeno due agenti definiti (vedi [Capitolo 11](./11-progettare-il-tuo-team-di-agenti.md)). Familiarità con i concetti di sessione e canale ([Capitolo 2](../PARTE-I-Capire-OpenClaw/02-anatomia-di-un-agente-openclaw.md)).

## Contenuto principale

### 12.1 Una mezz'ora di venerdì sera

Venerdì, 18:40. Stai chiudendo la settimana quando arriva l'email di un cliente: il form dei lead sul sito dà errore al submit, e non è il primo a segnalarlo. Apri Telegram e scrivi a Polly: "Il form dei lead sul sito è rotto, i clienti ricevono un errore quando inviano. Puoi occupartene?".

Polly non è una sviluppatrice: è la tua assistente personale, e nel suo SOUL.md c'è scritto chiaro che il codice non lo tocca — demanda a Kelly, l'agente developer (lo hai conosciuto nel team di Claire Vo, [Capitolo 11](./11-progettare-il-tuo-team-di-agenti.md)). Alle 19:12 Polly ti risponde: "Era la validazione del campo telefono, introdotta con l'aggiornamento di martedì: rifiutava i numeri con il prefisso internazionale. Kelly ha preparato la PR #214, i test passano. Procedo col deploy?". Tu scrivi "ok", e alle 19:18 il form funziona di nuovo. Con Kelly non hai mai parlato.

Questo capitolo spiega cosa è successo in quella mezz'ora: con quali meccanismi Polly ha parlato con Kelly, dove vive il permesso che le consente di farlo, come si evita che due agenti si rimbalzino messaggi all'infinito, e quanto è costata l'operazione.

Prima di entrare nei meccanismi, fissiamo il terreno di gioco — è il riassunto di quanto stabilito nel [Capitolo 10](./10-perche-un-solo-agente-non-basta.md). Ogni agente è un silos: il primo vive in `~/.openclaw/workspace/`, ogni agente aggiuntivo in `~/.openclaw/workspace-<nome>/`, e dentro ciascun workspace stanno la sua identità (gli otto file canonici), la sua `memory/`, le sue skill, i suoi cron e le sue sessioni di conversazione. Niente di tutto questo è visibile agli altri agenti: l'isolamento non è una convenzione di cortesia ma una garanzia che il Gateway fa rispettare. Ciò che invece è condiviso sta tutto a un livello sopra: il processo Gateway, la config YAML (`~/.openclaw/config.yaml`), le credenziali dei provider LLM, la macchina e i bot dei canali.

Il corollario è il punto di partenza di tutto il capitolo: **se Polly e Kelly devono collaborare, non possono farlo leggendosi i file a vicenda**, perché quella porta è chiusa per costruzione. Devono passare dal centralino — il Gateway — usando uno dei meccanismi espliciti che ora vediamo.

### 12.2 I tre meccanismi (più uno)

OpenClaw offre tre vie ufficiali con cui un agente comunica con un altro. Conviene dar loro tre nomi mentali, perché coprono tre bisogni diversi:

| Meccanismo | Quando usarlo |
|---|---|
| `sessions_send` | dialogo tra pari, contesto |
| `sessions_spawn` | incarico una-tantum, budget |
| cartella condivisa | file e artefatti di lavoro |

`sessions_send` è la **lettera**: un messaggio recapitato nella sessione di un altro agente, che lo leggerà e deciderà cosa farne. `sessions_spawn` è l'**incarico**: una sessione temporanea aperta apposta per un task, con un budget di scambi, il cui risultato torna al chiamante. La cartella condivisa è il **tavolo di lavoro**: una directory dichiarata nella config del Gateway dove più agenti depositano e leggono artefatti. Le sezioni che seguono li trattano uno per uno.

Esiste poi un quarto meccanismo, esterno a OpenClaw: la comunicazione **bot-to-bot di Telegram**, aperta dalla Bot API 10.0 (maggio 2026) e già incontrata nel [Capitolo 6](../PARTE-II-Installazione/06-configurare-telegram-e-altri-canali.md). Serve a far parlare agenti che vivono su *installazioni diverse* — il tuo Polly con l'agente di un collega — passando per un gruppo Telegram come farebbero due persone. Per gli agenti della *stessa* installazione resta la scelta sbagliata: ogni messaggio attraversa i server di Telegram (superficie pubblica, rate limit, niente garanzie di consegna interna) quando il Gateway offre la stessa cosa in locale, gratis e con i log sotto il tuo controllo. Regola pratica: traffico interno sul Gateway, bot-to-bot solo tra installazioni distinte.

### 12.3 `sessions_send`: la lettera

`sessions_send` è il tool nativo del Gateway con cui un agente recapita un messaggio nella sessione di un altro agente. L'hai già visto all'opera nel Capitolo 10, quando Polly ha trasferito a Max la conoscenza di marketing: Polly *scrive a* Max, il Gateway consegna, e Max decide cosa farne — rispondere, annotare nella propria memoria, ignorare. Nessuno dei due ha mai visto i file dell'altro: la conoscenza si consegna, non si copia.

La meccanica: quando Polly invoca il tool, il Gateway apre (o riprende) una sessione dedicata alla coppia — distinta dalle sessioni che ciascuno dei due ha con te sui canali, che restano `per-channel-peer` come da default del [Capitolo 2](../PARTE-I-Capire-OpenClaw/02-anatomia-di-un-agente-openclaw.md). Il messaggio arriva a Max come un turno di conversazione, col mittente dichiarato: Max sa che gli sta scrivendo un altro agente, non un umano. Se Max risponde, la risposta torna nella stessa sessione, e ogni scambio consuma un turno del budget (sezione 12.7).

Nei log la consegna si riconosce a colpo d'occhio. Con `openclaw logs --follow` vedrai righe come queste:

```text
14:02:31 polly -> sessions_send(to: kelly)
14:02:31 gateway: delivered (polly->kelly,
         turn 1/5)
14:03:18 kelly -> reply (session polly->kelly)
14:03:18 gateway: delivered (polly->kelly,
         turn 2/5)
```

Nota la seconda coppia di righe: la risposta di Kelly non è un nuovo invio ma un *reply* dentro la stessa sessione `polly->kelly`, e consuma il turno 2 dello stesso budget. La distinzione non è cosmetica: per rispondere a una conversazione già aperta a Kelly non serve alcun permesso, mentre per *iniziarne* una verso Polly gliene servirebbe uno — lo vedrai nella whitelist della sezione 12.6.

La caratteristica da tenere a mente è che `sessions_send` è **asincrono e conversazionale**: il mittente non resta bloccato in attesa, e il destinatario tratta il messaggio come tratterebbe il tuo — lo legge nel proprio contesto, con la propria identità e i propri tool. È il meccanismo giusto quando serve un dialogo tra pari: passaggi di contesto, richieste di parere, coordinamento continuativo. Quando invece serve "fai questo e riportami il risultato", c'è uno strumento più adatto.

### 12.4 `sessions_spawn`: l'incarico

`sessions_spawn` crea una **sessione temporanea** di un altro agente, dedicata a un singolo task: il chiamante formula l'incarico, l'agente eseguito lavora nella sessione effimera, e al termine il risultato torna al chiamante. Poi la sessione si chiude e non lascia code: niente conversazione aperta, niente contesto che si accumula.

La differenza rispetto a `sessions_send` è la stessa che passa tra scrivere a un collega e aprire una commessa: la lettera inizia (o continua) una relazione; l'incarico ha un perimetro, un budget e una consegna. Il budget si chiama `max-turns`: il numero massimo di scambi che la sessione può consumare prima che il Gateway la chiuda d'ufficio, riportando al chiamante quello che c'è. È il parametro che nel resto del capitolo ricorre ovunque, perché è la cintura di sicurezza del multi-agente.

Anche qui, i log raccontano la storia:

```text
09:15:04 polly -> sessions_spawn(agent: kelly,
         max-turns: 3)
09:16:42 gateway: spawn #4821 done
         (2 turns, 8.314 token)
```

Lo spawn ha due proprietà che lo rendono il cavallo di battaglia dei pattern di coordinamento. La prima è la **parallelizzabilità**: un agente può lanciare più spawn contemporaneamente — tre ricerche indipendenti a tre agenti diversi, o tre incarichi allo stesso — e raccogliere i risultati man mano che arrivano. La seconda è la **prevedibilità dei costi**: un incarico con `max-turns: 3` non potrà mai consumare più di tre scambi, comunque vada. Per i task ricorrenti vale lo stesso principio dentro i cron, dove il budget di esecuzione è materia del [Capitolo 18](../PARTE-VII-Uso-avanzato/18-cron-job-e-automazioni-avanzate.md).

**(i) Pro tip:** scegli il meccanismo guardando a cosa resta dopo. Se vuoi che il destinatario *ricordi* (nuove regole, contesto che gli servirà domani), usa `sessions_send`: il messaggio entra nella sua sessione e lui può annotarlo in memoria. Se vuoi solo il *risultato* e nessuna scia, usa `sessions_spawn`: la sessione effimera muore e la memoria dell'esecutore resta pulita.

### 12.5 La cartella condivisa: il tavolo di lavoro

Il terzo meccanismo non trasporta messaggi ma **file**. La cartella condivisa è una directory dichiarata esplicitamente nella config del Gateway e montata solo per gli agenti che elenchi — la sintassi è quella già vista nel Capitolo 10:

```yaml
shares:
  - path: "~/.openclaw/shared"
    agents: [polly, kelly]
```

Attenzione a non fraintendere: questa *non* è una breccia nell'isolamento dei workspace. Polly continua a non poter leggere `~/.openclaw/workspace-kelly/`, e viceversa: la cartella condivisa è uno spazio terzo, fuori da entrambi i workspace, che esiste solo perché tu l'hai dichiarato nella config — visibile, revocabile, e limitato agli agenti in elenco. L'isolamento resta la regola; la condivisione è un'eccezione dichiarata.

Il suo uso naturale sono gli **artefatti di progetto**: il CSV che Max prepara e Polly riassume, la bozza di report a cui lavorano in due, il file di specifiche che Kelly deve leggere prima di mettere mano al codice. Per tutto ciò che è più lungo di un messaggio, il pattern corretto è combinare due meccanismi: il file va nella cartella condivisa, e un `sessions_send` avvisa il destinatario — "ho lasciato le specifiche in `shared/form-fix.md`, dimmi quando hai finito". Il filesystem infatti non notifica nessuno: un file depositato senza avviso è un file che l'altro agente scoprirà per caso, forse mai.

**(#) Debug:** se un agente sostiene di "non vedere" un file che l'altro giura di aver depositato, verifica tre cose in ordine: che la voce `shares:` elenchi *entrambi* gli agenti; che il Gateway sia stato riavviato dopo la modifica alla config (`openclaw gateway restart`); e che il file sia davvero in `~/.openclaw/shared/` e non nel workspace privato di chi l'ha scritto — è l'errore più comune, e dal punto di vista dell'altro agente il file semplicemente non esiste.

### 12.6 Il pattern del coordinatore: la mezz'ora, spiegata

Torniamo al venerdì sera della sezione 12.1 e riavvolgiamo il nastro, questa volta guardando dentro la macchina. Il pattern in scena è il più importante del capitolo: il **coordinatore** — un agente dirige, gli altri eseguono, e tu parli solo col primo.

Prima di tutto, i permessi. La possibilità per Polly di rivolgersi a Kelly non vive nel suo TOOLS.md — che, come definito nel [Capitolo 2](../PARTE-I-Capire-OpenClaw/02-anatomia-di-un-agente-openclaw.md), contiene note operative in linguaggio naturale, non configurazione. Vive nello stesso posto del binding canale→agente del Capitolo 10: la **config YAML del Gateway**. È una whitelist esplicita:

```yaml
# ~/.openclaw/config.yaml
sessions:
  agents:
    # Agent-to-agent traffic is denied by
    # default: every route must be listed.
    allow:
      - from: polly
        to: [kelly, max]
      - from: holly
        to: [kelly]
    defaults:
      max-turns: 5
```

Il default è il silenzio: nessun agente può scrivere a un altro finché una regola `allow` non lo consente, e ogni regola dichiara una direzione (qui Polly può iniziare conversazioni con Kelly, non viceversa — Kelly può solo *rispondere* dentro le sessioni che Polly apre). Dopo ogni modifica, come sempre, `openclaw gateway restart`. E se ti stai chiedendo come mai il trasferimento Polly→Max del Capitolo 10 ti abbia funzionato senza toccare la config: la rotta `polly -> max` era già in whitelist — è la prima regola del blocco qui sopra. Se da te quel messaggio non è mai partito, la riga `allow` mancante era il motivo.

**(i) Pro tip:** come per i binding del Capitolo 10, lo schema esatto della config evolve con le versioni: prima di copiare questo blocco confrontalo con la Configuration reference ufficiale (link in fondo al capitolo) e verifica la tua versione con `openclaw --version`.

Ora il flusso, messaggio per messaggio. Alle 18:41 Polly riceve il tuo messaggio e fa quello che farebbe una brava capo-progetto: non inoltra il problema com'è, lo **scompone e lo perimetra**. Il suo `sessions_send` a Kelly è una delega ben scritta:

> "Kelly, segnalazione urgente dal sito: il form dei lead fallisce al submit, più clienti colpiti, ultima modifica nota il deploy di martedì. Ti chiedo: (1) individua la causa, (2) prepara una fix in una PR senza fare merge, (3) riportami causa e stato dei test in massimo 5 righe. Non serve che indaghi oltre il form."

Nota i tre ingredienti: il contesto minimo necessario (non l'intero thread email), il perimetro ("non indagare oltre"), e il formato della consegna ("5 righe"). Sono loro a tenere bassi i turni e i token.

Kelly lavora nel proprio workspace con i propri tool — GitHub, l'accesso al repository del sito — e alle 19:09 risponde nella sessione `polly->kelly`: causa individuata (la validazione del campo telefono), PR #214 aperta, test verdi, niente merge come richiesto. Polly riassume e ti riporta la decisione che conta: procedere o no col deploy. Tu dici "ok", Polly gira l'autorizzazione a Kelly, e alle 19:18 è finita.

Due scelte di design meritano di essere esplicitate. La prima: il merge in produzione è rimasto **a te**. Un coordinatore ben configurato concentra le decisioni irreversibili verso l'umano, non le distribuisce agli esecutori — è la boundary di approvazione vista con Felix nel Capitolo 11, e il motivo per cui la delega di Polly diceva "senza fare merge". La seconda: per un task una-tantum come questo Polly avrebbe potuto usare `sessions_spawn` invece di `sessions_send`; ha senso preferire la lettera quando, come qui, serve un dialogo (l'autorizzazione al deploy è un secondo scambio nella stessa conversazione). Per tre ricerche indipendenti da affidare a Max, lo spawn parallelo sarebbe stata la forma giusta.

Il pattern scala fino alla versione estrema vista nel Capitolo 11: la zero-human company di Nat Eliason, dove il coordinatore non è l'umano ma un altro agente — Felix, che ogni notte rivede il lavoro di Iris e Remy e ne aggiorna i processi. Anche lì la meccanica è questa: whitelist nella config, deleghe perimetrate, decisioni economiche escalate all'umano. Sul piano dei modelli, la regola del Capitolo 11 si applica pari pari: il coordinatore è l'agente che ragiona di più e sbaglia più caro (Claude Sonnet 4.6, o Opus 4.6 se il budget lo consente), gli esecutori possono spesso girare su modelli più leggeri.

### 12.7 Loop, conflitti e mention gating

Il multi-agente introduce una classe di guasti che il singolo agente non conosce: due processi educati che si rispondono a vicenda. Lo scenario è meno esotico di quanto sembri: Polly delega a Kelly, Kelly consegna e chiude con "fammi sapere se serve altro", Polly — addestrata alla cortesia — ringrazia, Kelly risponde "di nulla, a disposizione", e nessuno dei due ha un motivo per smettere. Ogni scambio costa token, e a tariffe da modello premium un loop notturno non sorvegliato è il modo più rapido per bruciare il budget del mese.

La difesa strutturale è il **budget di iterazioni**: il `max-turns` che hai visto nella config della sezione 12.6 (come default globale) e nel singolo `sessions_spawn` (come limite per incarico). Quando i turni si esauriscono, il Gateway chiude la sessione e lo annota nei log — il loop muore di morte amministrativa, non per buon senso dei partecipanti. Un valore di default sano è 5: abbastanza per delega, chiarimento e consegna, troppo poco perché i convenevoli decollino. La difesa comportamentale la scrivi invece nei SOUL.md: "nelle conversazioni con altri agenti, non rispondere a messaggi che non richiedono azione". Una riga che vale quanto il budget.

Il secondo guasto tipico vive nei **gruppi**. Metti Polly e Finn nello stesso gruppo Telegram di famiglia (a ciascuno il suo bot) e fai una domanda qualsiasi: senza protezioni rispondono entrambi, e il gruppo diventa un duetto. La prima protezione è il **mention gating**, già incontrato nei Capitoli 2 e 6: in un gruppo l'agente parla solo se menzionato esplicitamente. La seconda è la regola dell'**owner unico**: per ogni gruppo, un solo agente designato a rispondere alle menzioni generiche; gli altri intervengono solo se chiamati per nome. Vale anche qui la difesa in profondità del Capitolo 6: il mention gating di OpenClaw da una parte, il `/setprivacy` di @BotFather dall'altra.

Resta il conflitto più sottile, quello di **competenza**: il lead che scrive nel canale dove vivono sia Max (marketing) sia Sam (vendite) — di chi è? La risposta non è tecnologica ma editoriale, e l'hai già scritta nel Capitolo 11: le Boundaries nei SOUL.md, con la formula imparata a caro prezzo da Claire Vo — "questo agente NON fa X, demanda a Y". Il routing decide chi *riceve* il messaggio; le boundaries decidono chi *agisce*. Servono entrambi.

**(#) Debug:** sospetti un loop in corso? `openclaw logs --follow` e cerca la firma: coppie di `sessions_send` che si alternano tra gli stessi due agenti a pochi secondi di distanza, con contenuti sempre più corti. Per fermarlo subito, riavvia il Gateway (`openclaw gateway restart`: le sessioni agente-agente non riprendono da sole); poi abbassa `max-turns` e aggiungi la riga anti-convenevoli nei SOUL.md di entrambi.

### 12.8 L'escalation: Holly chiama Kelly

Il pattern di escalation è il coordinatore visto dal basso: non un capo che distribuisce lavoro, ma un esecutore che incontra un muro e chiama un collega più attrezzato. Il caso da manuale è support → developer.

Un cliente scrive alla casella di supporto: "Dalle 14 le chiamate API rispondono 429, abbiamo già riprovato". Holly, l'agente helpdesk, sa rispondere alle domande da FAQ ma questa non lo è: serve qualcuno che possa guardare i log del servizio. Il suo SOUL.md prevede il caso ("se la domanda richiede accesso a codice o log, chiedi a Kelly e non improvvisare"), e la config della sezione 12.6 le consente la rotta `holly -> kelly`. Parte il `sessions_send`:

> "Kelly, ticket dal cliente Rossi: API in 429 dalle 14, retry già tentati. Mi serve: causa probabile e una risposta che io possa girare al cliente in linguaggio non tecnico. Max 5 righe."

Kelly verifica e risponde nella sessione: il rate limiting è scattato per un picco di richieste da un'integrazione del cliente partita in loop alle 13:58; il limite si resetta da sé, ma conviene che il cliente fermi l'integrazione. Holly ricompone e risponde al ticket — ed è qui che il pattern paga: la risposta che parte è **arricchita**, con la competenza di Kelly dentro e il tono di Holly fuori. Il cliente ha fatto una domanda al supporto e ha ricevuto una risposta da supporto, puntuale come una da sviluppatore.

Tre regole tengono in piedi il pattern. Primo, l'escalation va **dichiarata nel SOUL.md** dell'agente che la origina, con il criterio di attivazione: senza quella riga, Holly tenterà di rispondere comunque, e un agente che improvvisa su materia tecnica è peggio di uno che dice "non lo so". Secondo, la rotta dev'essere nella **whitelist** — ed è una rotta a senso unico: Holly chiama Kelly, Kelly non ha motivo di iniziare conversazioni con Holly. Terzo, le **azioni** restano fuori: Kelly diagnostica, ma se la soluzione richiedesse un'azione con conseguenze (riavviare un servizio in produzione, emettere un rimborso) la decisione risale a te, per la stessa boundary di approvazione della sezione 12.6. L'escalation trasporta competenza, non autorità.

### 12.9 Costi e governance: chi può parlare con chi

Chiudiamo con le due domande da porsi *prima* di moltiplicare le rotte: quanto costa, e chi autorizzo.

Sul costo c'è una regola di pollice brutale: **ogni delega raddoppia il contesto**. Quando Polly gestisce un task da sola, paghi una volta il caricamento dei suoi file canonici più la conversazione. Quando lo delega a Kelly, paghi tutto due volte: il contesto di Polly che formula la delega, il contesto di Kelly che la riceve (i *suoi* file canonici, la *sua* memoria), e di nuovo Polly che legge la risposta. Token ×2 è la stima prudente per una delega semplice; le catene più lunghe — tu → Polly → Kelly → Polly → te con chiarimenti in mezzo — moltiplicano di conseguenza. Non è un motivo per evitare le deleghe: è un motivo per perimetrarle. Le mitigazioni le hai già viste passare: messaggi di delega con il contesto minimo (mai inoltrare interi thread), formato di consegna esplicito ("max 5 righe"), `sessions_spawn` con budget stretto per i task una-tantum, e modelli leggeri per gli esecutori ad alto volume. I conti veri — tariffe per modello, profili di spesa, monitoraggio con `/status` — sono materia del [Capitolo 14](../PARTE-V-Sicurezza-costi/14-gestire-i-costi-senza-sorprese.md).

Sulla governance, il principio è quello che la config della sezione 12.6 incorpora già: **default deny**. Nessuna rotta esiste finché non la dichiari, e ogni rotta dichiarata è una superficie in più: se un agente viene compromesso da una prompt injection ([Capitolo 13](../PARTE-V-Sicurezza-costi/13-sicurezza-la-guida-che-devi-leggere.md)), le sue rotte in uscita sono i corridoi lungo i quali l'attacco si propaga al resto del team. Un Finn compromesso che non può scrivere a nessuno è un incidente; un Finn compromesso con una rotta verso Kelly — che ha le chiavi del repository — è un disastro.

Da qui la topologia consigliata: la **stella**, non la rete. Un coordinatore con rotte verso gli esecutori, gli esecutori con al più la rotta di escalation che gli serve davvero, e nessun collegamento "tanto può servire". La whitelist della sezione 12.6 — Polly verso Kelly e Max, Holly verso Kelly, e basta — è una stella con un raggio di escalation; per la maggior parte dei team personali, è tutto ciò che serve. E come ogni configurazione di sicurezza, va rivista: un giro periodico di `openclaw logs --follow` sulle conversazioni agente-agente ti dice se le rotte che hai aperto vengono usate come pensavi — fa coppia con l'audit di sicurezza del Capitolo 13.

**(!) Attenzione:** ogni regola `allow` nella config è un permesso permanente, attivo anche quando dormi: gli agenti la useranno di notte, dai cron, senza di te nel ciclo. Prima di aprire una rotta chiediti: "sono tranquillo se questi due si parlano da soli alle 3 del mattino, al peggio delle loro capacità?". Se la risposta è no, la rotta non si apre — o si apre con un `max-turns` stretto e un'azione vincolata all'approvazione umana.

**Prompt pronto:**
> "Voglio impostare un pattern coordinatore tra [Agente A, ruolo PA] e [Agente B, ruolo developer]. Quando arriva un task complesso, A lo scompone, delega la parte tecnica a B con `sessions_send`, attende il risultato e mi risponde. Aiutami a: (1) configurare il permesso A→B nella config YAML del Gateway, (2) impostare un budget massimo di 5 iterazioni per evitare loop, (3) scrivere il prompt di delega che A userà verso B, (4) testare il flusso end-to-end su un task reale."

## Errori comuni e come risolverli

**Sintomo:** loop infinito tra due agenti che si rispondono a vicenda.
Causa: nessun budget di iterazioni configurato.
Fix: impostare `max-turns` nella config del Gateway (default globale) o nel singolo `sessions_spawn`; aggiungere nei SOUL.md la regola anti-convenevoli della sezione 12.7.

**Sintomo:** l'agente A non riesce a parlare con B.
Causa: rotta A→B assente dalla whitelist nella config YAML del Gateway (un "binding" scritto in TOOLS.md viene ignorato: TOOLS.md contiene note operative, non configurazione).
Fix: aggiungere la regola `allow` nella config, riavviare con `openclaw gateway restart`, verificare gli agenti con `openclaw agents list`.

**Sintomo:** messaggio duplicato in un gruppo (due agenti rispondono).
Causa: mention gating assente o due agenti "owner" sovrapposti.
Fix: mention gating attivo + un solo agente designato come owner del gruppo.

**Sintomo:** il pattern coordinatore non scala.
Causa: il coordinatore diventa collo di bottiglia.
Fix: trasformare task indipendenti in `sessions_spawn` paralleli invece che sequenziali.

**Sintomo:** lo spawn si chiude ma il risultato è incompleto o assente.
Causa: `max-turns` troppo basso per il task, o incarico troppo largo.
Fix: alzare il budget per quell'incarico, oppure spezzare il task in spawn più piccoli e paralleli.

**Sintomo:** la spesa LLM raddoppia dopo l'introduzione delle deleghe.
Causa: ogni delega carica due contesti completi (token ×2) e i messaggi di delega inoltrano interi thread.
Fix: contesto minimo e formato di consegna esplicito nelle deleghe; modelli leggeri per gli esecutori; vedi [Capitolo 14](../PARTE-V-Sicurezza-costi/14-gestire-i-costi-senza-sorprese.md).

**Sintomo:** un agente riceve deleghe da rotte che non ricordavi di aver aperto.
Causa: whitelist cresciuta senza revisione, regole `allow` "tanto può servire".
Fix: tornare alla topologia a stella (sezione 12.9), rimuovere le rotte inutilizzate, audit periodico con `openclaw logs --follow`.

## Checklist di fine capitolo

- [ ] Configurato almeno un pattern coordinatore/esecutore tra due agenti
- [ ] Budget di iterazioni impostato per evitare loop infiniti
- [ ] Mention gating attivo nei gruppi multi-agente
- [ ] Testato un pattern di escalation (support → developer) su un task reale
- [ ] Le rotte agente→agente sono una whitelist esplicita nella config YAML del Gateway (default deny)
- [ ] Le decisioni irreversibili (deploy, rimborsi, invii) restano vincolate all'approvazione umana
- [ ] So riconoscere una delega e un loop nei log (`openclaw logs --follow`)
- [ ] Gli esecutori ad alto volume girano su un modello più leggero dove possibile

## Link e risorse utili

- [Documentazione ufficiale](https://docs.openclaw.ai) — reference su `sessions_send`, `sessions_spawn`, binding e routing
- [OpenClaw — Configuration reference](https://docs.openclaw.ai/gateway/configuration) — lo schema della config del Gateway: `sessions`, `shares`, binding
- [Architecting the Agentic Future](https://dev.to/mechcloud_academy/architecting-the-agentic-future-openclaw-vs-nanoclaw-vs-nvidias-nemoclaw-9f8) — pattern multi-agente a confronto
- [Use OpenClaw to Build a Business That Runs Itself](https://creatoreconomy.so/p/use-openclaw-to-build-a-business-that-runs-itself-nat-eliason) — il coordinatore Felix nella zero-human company di Nat Eliason
- [Building a Million Dollar Zero Human Company](https://www.bankless.com/podcast/building-a-million-dollar-zero-human-company-with-openclaw-nat-eliason) — il ciclo di revisione notturna di Felix raccontato da Eliason

Per l'elenco completo delle fonti del libro, vedi [Appendice E](../Appendici/E-risorse-e-link-utili.md).

---

[← Capitolo 11](./11-progettare-il-tuo-team-di-agenti.md)  ·  [Indice](../README.md)  ·  [Capitolo 13 →](../PARTE-V-Sicurezza-costi/13-sicurezza-la-guida-che-devi-leggere.md)
