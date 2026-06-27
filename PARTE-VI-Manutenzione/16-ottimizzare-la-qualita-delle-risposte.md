# Capitolo 16 — Ottimizzare la qualità delle risposte [★★]

## Cosa imparerai

- Come editare SOUL.md per affinare personalità e confini
- Prompt engineering per agenti autonomi vs. chatbot
- Memory management: cosa far ricordare e cosa far dimenticare
- Come scegliere il modello giusto per ogni agente

## Prerequisiti

Aver fatto l'onboarding del tuo agente ([Capitolo 7](../PARTE-III-Primo-mese/07-prima-conversazione-onboarding-agente.md)) e averlo manutenuto per qualche settimana ([Capitolo 15](./15-care-and-feeding-tenere-l-agente-in-salute.md)). Devi avere abbastanza risposte reali da poter giudicare cosa migliorare.

## Contenuto principale

### Da vivo a bravo: il lavoro di cesello

Dopo qualche settimana di convivenza arriva un momento preciso: l'agente funziona — il Gateway è su, i cron scattano, il backup esiste — ma le risposte ti lasciano una vaga insoddisfazione. Polly risponde correttamente, però il digest mattutino è il triplo del necessario; ogni rifiuto comincia con tre righe di scuse; e ieri ha riassunto un'email delicata con il tono di un comunicato stampa. Niente è *rotto*. È tutto, semplicemente, mediocre.

Il Capitolo 15 ti ha insegnato a tenere l'agente **vivo**; questo capitolo ti insegna a renderlo **bravo**. La buona notizia è che la qualità delle risposte non è una proprietà misteriosa del modello: per la maggior parte vive in cose che puoi aprire con un editor di testo. I file di identità (SOUL.md e AGENTS.md su tutti), il modo in cui scrivi le istruzioni, la cura della memoria e la scelta del modello sono le quattro leve di questo capitolo. Nessuna richiede di scrivere codice; tutte richiedono il lavoro di cesello promesso nel Capitolo 7 — fatto però con metodo, non a tentoni.

### SOUL.md e AGENTS.md: il chi e il come

Il Capitolo 2 ha fissato la distinzione su cui si regge tutto il resto: **SOUL.md descrive chi è l'agente, AGENTS.md descrive come lavora**. "Sii ironica e usa l'understatement" è anima; "rispondi sempre sotto le 200 parole" è contratto di lavoro. Sembra una sottigliezza da editori, ma è la prima causa di agenti che migliorano a strappi: se mischi i due piani, ogni ritocco al tono rischia di rompere una procedura, e viceversa.

La conseguenza pratica è che ogni difetto che osservi nelle risposte ha un file di destinazione preciso. Prima di scrivere una riga, chiediti *dove va* la correzione:

| Il problema riguarda… | Il file giusto |
|---|---|
| tono, carattere, valori, confini | SOUL.md |
| procedure, soglie, ordine di lavoro | AGENTS.md |
| fatti stabili su di te | USER.md |
| fatti imparati nel tempo | MEMORY.md |
| come usare un tool o una skill | TOOLS.md |

Un esempio concreto. Polly ha mandato un'email a un cliente senza fartela leggere: il divieto ("mai inviare email senza approvazione") è un confine non negoziabile e va nel SOUL.md, sezione Boundaries. Polly ha scritto l'email giusta ma l'ha mandata dall'account personale invece che da quello di lavoro: quella è una nota operativa su un tool, e va in TOOLS.md. Polly è stata sgarbata: è una questione di voce, SOUL.md, sezione Vibe. La tabella sembra banale, ma usarla con disciplina è ciò che distingue un workspace che migliora da uno che si ingarbuglia.

### Le quattro sezioni di un SOUL.md che funziona

Un SOUL.md efficace non è un tema libero: la community ha convergito su quattro sezioni, le stesse che trovi negli schemi dell'[Appendice C](../Appendici/C-template-soul-identity.md) e nel mini-SOUL.md del capitolo extra HomeClaw. Vediamole con esempi di contenuto reale.

**Core Truths — le verità fondamentali.** Chi è l'agente, per chi lavora, quale principio guida ogni sua decisione quando le regole non bastano. È la sezione che il modello "consulta" nei casi non previsti, quindi va scritta come una bussola, non come un regolamento:

