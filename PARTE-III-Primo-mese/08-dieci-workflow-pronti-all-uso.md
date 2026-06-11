# Capitolo 8 — 10 workflow pronti all'uso [★★]

## Cosa imparerai

- 10 automazioni concrete con prompt copia-incolla
- Quali skill e integrazioni servono per ciascuna
- Stima dei costi per ogni workflow
- Come combinare cron, skill e canali senza farti male
- Il percorso consigliato: un workflow alla volta, non tutti insieme

## Prerequisiti

Aver fatto l'onboarding del tuo agente ([Capitolo 7](./07-prima-conversazione-onboarding-agente.md)). La skill `gog` (Gmail, Calendar, Drive) è già installata dal wizard del [Capitolo 5](../PARTE-II-Installazione/05-installazione-step-by-step.md): qui basta quella. Il [Capitolo 9](./09-aggiungere-strumenti-e-integrazioni.md) serve solo per gli approfondimenti (scope OAuth, CRM, strumenti di lavoro).

## Contenuto principale

### Come usare questo capitolo

Ogni workflow è una scheda autonoma con la stessa struttura: l'obiettivo, i prerequisiti specifici, il prompt pronto da copiare, le skill necessarie con il costo mensile stimato — e poi la parte che nelle guide manca quasi sempre: com'è davvero la prima volta, cosa aspettarti nella prima settimana e come capire se sta funzionando. I costi sono in euro e presuppongono Claude Sonnet 4.6, il modello di default del libro; con il routing dei modelli del [Capitolo 14](../PARTE-V-Sicurezza-costi/14-gestire-i-costi-senza-sorprese.md) si scende, con Opus 4.6 si sale.

I dieci workflow vengono dalla guida di Claire Vo — la fonte principale di questo capitolo, citata in fondo e in Appendice E — e seguono l'ordine in cui li presenta, non l'ordine di difficoltà. I workflow 1, 2, 3, 7 e 10 sono *personali*: bastano `gog`, la ricerca web e un canale, tutto già pronto se hai seguito la Parte II. I workflow 4, 5, 6, 8 e 9 sono *business*: presuppongono strumenti aziendali (CRM, Intercom, Linear, GitHub, Buffer) e hanno senso solo se quegli strumenti li usi già per lavoro. Ognuno è marcato all'inizio della scheda, così non perdi tempo su quelli che non ti riguardano.

**(!) Attenzione:** la regola più importante del capitolo: **un workflow alla volta**. Attivane uno, lascialo girare una settimana, misuralo, poi passa al successivo. Chi attiva cinque cron il primo giorno si ritrova con una raffica di notifiche che non legge, costi impossibili da attribuire e nessun modo di capire quale automazione ha sbagliato cosa.

### 1. Digest mattutino di email e calendario

*Workflow personale.* È il "hello world" degli agenti autonomi, quello con cui si apre praticamente ogni guida, a partire da quella di Claire Vo: ogni mattina alle 6:30 l'agente legge email e calendario e ti manda su Telegram le priorità del giorno, prima ancora che tu apra la inbox. Prerequisiti: `gog` autenticato (il self-test del Capitolo 5 lo verifica) e il canale Telegram attivo.

*Skill: gog, summarize. Costo: ~€5–14/mese.*

**Prompt pronto:**
> "Crea un cron che ogni mattina alle 6:30 (Europe/Rome) controlli la mia inbox Gmail e il mio Google Calendar delle prossime 24 ore. Invia su Telegram un digest di max 5 bullet (una frase ciascuno, ordine per priorità) con: email importanti che richiedono risposta, meeting del giorno con orario e partecipanti, scadenze in arrivo. Niente emoji. Se non c'è nulla di rilevante, scrivi solo 'Giornata libera'."

La prima volta va quasi sempre così: il digest arriva puntuale ma è lungo dodici righe, mette in cima una newsletter e ti dà del "voi". Non è un fallimento, è il punto di partenza: rispondi al messaggio con le correzioni ("troppo lungo; le newsletter non sono mai prioritarie; dammi del tu") e chiedi all'agente di ricordarle. Nella prima settimana aspettati due o tre iterazioni di questo tipo; dal quarto-quinto giorno il formato si stabilizza. La misura del successo è comportamentale: se dopo sette giorni apri il digest *invece* della inbox, il workflow funziona; se ti accorgi di ignorarlo, accorcialo ancora — un digest che non viene letto è solo un costo.

### 2. Coordinamento weekend famiglia

