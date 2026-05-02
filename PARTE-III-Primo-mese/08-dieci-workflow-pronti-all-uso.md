# Capitolo 8 — 10 workflow pronti all'uso [★★]

## Cosa imparerai

- 10 automazioni concrete con prompt copia-incolla
- Quali skill e integrazioni servono per ciascuna
- Stima dei costi per ogni workflow

## Prerequisiti

Aver fatto l'onboarding del tuo agente ([Capitolo 7](./07-prima-conversazione-onboarding-agente.md)). Per i workflow che richiedono Gmail/Calendar serve aver collegato `gog` (vedi [Capitolo 9](./09-aggiungere-strumenti-e-integrazioni.md)).

## Contenuto principale

Per ogni workflow: descrizione dell'obiettivo, prompt copia-incollabile da inviare al tuo agente, skill necessarie e costo mensile stimato. Il consiglio è di attivarne uno alla volta, lasciarlo girare per una settimana, e solo poi passare al successivo.

### 1. Digest mattutino di email e calendario

Ogni mattina alle 6:30, l'agente legge email e calendario e invia un riepilogo su Telegram con le priorità del giorno.

*Skill: gog, summarize. Costo: ~$5–15/mese.*

**Prompt pronto:**
> "Crea un cron che ogni mattina alle 6:30 (Europe/Rome) controlli la mia inbox Gmail e il mio Google Calendar delle prossime 24 ore. Invia su Telegram un digest di max 5 bullet (una frase ciascuno, ordine per priorità) con: email importanti che richiedono risposta, meeting del giorno con orario e partecipanti, scadenze in arrivo. Niente emoji. Se non c'è nulla di rilevante, scrivi solo 'Giornata libera'."

### 2. Coordinamento weekend famiglia

Ogni venerdì, messaggio di gruppo con il partner per confermare la logistica del weekend: attività dei figli, chi porta/ritira, conflitti di orari.

*Skill: gog, canale WhatsApp/Telegram con gruppo. Costo: ~$3–8/mese.*

**Prompt pronto:**
> "Crea un cron che ogni venerdì alle 18:00 mandi un messaggio nel gruppo Telegram 'Famiglia' con: (1) attività dei bambini di sabato e domenica con orario e luogo, (2) chi porta e chi ritira, (3) eventuali conflitti di orario tra i miei impegni e quelli del partner. Pesca i dati dal mio Google Calendar e dal calendario condiviso. Tono casual, max 8 righe."

### 3. Meeting prep "just in time"

30 minuti prima di ogni meeting, l'agente invia un briefing: partecipanti, agenda, ultima interazione con quella persona/azienda.

*Skill: gog, summarize, ricerca web. Costo: ~$10–20/mese.*

**Prompt pronto:**
> "Per ogni meeting nel mio Google Calendar, 30 minuti prima dell'orario di inizio mandami su Telegram un briefing con: (1) partecipanti e loro ruolo, (2) agenda dichiarata se presente, (3) sintesi dell'ultima conversazione email con quella persona/azienda, (4) un fatto rilevante recuperato dal web (ultime news dell'azienda, post LinkedIn recente). Max 150 parole, niente filler."

### 4. Ricerca trend social + generazione meme

Ogni mattina, scansione dei trending topic su Reddit/X nel settore scelto, generazione di un meme da approvare prima della pubblicazione.

*Skill: ricerca web, API social, generazione immagini. Costo: ~$15–30/mese.*

**Prompt pronto:**
> "Ogni mattina alle 8:00 scansiona i trending topic di r/[subreddit] e l'hashtag #[topic] su X delle ultime 24 ore. Identifica i 3 trend più rilevanti per il mio settore [descrivi]. Per il trend più caldo, genera una bozza di meme (testo + descrizione visiva) e me la mandi su Telegram per approvazione PRIMA di pubblicare. Mai pubblicare in autonomia."

### 5. Qualificazione lead PLG ed email automatiche

Ogni mattina, analisi delle iscrizioni delle ultime 24 ore, categorizzazione per valore, email leggera per aziende piccole, arricchimento profilo + conferma umana per enterprise.

*Skill: gog, CRM (Attio/HubSpot), ricerca web (Exa People API). Costo: ~$20–50/mese.*

**Prompt pronto:**
> "Ogni mattina alle 9:00 leggi le nuove iscrizioni delle ultime 24 ore dal CRM. Per ogni lead: (1) categorizza per valore stimato (small/mid/enterprise) usando l'arricchimento via Exa People API, (2) per i lead 'small' invia in autonomia un'email di benvenuto leggera (passa dal mio Gmail), (3) per i lead 'enterprise' arricchisci il profilo con news recenti dell'azienda e mettilo nella mia coda di follow-up con bozza di email da approvare. Mai inviare email a un 'enterprise' senza mia conferma esplicita."

### 6. Scrittura documentazione support

Ogni venerdì sera, analisi dei ticket di supporto risolti. Se una domanda è stata fatta 3+ volte, creare un issue su Linear con bozza di FAQ.

*Skill: email/Intercom, Linear, GitHub. Costo: ~$10–20/mese.*

**Prompt pronto:**
> "Ogni venerdì alle 19:00 analizza i ticket di supporto risolti negli ultimi 7 giorni (Intercom). Identifica le domande ricorrenti (≥3 volte). Per ognuna, crea un issue su Linear nel progetto 'Docs' con: titolo della FAQ, bozza di risposta (basata sui ticket reali), suggerimento di pagina docs dove inserirla. Tagga gli issue con `auto-faq` e assegnali a me. Non aprire PR su GitHub in autonomia."

### 7. Project management personale

Mantenere una to-do list con tutto ciò che l'utente dice di dover fare per un progetto, suddividere in task giornalieri, celebrare i risultati e segnalare ciò che manca.

