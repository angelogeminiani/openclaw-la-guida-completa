# Capitolo 1 — Cos'è OpenClaw e perché è importante [★]

## Cosa imparerai

- Che cos'è un agente autonomo e in che cosa si distingue da un chatbot
- La storia del progetto: da Clawdbot a OpenClaw in 90 giorni
- Perché Nvidia l'ha definito "the operating system for personal AI"
- In che modo si differenzia da ChatGPT, Siri e Alexa
- Come si distribuisce il lavoro di un agente in una giornata tipo

## Prerequisiti

Nessuno. Questo è il punto di ingresso del libro: ti basta una mezz'ora e voglia di capire cos'è davvero un agente autonomo.

## Contenuto principale

### L'era degli agenti personali

Per vent'anni abbiamo chiamato "intelligenti" software che, in realtà, erano dizionari verbali un po' sofisticati. Chiedevi qualcosa, ricevevi una risposta. Bello, utile, niente di rivoluzionario. Il 2026 è l'anno in cui questa abitudine si è rotta. Non perché i modelli linguistici siano diventati improvvisamente più bravi a parlare, ma perché qualcuno ha capito che la cosa interessante non è la conversazione: è l'azione.

OpenClaw è la dimostrazione più visibile di questo passaggio. È un framework open-source con licenza MIT che prende un LLM — Claude, GPT, Gemini, Nemotron, un modello locale, quello che preferisci — e lo trasforma in qualcosa di molto più simile a un dipendente che a un assistente vocale. Un dipendente digitale che vive su un computer dedicato, ha i suoi canali (Telegram, WhatsApp, Slack e oltre venti altri), legge la posta al posto tuo, controlla il calendario, scrive codice, naviga il web, prende decisioni nei limiti che gli hai dato. Quando Nvidia decide di ribattezzare la categoria, non usa giri di parole: lo definisce "the operating system for personal AI." È una frase di marketing, certo, ma cattura il punto.