```markdown
## Core Truths
- Lavori per Angelo, consulente freelance.
- Proteggi il suo tempo: ogni interruzione
  deve valere più di ciò che interrompe.
- Se non sei sicura, chiedi: una domanda
  costa meno di un errore.
```

**Boundaries — i confini non negoziabili.** Cosa l'agente non fa *mai*, qualunque cosa gli venga chiesto, da te o — peggio — da un contenuto esterno. È la sezione più importante per la sicurezza: come hai visto nel [Capitolo 13](../PARTE-V-Sicurezza-costi/13-sicurezza-la-guida-che-devi-leggere.md), i Boundaries sono anche la prima linea di difesa contro la prompt injection:

```markdown
## Boundaries
- Mai inviare email senza approvazione.
- Mai menzionare prezzi o trattative
  in canali di gruppo.
- Temi medici e finanziari: solo nel DM
  con Angelo, mai altrove.
```

**Vibe — la voce.** Come parla: registro, calore, ironia, gestione degli errori. È lo stesso nome che trovi nei template dell'Appendice C. Attenzione alla trappola già segnalata nel Capitolo 2: "diretta e calda, mai apologetica" è Vibe; "massimo 200 parole" è una regola operativa e va in AGENTS.md:

```markdown
## Vibe
- Diretta e calda. Niente formule di
  cortesia, niente scuse ripetute.
- Una battuta ogni tanto va bene; mai
  nei messaggi che riportano problemi.
```

**Continuity — la memoria intenzionale.** Cosa deve sopravvivere tra le sessioni e dove. Questa sezione fa da ponte verso il sistema di memoria che vediamo tra poco:

```markdown
## Continuity
- A fine giornata annota decisioni e
  promesse nella nota giornaliera.
- Le preferenze nuove vanno in MEMORY.md,
  non lasciate nella chat.
```

E le regole operative? Vanno nell'altro file. Un estratto di AGENTS.md coerente con il SOUL.md qui sopra:

```markdown
# AGENTS — Polly (estratto)
- Prima di rispondere leggi USER.md,
  MEMORY.md e le note di oggi e ieri.
- Risposte sotto le 200 parole, salvo
  richiesta esplicita.
- Azioni sopra 0,50 € di costo stimato:
  chiedi conferma prima di eseguire.
- Email: prepara la bozza, non inviare.
```

