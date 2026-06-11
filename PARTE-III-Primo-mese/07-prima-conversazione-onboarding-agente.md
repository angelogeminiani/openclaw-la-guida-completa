# Capitolo 7 — La prima conversazione: fare l'onboarding del tuo agente [★★]

## Cosa imparerai

- Cosa dire al tuo agente nei primi 10 minuti
- Come si auto-configura scrivendo i file .md
- Come dargli un nome, una personalità e un primo task
- Il mindset del "manager di agenti"

## Prerequisiti

Aver completato l'installazione ([Capitolo 5](../PARTE-II-Installazione/05-installazione-step-by-step.md)) e collegato almeno un canale ([Capitolo 6](../PARTE-II-Installazione/06-configurare-telegram-e-altri-canali.md)).

## Contenuto principale

### Dove si fa l'onboarding: TUI o Telegram?

Il Capitolo 5 si è chiuso con il primo "hatch": la TUI aperta, il lobster in ASCII art, l'agente che legge i suoi bootstrap files ancora vuoti e ti chiede di presentarti. Quel momento — la nascita — è già alle spalle, e non lo ripeteremo qui. Questo capitolo riguarda ciò che viene subito dopo, e che conta molto di più: la prima vera conversazione, quella in cui l'agente smette di essere un software appena installato e comincia a diventare *il tuo* agente.

Puoi farla in due posti, e vale la pena scegliere con cognizione. Nella **TUI**, restando sul terminale dove tutto è iniziato: è la scelta giusta per la parte "rituale" dell'onboarding, perché se qualcosa si inceppa sei nel posto migliore per accorgertene — puoi aprire una seconda finestra di terminale e guardare con `cat` i file che l'agente sta scrivendo, riga per riga. Oppure sul **canale** che hai collegato nel Capitolo 6, tipicamente Telegram: è la scelta più naturale per la parte "umana" della conversazione, perché avviene nello stesso posto dove l'agente vivrà davvero, con i tempi sciolti delle chat reali — rispondi dal divano, riprendi il filo il giorno dopo, mandi un vocale.

La regola pratica che suggerisce questo libro: **chiudi il rito di bootstrap nella TUI, fai la conversazione di conoscenza su Telegram.** Il rito (lo vediamo fra poco) è una sequenza di domande con un inizio e una fine, e conviene completarla in una sola seduta nel posto dove è partita. La conoscenza reciproca, invece, non finisce mai davvero: è fatta di messaggi sparsi nei primi giorni, e il canale di tutti i giorni è il suo habitat.

### Il cappello da manager

Prima di scrivere il primo messaggio, fermati un minuto e cambia cappello. La tentazione, dopo l'installazione, è trattare l'agente come l'ennesimo chatbot: aprire la chat e digitare "ciao, cosa sai fare?". È la domanda sbagliata, perché ribalta le responsabilità. Un chatbot è un prodotto finito che si presenta da solo; un agente OpenClaw appena nato è un *dipendente al primo giorno di lavoro*, e il primo giorno di lavoro non lo gestisce il dipendente: lo gestisce il manager. Cioè tu.

Come dice Claire Vo: "Come un dipendente, il tuo agente non può essere bravo in tutto. Pensa a un ruolo specifico." Assistente personale? Social media manager? Sviluppatore? Iniziare con un ruolo e aggiungerne altri dopo. È lo stesso principio che guiderà la Parte IV sul multi-agente: la specializzazione non è un vezzo, è il modo in cui si ottengono risposte buone. Un agente con il mansionario "fai tutto" produce risposte da "faccio tutto": generiche, prolisse, senza priorità.

