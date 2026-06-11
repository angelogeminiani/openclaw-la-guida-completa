# Capitolo 9 — Aggiungere strumenti e integrazioni [★★]

## Cosa imparerai

- Come collegare Gmail, Calendar, Drive, GitHub, Linear, Notion, Obsidian, CRM
- Come configurare la ricerca web e gli smart home device
- Come far "scoprire" nuovi tool all'agente
- Le regole di sicurezza per le integrazioni

## Prerequisiti

Aver provato almeno un workflow del [Capitolo 8](./08-dieci-workflow-pronti-all-uso.md). Per ogni integrazione serve un account sul servizio corrispondente (Gmail, GitHub, Linear, ecc.).

## Contenuto principale

Martedì mattina, ore 9:10. Chiedi a Polly di prepararti il solito brief e lei risponde: "Fatto. Però ho notato che mi chiedi ogni giorno di controllare gli issue su Linear, e io Linear non lo vedo. Vuoi che ti spieghi come darmi accesso?" Questo è il momento in cui un agente smette di essere una chat con superpoteri e diventa un collega operativo: quando comincia a *toccare* gli strumenti che usi davvero. Questo capitolo è la guida a quel passaggio — quali porte d'ingresso esistono, come aprirle una alla volta, e come farlo senza consegnare le chiavi di casa.

### Le quattro porte d'ingresso

Prima di collegare qualunque cosa, conviene avere chiaro il modello. Come hai visto nel Capitolo 2, un agente OpenClaw accede al mondo esterno attraverso quattro vie distinte, e scegliere quella giusta evita ore di frustrazione.

La prima sono i **tool nativi** del Gateway: filesystem, shell, ricerca web di base. Ci sono già, non vanno installati. La seconda sono le **skill**: pacchetti installabili dal registry ClawHub con `openclaw skills install <nome>`. Attenzione a un equivoco diffuso: `gog` — l'integrazione Google che hai installato durante l'onboarding del Capitolo 5 — è una **skill**, non un CLI tool a sé stante. È un bundle che insegna all'agente a parlare con Gmail, Calendar e Drive, con la sua autenticazione OAuth e le sue convenzioni. La terza via sono i **server MCP** (Model Context Protocol), lo standard aperto per esporre API e dati esterni in modo uniforme: ne parliamo in una sezione dedicata. La quarta è la più artigianale e la più sottovalutata: **descrivere un'API in TOOLS.md** e lasciare che l'agente la usi con i tool nativi (shell e `curl`).

Una bussola rapida:

| Caso | Porta consigliata |
|------|-------------------|
| Gmail, Calendar, Drive | skill `gog` |
| Servizio con server MCP | MCP |
| API interna o di nicchia | TOOLS.md + REST |
| File e comandi locali | tool nativi |

La regola pratica: se esiste una skill matura su ClawHub, usa quella; se il servizio pubblica un server MCP ufficiale, usa MCP; se nessuna delle due, TOOLS.md è il tuo amico. E in ogni caso vale il principio che ripeteremo fino alla noia: si parte in sola lettura, sempre.

**(i) Pro tip:** ogni integrazione ha un costo anche quando non la usi. Le descrizioni di skill e tool MCP entrano nel contesto dell'agente a ogni sessione, e contesto significa token: installare venti integrazioni "per sicurezza" rende l'agente più costoso e meno lucido. Aggiungi quando serve, rimuovi quando smetti di usare; il meccanismo di caricamento e il suo impatto sui costi sono spiegati nel [Capitolo 17](../PARTE-VII-Uso-avanzato/17-creare-skill-personalizzate.md).

### Google Workspace via gog: la prima integrazione vera

Se hai seguito il Capitolo 5, la skill `gog` è già installata e collegata alla Gmail dedicata creata durante il pre-work. Questa sezione serve a farla funzionare *bene*: scope graduali, account giusto, debug.