**(i) Pro tip:** ogni riga di SOUL.md e AGENTS.md viene ricaricata a ogni chiamata e pagata in token (è l'equazione del [Capitolo 14](../PARTE-V-Sicurezza-costi/14-gestire-i-costi-senza-sorprese.md)). Un SOUL.md sotto le 100 righe non è solo più economico: è anche più efficace, perché il modello rispetta meglio dieci regole nette di cinquanta regole diluite. Se il file cresce, consolida invece di aggiungere.

### Versionare l'anima: il SOUL.md come codice

Il [Capitolo 15](./15-care-and-feeding-tenere-l-agente-in-salute.md) ha messo il workspace sotto Git per la manutenzione: diff, rollback chirurgico, specchio off-site su un repo privato (e i segreti rigorosamente fuori). Per il lavoro di qualità, quello stesso Git diventa il tuo laboratorio. La pratica in più è una sola: **un tag prima di ogni esperimento**:

```bash
cd ~/.openclaw/workspace-polly
git add SOUL.md AGENTS.md
git commit -m "soul: shorter replies, no apologies"
git tag soul-2026-05-25
```

Da quel momento ogni iterazione è reversibile riga per riga: se la modifica peggiora le cose, `git checkout soul-2026-05-25 -- SOUL.md` riporta indietro solo l'anima, senza toccare memoria e note. E `git log --oneline SOUL.md` diventa la storia documentata del carattere del tuo agente — leggerla dopo tre mesi è istruttivo quanto rileggere le conversazioni.

C'è un dettaglio operativo che brucia ore ai principianti: i file canonici vengono caricati **all'inizio della sessione**. Se editi il SOUL.md mentre una conversazione è aperta, l'agente continua a usare la versione che ha in testa. Per forzare la rilettura immediata scrivi **`/reload`** nel canale — un comando slash come il `/status` del Capitolo 14 — oppure avvia una sessione nuova. È il primo controllo da fare quando "la modifica non ha funzionato": nove volte su dieci ha funzionato benissimo, ma non è mai stata letta.

**(!) Attenzione:** puoi chiedere all'agente di migliorare il proprio SOUL.md — il prompt a fine capitolo fa esattamente questo — ma con due paletti fissi. Primo: l'agente **propone il diff, tu lo applichi**; un agente che riscrive da solo la propria anima è un esperimento divertente finché un giorno non si "semplifica" via un Boundary. Secondo: **una modifica alla volta**. Se cambi tono, soglie e memoria nello stesso commit, non saprai mai quale dei tre ha migliorato (o peggiorato) le risposte.

### Prompt engineering per agenti: obiettivi, non comandi

Le tecniche di prompt che conosci dai chatbot reggono male qui, per una ragione strutturale: un chatbot risponde a un prompt che tu scrivi al momento, un agente autonomo decide *quando* e *come* agire mentre tu dormi. Le istruzioni nei file devono funzionare alle 3 di notte, senza di te, su casi che non hai previsto. Sei principi pratici, distillati da chi scrive SOUL.md da mesi (il riferimento della community è il metodo che Nat Eliason ha raccontato per i suoi agenti-business — vedi le fonti a fine capitolo).

**1. Scrivi obiettivi, non comandi.** "Assicurati che nessuna email importante venga persa" è meglio di "leggi la posta ogni ora": il comando si rompe appena il contesto cambia (la posta arriva su due account, il controllo orario non basta il giorno della scadenza), l'obiettivo lascia all'agente la libertà di adattare il mezzo al fine.

**2. Spiega il perché, non solo il cosa.** Una regola motivata generalizza: "Non scrivere ai clienti dopo le 21, molti sono all'estero e le notifiche notturne irritano" insegna all'agente a gestire anche il caso del cliente a New York alle 15 italiane. La regola nuda "non scrivere dopo le 21" no.

**3. Dai esempi netti.** Il modello impara più da una coppia giusto/sbagliato che da tre paragrafi astratti. Il SOUL.md di HomeClaw (capitolo extra) lo fa sistematicamente: «Esempio da non fare: 'temperatura **22°C**'. Esempio da fare: 'ventidue gradi'». Copia il pattern: ogni regola importante merita il suo mini-esempio.

**4. Anticipa gli edge case.** Cosa fa l'agente se la richiesta è ambigua? Se due regole confliggono? Se un tool fallisce a metà? Ogni caso limite non scritto è una decisione che il modello prenderà da solo — e la prenderà in modo diverso ogni volta. Una riga come "se un'azione è ambigua e irreversibile, fermati e chiedi" copre da sola una famiglia intera di incidenti.

**5. Rendi esplicite le priorità.** Quando le regole confliggono — e prima o poi confliggono — l'agente deve sapere quale vince. Una gerarchia dichiarata ("in ordine: sicurezza, privacy, accuratezza, velocità") trasforma un conflitto imprevedibile in una scelta deterministica.

**6. Una regola, una riga, verificabile.** "Sii professionale" non è verificabile; "niente emoji nei messaggi di lavoro" sì. Se non puoi guardare una risposta e dire *questa regola è stata rispettata: sì/no*, la regola non sta guidando niente — sta solo occupando token.

Per vedere i principi all'opera, una riscrittura reale. Prima: "Polly, gestisci bene le email." Dopo:

```markdown
- Obiettivo: nessuna email dei mittenti in
  USER.md → priority_list resta senza
  risposta per più di 4 ore lavorative.
- Perché: sono clienti attivi; il silenzio
  costa più di una risposta interlocutoria.
- Se non sai cosa rispondere, proponi a me
  una bozza invece di aspettare.
```

Stessa intenzione, ma adesso è un obiettivo misurabile, con il suo perché e il suo edge case. È questa la differenza tra un agente che "più o meno ci prende" e uno affidabile.

### Memoria: cosa ricordare, cosa dimenticare

La qualità delle risposte degrada in due modi opposti: l'agente che dimentica e l'agente che ricorda *troppo* — contesto stantio, fatti superati, note di tre mesi fa ricaricate ogni giorno. Il memory management è l'arte di stare nel mezzo.

Il modello di riferimento lo hai incontrato nel [Capitolo 7](../PARTE-III-Primo-mese/07-prima-conversazione-onboarding-agente.md): i tre livelli di Nat Eliason. Qui interessa la mappa sui file reali di OpenClaw, perché è sui file che si interviene. Il **knowledge graph** — il termine usato nel prompt di auto-diagnosi del Capitolo 15 — non è una tecnologia esotica: è la struttura di cartelle e file Markdown che organizzi *tu* nel workspace (per esempio col metodo PARA), con i dossier su progetti, clienti e persone; l'agente la legge su richiesta, non automaticamente. Le **note giornaliere** sono i file `memory/YYYY-MM-DD.md`: OpenClaw carica oggi e ieri a ogni sessione, ed è lì che vive il contesto operativo. La **conoscenza tacita** — preferenze, abitudini, regole non scritte — si deposita in MEMORY.md (i fatti che l'agente impara) e nel SOUL.md (i tratti che tu promuovi a carattere, via la sezione Continuity).

