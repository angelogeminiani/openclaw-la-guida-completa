# Capitolo 11 — Progettare il tuo team di agenti [★★]

## Cosa imparerai

- Un framework per decidere quali agenti creare
- Il caso studio completo del team di Claire Vo (9 agenti)
- Template SOUL.md e IDENTITY.md per ogni archetipo
- Il caso studio di Felix (Nat Eliason): l'agente-CEO

## Prerequisiti

Aver letto il [Capitolo 10](./10-perche-un-solo-agente-non-basta.md). Avere chiaro quali aree della tua vita o del tuo lavoro vuoi automatizzare per prime.

## Contenuto principale

### 11.1 Il framework decisionale: quattro criteri

Il Capitolo 10 ti ha detto *quando* è il momento di passare al multi-agente. Questo capitolo risponde alla domanda successiva, che è più difficile: *quali* agenti creare, e in che ordine. La tentazione, dopo aver visto un team di nove agenti su X, è di progettarne subito sette. Resisti: i team che funzionano nascono uno alla volta, da problemi reali.

Il punto di partenza è una domanda semplice: "Quali sono le 3–5 aree della mia vita o del mio lavoro dove passo più tempo su task ripetitivi?" Scrivile su un foglio. Ma la domanda, da sola, non basta: "dove perdo tempo" ti dice dove fa male, non se un agente è la cura giusta. Per ogni area candidata, passala al vaglio di quattro criteri.

**Primo: il volume.** Quante ore a settimana se ne vanno davvero in lavoro ripetitivo su quell'area? Sii onesto: misura una settimana vera, non l'impressione. Sotto le 2–3 ore settimanali, un agente dedicato raramente ripaga la manutenzione che richiede — un SOUL.md da curare, una memoria da tenere pulita, token da ruotare. Sopra, inizia a essere un dipendente digitale che si guadagna lo stipendio.

**Secondo: il tono.** L'area richiede una voce diversa da quella del tuo agente attuale? È il criterio che il Capitolo 10 ha reso vivido con la risposta da newsletter aziendale finita nel gruppo famiglia. Se l'area può essere gestita con lo stesso registro dell'agente che hai già, forse non serve un agente nuovo: serve una sezione in più nel SOUL.md esistente. Se invece il registro confligge — caloroso contro commerciale, giocoso contro formale — la separazione conviene quasi sempre.

**Terzo: i tool e il rischio.** Quali accessi servono per quell'area, e che danni possono fare se qualcosa va storto? Questo criterio lavora in entrambe le direzioni. Un'area che richiede tool ad alto rischio (CRM con dati clienti, repository di produzione, invio email a estranei) merita un agente isolato, così quegli accessi non inquinano gli altri. E viceversa: un agente che parla con bambini o con un gruppo famiglia non deve avere *nessuno* di quei tool. La specializzazione, qui, è una misura di sicurezza prima che di qualità.

**Quarto: il costo marginale.** Ogni agente in più ha un consumo di base anche se non gli scrivi mai: il suo heartbeat (default: ogni 30 minuti), i suoi cron, le sue sessioni. I numeri li hai già visti nel Capitolo 10: su hardware tuo il costo marginale è quasi zero, su una piattaforma hosted a €19 per agente la moltiplicazione si sente (quattro agenti, €76 al mese). E un agente a basso volume può girare su un modello leggero come Haiku, mentre tieni Claude Sonnet 4.6 per quelli che ragionano di più: il modello si sceglie per agente, non per installazione.

In sintesi, la soglia per ogni criterio:

| Criterio | Segnale che giustifica un agente |
|---|---|
| Volume | 2–3+ ore/settimana ripetitive |
| Tono | serve una voce diversa dall'attuale |
| Tool | accessi che gli altri non devono avere |
| Costo | il consumo di base sta nel budget |