*Workflow personale.* Ogni venerdì alle 18:00 un messaggio nel gruppo di famiglia mette in fila la logistica del weekend: attività dei figli, chi porta e chi ritira, conflitti di orario. È il mestiere di Finn, l'agente "famiglia" del cast di questo libro. Prerequisiti: un gruppo Telegram con il partner, l'agente aggiunto al gruppo (Capitolo 6) e i calendari rilevanti visibili a `gog` — incluso quello condiviso, che è il pezzo che quasi tutti dimenticano.

*Skill: gog, canale WhatsApp/Telegram con gruppo. Costo: ~€3–7/mese.*

**Prompt pronto:**
> "Crea un cron che ogni venerdì alle 18:00 mandi un messaggio nel gruppo Telegram 'Famiglia' con: (1) attività dei bambini di sabato e domenica con orario e luogo, (2) chi porta e chi ritira, (3) eventuali conflitti di orario tra i miei impegni e quelli del partner. Pesca i dati dal mio Google Calendar e dal calendario condiviso. Tono casual, max 8 righe."

La prima volta tipica: il riepilogo è corretto ma incompleto, perché il calendario del partner non era condiviso con l'account Google dell'agente — il conflitto di sabato mattina non poteva vederlo nessuno. Sistemata la condivisione, la prima settimana serve a calibrare tono (un gruppo famiglia non vuole un report aziendale) e livello di dettaglio. Successo misurabile: meno messaggi di coordinamento la domenica mattina. Se il venerdì sera nessuno legge il messaggio, spostalo al sabato alle 8:00: l'orario giusto è quello in cui la famiglia decide, non quello che sembra elegante.

### 3. Meeting prep "just in time"

*Workflow personale.* Trenta minuti prima di ogni meeting l'agente ti manda un briefing: chi c'è, di cosa si parla, com'è finita l'ultima volta. È il workflow con il miglior rapporto resa/sforzo per chi ha più di tre meeting al giorno. Prerequisiti: `gog` e la ricerca web configurata nel wizard (Brave Search di default).

*Skill: gog, summarize, ricerca web. Costo: ~€9–18/mese.*

**Prompt pronto:**
> "Per ogni meeting nel mio Google Calendar, 30 minuti prima dell'orario di inizio mandami su Telegram un briefing con: (1) partecipanti e loro ruolo, (2) agenda dichiarata se presente, (3) sintesi dell'ultima conversazione email con quella persona/azienda, (4) un fatto rilevante recuperato dal web (ultime news dell'azienda, post LinkedIn recente). Max 150 parole, niente filler."

La prima volta scoprirai che l'agente prepara con la stessa serietà il consiglio di amministrazione e il caffè quindicinale con il collega: il primo briefing su un meeting interno ricorrente è comicamente formale. La correzione standard è escludere i ricorrenti interni ("prepara solo i meeting con esterni o marcati come importanti"). Nella prima settimana sorveglia anche i falsi recuperi: se l'agente confonde l'azienda dell'interlocutore con un'omonima, diglielo subito — finisce in memoria e non si ripete. Successo: arrivi al meeting sapendo già l'ultima cosa che vi siete scritti. Voce di costo da tenere d'occhio: la ricerca web su ogni partecipante è quella che pesa di più; limitala ai meeting esterni.

### 4. Ricerca trend social + generazione meme

*Workflow business.* Ogni mattina l'agente scandaglia i trend del tuo settore su Reddit e X e ti propone un meme da approvare. È il territorio di Max, l'agente marketing. Le skill concrete: per leggere trend e discussioni basta la ricerca web già installata (Brave Search; Exa se vuoi ricerche semantiche più fini); per la bozza visiva serve la generazione immagini via API del tuo provider. Nota che il prompt qui sotto *non pubblica nulla*: la pubblicazione resta manuale (o passa da uno strumento di scheduling come Buffer, se vorrai aggiungerlo dopo). L'etichetta business non viene dagli strumenti, ma dal senso: una rassegna trend quotidiana con meme annesso ha valore solo se il marketing è il tuo lavoro.

*Skill: ricerca web (Brave/Exa), generazione immagini. Costo: ~€14–28/mese.*

**Prompt pronto:**
> "Ogni mattina alle 8:00 scansiona i trending topic di r/[subreddit] e l'hashtag #[topic] su X delle ultime 24 ore. Identifica i 3 trend più rilevanti per il mio settore [descrivi]. Per il trend più caldo, genera una bozza di meme (testo + descrizione visiva) e me la mandi su Telegram per approvazione PRIMA di pubblicare. Mai pubblicare in autonomia."