**L'account.** Usa l'account Google dedicato all'agente, non il tuo personale. Se per un workflow serve l'accesso al tuo calendario vero, la strada pulita è condividere il calendario con l'account dell'agente (da Google Calendar: impostazioni del calendario → "Condividi con persone specifiche" → permesso "Vedere tutti i dettagli degli eventi"). Stesso principio per Drive: condividi le singole cartelle che servono, non l'intero archivio. Così l'agente vede solo ciò che gli hai esplicitamente passato, e revocare l'accesso è un click.

**Gli scope, in due fasi.** L'autenticazione OAuth di `gog` parte la prima volta che l'agente prova a leggere la casella. Nella schermata di consenso Google, concedi nella prima fase solo le voci di *lettura* (leggere email, leggere eventi, leggere file). Le voci di *scrittura* — inviare email, creare eventi, modificare file — le aggiungerai tra una o due settimane, quando il digest mattutino del Capitolo 8 avrà girato abbastanza giorni da convincerti che l'agente legge le cose giuste e non fa pasticci. Per rifare il consenso con scope più ampi:

```bash
openclaw skills configure gog
```

**(i) Pro tip:** prima di concedere la scrittura, fai una prova generale: chiedi all'agente "componi la risposta a questa email ma NON inviarla, mostramela qui in chat". Se per una settimana le bozze sono buone, il passaggio a "invia pure" è una decisione informata, non un atto di fede.

