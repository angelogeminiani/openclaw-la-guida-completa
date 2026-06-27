# Changelog — OpenClaw: Guida Completa

Tutte le modifiche rilevanti al contenuto del libro sono registrate qui.

Il formato segue lo spirito di [Keep a Changelog](https://keepachangelog.com/it/1.1.0/): le voci sono raggruppate per data di revisione, dalla più recente alla più vecchia. La **versione di riferimento dei contenuti** resta maggio 2026 (fotografia temporale del libro); le revisioni successive correggono imprecisioni o annotano fatti emersi dopo la fotografia.

Categorie usate: **Corretto** (errori o dati imprecisi), **Aggiornato** (fatti cambiati dopo maggio 2026, segnalati come tali nel testo), **Aggiunto**, **Rimosso**.

## [Revisione giugno 2026 — verifica online] — 2026-06-27

Seconda passata di verifica dei fatti rispetto allo stato online a fine giugno 2026, in continuità con la revisione del 20 giugno. La fotografia dei contenuti resta maggio 2026; i fatti cambiati dopo sono annotati nei capitoli come "aggiornamento giugno 2026".

### Corretto

- **Cap. 4** — Data della CVE-2026-25253 portata al 3 febbraio 2026 (era "gennaio 2026"), in linea con la disclosure documentata (CVSS 8.8, one-click RCE via WebSocket).
- **Cap. 22 / Appendice E** — Data dell'accordo "Digital Omnibus on AI" precisata: intesa provvisoria del 6 maggio 2026, confermata dal Consiglio il 13 maggio (era genericamente "7 maggio"). Aggiunto l'obbligo di watermarking dei contenuti sintetici (slittato al 2 dicembre 2026).

### Aggiornato (fatti post-maggio 2026, annotati nel testo)

- **Cap. 1 / Cap. 21** — Stelle GitHub: aggiunta nota "oltre 378.000" a giugno 2026 (il dato canonico di ~350.000 ad aprile resta invariato).
- **Cap. 3 / Appendice B** — Schema di versioning: dalla serie 2026.6 il terzo numero è un contatore patch mensile (es. `2026.6.11`), non più il giorno del mese dello schema `2026.4.27`.
- **Cap. 14** — Box reversal Anthropic arricchito con data (15 giugno 2026) e importi del credito "Agent SDK" (Pro $20, Max 5× $100, Max 20× $200), con la fine del compute agentico illimitato a tariffa fissa.
- **Cap. 14 / Cap. 16** — Modelli: nota sull'uscita di Claude Opus 4.8, del livello Fable 5 e di GPT-5.2; gli esempi del libro restano su Sonnet 4.6 (default) e Haiku 4.5, tuttora attuali. Listino di maggio invariato come fotografia.
- **Cap. 13 / Cap. 17** — Sicurezza ClawHub: aggiunta nota sulla crescita delle skill malevole (da 341 a ~824, fino a ~1.184) col registry oltre le 10.700 skill, e sulle istanze esposte oltre le 220.000. Il conteggio canonico 341/2.857 (audit febbraio 2026) resta.

### Valutato e non modificato

- **Node.js minimo** — La documentazione online indica ora 22.19+ come floor pratico; il libro resta su 22.16+ (valore canonico fissato in CLAUDE.md, "24 raccomandato"), poiché le fonti sono discordanti (22.14 / 22.16 / 22.19).
- **Cina (Cap. 21–22)** — La "doppia strategia" (regolazione interna + sussidi dei governi locali) è già presente nel testo; nessuna modifica necessaria.
- **Nat Eliason (Cap. 11)** — Cifra ~$177.000 confermata ($177.417); nessuna correzione necessaria.

## [Revisione giugno 2026] — 2026-06-20

Passata di verifica dei fatti del progetto OpenClaw rispetto allo stato online a giugno 2026. La fotografia dei contenuti resta a maggio 2026: dove la realtà è cambiata dopo, i capitoli riportano note esplicite "aggiornamento giugno 2026".

### Corretto

- **Cap. 1** — Conteggio Moltbook allineato al Cap. 21: prima dell'acquisizione Meta ~1,5 milioni di profili riconducibili a ~17.000 proprietari (non "oltre 200.000 registrati", che è il dato del 5 febbraio). Stelle/fork GitHub portati a ~350.000 / 70.000+. Rinomina Clawdbot→Moltbot→OpenClaw precisata a "fine gennaio 2026".
- **Cap. 13** — Istanze esposte aggiornate da 42.000 (marzo) a oltre 135.000 (aprile 2026, dato più recente entro la finestra del libro).
- **Cap. 14** — Prezzo di Claude Opus 4.6 corretto da $15/$75 a $5/$25 per milione di token ($15/$75 era il listino del precedente Opus 4.1). Ricalcolati di conseguenza: budget per task, esempio dell'utente intensivo, giornata-tipo di Polly (~€134 → ~€45/mese), spread tra modelli (fattore 24 → 8) e descrizione della fascia premium.
- **Cap. 18** — Backoff dei retry cron corretto in backoff esponenziale a cinque gradini (30s, 1m, 5m, 15m, 60m). Corretto anche il default dei job one-shot: si auto-cancellano dopo il successo, con `--keep-after-run` per conservarli (prima era indicato l'opposto, `--delete-after-run`).
- **Cap. 21** — Stelle/fork GitHub portati a ~350.000 / 70.000+ (tre occorrenze).
- **Cap. 10 / Cap. 11** — Sintassi del comando aggiornata a `openclaw agents add <id> --workspace <path>` (modalità non interattiva con flag espliciti, id `main` riservato, flag `--model`/`--bind`), allineate checklist e prompt pronti.

### Aggiornato (fatti post-maggio 2026, annotati nel testo)

- **Cap. 6** — Aggiunto box "aggiornamento giugno 2026": con la serie 2026.6 il canale BlueBubbles è stato rimosso dal core; il comando `--channel imessage-bluebubbles` non è più disponibile. Aggiornati i link al plugin iMessage nativo e alla guida di migrazione "Coming from BlueBubbles".
- **Cap. 14** — Aggiunto box "aggiornamento giugno 2026": Anthropic ha parzialmente revocato il ban del 4 aprile, riabilitando le sottoscrizioni Claude con tool terzi tramite credito "Agent SDK". La narrazione canonica del 4 aprile resta invariata.
- **Cap. 22** — AI Act: distinte le scadenze dopo il "Digital Omnibus on AI" del 7 maggio 2026 — obblighi di trasparenza dal 2 agosto 2026, obblighi sui sistemi ad alto rischio rinviati al 2 dicembre 2027 (agosto 2028 per i prodotti regolamentati).

### Aggiunto

- **Cap. 2** — Aggiunti Feishu e Twitch all'elenco esemplificativo dei canali.
- **Cap. 13** — Caso Cisco arricchito con il nome della skill ("What Would Elon Do?") e lo scanner DefenseClaw.
- **Appendice E** — Voci per il plugin iMessage nativo, la guida di migrazione da BlueBubbles e il Digital Omnibus; le righe BlueBubbles legacy marcate "(deprecato 2026)".
- **README.md / index.html** — Aggiunta la dicitura "ultima revisione: giugno 2026" accanto alla versione di riferimento.

## [Edizione iniziale] — maggio 2026

Prima stesura completa del libro: 8 parti, 22 capitoli, capitolo extra HomeClaw e 5 appendici. Versione di riferimento dei contenuti: maggio 2026.
