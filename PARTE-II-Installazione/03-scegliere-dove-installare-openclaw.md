# Capitolo 3 — Scegliere dove installare OpenClaw [★]

**Cosa imparerai:**
- I tre percorsi di installazione: hosted, VPS cloud, hardware fisico
- Pro, contro e costi di ciascuna opzione
- La tabella decisionale "quale opzione fa per te?"
- La regola d'oro sulla sicurezza

**Contenuto principale:**

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

## Errori comuni e come risolverli

> *Sezione da rifinire in fase di stesura. Annota qui i sintomi reali che incontri seguendo il capitolo, le cause probabili e i fix verificati.*

| Sintomo | Causa probabile | Fix |
|---------|-----------------|-----|
| _TODO_ | _TODO_ | _TODO_ |

## Checklist di fine capitolo

> *Da adattare ai passi concreti coperti in questo capitolo.*

- [ ] _TODO: punto di verifica chiave 1_
- [ ] _TODO: punto di verifica chiave 2_
- [ ] _TODO: punto di verifica chiave 3_


---

[← Capitolo 2](../PARTE-I-Capire-OpenClaw/02-anatomia-di-un-agente-openclaw.md)  ·  [Indice](../README.md)  ·  [Capitolo 4 →](./04-preparare-un-ambiente-sicuro-docker-sandbox.md)