Da questa mappa discendono le tre operazioni di cura, in ordine di frequenza:

- **Salvare (continuo).** I fatti durevoli emersi in conversazione devono finire in MEMORY.md, non restare nella chat: la storia di sessione si compatta e si perde, i file no. Se l'agente non lo fa da solo, diglielo esplicitamente ("salvalo in MEMORY.md") finché la sezione Continuity non lo rende un'abitudine.
- **Archiviare (mensile).** Le note giornaliere più vecchie di qualche settimana vanno spostate in una cartella `memory/archive/`: escono dal carico quotidiano ma restano consultabili su richiesta. Archiviare, non cancellare: il contesto storico torna utile nei momenti più imprevisti. Il cron di compaction che automatizza il giro è nel [Capitolo 18](../PARTE-VII-Uso-avanzato/18-cron-job-e-automazioni-avanzate.md).
- **Correggere (quando serve).** Un fatto sbagliato in MEMORY.md è peggio di un fatto mancante, perché l'agente lo ripeterà con sicurezza. Quando l'agente "ricorda male", la cura non è ripeterglielo in chat: è aprire MEMORY.md e correggere la riga.

C'è infine la memoria che non è nei file: la **storia di sessione**. Una conversazione tenuta aperta per settimane accumula contesto morto che paghi a ogni messaggio e che diluisce le istruzioni recenti. La regola del Capitolo 14 vale anche per la qualità, non solo per i costi: sessioni nuove spesso, e ciò che merita di sopravvivere va nei file di memoria, non nella chat infinita.