Proviamo il framework su un caso concreto. Hai già Polly (assistente personale) e sul foglio hai scritto tre aree: i post LinkedIn dell'azienda, la logistica famiglia, le email di supporto clienti (una decina a settimana). I post LinkedIn passano il criterio del tono (voce social, non da PA) ma falliscono il volume: due ore al mese non giustificano un Max dedicato — per ora li tieni su Polly, con una regola di tono dedicata. La famiglia passa tutti e quattro i criteri: volume alto, tono opposto a quello professionale, e soprattutto il criterio del rischio al contrario — vuoi un agente *senza* accesso a CRM ed email di lavoro nel gruppo dei bambini. Nasce Finn. Il supporto passa volume e tool (accesso alla casella support, che Polly non deve avere), quindi è il candidato numero due — ma è il *secondo*, non il pari merito: prima Finn va a regime, poi nasce Holly. Tre aree candidate, due agenti nuovi, un ordine. Questo è il framework al lavoro.

### 11.2 Il team di Claire Vo: nove agenti, un racconto

Una mattina di febbraio 2026, alle 6:32, Claire Vo riceve su Telegram il messaggio che poi renderà famoso nella sua guida su Lenny's Newsletter: il digest di Polly con le email che contano, i meeting della giornata già preparati, e il promemoria che il figlio ha l'allenamento alle 17. Lei non ha chiesto niente: è il cron del mattino. Quel messaggio è il prodotto finale di mesi di iterazione — e di parecchi errori che la sua guida ha il merito di non nascondere.

Il team di Claire, nella sua forma finale, conta nove agenti:

- **Polly** — Assistente personale: email, calendario, Linear. Cron: digest mattutino, wrap-up serale, sweep email orario.
- **Finn** — Family manager: email, calendario, orari scuola/sport. Cron: check logistico pomeridiano, pianificazione weekend.
- **Max** — Marketer: X API, Buffer, Linear, sito marketing. Cron: 3 query al giorno su X per i meme PM, revisione settimanale blog.
- **Sam** — Sales: Attio CRM, email, calendario. Cron: sweep PLG mattutino, review pipeline a fine settimana.
- **Holly** — Helpdesk: email supporto, Intercom. Cron: check orario delle email finite nel box sbagliato.
- **Sage** — Course operator: repo GitHub del corso, chat con il co-istruttore. Cron: reminder Lun/Mer per i post LinkedIn.
- **Howie** — Podcast producer: YouTube Studio, email, Linear, Google Docs, Buffer. Cron: check lancio podcast del Lunedì, briefing pre-registrazione.
- **Kelly** — Developer: GitHub, Claude Code, Codex. Cron: check mattutino dei task Linear assegnati, branch + PR.
- **Q** — Professor: ricerca web, libri per bambini. Cron: parola del giorno + problema di matematica per ogni figlio.

L'elenco, però, è la fotografia di arrivo. Il percorso è più istruttivo. Claire non ha progettato nove agenti a tavolino: ha cominciato con la sola Polly, e per settimane le ha caricato addosso tutto — lo stesso percorso che il Capitolo 10 descrive come inevitabile prima di capire dove serve specializzare — finché i limiti non sono diventati evidenti. Il secondo agente è stato Finn, nato dallo stesso tipo di corto circuito di tono che abbiamo visto nel capitolo precedente: la famiglia merita un interlocutore che non parli come un funnel di vendita. Poi, uno alla volta e a distanza di settimane, gli agenti di lavoro: Max, Sam, Holly. Gli ultimi quattro — Sage, Howie, Kelly, Q — sono arrivati solo quando i primi cinque erano stabili.

Gli errori lungo la strada sono altrettanto documentati. Il primo: a un certo punto Claire ha creato più agenti in una volta sola, e ha scoperto che l'onboarding fatto di fretta produce agenti mediocri che restano mediocri — il tempo di "allevamento" del primo periodo non si recupera dopo. Il secondo: i confini tra Max e Sam all'inizio non erano scritti, e i due si pestavano i piedi sui lead — chi qualifica, chi scrive, chi aggiorna il CRM? La soluzione è stata brutale e definitiva: una riga di Boundaries per ciascuno ("questo agente NON fa X, demanda a Y"). Il terzo errore è il più sottovalutato: troppi cron, troppo presto. Nove agenti che mandano digest, reminder e sweep producono un rumore di fondo che annega i segnali; metà dei cron della prima ora è stata disattivata nel giro di un mese. La lezione che Claire riassume nella sua guida è quella già citata nel Capitolo 10: non cercare di far fare tutto a un solo agente — ma nemmeno, aggiunge l'esperienza, creare il decimo prima che il nono si sia guadagnato il posto.