L'esercizio concreto, da fare su carta prima di toccare la tastiera: scrivi le tre attività che ti rubano più tempo in una settimana tipo. Se vince il triangolo email-calendario-promemoria, il ruolo è assistente personale (l'archetipo "Polly" che questo libro usa dappertutto). Se vince la produzione di contenuti e i social, è un marketer (l'archetipo "Max"). Se vince il coordinamento della famiglia, è l'archetipo "Finn". Scegline *uno*. Gli altri diventeranno agenti a parte quando arriverai al Capitolo 10 — e a quel punto ringrazierai di non aver mescolato tutto in un solo SOUL.md.

C'è un secondo aspetto del cappello da manager che si nota meno: il manager non valuta il dipendente al primo giorno, lo *mette in condizione di lavorare*. Nei primi dieci minuti il tuo compito non è scoprire quanto è bravo l'agente; è dargli il contesto senza cui nessun collaboratore, umano o digitale, può essere bravo.

### I primi dieci minuti, narrati

Vediamo come suona un onboarding fatto bene, dall'inizio alla fine. Sono le 21:10 di un martedì di maggio 2026. Hai chiuso il rito di bootstrap nella TUI mezz'ora fa, hai collegato Telegram, e ora apri la chat con il tuo agente per la prima conversazione vera.

Cominci dalle presentazioni, come faresti con una persona: *"Ciao. Mi chiamo Gianluca, vivo a Bologna, fuso orario Europe/Rome. Faccio il product manager in una software house. Tu sarai la mia assistente personale."* Trenta secondi, e hai già consegnato quattro informazioni che l'agente userà in ogni risposta futura: nome, luogo, fuso, ruolo. Il fuso orario sembra un dettaglio burocratico ma non lo è: senza, ogni cron e ogni promemoria del Capitolo 18 partirebbe all'ora sbagliata.

L'agente risponde, chiede qualcosa su di te, e tu prosegui con la parte che vale di più: le sfide. *"Le tre cose che mi rubano tempo: una casella email che non riesco a tenere sotto controllo, troppe riunioni messe in calendario senza preavviso, e i promemoria di famiglia che dimentico. Voglio che tu mi aiuti soprattutto su queste."* Nota la forma: non stai elencando funzionalità che vorresti, stai descrivendo problemi che hai. È il modo migliore di parlare a un agente: ai problemi sa proporre soluzioni anche creative, alle richieste di funzionalità risponde in modo letterale.

Poi le preferenze di comunicazione: *"Scrivimi in italiano, risposte brevi, massimo tre o quattro frasi. Se una cosa è urgente dimmelo subito nella prima riga. Niente liste puntate se non te le chiedo."* Sembra pignoleria; è invece l'equivalente del "come preferisci ricevere i report?" che ogni buon collaboratore chiede al capo la prima settimana — solo che qui sei tu a doverlo dire senza aspettare la domanda.

E infine, la parte che troppi saltano e che è la più importante: i confini. *"Tre regole. Non inviare mai email a nome mio senza la mia approvazione esplicita. Non cancellare mai eventi dal calendario: proponi, e decido io. Se un'azione costa più di un euro, chiedimi prima."* Dieci minuti, sei ingredienti — nome, ruolo, fuso orario, sfide, preferenze, divieti — e l'onboarding essenziale è fatto. Il resto della conversazione può divagare: l'agente farà domande, tu risponderai, e ogni risposta finirà al posto giusto. Costo della seduta, con Claude Sonnet 4.6: pochi centesimi di dollaro, ben sotto $0,50 (~€0,46).

**(!) Attenzione:** i divieti che dichiari nei primi dieci minuti sono la tua rete di sicurezza per i mesi a venire. Un agente senza "non fare" espliciti prima o poi farà qualcosa che non avresti voluto — non per ribellione, ma perché nessuno gli aveva detto che non si faceva. Dichiara i divieti subito, falli scrivere nel SOUL.md, e verifica che ci siano davvero.

### L'auto-configurazione: il rito di BOOTSTRAP.md

Mentre la conversazione scorre, sotto il cofano succede una cosa precisa, che il Capitolo 2 ha già presentato e che qui vediamo all'opera. Al primo avvio OpenClaw crea nel workspace — `~/.openclaw/workspace/` per l'agente principale — un file chiamato `BOOTSTRAP.md`: è il **rito del primo avvio**. Non è un file di configurazione che scrivi tu, e non è nemmeno un file che resta: è il copione che guida l'agente nella conversazione di onboarding, e che gli dice come smistare le tue risposte nei file canonici.

Lo smistamento funziona così: quello che dici su *come l'agente appare* — il nome che gli dai, il ruolo — finisce in `IDENTITY.md`; quello che dici *su di te* — nome, città, fuso, sfide, le persone della tua cerchia — finisce in `USER.md`; quello che dici su *come deve comportarsi* — tono, lunghezza delle risposte, divieti — finisce in `SOUL.md`. Quando il rito è completo, OpenClaw cancella `BOOTSTRAP.md` da solo. La sua assenza è la prova che tutto è andato a buon fine; la sua presenza, settimane dopo, è il sintomo che il bootstrap è fallito (ci arriviamo tra un attimo).

La verifica, a fine seduta, vale i due minuti che costa. Apri un terminale:

```bash
ls ~/.openclaw/workspace/
cat ~/.openclaw/workspace/USER.md
cat ~/.openclaw/workspace/SOUL.md
```

Nel primo comando `BOOTSTRAP.md` non deve più comparire. Negli altri due cerca le tue parole: il fuso orario giusto, i tre divieti, le preferenze di tono. Se qualcosa manca o è impreciso, hai due strade equivalenti: dirlo all'agente ("nel mio USER.md manca che lavoro da remoto il venerdì: aggiungilo") oppure editare il file a mano con qualsiasi editor di testo. I file sono tuoi, e l'agente li rilegge a ogni sessione.

Due tetti da conoscere, già citati nel Capitolo 5: i bootstrap files vengono caricati fino a 150.000 caratteri complessivi, con un massimo di 20.000 per singolo file. Sopra quei limiti OpenClaw tronca in silenzio. È un motivo in più per non trasformare l'onboarding in un'autobiografia: all'agente servono i fatti operativi, non la storia della tua vita.

### Quando il rito fallisce (e come riavviarlo)

Il bootstrap può fallire per ragioni banali: hai chiuso la TUI a metà delle domande, il Gateway è stato riavviato durante il rito, sei passato a Telegram prima della fine e la sessione si è persa per strada. Il sintomo è sempre lo stesso: `BOOTSTRAP.md` è ancora nella radice del workspace giorni dopo, e l'agente sembra "vuoto" — non sa chi sei, non ha personalità, ti chiama "utente".

**(#) Debug:** la procedura di ripartenza è meno drammatica di quanto sembri. Primo: verifica il sintomo con `ls ~/.openclaw/workspace/` — se `BOOTSTRAP.md` c'è ancora, il rito è aperto. Secondo: apri la TUI con `openclaw` e riprendi la conversazione da dove si era interrotta; l'agente rilegge il copione e ricomincia a fare domande. Terzo: completa il rito *in quella seduta*, senza cambiare canale a metà. Quarto: verifica che il file sia sparito e che `IDENTITY.md`, `USER.md` e `SOUL.md` contengano le tue risposte. Se la TUI non riaggancia il rito, `openclaw doctor` segnala lo stato dei bootstrap files, e nel caso peggiore puoi rilanciare il wizard con `openclaw onboard` come nel Capitolo 5 — in tal caso, prima di rispondere alle domande, controlla con `cat` cosa contengono già i file di identità, così ti accorgi subito se qualcosa viene sovrascritto.

### Nome, emoji, vibe

Con i file di base al loro posto, arriva la parte divertente: dare all'agente un'identità riconoscibile. Non è folklore. Un nome proprio cambia il modo in cui *tu* tratti l'agente — si delega più volentieri a "Polly" che a "openclaw-main" — e nei setup multi-agente della Parte IV diventa pura necessità: quando gli agenti sono sei, i nomi sono l'unico modo per non perdersi.

La community ha già i suoi classici. "Polly" è l'assistente personale del caso studio di Claire Vo, che incontrerai per esteso nel Capitolo 11 insieme al resto del suo team. "Felix" è l'agente-business di Nat Eliason, quello della storia raccontata nel podcast Bankless. "Max" è l'archetipo del marketer che questo libro usa negli esempi. Non c'è una regola: funzionano i nomi brevi, pronunciabili, che non collidono con persone reali della tua cerchia (chiamare l'agente come qualcuno di casa è un esperimento che finisce male nelle notifiche di Telegram).

Al nome si accompagnano l'emoji identificativa — il lobster è il default culturale di OpenClaw, ma qualunque simbolo che lo distingua a colpo d'occhio nelle notifiche va bene — e il *vibe*: il tono di fondo. Professionale e asciutto, amichevole e caldo, ironico, formale. Il posto giusto per fissarlo è una riga in `IDENTITY.md` per la parte visibile (nome, emoji, descrizione breve) e qualche riga in `SOUL.md` per la parte comportamentale. Se durante l'onboarding hai già detto come vuoi che parli, è probabile che il rito abbia popolato entrambi; rileggili e affina. Il Capitolo 16 è dedicato per intero a questo lavoro di cesello.

**(i) Pro tip:** scegli il vibe pensando a dove leggerai i messaggi. Un tono brillante e scherzoso diverte in chat la sera; alle 7:02 del mattino, nel digest che apri ancora mezzo addormentato, l'ironia invecchia in fretta. La maggior parte degli utenti di lungo corso converge su toni caldi ma sobri — e tiene l'umorismo per agenti specifici, non per l'assistente di default.

### Il primo task: un test di fiducia, non di performance

Il primo task che assegni all'agente ha una funzione diversa da quella che sembra. Non serve a misurare quanto è capace — per quello c'è tutto il tempo — serve a costruire fiducia nei due sensi: tu impari a vedere *come* lavora (cosa fa di sua iniziativa, dove si ferma a chiedere), e lui accumula in memoria il primo contesto reale su di te. Per questo il task ideale è piccolo, leggibile e a rischio zero:

- "Leggi le mie ultime 10 email e fammi un riassunto"
- "Cosa c'è nel mio calendario domani?"
- "Cerca le ultime notizie su [argomento]"

Tutti e tre condividono le stesse proprietà: si completano in un minuto, il risultato è verificabile a colpo d'occhio, e niente viene modificato, inviato o cancellato. È l'equivalente del primo incarico che un buon manager dà al nuovo assunto: utile ma non critico, abbastanza concreto da generare un feedback immediato.

Resisti alla tentazione opposta, che è la più diffusa nella prima settimana: il task spettacolare. "Organizzami il viaggio a Lisbona" come prima richiesta è un pessimo test — coinvolge troppe skill, troppi passaggi, troppe preferenze che l'agente ancora non conosce. Se va male non saprai *cosa* è andato male, e l'unico risultato sarà la sfiducia reciproca. La scala giusta è: prima settimana, task di lettura e riassunto; seconda settimana, i workflow guidati del Capitolo 8; poi, gradualmente, l'autonomia.

Quando il primo task riesce, chiudi il cerchio con un feedback esplicito: "perfetto, questo formato di riassunto va benissimo: ricordalo". Quella frase, all'apparenza di cortesia, è in realtà materiale di memoria: l'agente la salverà, e il prossimo riassunto arriverà già nel formato giusto.

### La memoria a tre livelli di Nat Eliason

A proposito di memoria: vale la pena chiudere l'onboarding sapendo *dove* finisce quello che l'agente impara, perché è nei primi giorni che si formano le buone (o cattive) abitudini. Nat Eliason — l'autore di Felix — organizza la memoria dei suoi agenti su tre livelli, uno schema che la community ha adottato come riferimento.

Il primo livello è il **knowledge graph**: una struttura di cartelle e file Markdown nel workspace, organizzata secondo il metodo PARA (Projects, Areas, Resources, Archives — progetti attivi, aree di responsabilità, materiale di consultazione, archivio), dove vive la conoscenza strutturata: i progetti in corso, i dossier sui clienti, i documenti di riferimento. Il secondo livello sono le **note giornaliere**: il diario in `memory/YYYY-MM-DD.md` che già conosci dal Capitolo 2, con il contesto vivo di oggi e di ieri. Il terzo livello è la **conoscenza tacita**: preferenze, abitudini, regole non scritte ("il venerdì niente riunioni", "i riassunti li vuole corti") che l'agente assorbe conversazione dopo conversazione.

Se hai letto il Capitolo 2, la mappa è immediata: le note giornaliere di Eliason *sono* il terzo strato di OpenClaw (`memory/`); la conoscenza tacita si deposita in `MEMORY.md` e nel `SOUL.md` (secondo e primo strato); il knowledge graph è l'unico pezzo che OpenClaw non crea da solo — sono cartelle che organizzi tu nel workspace e che l'agente legge *su richiesta*, non automaticamente (la stessa regola dei file sotto `projects/` vista nel Capitolo 5). Il punto operativo per la prima settimana è uno: la conoscenza tacita non si forma da sola. Si forma se, ogni volta che l'agente fa una cosa nel modo giusto o sbagliato, tu glielo dici e gli chiedi di ricordarlo.

### Mezz'ora oggi, dieci minuti al mese

Un'ultima cosa, che è la promessa fatta dal Capitolo 2 a proposito di `USER.md`: l'onboarding non è un evento, è un rito di ingresso più una manutenzione periodica. La regola pratica è **mezz'ora di onboarding oggi, e tornarci due o tre volte al mese** per dieci minuti.

La ragione è che `USER.md` — come ha spiegato il Capitolo 2 — è il dossier che mantieni *intenzionalmente* tu: a differenza di `MEMORY.md` e delle note giornaliere, che l'agente aggiorna da solo, resta fermo finché non lo tocchi, e la vita lo rende obsoleto in fretta. Cambi progetto, il fuso orario varia per un mese di trasferta, una persona entra nella tua cerchia stretta, una preferenza dichiarata a maggio non vale più a settembre. Un `USER.md` stantio produce errori subdoli: l'agente non sbaglia, esegue correttamente istruzioni vecchie — che è il tipo di errore più difficile da diagnosticare.

Il rituale mensile è semplice: chiedi all'agente di rileggerti il suo `USER.md` e di segnalarti ciò che gli risulta obsoleto o contraddittorio (trovi il prompt pronto qui sotto), correggi, e fai lo stesso con i divieti nel `SOUL.md`. Dieci minuti che ti risparmiano i "ma te l'avevo detto!" — i quali, come ha mostrato il Capitolo 2, nove volte su dieci sono in realtà dei "te l'avevo detto, ma era scritto nel posto sbagliato".

## Prompt pronti all'uso

**Prompt pronto:**
> "Il tuo nome è Polly. Sei la mia assistente personale. Il tuo tono è professionale ma caldo, conciso (3-4 frasi per risposta), orientato all'azione. Non inviare mai email senza la mia approvazione. Aggiorna il tuo SOUL.md con queste istruzioni."

**Prompt pronto** (i primi dieci minuti, da adattare):
> "Mi presento: mi chiamo [nome], vivo a [città], fuso orario [Europe/Rome]. Faccio [ruolo]. Le tre cose che mi rubano più tempo sono: [1], [2], [3]. Preferenze: rispondimi in italiano, risposte brevi, le urgenze nella prima riga. Tre regole: non inviare mai nulla a nome mio senza approvazione; non cancellare mai eventi dal calendario; se un'azione costa più di un euro, chiedi prima. Salva tutto nei file giusti e dimmi cosa hai scritto e dove."

**Prompt pronto** (verifica di fine onboarding):
> "Rileggi il tuo IDENTITY.md, il tuo SOUL.md e il mio USER.md. Riassumimi in tre paragrafi chi sei, come devi comportarti e cosa sai di me. Segnala qualsiasi cosa mancante, imprecisa o contraddittoria."

**Prompt pronto** (manutenzione mensile di USER.md):
> "Apri il mio USER.md e leggimelo voce per voce. Per ogni voce dimmi se negli ultimi 30 giorni hai osservato qualcosa che la contraddice o la rende obsoleta. Proponi le modifiche, ma non applicarle finché non confermo."

## Errori comuni e come risolverli

**Sintomo:** l'agente sembra "vuoto", senza personalità.
Causa: USER.md/SOUL.md non sono stati popolati durante
l'onboarding.
Fix: dedicare 30 minuti reali, condividere ruolo, sfide,
preferenze, cosa NON deve mai fare.

**Sintomo:** risposte generiche e prolisse.
Causa: SOUL.md ancora di default.
Fix: rivedere SOUL.md: aggiungere sezione "Boundaries"
con almeno 3 "non fare" e "Vibe" con il tono richiesto.

**Sintomo:** l'agente non chiama l'utente per nome.
Causa: nome non scritto in USER.md.
Fix: dirglielo esplicitamente ("mi chiamo X, salvalo nel
mio profilo") e verificare con
`cat ~/.openclaw/workspace/USER.md`.

**Sintomo:** BOOTSTRAP.md è ancora nel workspace giorni
dopo il primo avvio.
Causa: il rito di bootstrap si è interrotto (TUI chiusa,
Gateway riavviato, cambio di canale a metà).
Fix: riaprire la TUI con `openclaw`, completare le domande
in una sola seduta, verificare con
`ls ~/.openclaw/workspace/` che il file sia sparito.

**Sintomo:** l'agente "dimentica" preferenze dichiarate in
chat pochi giorni prima.
Causa: la preferenza è rimasta in conversazione e non è
mai stata salvata nei file di memoria.
Fix: chiedere esplicitamente "salva questo in USER.md" (o
in MEMORY.md) e verificare che il file sia cambiato.

## Checklist di fine capitolo

- [ ] Nome, ruolo, fuso orario e preferenze condivise con l'agente
- [ ] USER.md popolato (verificato con `cat`)
- [ ] SOUL.md ha almeno 3 regole di "non fare"
- [ ] Primo task piccolo completato dall'agente
- [ ] L'agente sa cosa NON deve mai fare in autonomia
- [ ] BOOTSTRAP.md non è più nella radice del workspace
- [ ] L'agente ha nome, emoji e vibe scritti in IDENTITY.md
- [ ] Promemoria ricorrente creato per rivedere USER.md 2–3 volte al mese

## Link e risorse utili

- [The Complete Guide to Building Your Personal AI Agent](https://www.lennysnewsletter.com/p/openclaw-the-complete-guide-to-building) — i consigli di Claire Vo sull'onboarding
- [Use OpenClaw to Build a Business That Runs Itself](https://creatoreconomy.so/p/use-openclaw-to-build-a-business-that-runs-itself-nat-eliason) — l'approccio di Nat Eliason all'onboarding
- [Onboarding overview — documentazione ufficiale](https://docs.openclaw.ai/start/onboarding-overview) — il flusso di onboarding e le opzioni del wizard
- [OpenClaw Memory Files: AGENTS.md, IDENTITY.md, SOUL.md & More](https://openclaw-setup.me/blog/openclaw-internals/openclaw-memory-files/) — dove finisce quello che dici durante l'onboarding
- [OpenClaw Memory Masterclass](https://velvetshark.com/openclaw-memory-masterclass) — la memoria persistente in profondità
- [Building a Million Dollar Zero Human Company](https://www.bankless.com/podcast/building-a-million-dollar-zero-human-company-with-openclaw-nat-eliason) — Nat Eliason racconta Felix e il suo sistema di memoria

Per l'elenco completo delle fonti del libro, vedi [Appendice E](../Appendici/E-risorse-e-link-utili.md).

---

[← Capitolo 6](../PARTE-II-Installazione/06-configurare-telegram-e-altri-canali.md)  ·  [Indice](../README.md)  ·  [Capitolo 8 →](./08-dieci-workflow-pronti-all-uso.md)