**(#) Debug:** l'agente ignora una preferenza che giuri di avergli dato? Prima di toccare il SOUL.md, trova *dove* è finita: `grep -ri "parola-chiave" ~/.openclaw/workspace-polly/` ti dice in tre secondi se la preferenza è in un file canonico, in una nota archiviata o da nessuna parte (era rimasta nella chat). La griglia dei quattro strati del Capitolo 2 fa il resto.

**Prompt pronto:**
> "Fai pulizia della tua memoria. Leggi MEMORY.md e le note degli ultimi 30 giorni in `memory/` e proponi tre liste: (1) fatti obsoleti o sbagliati da correggere, (2) note giornaliere da spostare in `memory/archive/`, (3) preferenze emerse nelle conversazioni che meritano di essere promosse in MEMORY.md. Non modificare nulla senza la mia conferma."

### Il modello giusto per ogni agente

Fino al 4 aprile 2026 molti sceglievano il modello una volta sola — "il più potente che la sottoscrizione copre" — e non ci pensavano più. Il ban di Anthropic ha cambiato la domanda: ora che su Claude si paga per token, la scelta del modello è una decisione di qualità *e* di budget, da prendere agente per agente e task per task. I conti dettagliati sono nel Capitolo 14; qui interessa il criterio:

| Lavoro | Modello adatto |
|---|---|
| ragionamento complesso | Claude Opus 4.6 |
| task quotidiani | Sonnet 4.6, GPT-5.1 |
| heartbeat e cron | Haiku, Flash, Kimi K2.5 |
| privacy totale | Nemotron locale |

Tradotto in pratica: **Claude Opus 4.6** (via API key) per il ragionamento difficile e le decisioni delicate — è il più costoso e va usato con parsimonia, su richiesta e non come default. **Claude Sonnet 4.6** — il default di questo libro — o **GPT-5.1** per il lavoro quotidiano. **Claude Haiku, Gemini Flash, Kimi K2.5, MiniMax M2.5** per heartbeat, cron e task ripetitivi: rispondere `HEARTBEAT_OK` non richiede un premio Nobel, e i battiti sono quasi il 40% dei token della giornata (i conti sono nel Capitolo 14). **Nemotron (Nvidia) o Llama in locale** per gli agenti che trattano dati che non devono uscire di casa: qualità inferiore sui task complessi, ma costo zero per token e privacy totale. Infine la **sottoscrizione ChatGPT Pro** ($200/mese, ~€185) resta l'alternativa flat-rate per gli agenti ad alto volume. Il routing che assegna i modelli — globale, per agente, per tipo di task — si configura nella config del Gateway: lo YAML completo è nel Capitolo 14.

**(i) Pro tip — aggiornamento giugno 2026:** per la fascia premium sono nel frattempo usciti **Claude Opus 4.8** e **Fable 5** (lato OpenAI **GPT-5.2**); il criterio di assegnazione resta identico, cambia solo l'etichetta del modello di punta.

Il punto che riguarda *questo* capitolo è un altro, e sorprende tutti la prima volta: **il SOUL.md si tara sul modello**. Claude e GPT non rispondono allo stesso modo alle stesse istruzioni: uno prende alla lettera gli esempi, l'altro pesa di più le regole astratte; uno eccede in cautela, l'altro in iniziativa. Se cambi modello a un agente — per costi, per il ban, per curiosità — metti in conto una settimana di ri-taratura: rilancia il tuo test set (arriva nella prossima sezione), osserva dove il tono o l'obbedienza alle regole sono cambiati, e ritocca. Un SOUL.md eccellente su Sonnet può produrre risposte legnose su un modello economico: non è un peggioramento del tuo lavoro, è un destinatario diverso che legge le stesse istruzioni.

### Il ciclo di miglioramento settimanale

Tutto quanto sopra diventa un metodo solo se ha un ritmo. Il ciclo che funziona è settimanale — si aggancia bene al tagliando del Capitolo 15: prima i cinque minuti di meccanica, poi il quarto d'ora di qualità. Cinque passi:

1. **Rileggi le conversazioni della settimana.** Venti–trenta risposte bastano. Cerchi i pattern, non gli episodi: l'errore che si ripete tre volte è un difetto dei file, quello capitato una volta è rumore.
2. **Classifica ogni difetto col suo file.** Usa la tabella della sezione "il chi e il come": tono → SOUL.md, procedura → AGENTS.md, fatto sbagliato → MEMORY.md, uso errato di un tool → TOOLS.md.
3. **Una modifica alla volta**, commit e tag come visto sopra. Le micro-modifiche settimanali battono la grande riscrittura trimestrale: sono diagnosticabili, reversibili e non destabilizzano il resto.
4. **Rilancia il test set.** Tieni in un file del workspace 5–10 prompt-tipo che rappresentano il lavoro vero del tuo agente — il digest, il brief cliente, la domanda ambigua, il caso limite che una volta l'ha mandato in tilt. Dopo ogni modifica, rilanciali e confronta: è l'unico modo per capire se l'iterazione ha migliorato qualcosa o ha solo cambiato aria.
5. **Giudica dopo una settimana, non dopo un'ora.** La prima risposta dopo un ritocco è sempre promettente; quella che conta è la ventesima.

L'asso nella manica è che il tuo agente può fare con te la parte più noiosa del lavoro: l'analisi. Ha accesso alle proprie conversazioni e ai propri file, e chiedergli di proporre il diff — mai di applicarlo — è il modo più rapido di iniziare il ciclo. Il prompt qui sotto è pensato esattamente per il passo 1 e 2.

**Prompt pronto:**
> "Aiutami a migliorare il tuo SOUL.md. Analizza le ultime 20 risposte che mi hai dato e identifica: (1) dove sei stato troppo prolisso, (2) dove hai usato un tono inappropriato (troppo formale, troppo casual, troppo apologetico), (3) dove hai violato un mio confine implicito. Proponi 3-5 aggiunte concrete al SOUL.md, mostrandomi il diff esatto da applicare e spiegandomi il perché di ognuna."

## Errori comuni e come risolverli

**Sintomo:** risposte ancora generiche dopo aver editato SOUL.md.
Causa: SOUL.md non riletto nella sessione corrente.
Fix: forzare la rilettura con `/reload` (o aprire una sessione nuova) e verificare che le modifiche siano davvero in `~/.openclaw/workspace-<nome>/SOUL.md`.

**Sintomo:** l'agente "ricorda" cose vecchie sbagliate.
Causa: knowledge graph stantio, note obsolete non archiviate.
Fix: pulizia mensile: archiviare invece di cancellare per non perdere il contesto storico; correggere a mano le righe sbagliate di MEMORY.md.

**Sintomo:** cambio modello peggiora le risposte.
Causa: SOUL.md tarato sul modello precedente.
Fix: rivedere SOUL.md per il nuovo modello (Claude e GPT rispondono diversamente agli stessi prompt) e rilanciare il test set.

**Sintomo:** difficile capire quali iterazioni hanno migliorato.
Causa: nessun test set di prompt di riferimento.
Fix: tenere un set di 5-10 prompt-tipo da rilanciare dopo ogni modifica per confronto.

**Sintomo:** una regola nuova viene rispettata a giorni alterni.
Causa: regola nel file sbagliato (es. procedura operativa nel SOUL.md) o formulata in modo vago e non verificabile.
Fix: spostarla nel file giusto (tabella della sezione "il chi e il come") e riscriverla con obiettivo, perché ed esempio netto.

**Sintomo:** dopo mesi di ritocchi il SOUL.md è un patchwork contraddittorio.
Causa: aggiunte stratificate senza mai rileggere il file per intero.
Fix: una volta al mese rileggere e consolidare tutto il SOUL.md; `git log SOUL.md` mostra dove si sono accumulati gli strati.

## Checklist di fine capitolo

- [ ] SOUL.md versionato in Git (anche solo locale)
- [ ] Almeno una iterazione settimanale di affinamento prevista
- [ ] Memory management attivo: so cosa salvare, cosa archiviare, cosa eliminare
- [ ] Modello scelto in modo consapevole per ogni agente (non solo "il più potente")
- [ ] Ho un set di 5-10 prompt-tipo per testare le iterazioni
- [ ] So distinguere cosa va nel SOUL.md (chi è) e cosa in AGENTS.md (come lavora), e i miei file lo rispettano
- [ ] Le mie regole sono verificabili: obiettivi con il loro perché, non comandi vaghi
- [ ] Dopo ogni modifica ai file canonici forzo la rilettura con `/reload` o con una sessione nuova

## Link e risorse utili

- [Use OpenClaw to Build a Business That Runs Itself](https://creatoreconomy.so/p/use-openclaw-to-build-a-business-that-runs-itself-nat-eliason) — come Nat Eliason scrive i SOUL.md dei suoi agenti
- [Documentazione ufficiale](https://docs.openclaw.ai) — best practice di prompt e memoria a tre livelli
- [SOUL.md & Identity — Designing Your Agent's Personality](https://learnopenclaw.com/core-concepts/soul-md) — guida pratica alla scrittura delle quattro sezioni
- [OpenClaw Memory Masterclass](https://velvetshark.com/openclaw-memory-masterclass) — VelvetShark, la memoria che sopravvive alle sessioni
- [Memory concepts](https://github.com/openclaw/openclaw/blob/main/docs/concepts/memory.md) — i quattro strati di memoria nella documentazione del repo
- [Building a Million Dollar Zero Human Company](https://www.bankless.com/podcast/building-a-million-dollar-zero-human-company-with-openclaw-nat-eliason) — Nat Eliason racconta il sistema a tre livelli dei suoi agenti

Per l'elenco completo delle fonti del libro, vedi [Appendice E](../Appendici/E-risorse-e-link-utili.md).

---

[← Capitolo 15](./15-care-and-feeding-tenere-l-agente-in-salute.md)  ·  [Indice](../README.md)  ·  [Capitolo 17 →](../PARTE-VII-Uso-avanzato/17-creare-skill-personalizzate.md)
