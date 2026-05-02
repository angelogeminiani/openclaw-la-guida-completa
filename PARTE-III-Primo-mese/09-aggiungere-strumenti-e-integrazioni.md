# Capitolo 9 — Aggiungere strumenti e integrazioni [★★]

## Cosa imparerai

- Come collegare Gmail, Calendar, Drive, GitHub, Linear, Notion, Obsidian, CRM
- Come configurare la ricerca web e gli smart home device
- Come far "scoprire" nuovi tool all'agente
- Le regole di sicurezza per le integrazioni

## Prerequisiti

Aver provato almeno un workflow del [Capitolo 8](./08-dieci-workflow-pronti-all-uso.md). Per ogni integrazione serve un account sul servizio corrispondente (Gmail, GitHub, Linear, ecc.).

## Contenuto principale

1. **Gmail, Google Calendar, Google Drive — via gog.** Il CLI tool per l'integrazione Google. Chiedere all'agente: "Come ti do accesso read-only alla mia Gmail?" e seguire le istruzioni. Partire sempre con accesso in sola lettura.

2. **GitHub.** Personal Access Token con scope limitato (solo i repository necessari). L'agente diventa uno sviluppatore on-demand.

3. **Linear, Notion, Obsidian.** Linear per assegnare task; Notion/Obsidian come spazio di collaborazione condiviso (OpenClaw ama scrivere in Markdown, Obsidian è la scelta naturale).

4. **CRM (Attio, HubSpot).** Token API per qualificazione lead e gestione pipeline.

5. **Ricerca web.** Brave API (precaricata), Exa (raccomandato per ricerche avanzate), Perplexity, Firecrawl.

6. **Smart home.** Eight Sleep (temperatura letto), Sonos (musica), Philips Hue (luci), Home Assistant. Esempio di Claire Vo: "Ho un neonato, abbassa le luci e metti il rumore bianco alle 20:30."

7. **API personalizzate.** Come far scoprire nuovi tool: descriverli nel TOOLS.md, dare le istruzioni di autenticazione, e l'agente li integrerà autonomamente.

8. **Model Context Protocol (MCP).** 860+ tool disponibili via MCP. Panoramica del protocollo e come installare connettori.

**(!) Attenzione — Regole di sicurezza per le integrazioni:**
- Iniziare **sempre** con token read-only
- Non dare accesso in scrittura a email, documenti o codice finché non ci si fida dell'agente
- Ricordare: l'agente può inviare email, sovrascrivere documenti, eliminare ticket, compilare form, fare deploy di codice in produzione — se ha i permessi per farlo
- Usare 1Password o un password manager per gestire API key e token

**Prompt pronto:**
> "Voglio collegarti al mio Gmail e Google Calendar tramite la skill `gog`. Aiutami a configurarla nel modo più sicuro: (1) consigliami se usare il mio account principale o crearne uno dedicato, (2) elenca gli scope OAuth minimi che servono per leggere ma non inviare, (3) propone un test piccolo per verificare che funzioni, (4) spiegami come revocare l'accesso se cambio idea."

## Errori comuni e come risolverli

| Sintomo | Causa probabile | Fix |
|---------|-----------------|-----|
| `gog` non riesce a leggere Gmail | Scope OAuth insufficiente o consenso scaduto | Rifare l'autenticazione con scope minimi necessari, verificare con `gog status`. |
| Token GitHub finito nei log | PAT con scope troppo ampi salvato in chiaro o stampato per debug | Rotate immediato del token, usare PAT con scope minimi, salvare in `.env` e mai in console. |
| L'agente cita un'integrazione che "esiste" ma non funziona | Hallucinazione del modello LLM | Verificare sempre nei docs ufficiali (`docs.openclaw.ai`) prima di credere a una capability. |
| Integrazione funziona oggi, fallisce domani | Token scaduto o servizio cambia API | Configurare un alert sul cron che usa l'integrazione; rotate periodico dei token. |

## Checklist di fine capitolo

- [ ] Almeno un'integrazione configurata e testata con un piccolo task
- [ ] Token con scope minimo necessario (mai "admin" se basta "read")
- [ ] Tutti i secrets in `.openclaw/.env`, mai nel codice o in chat
- [ ] Ho un piano di rotazione dei token (es. trimestrale)

## Link e risorse utili

- [Documentazione ufficiale](https://docs.openclaw.ai) — lista completa di skill, integrazioni e MCP supportati
- [The Complete Guide to Building Your Personal AI Agent](https://www.lennysnewsletter.com/p/openclaw-the-complete-guide-to-building) — esempi di integrazione con Gmail, Linear e Notion

Per l'elenco completo delle fonti del libro, vedi [Appendice E](../Appendici/E-risorse-e-link-utili.md).

---

[← Capitolo 8](./08-dieci-workflow-pronti-all-uso.md)  ·  [Indice](../README.md)  ·  [Capitolo 10 →](../PARTE-IV-Multi-agente/10-perche-un-solo-agente-non-basta.md)