Il vincolo di approvazione nel prompt non è prudenza di maniera: un agente con accesso ai social e libertà di iniziativa è esattamente lo scenario da cui nascono storie come il caso MoltMatch ([Capitolo 13](../PARTE-V-Sicurezza-costi/13-sicurezza-la-guida-che-devi-leggere.md)). La prima settimana aspettati meme mediocri: l'umorismo è l'ultima cosa che si calibra, e si calibra con gli esempi — manda all'agente tre meme che ti piacciono e digli "questo è il tono". Successo: almeno due dei tre trend proposti ogni mattina sono davvero rilevanti per il tuo settore. Il meme è il bonus; la rassegna trend è il valore.

### 5. Qualificazione lead PLG ed email automatiche

*Workflow business.* Ogni mattina l'agente guarda chi si è iscritto al tuo prodotto nelle ultime 24 ore, distingue i lead piccoli da quelli enterprise, scrive ai primi e prepara i secondi per te. È la specialità di Sam, l'agente vendite. Prerequisiti: un CRM collegato (Attio o HubSpot, Capitolo 9), Exa per l'arricchimento dei profili e — punto delicato — lo scope di *invio* su Gmail: è l'unico workflow del capitolo a richiederlo davvero.

*Skill: gog, CRM (Attio/HubSpot), ricerca web (Exa People API). Costo: ~€18–46/mese.*

**Prompt pronto:**
> "Ogni mattina alle 9:00 leggi le nuove iscrizioni delle ultime 24 ore dal CRM. Per ogni lead: (1) categorizza per valore stimato (small/mid/enterprise) usando l'arricchimento via Exa People API, (2) per i lead 'small' invia in autonomia un'email di benvenuto leggera (passa dal mio Gmail), (3) per i lead 'enterprise' arricchisci il profilo con news recenti dell'azienda e mettilo nella mia coda di follow-up con bozza di email da approvare. Mai inviare email a un 'enterprise' senza mia conferma esplicita."

**(!) Attenzione:** non dare lo scope di invio il primo giorno. Fai girare il workflow una settimana in modalità bozza — tutte le email in coda di approvazione, anche le "small" — e leggi cosa *avrebbe* mandato. Solo quando le bozze sono indistinguibili dalle tue, concedi l'invio autonomo per la fascia small. È la versione operativa della regola del Capitolo 9: si parte read-only, si allarga dopo.

La misura del successo qui è facile, perché è un workflow di lavoro: tasso di risposta delle email di benvenuto rispetto a prima, e tempo medio tra iscrizione e primo contatto. Se l'arricchimento via Exa sbaglia spesso la classificazione small/enterprise, aggiungi al prompt criteri espliciti tuoi (numero dipendenti, settore, dominio email aziendale o gratuito).

Un'ultima cosa che le guide americane non dicono: arricchire profili di persone fisiche con dati raccolti dal web è trattamento di dati personali. Se operi in Europa, la verifica con chi gestisce la privacy in azienda va fatta *prima* di attivare il workflow, non dopo.

### 6. Scrittura documentazione support

*Workflow business.* Ogni venerdì sera l'agente rilegge i ticket di supporto risolti nella settimana e trasforma le domande ricorrenti in bozze di FAQ, una issue Linear per ciascuna. È il lavoro silenzioso di Holly, l'agente support: nessuno se ne accorge finché la documentazione non smette di invecchiare. Prerequisiti: accesso in lettura a Intercom (o alla casella di supporto) e a Linear (Capitolo 9).

*Skill: email/Intercom, Linear. Costo: ~€9–18/mese.* (GitHub non serve: il divieto nel prompt è un confine, la pubblicazione delle docs resta tua.)

**Prompt pronto:**
> "Ogni venerdì alle 19:00 analizza i ticket di supporto risolti negli ultimi 7 giorni (Intercom). Identifica le domande ricorrenti (≥3 volte). Per ognuna, crea un issue su Linear nel progetto 'Docs' con: titolo della FAQ, bozza di risposta (basata sui ticket reali), suggerimento di pagina docs dove inserirla. Tagga gli issue con `auto-faq` e assegnali a me. Non aprire PR su GitHub in autonomia."

