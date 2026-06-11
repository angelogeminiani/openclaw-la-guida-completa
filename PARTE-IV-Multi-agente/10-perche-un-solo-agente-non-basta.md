# Capitolo 10 — Perché un solo agente non basta [★★]

## Cosa imparerai

- Il principio della specializzazione applicato agli agenti AI
- Come aggiungere un nuovo agente con un comando
- Come i workspace separati garantiscono isolamento
- Come trasferire conoscenza tra agenti

## Prerequisiti

Avere già un agente attivo ([Capitolo 7](../PARTE-III-Primo-mese/07-prima-conversazione-onboarding-agente.md)) e averlo usato per almeno una settimana, così da capire dove serve davvero specializzare.

## Contenuto principale

### 10.1 Il problema dell'agente tuttofare

Facciamo un salto in avanti di un mese rispetto al Capitolo 7. Polly, la tua assistente personale, funziona. Il digest mattutino arriva puntuale alle 7:02, il meeting prep è diventato un riflesso condizionato, e hai smesso di controllare il calendario a mano. Funziona così bene che hai iniziato a caricarle addosso tutto il resto: il calendario editoriale dei post LinkedIn, il follow-up dei lead che compilano il form sul sito, la logistica del weekend con la famiglia, il monitoraggio dei competitor.

Poi una sera succede una cosa piccola ma rivelatrice. Nel gruppo Telegram di famiglia qualcuno chiede a che ora è la visita dal dentista del piccolo, e Polly risponde con un tono da newsletter aziendale: "Ottima domanda! L'appuntamento è confermato per giovedì alle 16:30. Vuoi che prepari un riepilogo dei prossimi appuntamenti sanitari della famiglia?". Tecnicamente corretto. Umanamente, fuori posto: è il tono che le hai insegnato per i lead, finito nella chat sbagliata.

Se apri il suo `SOUL.md` capisci perché. In un mese è cresciuto fino a una sessantina di regole, e alcune si contraddicono: "sii calorosa e informale" (scritta pensando alla famiglia) convive con "sii sintetica e professionale, chiudi sempre con una call to action" (scritta pensando ai lead). La memoria è messa anche peggio: nelle note giornaliere di `memory/` il pricing in revisione del cliente Rossi sta a tre righe dall'orario dell'allenamento di calcio dei bambini. Ogni sessione carica tutto questo contesto — e lo paghi due volte: in token a ogni richiesta, e in qualità, perché l'agente deve decidere ogni volta *quale* Polly essere.

Questo degrado ha un nome informale nella community: l'agente "con troppi cappelli". Non è un bug di OpenClaw e non si risolve con un modello più potente. È il limite strutturale di un'identità che prova a coprire troppi ruoli. La soluzione non è scrivere un SOUL.md più furbo: è smettere di avere un solo agente.

### 10.2 Il principio della specializzazione

Claire Vo, che su questo problema ha costruito il caso studio più citato della community (il suo team di nove agenti, che vedremo nel [Capitolo 11](./11-progettare-il-tuo-team-di-agenti.md)), lo riassume così: "Ho scoperto che non dovresti cercare di far fare tutto a un solo agente". Un agente con un'identità stretta fa un lavoro migliore — ed è anche più divertente da usare, perché la personalità può essere calibrata sul ruolo invece che annacquata su tutti.

La metafora giusta è quella del team. Nessuna azienda assume una persona sola per fare vendite, supporto, marketing e contabilità: non perché una persona non possa imparare quattro mestieri, ma perché il cambio continuo di contesto distrugge la qualità di ognuno. Con gli agenti vale lo stesso principio, con un vantaggio in più: assumere il quinto "dipendente digitale" costa un comando, non uno stipendio.