*Skill: memoria, Linear/Notion. Costo: ~$5–10/mese.*

**Prompt pronto:**
> "Voglio che gestisci la mia to-do list per il progetto [nome]. Ogni volta che ti dico in chat 'da fare X' o 'devo Y', salvi la voce in una pagina Notion dedicata. Ogni mattina alle 8:30 mi mandi su Telegram i 3 task più prioritari per oggi (max 1h ciascuno se possibile). Ogni sera alle 19:00 mi chiedi cosa ho chiuso, aggiorni Notion, e mi mandi un breve riepilogo: cosa è andato, cosa è rimasto, cosa proponi per domani."

### 8. Monitoraggio competitivo e aggiornamento sito

Ogni settimana, ricerca web sulle feature dei competitor, aggiornamento automatico delle pagine di confronto sul sito con PR su GitHub.

*Skill: ricerca web, GitHub, browser automation. Costo: ~$15–30/mese.*

**Prompt pronto:**
> "Ogni lunedì alle 10:00 controlla le pagine dei prodotti di [competitor 1, 2, 3]. Per ogni cambio rilevante (nuova feature, nuovo prezzo, modifica al pricing) confronta con la nostra pagina di comparazione su [URL] e prepara una PR su GitHub nel repo `marketing-site` con la modifica suggerita. Includi nel testo della PR: cosa è cambiato lato competitor, link alla fonte, motivazione della modifica proposta. Non fare merge in autonomia."

### 9. Gestione pipeline podcast/content

Gestire la pipeline degli ospiti, preparare briefing pre-registrazione, proporre idee per titoli/thumbnail, ricordare di postare sui social dopo la pubblicazione.

*Skill: gog, YouTube Studio, Linear, Buffer. Costo: ~$10–25/mese.*

**Prompt pronto:**
> "Sei il mio producer del podcast. Mantieni in Linear la pipeline degli ospiti con stato (invitato / confermato / registrato / pubblicato). 48 ore prima di ogni registrazione mandami su Telegram un briefing dell'ospite (background, ultimi 3 contenuti pubblici, 5 domande possibili). Quando un episodio passa a stato 'pubblicato', proponi 3 titoli e 3 idee thumbnail per YouTube e schedula 4 post su Buffer (LinkedIn, X, Instagram, newsletter) distribuiti nei 7 giorni successivi. Ogni post va da me per approvazione prima della schedulazione."

### 10. Assistente educativo per bambini

Ogni mattina, parola del giorno e problema di matematica personalizzato per l'età di ciascun figlio. Rispondere alle domande "curiose" dei bambini durante la giornata.

*Skill: ricerca web. Costo: ~$3–8/mese.*

**Prompt pronto:**
> "Ogni mattina alle 7:30 mandami su Telegram, in due messaggi separati: (1) per [nome figlio 1, età N], la parola del giorno con definizione semplice e un esempio, più un problema di matematica adatto alla terza elementare; (2) per [nome figlio 2, età M], stessa cosa adattata alla quinta elementare. Tono allegro, max 5 righe per figlio. Quando i bambini ti scrivono direttamente con domande curiose ('perché il cielo è blu?'), rispondi in modo accurato ma comprensibile per la loro età, senza link esterni."

**(i) Pro tip:** Il sistema di memoria a 3 livelli di Nat Eliason è la singola innovazione più utile: (1) Knowledge graph con cartelle PARA, (2) Note giornaliere in markdown, (3) Conoscenza tacita (preferenze, abitudini, regole). Implementarlo fin dal primo giorno migliora drasticamente le risposte dell'agente.

## Errori comuni e come risolverli

| Sintomo | Causa probabile | Fix |
|---------|-----------------|-----|
| Il workflow non scatta al mattino | Cron senza timezone esplicito (default UTC) o computer in sleep | Specificare timezone (`Europe/Rome`), disabilitare lo sleep del Mac per gli orari programmati. |
| Digest mattutino prolisso e illeggibile | Prompt troppo aperto | Vincolare nel prompt: "max 5 bullet, una frase ciascuno, ordine per priorità". |
| Voglia di attivare tutti i workflow nello stesso giorno | Entusiasmo iniziale | Uno alla volta. Una settimana di test per workflow prima di passare al successivo. |
| Costo mensile più alto del previsto | Workflow ricorrenti con modello costoso (Opus) o contesto stantio | Routing modelli (Opus solo dove serve), pulizia conversazione storica. |

## Checklist di fine capitolo

- [ ] Ho scelto e attivato UN solo workflow (non tutti insieme)
- [ ] Il workflow è in produzione da almeno 3 giorni
- [ ] Costo settimanale del workflow misurato
- [ ] Output verificato manualmente almeno una volta
- [ ] Ho deciso se mantenerlo, raffinarlo o rimuoverlo

## Link e risorse utili

- [The Complete Guide to Building Your Personal AI Agent](https://www.lennysnewsletter.com/p/openclaw-the-complete-guide-to-building) — workflow del team di Claire Vo
- [Building a Million Dollar Zero Human Company](https://www.bankless.com/podcast/building-a-million-dollar-zero-human-company-with-openclaw-nat-eliason) — l'episodio Bankless con Nat Eliason
- [OpenClaw Income Generation Stories](https://openclawdesktop.com/blog/openclaw-income-generation-community-stories.html) — casi reali raccolti dalla community

Per l'elenco completo delle fonti del libro, vedi [Appendice E](../Appendici/E-risorse-e-link-utili.md).

---

[← Capitolo 7](./07-prima-conversazione-onboarding-agente.md)  ·  [Indice](../README.md)  ·  [Capitolo 9 →](./09-aggiungere-strumenti-e-integrazioni.md)