La prima settimana l'agente tende a vedere ricorrenze ovunque: tre ticket vagamente simili diventano una FAQ inutile. La correzione è alzare l'asticella nel prompt ("stessa domanda, non stesso tema") e dargli un esempio di FAQ fatta bene. Il successo si misura sul mese, non sulla settimana: dove le FAQ sono state pubblicate, i ticket sulla stessa domanda devono scendere. E nota il confine già scritto nel prompt: l'agente *propone* su Linear, non tocca GitHub — la pubblicazione resta un atto umano.

### 7. Project management personale

*Workflow personale.* L'agente come project manager di te stesso: raccoglie tutto quello che dici di dover fare, lo organizza, te lo ripropone in dosi gestibili e tiene il conto di cosa hai chiuso. È il workflow più sottovalutato del capitolo, perché non automatizza un compito ma una *disciplina*. Prerequisiti minimi: basta la memoria dell'agente; Notion o Linear sono opzionali ma rendono la lista consultabile fuori dalla chat.

*Skill: memoria, Linear/Notion. Costo: ~€5–9/mese.*

**Prompt pronto:**
> "Voglio che gestisci la mia to-do list per il progetto [nome]. Ogni volta che ti dico in chat 'da fare X' o 'devo Y', salvi la voce in una pagina Notion dedicata. Ogni mattina alle 8:30 mi mandi su Telegram i 3 task più prioritari per oggi (max 1h ciascuno se possibile). Ogni sera alle 19:00 mi chiedi cosa ho chiuso, aggiorni Notion, e mi mandi un breve riepilogo: cosa è andato, cosa è rimasto, cosa proponi per domani."

La prima settimana il rischio è l'effetto sagra di paese: l'agente celebra ogni task chiuso con un entusiasmo fuori scala. Una riga nel SOUL.md ("riconosci i progressi in modo sobrio") sistema il tono. Il punto critico vero è la fiducia: il workflow funziona solo se *tutto* passa dall'agente — se metà dei task vive in un'altra app, il riepilogo serale è teatro. Successo: per almeno metà dei giorni, le tre priorità del mattino coincidono con le cose che hai davvero fatto. Se la lista cresce e basta, chiedi una revisione settimanale: cosa archiviare, cosa è bloccato da settimane, cosa non era mai stato un task vero.

### 8. Monitoraggio competitivo e aggiornamento sito

*Workflow business.* Ogni lunedì l'agente passa in rassegna i siti dei concorrenti e, se qualcosa è cambiato, prepara una pull request con l'aggiornamento della tua pagina di confronto. Prerequisiti: un Personal Access Token GitHub limitato al solo repo del sito (Capitolo 9) e la ricerca web. È il workflow tecnicamente più delicato del capitolo: tocca il tuo sito pubblico, anche se solo via PR.

*Skill: ricerca web, GitHub, browser automation. Costo: ~€14–28/mese.*

**Prompt pronto:**
> "Ogni lunedì alle 10:00 controlla le pagine dei prodotti di [competitor 1, 2, 3]. Per ogni cambio rilevante (nuova feature, nuovo prezzo, modifica al pricing) confronta con la nostra pagina di comparazione su [URL] e prepara una PR su GitHub nel repo `marketing-site` con la modifica suggerita. Includi nel testo della PR: cosa è cambiato lato competitor, link alla fonte, motivazione della modifica proposta. Non fare merge in autonomia."

La prima settimana le PR saranno rumorose: i siti dei competitor cambiano di continuo per ragioni irrilevanti (un typo, un banner stagionale) e all'inizio l'agente non distingue un restyling da un cambio di pricing. Definisci nel prompt cosa è "rilevante" — prezzi, feature, piani — e digli di ignorare il resto. Misura del successo: il rapporto tra PR aperte e PR che hai davvero mergiato; se su dieci ne passi una, il filtro è troppo lasco. E il confine resta assoluto: il merge è tuo, sempre.

### 9. Gestione pipeline podcast/content

*Workflow business.* L'agente come producer: pipeline degli ospiti in Linear, briefing automatico prima della registrazione, proposte di titoli e thumbnail, post social distribuiti nella settimana dopo la pubblicazione. Prerequisiti: Linear e `gog` (per il calendario delle registrazioni), Buffer per lo scheduling social. È il workflow con più pezzi in movimento del capitolo: tra i business, attivalo per ultimo.

*Skill: gog, YouTube Studio, Linear, Buffer. Costo: ~€9–23/mese.*

