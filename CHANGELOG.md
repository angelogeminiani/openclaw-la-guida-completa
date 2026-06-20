# Changelog — OpenClaw: Guida Completa

Tutte le modifiche rilevanti al contenuto del libro sono registrate qui.

Il formato segue lo spirito di [Keep a Changelog](https://keepachangelog.com/it/1.1.0/): le voci sono raggruppate per data di revisione, dalla più recente alla più vecchia. La **versione di riferimento dei contenuti** resta maggio 2026 (fotografia temporale del libro); le revisioni successive correggono imprecisioni o annotano fatti emersi dopo la fotografia.

Categorie usate: **Corretto** (errori o dati imprecisi), **Aggiornato** (fatti cambiati dopo maggio 2026, segnalati come tali nel testo), **Aggiunto**, **Rimosso**.

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
