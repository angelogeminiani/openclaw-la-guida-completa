# Capitolo 9 — Aggiungere strumenti e integrazioni [★★]

**Cosa imparerai:**
- Come collegare Gmail, Calendar, Drive, GitHub, Linear, Notion, Obsidian, CRM
- Come configurare la ricerca web e gli smart home device
- Come far "scoprire" nuovi tool all'agente
- Le regole di sicurezza per le integrazioni

**Contenuto principale:**

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

---

## PARTE IV — Setup multi-agente

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

[← Capitolo 8](./08-dieci-workflow-pronti-all-uso.md)  ·  [Indice](../README.md)  ·  [Capitolo 10 →](../PARTE-IV-Multi-agente/10-perche-un-solo-agente-non-basta.md)