La specializzazione paga su quattro fronti concreti. Primo, un SOUL.md corto e coerente: ogni regola vale sempre, niente più "dipende dal contesto". Secondo, memoria pulita: l'agente marketing ricorda i lead, l'agente famiglia ricorda il dentista, e nessuno dei due carica il contesto dell'altro. Terzo, sicurezza: ogni agente riceve solo i tool che servono al suo ruolo, e questo riduce la superficie di attacco — se l'agente famiglia non ha accesso al CRM, una prompt injection nel gruppo famiglia non può toccare i clienti (il modello di rischio completo è nel [Capitolo 13](../PARTE-V-Sicurezza-costi/13-sicurezza-la-guida-che-devi-leggere.md)). Quarto, manutenzione: quando qualcosa si rompe, sai subito in quale workspace guardare.

E, contrariamente all'intuizione, moltiplicare gli agenti non significa moltiplicare i costi: ci torniamo nella sezione 10.6 con i numeri.

### 10.3 Aggiungere un agente: `openclaw agents add`

Creare il secondo agente è un comando:

```bash
openclaw agents add max
```

Dietro le quinte succedono tre cose. Primo, il Gateway crea il workspace dedicato `~/.openclaw/workspace-max/` — il tuo primo agente vive in `~/.openclaw/workspace/`, ogni agente aggiuntivo in `~/.openclaw/workspace-<nome>/`. Secondo, dentro il workspace vengono seminati i file canonici che conosci dal [Capitolo 2](../PARTE-I-Capire-OpenClaw/02-anatomia-di-un-agente-openclaw.md), incluso un `BOOTSTRAP.md` nuovo di zecca: anche Max dovrà fare il suo rito del primo avvio, esattamente come Polly nel Capitolo 7, e anche il suo BOOTSTRAP.md si auto-cancellerà a onboarding completato. Terzo, il Gateway registra il nuovo agente nel routing, pronto per ricevere un binding (sezione 10.4).

Per verificare che la creazione sia andata a buon fine:

```bash
openclaw agents list
ls -la ~/.openclaw/workspace-max/
```

La domanda da farsi a questo punto è: che cosa è davvero separato tra Polly e Max, e che cosa invece condividono? La risposta in tabella:

| Isolato per agente | Condiviso |
|---|---|
| SOUL, IDENTITY, USER, AGENTS | il processo Gateway |
| TOOLS.md e skill installate | la config YAML del Gateway |
| `memory/` e MEMORY.md | credenziali dei provider LLM |
| cron e HEARTBEAT.md | la macchina (CPU, disco) |
| sessioni di conversazione | i canali fisici (i bot) |

Una precisazione sulla colonna di destra: condividere le credenziali dei provider non significa condividere il modello. Ogni agente può girare su un modello diverso — Claude Sonnet 4.6 per Polly che gestisce i clienti, Haiku per un agente che fa solo task leggeri e ripetitivi. È una delle leve di costo più efficaci del multi-agente, e la vedremo nel [Capitolo 16](../PARTE-VI-Manutenzione/16-ottimizzare-la-qualita-delle-risposte.md).

L'isolamento dei workspace non è una convenzione di cortesia: è una garanzia che il Gateway fa rispettare. Max non può leggere `~/.openclaw/workspace/` di Polly, né viceversa. Ogni agente vede solo la propria identità, la propria memoria, i propri cron. È questa garanzia che rende il multi-agente sicuro — ed è per questo che il trasferimento di conoscenza tra agenti (sezione 10.5) passa per meccanismi espliciti, mai per l'accesso diretto al workspace altrui.

L'onboarding di Max merita la stessa cura del primo: dedicagli i suoi dieci minuti, ma con un perimetro stretto. A Max racconti il funnel, il tono dei post, i competitor; non gli racconti la famiglia, e non gli dai i tool per arrivarci.

**(!) Attenzione:** ogni agente in più è anche una identità in più da proteggere. Prima di dare a Max token e accessi, rileggi la regola del Capitolo 9: si parte sempre read-only, con lo scope minimo che serve al ruolo.

### 10.4 Routing e binding: chi risponde a chi