Per capire la differenza concreta, immagina questa scena. Sono le 7:00 del mattino. Il telefono vibra: sul canale Telegram dedicato c'è un messaggio del tuo agente. Dice che hai 23 email nuove, di cui 4 che richiedono risposta entro la giornata; il primo meeting è alle 9:30 con un cliente nuovo, e ha già preparato un brief di tre paragrafi su di lui leggendo il sito e l'ultima newsletter; il caffè è finito ieri sera (l'ha visto da una nota su Obsidian) e ha aggiunto la marca giusta al carrello di un servizio di consegna ma non lo conferma finché non glielo dici tu. Tu rispondi "ok, conferma il caffè e mandami il brief". Lui esegue. Niente di tutto questo è successo perché glielo hai chiesto stamattina: era già nei suoi compiti, gestiti da una manciata di cron job che lui stesso si è scritto la prima settimana che lavorate insieme. Questo è un agente. Un chatbot, alle 7:00, dorme.

### Da Clawdbot a OpenClaw: 90 giorni

La storia di OpenClaw è anomala perfino per gli standard del 2026. A novembre 2025 Peter Steinberger — austriaco, fondatore di PSPDFKit con un'exit da circa 100 milioni di euro alle spalle, in pausa creativa dopo l'uscita dall'azienda — pubblica su GitHub un esperimento personale chiamato Clawdbot. È un piccolo wrapper su Claude che permette di chattare con un agente via Telegram. Niente di pretenzioso: è "vibe coding", come lo definirà lui stesso. Pochi giorni dopo, il progetto ha già qualche centinaio di stelle.

A gennaio 2026 arriva la prima frizione: Anthropic contesta l'uso del nome perché "Clawd" gioca troppo apertamente con "Claude" e con la mascotte ufficiale del lobster. Steinberger rinomina il progetto Moltbot. Il nome resiste tre giorni — "Moltbot non suonava bene", riconoscerà poi — e diventa OpenClaw. È da qui che la curva di adozione esplode. Il 24 gennaio 2026 DigitalOcean lancia il primo Marketplace 1-Click ufficiale per OpenClaw, segnale che il progetto è uscito dall'ambito hobbystico. Quattro giorni dopo, il 28 gennaio, Matt Schlicht presenta Moltbook: un social network in cui non sono gli umani a postare, ma i loro agenti. Sembra una boutade; al 5 febbraio ha già più di 200.000 agenti registrati. In sessanta giorni il repository GitHub ha superato 247.000 stelle, un ritmo che React, in dieci anni di vita, non ha mai avvicinato.

Il 14 febbraio 2026 arriva il colpo di scena. Steinberger annuncia di aver accettato un ruolo in OpenAI e di trasferire OpenClaw a una fondazione open-source indipendente, supportata ma non controllata da OpenAI. La missione che si dà nella nuova casa la riassume in una frase: "costruire un agente che anche mia mamma possa usare." Per molti progetti questo sarebbe stato il momento dell'incertezza; per OpenClaw è il momento della legittimazione. La community capisce che il software resterà open, BYOK (bring-your-own-key: il modello lo porti tu, con la tua chiave API), model-agnostic. Le stelle continuano a salire: ad aprile 2026 sono oltre 343.000, con 67.000+ fork. Il 10 marzo Meta Superintelligence Labs annuncia l'acquisizione di Moltbook: la prima exit visibile dell'ecosistema, mentre il framework su cui poggia rimane open. La biforcazione è netta e ha conseguenze importanti per la governance, di cui parla il Capitolo 21.

#### La svolta del 4 aprile

Il 4 aprile 2026 arriva il terremoto. Anthropic blocca via OAuth l'uso delle sottoscrizioni Claude Pro e Max con OpenClaw e con qualunque altro tool di terze parti. Chi finanziava l'agente con i $20 (~€18) al mese del Pro si ritrova spento dall'oggi al domani; chi era passato a Max scopre che l'unico percorso supportato è ora la API key dedicata, con costi che si misurano per token. È un giorno di panico nella community: thread di Hacker News in tempo reale, fork del progetto pensati per altri provider, guide spuntate nel giro di ore per migrare a Kimi K2.5, MiniMax M2.5, GPT-5.1 o ai modelli locali Nemotron. Il Capitolo 14 ricostruisce la cronologia ora per ora; qui basta sapere che da quel giorno l'equazione dei costi di OpenClaw è cambiata, e che il libro tiene conto di entrambi gli scenari (pre-ban e post-ban) perché molti lettori incontreranno tutorial vecchi che non lo fanno.

Le date da ricordare, in fila:

- **novembre 2025** — nasce Clawdbot, esperimento personale
- **gennaio 2026** — rinomina: Clawdbot → Moltbot → OpenClaw
- **24 gennaio 2026** — DigitalOcean lancia l'1-Click ufficiale
- **28 gennaio 2026** — debutta Moltbook, il social degli agenti
- **14 febbraio 2026** — Steinberger entra in OpenAI; OpenClaw passa a una fondazione indipendente
- **10 marzo 2026** — Meta Superintelligence Labs acquisisce Moltbook
- **4 aprile 2026** — ban di Anthropic sulle sottoscrizioni Claude Pro/Max

### Chatbot, assistente, agente: tre cose diverse

Il marketing AI ha mescolato in una sola parola — "assistente" — tre categorie che funzionano in modi profondamente diversi. È la distinzione che decide se le tue aspettative saranno confermate o tradite.

Il confronto regge su sei assi.

**Chi inizia l'azione.** Nel chatbot (ChatGPT, Claude chat), sempre l'utente. Nell'assistente proattivo (Siri, Alexa, Google Assistant), l'utente o un trigger predefinito — la sveglia, il calendario. Nell'agente autonomo, l'utente, un trigger, oppure l'agente stesso, via cron e heartbeat.

**Memoria.** Il chatbot ricorda la sessione corrente, con persistenza opzionale; l'assistente ha template ristretti (preferenze, lista della spesa); l'agente ha una memoria persistente, multi-livello e — soprattutto — editabile da te.

**Strumenti e integrazioni.** Per chatbot e assistenti li decide il vendor, preconfezionati. Per l'agente li configuri tu, li espandi a runtime, e si integra con qualsiasi cosa abbia un'API o una shell.

**Esecuzione fra una richiesta e l'altra.** Chatbot e assistenti: nessuna. L'agente lavora in background, 24 ore su 24.

**Lock-in del modello.** Totale per chatbot e assistenti, vincolati al fornitore. Nessuno per l'agente: il modello lo porti tu (BYOK) e lo cambi quando vuoi.

Un chatbot non sa che ora è quando non gli stai parlando. Un assistente proattivo sa che ora è ma agisce solo dentro i binari che il vendor ha previsto. Un agente autonomo sa che ora è, decide cosa fare di sua iniziativa entro confini che hai scritto tu, e quando non sa cosa fare ti scrive per chiedere. È il tipo di differenza che si capisce solo dopo qualche giorno di convivenza, ed è il motivo per cui il Capitolo 7 di questo libro è dedicato esclusivamente ai primi dieci minuti di onboarding.

#### L'architettura in 60 secondi

Sotto il cofano, OpenClaw è composto da quattro pezzi che lavorano insieme. Il primo è il **Gateway**, un processo locale che fa da centralino: tutto entra e tutto esce da qui. Il secondo sono i **canali**, le connessioni verso l'esterno (Telegram, WhatsApp, Slack, Discord, Signal, iMessage e altri ancora) — ogni canale è un plug-in che parla un protocollo specifico e consegna i messaggi al Gateway. Il terzo sono gli **agenti**, identità separate con propri file `SOUL.md` e `IDENTITY.md`, ognuno con il suo workspace, le sue skill, la sua memoria. Il quarto sono le **skill**: cartelle con un `SKILL.md` dentro che insegnano all'agente come fare cose specifiche (mandare email, leggere PDF, cercare sul web). A coordinare il tempo ci sono i **cron job**, che fanno scattare azioni a intervalli regolari, e l'**heartbeat**, un battito di sistema che permette all'agente di pensare anche quando nessuno gli ha appena scritto.

Il flusso di un task tipico si legge così: arriva un messaggio su un canale, il Gateway lo riceve e lo instrada all'agente giusto sulla base del binding configurato, l'agente apre o riprende una sessione, ragiona, chiama una o più skill, esegue, e infine torna al canale con la risposta. In pseudocodice, un ciclo minimo:

```yaml
# A simplified message lifecycle, top-down.
inbound:
  channel: telegram
  binding: agent.polly
agent:
  sessions: main
  thinks_with: claude-sonnet-4-6
  uses_skills: [gog, summarize, web_search]
outbound:
  reply_to: telegram
  attach: [link_preview, optional_artifact]
```

Il Capitolo 2 sviluppa il modello mentale, il Capitolo 20 entra nei dettagli tecnici (WebSocket control plane, Pi agent runtime, Live Canvas). Per ora è sufficiente avere questa mappa in testa.

### Una giornata tipo con il tuo agente

Per ancorare l'idea nel concreto, segui un agente attraverso una giornata qualunque. Non è prescrittivo — il tuo agente farà cose diverse — ma serve a vedere come il lavoro autonomo si distribuisce nel tempo, senza che tu debba pensarci.

**Mattina, 7:00.** L'heartbeat ha già fatto scattare il digest delle email e del calendario. Sul tuo Telegram trovi tre paragrafi: cosa è successo dalle 18:00 di ieri, cosa serve oggi, cosa puoi ignorare. Tu rispondi due monosillabi ("conferma il caffè", "no, non rispondo io a quella mail"). L'agente esegue.

**Mezzogiorno, 12:30.** Stai per andare a pranzo. Ricevi un ping: il cliente delle 14:30 ha appena pubblicato un post su LinkedIn che probabilmente vorrai citare nel meeting. Nessun agente di calendario te lo avrebbe segnalato. Il tuo sì, perché ha dei cron job che, mezz'ora prima di ogni meeting, controllano i canali pubblici del partecipante esterno e ti mandano un breve aggiornamento rispetto al brief di stamattina.

**Pomeriggio, 15:45.** Il meeting è andato bene. Mentre cammini al supermercato scrivi all'agente: "preparami una bozza di follow-up per il cliente X, tienila corta, riprendi il punto sul pricing". Quando arrivi a casa, nella cartella `~/Drafts/` trovi un file `.md` con la bozza. Tu correggi due frasi e dai l'OK per l'invio.

**Sera, 22:00.** Tu stai per spegnere il telefono. L'agente sta entrando nella sua finestra di manutenzione: sintetizza la giornata in una nota, aggiorna il knowledge graph con tre fatti nuovi, prepara il digest per domani. Se gli hai dato il permesso, può anche eseguire il backup della cartella `~/.openclaw/` su un volume crittografato (la routine di backup la imposti nel Cap. 3; permessi e cifratura sono al Cap. 13).

Niente di quanto sopra è inventato: sono pattern reali, ricavati dai workflow del Cap. 8 e dai cron del Cap. 18. Il punto del capitolo è solo riconoscere che, fra le 7:00 e le 22:00, il lavoro è successo perché qualcuno lo ha *fatto succedere*, non perché tu lo hai chiesto.

### Per chi è OpenClaw — e per chi non lo è

OpenClaw funziona molto bene per tre profili. Il primo è il **knowledge worker** che vive di email, calendario, ricerca, documenti: un agente che gestisce il digest mattutino, prepara i meeting e segue i lead libera due o tre ore di lavoro a basso valore. Il secondo è il **founder o solopreneur** che vuole automatizzare interi pezzi di azienda: Nat Eliason ne ha parlato apertamente raccontando una "zero-human company" da oltre $177.000 (~€163.000) in due mesi, costruita sopra un piccolo team di agenti specializzati. Il terzo è la **famiglia o coppia tech-savvy** che adotta un agente come maggiordomo digitale per spese, calendario condiviso, viaggi, scuola dei bambini.

OpenClaw è una scelta sbagliata per altri tre profili, almeno oggi. Chi cerca **un'esperienza simile a ChatGPT**, dove la cosa più sofisticata è una conversazione lunga, qui si trova davanti un'overdose di complessità che non gli serve: meglio restare sul prodotto consumer. Chi opera in **ambienti regolati con vincoli stretti di data residency** — l'obbligo di tenere i dati entro confini geografici definiti — come sanità, finanza e settore pubblico deve fare un'analisi seria di rischio e di conformità prima di pensarci, perché il modello di esecuzione di OpenClaw — accesso pieno al filesystem, esecuzione di comandi shell, comunicazione con API esterne — non è compatibile out-of-the-box con la maggior parte dei requisiti regolatori; in quei casi conviene guardare a NemoClaw o IronClaw (vedi più sotto). Chi pensa di provarlo "giusto un attimo" sul **portatile di lavoro** sta facendo un errore di sicurezza che il Capitolo 13 spiega in dettaglio: OpenClaw va su un computer dedicato, sempre.

### Il fenomeno culturale

I numeri di adozione del progetto sono difficili da inquadrare con metriche tradizionali. Ad aprile 2026 il repository GitHub conta 343.000+ stelle e 67.000+ fork, con oltre 200.000 agenti registrati su Moltbook prima dell'acquisizione Meta. Sono dati che, da soli, dicono poco; quello che li rende interessanti è il tessuto culturale che si è formato attorno. La community si chiama #LobsterGang, prende il nome dalla mascotte (un'aragosta digitale che muta — "molts" — quando l'agente si aggiorna), parla un suo gergo fatto di submolts, hatch (la "schiusa": il primo avvio di un agente), soul-files, e produce meme con la stessa frequenza con cui produce pull request.

Sopra il framework è cresciuto un mercato di piattaforme che eliminano la frizione di installare in proprio: StartClaw, MyClaw, SimpleClaw, UniClaw, Plus One, OpenClaw Desktop. Sono tutte hosted, ognuna con un taglio diverso (alcune più orientate ai team, altre alle famiglie, una perfino integrata in una newsletter). Ne parla il Capitolo 3, che aiuta a scegliere se installare in proprio o appoggiarsi a un servizio. In parallelo è esploso il registry di skill chiamato ClawHub, con migliaia di skill di terze parti — di cui, va detto subito, una percentuale non trascurabile è risultata problematica dal punto di vista della sicurezza (è la storia di ClawHavoc, raccontata nel Capitolo 13).

Claire Vo, che ha scritto sulla guida-fiume di Lenny's Newsletter una delle analisi più lette sul tema, sintetizza l'effetto del prodotto come "il primo prodotto agentico che provoca la sensazione di assumere un team". È una frase ottimistica, e non andrebbe presa alla lettera; ma cattura perché OpenClaw, a differenza di tante automazioni che si "imparano da capo", richiede un'attitudine da manager più che da utente.

### Confronto con le alternative

OpenClaw non è solo nel suo segmento, e tutto il libro presuppone che il lettore sia in grado di scegliere consapevolmente. La tabella seguente riassume le sei alternative più rilevanti a maggio 2026.

- **NanoClaw** — per hobbisti e dev prudenti. Container Docker isolati per chat, solo Claude, giovane ma stabile. Sceglilo se vuoi il minimo set-up sicuro e non ti serve il multi-canale ricco.
- **NemoClaw** (Nvidia) — per l'enterprise. Sandboxing OpenShell a livello kernel con policy YAML, multi-modello via router locale/cloud, maturità early enterprise. Sceglilo se hai requisiti di compliance e vuoi lo stack Nvidia.
- **IronClaw** (NEAR AI) — per chi mette la privacy prima di tutto. Sandbox in Rust con focus sulla memory safety, model-agnostic, ancora early. Sceglilo se privilegi la safety formale e la zero telemetria.
- **ZeroClaw** — per l'edge computing. Un binary di 3,4 MB, deny-by-default, model-agnostic, early. Sceglilo per un agente su device costretto (Raspberry Pi, micro-VPS).
- **Moltworker** — per chi non vuole gestire infrastruttura. Sandbox gestita da Cloudflare, modello proprietario del provider, esperienza hosted/serverless.
- **Claude Code / Codex CLI** — per sviluppatori. Nessun sandboxing (girano nel terminale), vincolati ad Anthropic/OpenAI, maturi. Sceglili se il tuo unico caso d'uso è il coding.

In termini pratici: scegli OpenClaw quando vuoi il sistema più completo, multi-canale, multi-agente, con la possibilità di sostituire il modello in qualsiasi momento; scegli NanoClaw se preferisci un perimetro più piccolo e ti basta Claude; scegli NemoClaw se la conversazione che dovrai fare con il tuo team di sicurezza prevede già la parola "policy"; scegli IronClaw se la sicurezza la prendi sul serio fin dal linguaggio con cui è scritto il software; scegli Claude Code o Codex CLI se non ti interessa l'agente personale e ti basta uno strumento da terminale per programmare. Il libro dedica capitoli specifici a ciascuna alternativa quando entra nei rispettivi temi (sicurezza al Cap. 13, deploy al Cap. 19, ecosistema al Cap. 21).

### Tre obiezioni che sentirai (e cosa rispondere)

Quando racconti a qualcuno che usi OpenClaw, ricevi quasi sempre tre risposte. Vale la pena anticiparle, perché sono utili anzitutto a te per ridimensionare le aspettative.

**"Ma è solo un wrapper di Claude, no?"** Una metà di verità. OpenClaw non possiede un modello: usa Claude, GPT, Gemini, Nemotron, ciò che gli dai. Quello che il framework aggiunge è tutto il resto: gli agenti come unità di esecuzione, le sessioni che sopravvivono fra una conversazione e l'altra, il routing dei canali, il sistema di skill, i cron, l'heartbeat, l'isolamento dei workspace. Chiamarlo "wrapper" è come chiamare un sistema operativo "wrapper di un microprocessore". Tecnicamente non è falso, ma manca la parte interessante.

**"Se ha accesso al computer, prima o poi fa danni."** Anche qui la metà di verità è reale: OpenClaw può fare danni, e in 90 giorni di vita pubblica li ha fatti. Le storie ci sono e vanno dette: il caso MoltMatch documentato da Jack Luo (un agente che ha agito oltre i limiti previsti dall'utente), le skill di terze parti malevole su ClawHub raccolte sotto il nome ClawHavoc, vulnerabilità come **ClawJacked** — il nome con cui la community chiama la CVE-2026-25253. La risposta corretta non è "non succederà", è "ho pianificato il dove e il come". Il Cap. 13 entra nei dettagli, ma il principio è semplice: computer dedicato, sandbox, scope minimo per i token, audit periodico. Chi salta questi passaggi finisce nelle storie. Chi li rispetta riduce il rischio a un livello accettabile.

**"Ma posso fare la stessa cosa con Zapier o n8n."** Per molti task automatici sì. Zapier e n8n risolvono molto bene il caso "trigger → azione → sì/no". OpenClaw risolve un caso diverso: "trigger → ragionamento → decisione → eventualmente più azioni → eventualmente fare una domanda all'umano → riprendere domani". Il discrimine è la presenza del *ragionamento* fra il trigger e l'azione, e il fatto che il ragionamento venga da un LLM con contesto persistente. Se i tuoi workflow non hanno bisogno di ragionamento, OpenClaw è overkill: resta su Zapier. Se ne hanno bisogno, OpenClaw è la categoria giusta.

**(i) Pro tip:** se sei indeciso fra OpenClaw e una delle alternative, non scegliere oggi. Leggi il Capitolo 3 (dove installare) e il Capitolo 13 (sicurezza) e poi torna qui: il 90% delle decisioni si prende sulla base del *dove* prima ancora che del *cosa*.

**Prompt pronto:** *(da usare dopo l'installazione — Cap. 5)*
> "Presentati. Dimmi chi sei, cosa sai fare e quali limiti hai. Elenca i canali attraverso cui possiamo parlare e le skill che hai installate."

**(!) Attenzione:** OpenClaw ha accesso completo al computer su cui gira: filesystem, rete, comandi shell. Questo lo rende potente *e* pericoloso. Non installarlo mai su un computer in uso attivo.

## Errori comuni e come risolverli

**Sintomo:** confondere OpenClaw con Claude o ChatGPT.
Causa: marketing AI poco preciso, abitudine ai chatbot.
Fix: OpenClaw è un *framework* che usa un LLM (Claude,
GPT, Nemotron, ecc.). Il framework agisce, l'LLM ragiona.

**Sintomo:** aspettarsi che l'agente "indovini" cosa fare.
Causa: mindset da chatbot conversazionale.
Fix: trattare OpenClaw come un dipendente da onboardare:
serve specificare ruolo, compiti, confini (vedi Cap. 7).

**Sintomo:** volerlo provare "giusto un attimo" sul
portatile di lavoro.
Causa: non si percepisce ancora il rischio dell'accesso
pieno al sistema.
Fix: fermarsi e leggere i Cap. 3, 4 e 13 prima di
installare. La prima installazione va su un dispositivo
dedicato.

**Sintomo:** trattare OpenClaw come uno Zapier più
sofisticato.
Causa: confondere automazione deterministica e
ragionamento.
Fix: vedi sezione "Tre obiezioni": se i tuoi workflow non
hanno bisogno di ragionamento, OpenClaw è overkill —
resta su Zapier o n8n.

## Checklist di fine capitolo

- [ ] So spiegare in una frase la differenza tra agente autonomo e chatbot
- [ ] Conosco il modello di rilascio di OpenClaw (open-source MIT, BYOK, hosted alternatives)
- [ ] Ho memorizzato le date chiave del 2026 (ban Anthropic 4 aprile, Moltbook→Meta 10 marzo, Steinberger→OpenAI 14 febbraio)
- [ ] Ho in mente come si distribuisce il lavoro di un agente in una giornata tipo (mattina, pranzo, pomeriggio, sera)
- [ ] Conosco le tre obiezioni più comuni e ho una risposta breve per ciascuna
- [ ] Ho deciso se è il caso di andare avanti col libro o fermarmi qui

## Link e risorse utili

- [Sito ufficiale di OpenClaw](https://openclaw.ai) — panoramica del progetto e link rapidi
- [OpenClaw su Wikipedia](https://en.wikipedia.org/wiki/OpenClaw) — voce enciclopedica con la cronologia
- [The Complete Guide to Building Your Personal AI Agent](https://www.lennysnewsletter.com/p/openclaw-the-complete-guide-to-building) — la guida-fiume di Claire Vo su Lenny's Newsletter
- [From Clawdbot to OpenClaw](https://www.cnbc.com/2026/02/02/openclaw-open-source-ai-agent-rise-controversy-clawdbot-moltbot-moltbook.html) — CNBC ricostruisce i 90 giorni del progetto

Per l'elenco completo delle fonti del libro, vedi [Appendice E](../Appendici/E-risorse-e-link-utili.md).

---

[← README parte](./README.md)  ·  [Indice](../README.md)  ·  [Capitolo 2 →](./02-anatomia-di-un-agente-openclaw.md)