**Prompt pronto:**
> "Sei il mio producer del podcast. Mantieni in Linear la pipeline degli ospiti con stato (invitato / confermato / registrato / pubblicato). 48 ore prima di ogni registrazione mandami su Telegram un briefing dell'ospite (background, ultimi 3 contenuti pubblici, 5 domande possibili). Quando un episodio passa a stato 'pubblicato', proponi 3 titoli e 3 idee thumbnail per YouTube e schedula 4 post su Buffer (LinkedIn, X, Instagram, newsletter) distribuiti nei 7 giorni successivi. Ogni post va da me per approvazione prima della schedulazione."

La prima volta il briefing dell'ospite sarà generico — il classico profilo che potresti copiare da Wikipedia. La differenza la fanno le fonti: dai all'agente i link giusti (sito personale, newsletter, ultimo progetto pubblicato) e digli di partire da lì. Nella prima settimana valuta i tre output separatamente: la pipeline in Linear funziona quasi subito, i titoli richiedono esempi del tuo stile, i post social vanno riletti sempre. Successo: il tempo di preparazione per episodio, misurato prima e dopo. Se non scende, il workflow sta producendo materiale che poi rifai da zero — e va ricalibrato o spento.

### 10. Assistente educativo per bambini

*Workflow personale.* Ogni mattina una parola del giorno e un problema di matematica su misura per ciascun figlio; durante la giornata, risposte a misura di bambino alle domande curiose. È Q, l'agente educativo del cast — che per ora è solo un *ruolo* del tuo unico agente: diventerà un agente dedicato nella Parte IV ([Capitolo 10](../PARTE-IV-Multi-agente/10-perche-un-solo-agente-non-basta.md)). Prerequisiti: un gruppo o canale dedicato e supervisionato — i bambini non devono avere accesso diretto all'agente "adulto" che gestisce email e calendario.

*Skill: ricerca web. Costo: ~€3–7/mese.*

**Prompt pronto:**
> "Ogni mattina alle 7:30 mandami su Telegram, in due messaggi separati: (1) per [nome figlio 1, età N], la parola del giorno con definizione semplice e un esempio, più un problema di matematica adatto alla terza elementare; (2) per [nome figlio 2, età M], stessa cosa adattata alla quinta elementare. Tono allegro, max 5 righe per figlio. Quando i bambini ti scrivono direttamente con domande curiose ('perché il cielo è blu?'), rispondi in modo accurato ma comprensibile per la loro età, senza link esterni."

**(!) Attenzione:** prima di attivarlo, scrivi nel SOUL.md le regole per le conversazioni con i minori: linguaggio adatto all'età, nessun link esterno, nessuna raccolta di informazioni personali, e sulle domande sensibili "chiedi a mamma o papà". I bambini usano il gruppo dal dispositivo di un genitore, non da un account di messaggistica personale. E vale doppio la regola del Capitolo 13: mai il bot in gruppi con sconosciuti.

La prima settimana serve a calibrare la difficoltà: il problema "da terza elementare" della prima mattina sarà troppo facile o troppo difficile, e la correzione migliore è far valutare al bambino stesso ("era facile? era noioso?") e riferire all'agente. La misura del successo è una sola e non ammette scorciatoie: i bambini tornano a fare domande di loro iniziativa. Se dopo due settimane il rito del mattino è diventato un compito, cambia formato — l'agente sa fare indovinelli, storie a puntate, sfide a punti.

### 11. Bonus: la manutenzione di sé

C'è un workflow che non compare nelle liste della community ma che i Capitoli 3 e 5 hanno già apparecchiato: l'agente che si prende cura della propria infrastruttura. Una volta a settimana: backup completo, report dei costi, controllo dei cron falliti. I comandi li conosci già:

```bash
openclaw backup create --include-workspace
openclaw cost report --since today
```

**Prompt pronto:**
> "Crea un cron che ogni domenica alle 22:00: (1) esegua il backup completo di configurazione e workspace, (2) mi mandi su Telegram il totale dei costi della settimana, suddiviso per workflow e per modello, usando i dati dell'hook cost-tracker, (3) elenchi gli eventuali cron falliti negli ultimi 7 giorni. Se il backup fallisce, avvisami subito invece di aspettare il report."

Cinque minuti di setup, e il check mensile promesso nella checklist del Capitolo 3 diventa un messaggio che arriva da solo. È anche il modo più indolore di scoprire un cron impazzito che brucia token nella notte — prima che lo scopra l'estratto conto.

### Il percorso del primo mese