Ora hai due agenti, ma i messaggi devono sapere dove andare. Il meccanismo si chiama *binding*: l'associazione tra un canale (o un account, o un singolo peer) e l'agente che deve gestirlo. Il posto dove vive il binding è uno solo: la **config YAML del Gateway** — il file `~/.openclaw/config.yaml` che il wizard ha scritto durante l'installazione (Capitolo 5). Non in TOOLS.md — che, come definito nel Capitolo 2, contiene note operative in linguaggio naturale, non configurazione di routing. Se scrivi il binding in TOOLS.md, il Gateway semplicemente lo ignora.

Lo scenario classico: il Telegram personale parla con Polly, lo Slack di lavoro parla con Max.

```yaml
# ~/.openclaw/config.yaml
agents:
  polly:
    workspace: "~/.openclaw/workspace"
  max:
    workspace: "~/.openclaw/workspace-max"

bindings:
  - agent: polly
    channel: telegram
  - agent: max
    channel: slack
```

È lo stesso blocco `agents:` che hai già incontrato nel [Capitolo 4](../PARTE-II-Installazione/04-preparare-un-ambiente-sicuro-docker-sandbox.md) per il sandboxing (`agents.defaults.sandbox`): lì si configurano i default validi per tutti, qui le voci per i singoli agenti.

Dopo ogni modifica alla config, riavvia il Gateway:

```bash
openclaw gateway restart
```

Il binding può scendere anche sotto il livello del canale: lo stesso bot Telegram può instradare il gruppo famiglia verso un agente e i messaggi diretti verso un altro, usando il peer come discriminante. È il pattern già visto di sfuggita nel Capitolo 6 con il channel binding di Slack (`#sales` → Sam, `#support` → Holly): canali e gruppi diversi, agenti diversi, stesso Gateway. La sintassi esatta dei binding per peer e la comunicazione agente→agente sono materia del [Capitolo 12](./12-comunicazione-e-coordinamento-tra-agenti.md).

Una cosa che il binding *non* cambia: le sessioni restano separate per canale e per interlocutore (il default `per-channel-peer` del Capitolo 6). Dare un canale a Max non fonde le conversazioni: ogni coppia canale-persona resta un filo a sé, a meno di unificazione esplicita.

**(i) Pro tip:** lo schema esatto della config evolve con le versioni di OpenClaw. Prima di copiare blocchi YAML da guide trovate in giro (incluso questo libro), confrontali con la Configuration reference ufficiale — il link è in fondo al capitolo — e verifica la tua versione con `openclaw --version`.

### 10.5 Trasferire conoscenza senza rompere l'isolamento

C'è un'obiezione che a questo punto sorge spontanea: se i workspace sono isolati per garanzia, come fa Polly a "passare" a Max tutto quello che ha imparato sul marketing nel suo primo mese? La risposta è che la conoscenza non si copia da workspace a workspace: **si consegna**, attraverso uno dei due meccanismi espliciti previsti dal Gateway.

Il primo è `sessions_send`: il tool nativo con cui un agente recapita un messaggio alla sessione di un altro agente, passando dal Gateway. Niente accesso ai file altrui: Polly *scrive a* Max, esattamente come faresti tu, e Max decide cosa farne — tipicamente, annotarlo nella propria memoria e nei propri file di identità. Come per i binding, anche questa possibilità vive nella config YAML del Gateway: la rotta Polly→Max deve essere autorizzata da una regola esplicita (negli esempi che seguono lo diamo per fatto). È lo stesso meccanismo che nel Capitolo 12 userai per i pattern di coordinamento — sintassi della whitelist inclusa; per ora basta sapere che esiste e che è il modo canonico per far parlare due agenti.

Il secondo è la **cartella condivisa**: una directory dichiarata esplicitamente nella config del Gateway e montata per gli agenti che elenchi, utile per gli artefatti di progetto (documenti, CSV, bozze) su cui più agenti devono lavorare:

```yaml
shares:
  - path: "~/.openclaw/shared"
    agents: [polly, max]
```

Nota la differenza di filosofia: l'isolamento resta la regola, la condivisione è un'eccezione dichiarata, visibile e revocabile nella config. Mai, in nessun caso, un agente accede direttamente al workspace di un altro.

Vediamo il trasferimento in pratica. Hai creato Max e vuoi che il marketing migri da Polly a lui:

> "Polly, da oggi c'è Max: il marketing è suo. Inviagli via sessions_send tutto ciò che nel tuo SOUL.md, nelle tue memorie e nei tuoi cron riguarda il marketing — regole di tono, lead aperti, calendario editoriale, lezioni imparate. Quando Max conferma di aver registrato tutto, rimuovi quelle parti dal tuo workspace e disattiva i tuoi cron di marketing."

Cosa succede dietro le quinte: Polly rilegge i propri file, estrae le sezioni pertinenti, le impacchetta in una serie di messaggi a Max; Max le riceve nella propria sessione e le scrive nei *suoi* file — il tono dei post nel suo SOUL.md, i lead aperti nella sua memoria. Poi Polly fa pulizia da sé: snellisce il SOUL.md e disattiva i cron migrati. Puoi verificare con:

```bash
openclaw cron list
openclaw cron disable <id>
```

**(!) Attenzione:** la seconda metà del prompt — "rimuovi e disattiva" — è distruttiva. Prima di lanciare una migrazione, fai un backup di `~/.openclaw/` (la procedura completa è nel [Capitolo 15](../PARTE-VI-Manutenzione/15-care-and-feeding-tenere-l-agente-in-salute.md)): se Max ha registrato male qualcosa, vuoi poter tornare indietro.