**(#) Debug:** se `gog` smette di leggere la casella, nove volte su dieci è il consenso OAuth scaduto o revocato. Sintomi tipici: l'agente risponde "non riesco ad accedere a Gmail" oppure il digest mattutino arriva vuoto. Rilancia `openclaw skills configure gog` con Chrome aperto come browser di default e rifai il giro di consenso. Per verificare lo stato dell'accesso dal lato Google: myaccount.google.com → Sicurezza → "Connessioni di terze parti" (il percorso esatto può variare con gli aggiornamenti dell'interfaccia Google).

### GitHub: un PAT con il guinzaglio corto

Collegare GitHub trasforma l'agente in uno sviluppatore on-demand: può leggere issue, riassumere PR, analizzare codice. La chiave d'accesso è un Personal Access Token (PAT), e GitHub offre il formato giusto per i nostri scopi: i token **fine-grained**, che permettono di limitare sia i repository sia i permessi.

La procedura, passo per passo:

1. Su GitHub: foto profilo → *Settings* → *Developer settings* → *Personal access tokens* → *Fine-grained tokens* → *Generate new token*.
2. Dagli un nome descrittivo (`openclaw-readonly`) e una scadenza breve: 90 giorni. La scadenza è una funzione, non un fastidio — ti obbliga alla rotazione.
3. In *Repository access* scegli *Only select repositories* e seleziona solo i repo su cui l'agente deve lavorare. Mai *All repositories*.
4. In *Permissions* concedi il minimo: *Contents: Read-only* e *Issues: Read-only* bastano per il 90% dei casi d'uso iniziali. Niente *Administration*, niente *Workflows*.
5. Genera il token, salvalo **subito nel password manager** (lo vedi una volta sola) e consegnalo all'agente in modo che finisca nello store cifrato di OpenClaw, non in un file in chiaro.

Per la consegna, il dialogo è semplice: "Ti ho creato un PAT GitHub read-only per i repo X e Y. Te lo incollo ora: salvalo nelle tue credenziali cifrate e poi dimmi quanti issue aperti ci sono su X". L'ultimo pezzo della frase non è cortesia: è il test immediato che verifica che il token funzioni e che gli scope bastino.

Quando, settimane dopo, vorrai che l'agente apra issue o proponga PR, non allargare il token esistente: creane uno nuovo con *Issues: Read and write* (ed eventualmente *Pull requests: Read and write*), sempre limitato agli stessi repository. Due token con nomi chiari sono più facili da revocare di un token onnipotente.

### Linear, Notion e Obsidian

Questi tre sono lo spazio di collaborazione naturale tra te e l'agente, ognuno con il suo carattere.

**Linear** è il più immediato. Genera una API key personale da *Settings* → *Security & access* → *Personal API keys* (il percorso esatto può variare con le versioni dell'interfaccia), dalle un nome (`openclaw`), salvala nel password manager e consegnala all'agente come hai fatto col PAT GitHub. Le chiavi personali di Linear ereditano i tuoi permessi, quindi il contenimento qui si fa a monte: se vuoi un perimetro stretto, crea un account Linear dedicato all'agente con accesso ai soli team rilevanti — lo stesso pattern dell'account Google dedicato. Il primo task di prova: "elencami gli issue assegnati a me nel progetto Docs, solo titoli e stati".

**Notion** ha un passaggio in più che inganna quasi tutti la prima volta. Su notion.so/my-integrations crei una *internal integration* e ottieni il token, ma il token da solo non vede *niente*: in Notion ogni integrazione va invitata esplicitamente nelle pagine. Apri la pagina (o il database) che vuoi condividere → menu `···` → *Connections* → aggiungi la tua integrazione. La pagina e tutte le sue sottopagine diventano visibili; il resto del workspace resta invisibile. È un modello di sicurezza eccellente proprio perché è opt-in pagina per pagina: sfruttalo creando una pagina radice "Agente" e condividendo solo quella.

**Obsidian** è il caso più semplice e più elegante: non c'è nessun token, perché un vault Obsidian è una cartella di file Markdown sul filesystem — e OpenClaw *vive* di Markdown. Basta dire all'agente dov'è il vault e annotare le convenzioni in TOOLS.md: in quale cartella può scrivere, quale formato usare per i titoli, cosa non toccare. Se il Gateway gira su una macchina diversa da quella dove tieni il vault, la via standard è una cartella sincronizzata (Syncthing, iCloud Drive) montata sulla macchina dell'agente. Nat Eliason ha costruito su questo pattern l'intero sistema di memoria dei suoi agenti: file Markdown semplici, leggibili e versionabili, niente database.

**(i) Pro tip:** qualunque sia lo strumento, dai all'agente una "zona franca" in scrittura fin dal primo giorno — una pagina Notion, una cartella del vault, un progetto Linear di prova. Il modo più rapido per capire come scrive un agente è dargli un posto dove può scrivere senza fare danni.

### CRM: Attio e HubSpot

Se usi l'agente per lavoro commerciale — qualificazione lead, pipeline, follow-up come nel workflow 5 del Capitolo 8 — il CRM è l'integrazione che rende tutto concreto. Sia Attio sia HubSpot espongono API a token: in Attio generi una API key dalle impostazioni del workspace, in HubSpot crei una *private app* scegliendo gli scope (e qui vale la solita liturgia: scope CRM in sola lettura nella prima fase). Il rischio specifico dei CRM non è tecnico ma relazionale: un agente con accesso in scrittura al CRM può contattare clienti veri. Prima di dargli la possibilità di inviare email a un lead, fagli passare un periodo in cui *prepara* le email e te le sottopone in chat per approvazione. Quando il tasso di "approvo senza modifiche" supera il 90%, puoi parlare di autonomia.

### Ricerca web: oltre Brave

Il Capitolo 5 ha lasciato attiva Brave Search, e per la maggior parte degli usi va benissimo: da febbraio 2026 il piano gratuito vale $5 (~€4,60) di crediti al mese, circa 1.000 query, sufficienti per un agente personale. La domanda di questo capitolo è: quando ha senso aggiungere altro?

**Exa** è il complemento più utile: ricerca semantica, fortissima nei task "trovami altre cose come questa" (competitor, articoli simili, persone con un certo profilo). Se usi il workflow di monitoraggio competitivo o la qualificazione lead, Exa cambia la qualità dei risultati. **Perplexity API** restituisce risposte già sintetizzate e ragionate: più lenta e più costosa per singola chiamata, utile quando vuoi che un cron produca direttamente un paragrafo di sintesi invece di una lista di link. **Firecrawl** non è un motore di ricerca ma uno scraper: serve quando l'agente deve *leggere in profondità* pagine specifiche (documentazione, listini, changelog), ed è il naturale secondo stadio dopo una ricerca. La combinazione tipica per un agente di ricerca serio è Brave per le query generiche + Exa per quelle semantiche + Firecrawl per l'estrazione.

Ogni provider aggiuntivo significa una API key in più: vale la routine ormai familiare — chiave generata, salvata nel password manager, consegnata all'agente verso lo store cifrato, mai in un file in chiaro.

### Smart home: l'esempio Home Assistant

La smart home è l'integrazione che fa più scena ("Ho un neonato, abbassa le luci e metti il rumore bianco alle 20:30" — l'esempio è di Claire Vo) e, paradossalmente, una delle più sicure da concedere: le luci di casa sono meno delicate della tua inbox. Eight Sleep, Sonos e Philips Hue hanno API dirette utilizzabili con i rispettivi token, ma la strada che consigliamo è un'altra: far passare tutto da **Home Assistant**, che fa da hub unico e dà all'agente una sola API per l'intera casa.

L'esempio completo. Su Home Assistant, crea un token dedicato: profilo utente → scheda *Sicurezza* → *Token di accesso a lunga scadenza* → *Crea token*, nome `openclaw`. Salvalo nel password manager e consegnalo all'agente come sempre. Poi verifica che la REST API risponda dalla macchina dove gira il Gateway:

```bash
# test: list entity states via HA REST API
curl -s -H "Authorization: Bearer <token>" \
  http://homeassistant.local:8123/api/states \
  | head -c 300
```

Se vedi un JSON di entità, il collegamento c'è.

**(#) Debug:** `homeassistant.local` si risolve via mDNS, che l'hardening del Capitolo 4 disabilita dentro il container. Se il Gateway gira in sandbox e il curl di prova va in timeout, usa l'indirizzo IP statico di Home Assistant al posto del nome `.local` — e aggiungilo all'allowlist di rete. Ora la parte che trasforma una API in una integrazione: le istruzioni operative in TOOLS.md.

```markdown
## Home Assistant
- URL: http://homeassistant.local:8123
- Token: nello store cifrato, voce "ha-openclaw"
- Usa la REST API (/api/states, /api/services)
  per leggere stati e attivare scene.
- Solo lettura su: caldaia, allarme, serrature.
- Mai chiamare servizi su device sconosciuti:
  prima chiedi conferma in chat.
```

Da questo momento puoi parlare alla casa in linguaggio naturale: "che temperatura c'è in camera?", "alle 20:30 attiva la scena Notte". E l'ultima riga del blocco qui sopra non è decorativa: serrature e allarmi vanno esclusi dalla scrittura *per iscritto*, perché l'agente legge TOOLS.md a ogni sessione e quelle tre righe sono il tuo guardrail permanente.

**(!) Attenzione:** un agente che controlla la casa è un agente che può aprire la porta. Se hai serrature smart, trattale come tratteresti l'accesso in scrittura alla tua email: escluse di default, e se proprio devono entrare in un workflow, solo con conferma esplicita in chat per ogni singola azione.

### MCP: lo standard dei connettori

Finora abbiamo collegato servizi uno alla volta, ognuno col suo rito. Il **Model Context Protocol (MCP)** è il tentativo — riuscito — di standardizzare questo lavoro: un protocollo aperto, nato in casa Anthropic a fine 2024 e adottato trasversalmente dall'industria, in cui ogni servizio espone un "server" che descrive i propri strumenti in formato uniforme. L'agente si connette al server e *scopre da solo* cosa può fare: quali operazioni esistono, che parametri vogliono, cosa restituiscono. Ad aprile 2026 il conteggio superava gli 860 tool MCP disponibili tra server ufficiali e di community: GitHub, Linear, Notion, Slack, Stripe, database, browser.

Quando preferire MCP a una skill? La skill incapsula anche *come* usare bene uno strumento (convenzioni, prompt, flussi: `gog` ne è l'esempio); il server MCP espone le operazioni grezze e lascia il "come" all'agente. In pratica: per i servizi che il libro ha già coperto con skill mature, resta sulla skill; per la coda lunga di tutto il resto, MCP è la via più rapida e più mantenuta.

I server MCP si dichiarano nella configurazione del Gateway. La forma è questa (indicativa — la sintassi esatta evolve, verificala nella Configuration reference della documentazione ufficiale, in Appendice E):

```yaml
# ~/.openclaw/config.yaml — MCP server (indicative)
mcp:
  servers:
    <nome-server>:
      command: "npx"
      args: ["-y", "<pacchetto-server-mcp>"]
```

Dopo il riavvio del Gateway (`openclaw gateway restart`), chiedi all'agente "che tool MCP vedi?" per verificare che il server sia caricato. Vale anche qui la regola della supply chain che approfondiremo nel [Capitolo 13](../PARTE-V-Sicurezza-costi/13-sicurezza-la-guida-che-devi-leggere.md): un server MCP è codice di terze parti che gira con i permessi dell'agente. Installa solo server ufficiali o con reputazione verificabile, e dai loro credenziali con lo scope minimo, come a qualunque altra integrazione.

Una menzione a parte merita **Composio**, il meta-connettore: un servizio che aggrega centinaia di integrazioni (con relativa gestione OAuth) dietro un'unica autenticazione, esposta anche via MCP. È la scorciatoia quando devi collegare cinque servizi SaaS in un pomeriggio; il prezzo è che un solo fornitore vede i token di tutti i tuoi servizi. Per un uso personale con servizi delicati (email, CRM con dati di clienti), valuta se la comodità vale la concentrazione del rischio.

### API personalizzate via TOOLS.md

E quando non esiste né skill né server MCP — l'API interna della tua azienda, il gestionale di nicchia, il servizio appena nato? Qui OpenClaw mostra il suo tratto più caratteristico: non serve scrivere un connettore. L'agente sa già usare `curl` e leggere JSON; quello che gli manca è la *conoscenza locale* — dove sta l'API, come ci si autentica, cosa è lecito fare. Ed è esattamente ciò che TOOLS.md esiste per contenere: note operative in linguaggio naturale, come le ha definite il Capitolo 2.

Il metodo in tre mosse. Primo: scrivi in TOOLS.md una scheda come quella vista per Home Assistant — endpoint base, dove vive il token (nello store cifrato, mai il token stesso in chiaro nel file), le due o tre chiamate utili, i divieti. Secondo: se l'API ha una documentazione OpenAPI o una pagina di reference, indicane la posizione — l'agente andrà a leggersela da solo quando serve. Terzo: chiedi un task piccolo e verificabile ("interroga l'endpoint di stato e dimmi cosa risponde") e osserva. Se l'agente sbaglia qualcosa — un header, una convenzione di paginazione — correggi la scheda in TOOLS.md, non l'agente: la prossima sessione ripartirà dalla versione corretta. È documentazione che diventa capacità, ed è il motivo per cui un TOOLS.md curato vale più di dieci integrazioni installate e dimenticate.

### Le regole di sicurezza delle integrazioni

Chiudiamo con la parte che regge tutto il resto. Ogni integrazione di questo capitolo è una chiave consegnata a un software che agisce in autonomia: la differenza tra un assistente potente e un incidente raccontato sui forum sta nelle regole di custodia.

La prima regola l'hai già letta cinque volte: **read-only prima, scrittura poi**, e solo dopo un periodo di osservazione. La seconda: **scope minimo** — il token perfetto è quello che permette esattamente il task previsto e nient'altro (il PAT fine-grained limitato a due repo ne è il modello). La terza riguarda la custodia: i token vivono nel **password manager** (la tua copia) e nello **store cifrato di OpenClaw** sotto `~/.openclaw/credentials/` (la copia dell'agente). Mai — e qui il libro è categorico, come lo è stato nei Capitoli 4 e 5 — in un file `.env` in chiaro, in uno script, in un messaggio di chat che non sia la consegna iniziale, o peggio in un repository. Se l'agente gira in sandbox, la forma più alta di custodia è il *credential proxy* del [Capitolo 4](../PARTE-II-Installazione/04-preparare-un-ambiente-sicuro-docker-sandbox.md): le chiavi non entrano proprio nel perimetro che l'agente può leggere. La quarta regola: **rotazione** — le scadenze brevi dei token non sono burocrazia, sono il meccanismo che limita la finestra di danno di una chiave compromessa. E l'ultima: ogni tre mesi, un giro di pulizia — `openclaw security audit` e una passata sui pannelli dei servizi (Google, GitHub, Linear, Notion) per revocare ciò che non usi più.

Un dettaglio facile da dimenticare se hai seguito l'hardening del Capitolo 4: se il Gateway gira dietro una rete con egress filtering, ogni integrazione nuova richiede di aggiungere i suoi domini all'allowlist in uscita (api.github.com, api.linear.app, api.notion.com, l'IP di Home Assistant, e così via). Il sintomo classico è un'integrazione che funziona nei test fatti dall'host e fallisce — in silenzio, o con un timeout — quando a usarla è l'agente dal container. Aggiorna l'allowlist *prima* di consegnare il token e ti risparmi una sessione di debug.

**(!) Attenzione — Regole di sicurezza per le integrazioni:**
- Iniziare **sempre** con token read-only
- Non dare accesso in scrittura a email, documenti o codice finché non ci si fida dell'agente
- Ricordare: l'agente può inviare email, sovrascrivere documenti, eliminare ticket, compilare form, fare deploy di codice in produzione — se ha i permessi per farlo
- Usare 1Password o un password manager per gestire API key e token

## Prompt pronti all'uso

**Prompt pronto:**
> "Voglio collegarti al mio Gmail e Google Calendar tramite la skill `gog`. Aiutami a configurarla nel modo più sicuro: (1) consigliami se usare il mio account principale o crearne uno dedicato, (2) elenca gli scope OAuth minimi che servono per leggere ma non inviare, (3) proponi un test piccolo per verificare che funzioni, (4) spiegami come revocare l'accesso se cambio idea."

**Prompt pronto:**
> "Ti ho creato un Personal Access Token GitHub fine-grained, read-only, limitato ai repository [X] e [Y]. Te lo incollo nel prossimo messaggio: salvalo nel tuo store di credenziali cifrato, conferma di averlo salvato senza ripeterlo in chat, e poi fai un test: elencami gli issue aperti su [X] con titolo e data."

**Prompt pronto:**
> "Fai un inventario delle tue integrazioni: per ognuna dimmi (1) che accesso hai (lettura/scrittura), (2) quando l'abbiamo configurata, (3) quando l'hai usata l'ultima volta. Segnala quelle che non usi da più di un mese: valuteremo insieme se revocarle."

**Prompt pronto:**
> "Vorrei che tu potessi lavorare con [servizio]. Cerca se esiste una skill su ClawHub o un server MCP ufficiale per questo servizio: dimmi chi lo mantiene, quando è stato aggiornato l'ultima volta e che permessi richiede. Poi proponimi un piano di integrazione in sola lettura, con il test più piccolo possibile per verificarla. Non installare niente senza la mia conferma."

## Errori comuni e come risolverli

**Sintomo:** `gog` non riesce a leggere Gmail.
Causa: scope OAuth insufficiente o consenso scaduto.
Fix: rilanciare `openclaw skills configure gog` e
rifare il consenso OAuth con gli scope minimi
necessari.

**Sintomo:** token GitHub finito nei log.
Causa: PAT con scope troppo ampi salvato in chiaro
o stampato per debug.
Fix: rigenera subito il token, usa un PAT
fine-grained con scope minimi, conservalo nel
password manager e nello store cifrato — mai in
chiaro, mai in console.

**Sintomo:** l'agente cita un'integrazione che
"esiste" ma non funziona.
Causa: allucinazione del modello LLM.
Fix: verificare sempre nei docs ufficiali
(`docs.openclaw.ai`) prima di credere a una
capability.

**Sintomo:** integrazione funziona oggi, fallisce
domani.
Causa: token scaduto o servizio cambia API.
Fix: configurare un alert sul cron che usa
l'integrazione; rotazione periodica dei token.

**Sintomo:** il token Notion è valido ma l'agente
"non vede" nessuna pagina.
Causa: l'integrazione non è stata invitata nelle
pagine (in Notion l'accesso è opt-in per pagina).
Fix: aprire la pagina → menu `···` → *Connections*
→ aggiungere l'integrazione.

**Sintomo:** l'integrazione funziona nei test
dall'host ma fallisce quando la usa l'agente dal
sandbox.
Causa: dominio dell'API assente dall'allowlist di
egress del Capitolo 4, o nome `.local` (mDNS) non
risolvibile dentro il container.
Fix: aggiungere il dominio all'allowlist, usare IP
statici al posto dei nomi mDNS, poi
`openclaw gateway restart`.

**Sintomo:** il server MCP è in config ma l'agente
non vede i suoi tool.
Causa: Gateway non riavviato dopo la modifica, o
sintassi della config non valida.
Fix: `openclaw gateway restart`, poi chiedere
all'agente "che tool MCP vedi?"; controllare
`openclaw logs --follow` per errori di avvio.

## Checklist di fine capitolo

- [ ] Almeno un'integrazione configurata e testata con un piccolo task
- [ ] Token con scope minimo necessario (mai "admin" se basta "read")
- [ ] Tutti i secrets nel password manager e nello store cifrato `~/.openclaw/credentials/` — mai in un `.env` in chiaro, nel codice o in chat
- [ ] Ho un piano di rotazione dei token (es. trimestrale)
- [ ] Gli accessi in scrittura sono arrivati solo dopo un periodo di osservazione in read-only
- [ ] Se l'agente gira in sandbox, il credential proxy del Capitolo 4 è attivo

## Link e risorse utili

- [Documentazione ufficiale](https://docs.openclaw.ai) — lista completa di skill, integrazioni e MCP supportati
- [The Complete Guide to Building Your Personal AI Agent](https://www.lennysnewsletter.com/p/openclaw-the-complete-guide-to-building) — esempi di integrazione con Gmail, Linear e Notion
- [Configuration reference](https://docs.openclaw.ai/gateway/configuration) — sintassi della config del Gateway, inclusi i server MCP
- [Use OpenClaw to Build a Business That Runs Itself](https://creatoreconomy.so/p/use-openclaw-to-build-a-business-that-runs-itself-nat-eliason) — il sistema Markdown-first di Nat Eliason
- [Run OpenClaw Securely in Docker Sandboxes](https://www.docker.com/blog/run-openclaw-securely-in-docker-sandboxes/) — credential proxy e isolamento delle chiavi

Per l'elenco completo delle fonti del libro, vedi [Appendice E](../Appendici/E-risorse-e-link-utili.md).

---

[← Capitolo 8](./08-dieci-workflow-pronti-all-uso.md)  ·  [Indice](../README.md)  ·  [Capitolo 10 →](../PARTE-IV-Multi-agente/10-perche-un-solo-agente-non-basta.md)