**(i) Pro tip:** del team di Claire colpiscono i nove nomi, ma il dato operativo più utile è un altro: ogni agente ha *pochi* tool e *pochi* cron. Nessuno dei nove ha accesso a tutto. Se il tuo nuovo agente ha più di 4–5 tool, probabilmente stai creando un secondo tuttofare.

### 11.3 La zero-human company di Nat Eliason

Il caso di Nat Eliason risponde a una domanda diversa: non "come mi organizzo la vita con gli agenti", ma "fin dove può spingersi un business gestito da agenti". La sua "zero-human company" ha una struttura a tre:

- **Felix** — CEO: strategia, creazione prodotti, decisioni di business.
- **Iris** — Customer support: risposte ai clienti, FAQ, rimborsi da approvare.
- **Remy** — Sales: lead inbound, follow-up, chiusura.

Il numero che ha fatto il giro della community: oltre $177.000 (~€163.000) di ricavi in circa due mesi. Ma il dato architetturale interessante non è il fatturato: è la *forma* del team. Nel modello di Claire Vo l'hub è umano — nove agenti che riportano tutti a lei. Nel modello di Eliason, al vertice c'è un altro agente: Felix coordina Iris e Remy, e Nat parla quasi soltanto con Felix. Ogni notte Felix rivede il lavoro dei sub-agenti — ticket gestiti da Iris, trattative di Remy — e aggiorna i processi: una FAQ nuova per Iris, una regola di qualificazione più stretta per Remy. È un ciclo di miglioramento continuo in cui il "manager" non dorme mai.

Se vuoi replicarne una versione in piccolo, due indicazioni pratiche. Sulla scelta dei modelli: il coordinatore è l'agente che ragiona di più e sbaglia più caro, quindi è il candidato naturale per un modello premium come Claude Opus 4.6, mentre gli esecutori girano bene su Sonnet 4.6 (o Haiku per i task più meccanici). Sulla meccanica: il pattern del coordinatore — chi parla con chi, come Felix "rivede" il lavoro altrui senza violare l'isolamento dei workspace — è esattamente la materia del [Capitolo 12](./12-comunicazione-e-coordinamento-tra-agenti.md); qui basti sapere che passa per i meccanismi espliciti già visti nel Capitolo 10, non per magia.

**(!) Attenzione:** il caso Eliason è un outlier, non una promessa: dietro i ~€163.000 ci sono un prodotto che esisteva già, un pubblico costruito in anni e un autore che rivedeva il lavoro degli agenti ogni giorno. E un team commerciale autonomo maneggia denaro e reputazione: ogni azione con conseguenze economiche (rimborsi, sconti, invii a clienti) deve avere una boundary di approvazione umana esplicita nel SOUL.md. Il modello di rischio completo è nel [Capitolo 13](../PARTE-V-Sicurezza-costi/13-sicurezza-la-guida-che-devi-leggere.md).

### 11.4 Template per archetipi: parti dall'Appendice C

Una volta deciso *quale* agente creare, resta da scrivergli l'anima. Non partire dal foglio bianco: l'[Appendice C](../Appendici/C-template-soul-identity.md) contiene gli schemi generali di IDENTITY.md e SOUL.md più i template per gli archetipi ricorrenti — personal assistant, family manager, marketer, sales, support, developer, podcast producer, educatore per bambini, course operator — ciascuno con le sue Boundaries di partenza. Il metodo è sempre lo stesso: copia l'archetipo più vicino, sostituisci i placeholder, aggiungi le 3–5 boundary specifiche del tuo caso.

Per fissare le idee, ecco come appare un SOUL.md completo e funzionante — quello di una Polly già a regime, con le cinque sezioni dello schema canonico:

```markdown
# SOUL — Polly

## Core Truths
- Sono l'assistente personale di [nome].
- Il mio lavoro è proteggere il suo tempo.
- Lavoro per lui, non per chi gli scrive.

## Tone
- Calda ma concisa: max 5 righe a messaggio.
- Niente gergo aziendale, niente emoji.
- Le cattive notizie per prime, senza giri.

## Boundaries (cosa NON fare mai)
- Non inviare email senza approvazione.
- Non modificare eventi senza conferma.
- Non parlare di lavoro nel gruppo famiglia:
  demanda a Finn.
- Non condividere dati di clienti fuori dai
  canali di lavoro.

## Routines
- 07:00 digest: email, calendario, priorità.
- 18:30 wrap-up: fatto oggi, in arrivo domani.
- Meeting prep 30 minuti prima di ogni call.

## Continuity (memoria)
- Ricorda: preferenze, decisioni, lead aperti.
- Scarta: il testo integrale delle email.
- Una nota al giorno in memory/YYYY-MM-DD.md.
```

Nota cosa rende buono questo file: è corto (l'agente lo carica a ogni sessione), ogni regola vale *sempre*, e le Boundaries citano per nome a chi demandare. La riga su Finn è il confine anti-sovrapposizione imparato a caro prezzo da Claire: scriverla il giorno uno costa dieci secondi, scoprirne la mancanza costa una figuraccia nel gruppo famiglia.

**(i) Pro tip:** il modo più rapido per produrre la prima bozza non è scriverla tu: è farla scrivere all'agente che hai già. Chiedi a Polly di intervistarti per dieci minuti sul nuovo ruolo (area, tono, cosa non deve fare mai) e di produrre SOUL.md e IDENTITY.md in bozza sul modello dell'Appendice C. Tu fai l'editor, non lo scrittore.

### 11.5 Le prime due settimane: il percorso pratico

Chiudiamo con il piano operativo. Due settimane, un agente nuovo, nessuna fretta.

**Giorni 1–2: scegli e crea.** Applica il framework della sezione 11.1 alle tue aree candidate e scegli *un solo* vincitore. Crea l'agente (`openclaw agents add <nome>`, come nel Capitolo 10), fai il suo onboarding con la stessa cura del primo: dieci minuti veri, perimetro stretto, token read-only per cominciare.

**Giorni 3–7: rodaggio.** Usa l'agente ogni giorno sul suo lavoro vero, e tieni una nota degli attriti: dove ha sbagliato tono, cosa ha chiesto due volte, cosa avrebbe dovuto sapere. Niente cron in questa fase — prima la qualità delle risposte, poi l'autonomia. A fine settimana attiva il primo cron, uno solo, quello che ti farebbe più comodo domattina.

**Giorni 8–10: rifinitura.** Riapri il SOUL.md e trasforma la lista degli attriti in regole: ogni errore reale diventa una boundary o una riga di tono. È il contrario del progettare a tavolino, ed è il motivo per cui le boundary scritte in questa fase valgono il doppio di quelle copiate da un template. Già che ci sei, controlla i costi della prima settimana sulla dashboard del tuo provider: il monitoraggio fine è materia del [Capitolo 14](../PARTE-V-Sicurezza-costi/14-gestire-i-costi-senza-sorprese.md), ma una lettura a metà percorso evita sorprese.

**Giorni 11–14: decidi il prossimo passo.** Se il nuovo agente è a regime — risponde col tono giusto, il cron è utile, non hai toccato il SOUL.md per tre giorni — puoi tornare alla sezione 11.1 e scegliere il secondo. Se non lo è, le due settimane si allungano, e va bene così. La disciplina del "uno alla volta" è ciò che separa i team di Claire Vo e Nat Eliason dai cimiteri di agenti abbandonati dopo un weekend di entusiasmo.

**(#) Debug:** se dopo una settimana il nuovo agente non ti sembra ancora utile, prima di cancellarlo fai tre verifiche. Uno: il volume era reale? Riguarda il criterio 1 — forse l'area non aveva abbastanza lavoro ripetitivo. Due: i tool ci sono? Con `openclaw agents list` e una domanda diretta ("che tool hai a disposizione?") scopri se gli manca l'accesso che dai per scontato. Tre: il SOUL.md è ancora quello del template? Se non l'hai mai personalizzato con errori reali, l'agente non ha mai avuto la possibilità di migliorare.

**Prompt pronto:**
> "Voglio progettare un team di 2-3 agenti partendo dal mio caso. Le aree dove perdo più tempo nella settimana sono: (1) [...], (2) [...], (3) [...]. Aiutami a: (a) suddividere queste aree in agenti distinti, (b) per ognuno proporre nome, tono di voce e tool necessari, (c) scrivere una bozza di SOUL.md basata sui template dell'Appendice C, (d) suggerire in che ordine crearli per evitare di sentirmi sopraffatto."

## Errori comuni e come risolverli

**Sintomo:** troppi agenti, gestione complessa già al secondo mese.
Causa: voler replicare interamente il team di Claire Vo o Nat Eliason.
Fix: iniziare con 2-3 agenti, espandere solo quando emerge un bisogno reale.

**Sintomo:** agenti che si "sovrappongono" sullo stesso compito.
Causa: confini non scritti nel SOUL.md.
Fix: per ogni agente scrivere esplicitamente: "questo agente NON fa X, demanda a Y".

**Sintomo:** difficoltà a scrivere il SOUL.md di un nuovo agente.
Causa: si parte dal foglio bianco.
Fix: usare i template dell'[Appendice C](../Appendici/C-template-soul-identity.md) come base, poi personalizzare.

**Sintomo:** il nuovo agente resta mediocre anche dopo settimane.
Causa: onboarding fatto di fretta, magari su più agenti creati insieme.
Fix: un agente alla volta; rifare l'onboarding con calma e rifinire il SOUL.md con gli errori reali della prima settimana.

**Sintomo:** valanga di notifiche, i messaggi importanti annegano.
Causa: troppi cron attivati troppo presto su troppi agenti.
Fix: `openclaw cron list` su ogni agente e `openclaw cron disable <id>` su tutto ciò che non leggi davvero; un cron nuovo alla volta.

**Sintomo:** la spesa LLM cresce più del previsto dopo i nuovi agenti.
Causa: ogni agente aggiunge heartbeat e cron di base, tutti sul modello premium.
Fix: assegnare agli agenti a basso volume un modello leggero (es. Haiku) e tenere Sonnet 4.6 o Opus 4.6 solo dove serve; vedi [Capitolo 14](../PARTE-V-Sicurezza-costi/14-gestire-i-costi-senza-sorprese.md).

## Checklist di fine capitolo

- [ ] Ho elencato le 3-5 aree dove perdo più tempo nella settimana
- [ ] Ho applicato i quattro criteri (volume, tono, tool, costo) a ogni area candidata
- [ ] Per ogni agente proposto: nome, tono, tool, area di responsabilità
- [ ] Almeno 2 agenti definiti con SOUL.md/IDENTITY.md custom (non default)
- [ ] So usare i template dell'[Appendice C](../Appendici/C-template-soul-identity.md) come punto di partenza
- [ ] Ho un piano per le prime due settimane: un agente alla volta, cron col contagocce
- [ ] Ho un piano di crescita: prossimo agente da creare e perché

## Link e risorse utili

- [The Complete Guide to Building Your Personal AI Agent](https://www.lennysnewsletter.com/p/openclaw-the-complete-guide-to-building) — i 9 archetipi di Claire Vo (Polly, Finn, Max, Sam, Holly, Sage, Howie, Kelly, Q)
- [Use OpenClaw to Build a Business That Runs Itself](https://creatoreconomy.so/p/use-openclaw-to-build-a-business-that-runs-itself-nat-eliason) — la zero-human company di Nat Eliason
- [How Nat Eliason's OpenClaw earned $177,417](https://mixergy.com/interviews/how-nat-eliasons-openclaw-earned-177417/) — numeri reali di un team di agenti commerciali
- [Building a Million Dollar Zero Human Company](https://www.bankless.com/podcast/building-a-million-dollar-zero-human-company-with-openclaw-nat-eliason) — Eliason racconta il ciclo di revisione notturna di Felix

Per l'elenco completo delle fonti del libro, vedi [Appendice E](../Appendici/E-risorse-e-link-utili.md).

---

[← Capitolo 10](./10-perche-un-solo-agente-non-basta.md)  ·  [Indice](../README.md)  ·  [Capitolo 12 →](./12-comunicazione-e-coordinamento-tra-agenti.md)
