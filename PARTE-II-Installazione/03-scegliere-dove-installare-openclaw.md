# Capitolo 3 — Scegliere dove installare OpenClaw [★]

## Cosa imparerai

- I tre percorsi di installazione: hosted, VPS cloud, hardware fisico
- Pro, contro e costi di ciascuna opzione
- La tabella decisionale "quale opzione fa per te?"
- La regola d'oro sulla sicurezza

## Prerequisiti

Aver letto i Capitoli [1](../PARTE-I-Capire-OpenClaw/01-cos-e-openclaw-e-perche-e-importante.md) e [2](../PARTE-I-Capire-OpenClaw/02-anatomia-di-un-agente-openclaw.md). Avere un'idea (anche vaga) di budget mensile e di quanto vuoi che l'agente faccia per te.

## Contenuto principale

1. **Opzione 1 — Piattaforme hosted.** Panoramica delle startup che offrono OpenClaw "chiavi in mano":
   - **StartClaw** (startclaw.com) — interfaccia semplice, pricing mensile
   - **MyClaw** (myclaw.ai) — focus su facilità d'uso
   - **SimpleClaw** (simpleclaw.com) — onboarding guidato
   - **UniClaw** (uniclaw.ai) — multi-agente integrato
   - **Plus One** (Every/every.to) — editoriale, integrato con la piattaforma Every
   - Pro: nessun hardware, nessuna manutenzione, pronto in minuti
   - Contro: minor controllo, costo mensile, dipendenza da terzi, funzionalità limitate
   - Claire Vo: "Ne ho provate diverse, sono slick, ma mi sono sempre bloccata su qualcosa"

2. **Opzione 2 — VPS cloud.** Per utenti intermedi e sviluppatori:
   - **Railway** — 1-Click deploy, il più veloce
   - **DigitalOcean** — hardened security image, 1-Click deploy ($24/mese per immagine sicura)
   - **Google Cloud** — container e sicurezza enterprise
   - **Render** — deploy serverless-like
   - **Hostinger** — VPS Docker
   - Pro: economico ($5–24/mese), potente, nessun hardware
   - Contro: richiede competenze CLI, manutenzione periodica

3. **Opzione 3 — Hardware fisico.** L'opzione classica e "meme-worthy":
   - Mac Mini M4 (modello base: ~$600) — la scelta preferita dalla community
   - Vecchio laptop (MacBook Air, qualsiasi PC con Node.js 22+)
   - Raspberry Pi (possibile ma limitato)
   - Pro: controllo totale, privacy assoluta, educativo, divertente
   - Contro: costo iniziale, serve monitor/tastiera/mouse per setup

4. **Tabella decisionale.** Matrice basata su budget (€0–50/mese, €50–100, €100+), competenze tecniche (nessuna, base, avanzate), e uso previsto (personale leggero, business, sviluppo).

**(!) Attenzione — LA REGOLA D'ORO:** MAI installare OpenClaw su un computer personale o di lavoro in uso attivo. L'agente ha accesso potenziale a tutti i file. Il rischio di cancellazione accidentale, invio di dati sensibili o comportamenti imprevisti è reale. Usare sempre un dispositivo dedicato o un VPS isolato.

**Prompt pronto:**
> "Aiutami a scegliere dove installare OpenClaw. Devo decidere fra (1) hosted come StartClaw o MyClaw, (2) un VPS cloud, (3) hardware fisico (Mac Mini o vecchio laptop). Il mio budget mensile è X €, le mie competenze tecniche sono [base / intermedie / avanzate] e voglio usarlo principalmente per [descrivi]. Confronta pro e contro per il mio caso e dammi una raccomandazione motivata in massimo 200 parole."

## Errori comuni e come risolverli

| Sintomo | Causa probabile | Fix |
|---------|-----------------|-----|
| "Lo metto sul mio MacBook di lavoro per provare" | Non si è ancora interiorizzato cosa significa accesso pieno al sistema | Non farlo. Mac Mini dedicato, vecchio laptop o VPS. Mai dispositivo in uso attivo o con dati sensibili. |
| Costo VPS molto più alto del previsto | Provider con bandwidth a consumo, o LLM via API molto verboso | Leggere il TOS sul traffico prima di scegliere e impostare un alert di spesa nel pannello del provider. |
| Raspberry Pi inutilizzabile dopo qualche giorno | Workload pesante (browser automation, media) su SD card lenta | Limitare il Pi ad agenti leggeri (testo, cron). Per workload pesanti servono Mac Mini o VPS. |

## Checklist di fine capitolo

- [ ] Ho scelto fra hosted, VPS cloud o hardware fisico in modo motivato
- [ ] Ho calcolato un budget mensile realistico (infrastruttura + LLM)
- [ ] Il dispositivo o il VPS NON contiene dati personali o di lavoro sensibili
- [ ] Ho verificato che il provider scelto non abbia restrizioni d'uso su agenti AI
- [ ] Ho letto in anteprima il Cap. 4 sul sandboxing prima di passare all'installazione

## Link e risorse utili

- [OpenClaw Setup Guide 2026](https://popularaitools.ai/blog/openclaw-setup-guide-2026) — panoramica delle opzioni di installazione
- [Run OpenClaw with DigitalOcean](https://www.digitalocean.com/community/tutorials/how-to-run-openclaw) — guida ufficiale DigitalOcean al deploy
- [7 Best OpenClaw Alternatives](https://remoteopenclaw.com/blog/openclaw-alternatives-comprehensive-2026) — rassegna delle hosted platform e dei wrapper

Per l'elenco completo delle fonti del libro, vedi [Appendice E](../Appendici/E-risorse-e-link-utili.md).

---

[← Capitolo 2](../PARTE-I-Capire-OpenClaw/02-anatomia-di-un-agente-openclaw.md)  ·  [Indice](../README.md)  ·  [Capitolo 4 →](./04-preparare-un-ambiente-sicuro-docker-sandbox.md)