Messa in fila, la strategia è questa: settimana uno, il digest mattutino (workflow 1) — è il più semplice e ti insegna il ciclo feedback-correzione-memoria che vale per tutti gli altri. Settimana due, un secondo workflow personale (2, 3 o 7, a seconda della tua vita). Settimana tre, il primo workflow business *se* ti serve, partendo dal più prudente — il 6, che lavora in sola lettura e a cadenza settimanale. Settimana quattro, il workflow 11 di manutenzione, e una revisione onesta: cosa tieni, cosa raffini, cosa spegni. Quattro workflow ben calibrati battono dieci workflow attivati di fretta — e a fine mese avrai anche i dati di costo reali per decidere come crescere.

**(i) Pro tip:** il sistema di memoria a tre livelli di Nat Eliason — knowledge graph in cartelle PARA, note giornaliere, conoscenza tacita: lo hai visto nel [Capitolo 7](./07-prima-conversazione-onboarding-agente.md) — non è un workflow, ma moltiplica il rendimento di tutti quelli del capitolo. Nei termini dei quattro strati del Capitolo 2: le note giornaliere sono il terzo strato, la conoscenza tacita si deposita in MEMORY.md e SOUL.md, il knowledge graph è la parte che organizzi tu nel workspace. Più i dossier (clienti, ospiti del podcast, abitudini della famiglia) sono curati, meno i workflow devono ricostruire il contesto da zero — e meglio rispondono.

## Errori comuni e come risolverli

**Sintomo:** il workflow non scatta al mattino.
Causa: cron senza timezone esplicito (default UTC);
computer in sleep; su VPS, timezone del server diverso
dal tuo.
Fix: specificare il timezone (`Europe/Rome`) nel prompt
del cron; disabilitare lo sleep del Mac negli orari
programmati; su VPS verificare con `timedatectl` e non
fidarsi mai dell'ora "locale" della macchina.

**Sintomo:** digest mattutino prolisso e illeggibile.
Causa: prompt troppo aperto.
Fix: vincolare nel prompt: "max 5 bullet, una frase
ciascuno, ordine per priorità".

**Sintomo:** voglia di attivare tutti i workflow nello
stesso giorno.
Causa: entusiasmo iniziale.
Fix: uno alla volta. Una settimana di test per workflow
prima di passare al successivo.

**Sintomo:** costo mensile più alto del previsto.
Causa: workflow ricorrenti con modello costoso (Opus)
o contesto stantio.
Fix: routing dei modelli (Opus solo dove serve), pulizia
della conversazione storica, report settimanale del
workflow 11.

**Sintomo:** nel gruppo famiglia l'agente non risponde.
Causa: mention gating attivo sui gruppi (Cap. 6).
Fix: menzionare il bot nel messaggio, oppure regolare
l'attivazione di gruppo nella config del Gateway.

**Sintomo:** il briefing pre-meeting parla dell'azienda
sbagliata.
Causa: omonimia non gestita nella ricerca web.
Fix: correggere subito in chat e far salvare in memoria
l'associazione giusta (persona → azienda → dominio).

## Checklist di fine capitolo

- [ ] Ho scelto e attivato UN solo workflow (non tutti insieme)
- [ ] Il workflow è in produzione da almeno 3 giorni
- [ ] Costo settimanale del workflow misurato
- [ ] Output verificato manualmente almeno una volta
- [ ] Ho deciso se mantenerlo, raffinarlo o rimuoverlo
- [ ] Per i workflow business: prerequisiti (CRM, Linear, ecc.) verificati prima dell'attivazione
- [ ] Workflow 11 pianificato: backup e report costi settimanali attivi entro il primo mese

## Link e risorse utili

- [The Complete Guide to Building Your Personal AI Agent](https://www.lennysnewsletter.com/p/openclaw-the-complete-guide-to-building) — workflow del team di Claire Vo
- [Building a Million Dollar Zero Human Company](https://www.bankless.com/podcast/building-a-million-dollar-zero-human-company-with-openclaw-nat-eliason) — l'episodio Bankless con Nat Eliason
- [OpenClaw Income Generation Stories](https://openclawdesktop.com/blog/openclaw-income-generation-community-stories.html) — casi reali raccolti dalla community

Per l'elenco completo delle fonti del libro, vedi [Appendice E](../Appendici/E-risorse-e-link-utili.md).

---

[← Capitolo 7](./07-prima-conversazione-onboarding-agente.md)  ·  [Indice](../README.md)  ·  [Capitolo 9 →](./09-aggiungere-strumenti-e-integrazioni.md)