**(#) Debug:** dopo la migrazione, fai il collaudo in tre mosse. Uno: chiedi a Max un riepilogo di quello che ha ricevuto ("Max, raccontami cosa sai dei lead aperti") e confrontalo con quello che sapeva Polly. Due: verifica con `openclaw cron list` che i cron di marketing risultino attivi per Max e disattivati per Polly — il duplicato è l'errore più comune, e produce doppi messaggi. Tre: chiedi a Polly una domanda di marketing: la risposta giusta è che ti rimandi a Max.

### 10.6 Quando NON moltiplicare gli agenti

Il multi-agente è un unlock, non un obbligo, e c'è un momento sbagliato per farlo: troppo presto. Se il tuo primo agente non ha ancora una settimana di lavoro vero alle spalle, non hai i dati per sapere *dove* serve specializzare — e rischi di progettare un team sulla carta invece che sui problemi reali.

Sul fronte costi, i numeri del Capitolo 3 aiutano a ragionare. Se OpenClaw gira su hardware tuo, gli agenti in più sono quasi gratis: quattro agenti su un Mac mini M4 costano, di elettricità e ferro, quanto uno solo — la macchina è comunque accesa e per lo più inattiva. Su una piattaforma hosted il discorso cambia: su MaxClaw, a €19 per agente al mese, quattro agenti fanno €76 al mese, e la moltiplicazione si sente (i conti completi sono nel [Capitolo 3](../PARTE-II-Installazione/03-scegliere-dove-installare-openclaw.md)). In entrambi i casi resta il costo LLM: ogni agente ha il suo heartbeat (default: ogni 30 minuti) e i suoi cron, quindi ogni agente in più aggiunge un consumo di base anche se non gli scrivi mai.

C'è poi il costo nascosto, che non si misura in euro: la manutenzione. Ogni agente è un SOUL.md da curare, una memoria da tenere pulita, un set di token da ruotare, un sospettato in più quando qualcosa si rompe. Il "care and feeding" del Capitolo 15 si moltiplica per N.

La regola pratica: crea il secondo agente quando vedi almeno uno di questi segnali — regole di tono che si contraddicono nel SOUL.md; memoria che mescola contesti che non dovrebbero toccarsi (clienti e famiglia); un'area che richiede tool ad alto rischio che il resto dell'agente non deve avere; un canale intero (lo Slack di lavoro, il gruppo famiglia) che merita un interlocutore dedicato. Se nessun segnale è acceso, un agente ben curato batte due agenti mediocri.

**Prompt pronto:**
> "Voglio creare un secondo agente specializzato accanto a te. Si chiamerà [nome], si occuperà di [area, es. "gestione famiglia"]. Aiutami a: (1) lanciare `openclaw agents add` con i parametri giusti, (2) impostare il suo workspace, IDENTITY.md e una prima bozza di SOUL.md, (3) decidere quali tool gli servono e quali esplicitamente NON deve avere, (4) instradare verso di lui i messaggi del canale [Telegram / Slack / WhatsApp]."

**(i) Pro tip:** Il multi-agente è stato il vero unlock per Claire Vo. Invece di un bot che fa tutto, un team di bot specializzati produce risultati migliori, più velocemente, con meno errori.

## Errori comuni e come risolverli

**Sintomo:** l'agente unico diventa incoerente nelle risposte: cambia tono e personalità da un messaggio all'altro.
Causa: SOUL.md sovraccarico di responsabilità diverse.
Fix: dividere in 2-3 agenti specializzati (es. uno PA, uno developer).

**Sintomo:** confusione su quale agente sta rispondendo.
Causa: nomi e canali poco distintivi.
Fix: nome + emoji distintivi + un canale dedicato per ogni agente quando possibile.

**Sintomo:** conoscenza non condivisa tra agenti.
Causa: memorie completamente isolate.
Fix: cartella condivisa configurata nel Gateway per gli artefatti comuni, oppure `sessions_send` per trasferire contesto puntualmente.

**Sintomo:** il binding scritto in TOOLS.md viene ignorato.
Causa: TOOLS.md contiene note operative, non configurazione: il routing vive nella config YAML del Gateway.
Fix: spostare il binding nella config e riavviare con `openclaw gateway restart`.

**Sintomo:** il nuovo agente non risponde sul suo canale.
Causa: binding mancante nella config, oppure onboarding mai completato.
Fix: verificare l'agente con `openclaw agents list`, controllare il blocco `bindings`, e accertarsi che il suo BOOTSTRAP.md si sia auto-cancellato (se è ancora lì, il bootstrap è fallito).

**Sintomo:** doppi messaggi dopo una migrazione di competenze.
Causa: cron duplicati — attivi sia sul vecchio sia sul nuovo agente.
Fix: `openclaw cron list` su entrambi e `openclaw cron disable <id>` sul vecchio.

## Checklist di fine capitolo

- [ ] Ho identificato almeno un'area dove serve un secondo agente
- [ ] Ho creato un secondo agente con `openclaw agents add <nome>`
- [ ] I due agenti hanno workspace, identità, tool e cron separati
- [ ] So come instradare i messaggi al giusto agente (binding/routing)
- [ ] Il binding canale→agente è nella config YAML del Gateway, non in TOOLS.md
- [ ] Ho fatto un backup di `~/.openclaw/` prima di migrare conoscenza tra agenti

## Link e risorse utili

- [The Complete Guide to Building Your Personal AI Agent](https://www.lennysnewsletter.com/p/openclaw-the-complete-guide-to-building) — come Claire Vo ha diviso il suo team in 9 agenti
- [OpenClaw — Configuration reference](https://docs.openclaw.ai/gateway/configuration) — lo schema della config del Gateway, inclusi canali e binding

Per l'elenco completo delle fonti del libro, vedi [Appendice E](../Appendici/E-risorse-e-link-utili.md).

---

[← Capitolo 9](../PARTE-III-Primo-mese/09-aggiungere-strumenti-e-integrazioni.md)  ·  [Indice](../README.md)  ·  [Capitolo 11 →](./11-progettare-il-tuo-team-di-agenti.md)
