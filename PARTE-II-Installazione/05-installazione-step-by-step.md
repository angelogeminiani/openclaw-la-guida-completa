# Capitolo 5 — Installazione step-by-step [★]

**Cosa imparerai:**
- Come preparare il computer per l'installazione
- Come completare l'onboarding senza errori
- Come scegliere modello LLM, autenticazione e canale
- Come effettuare il primo "hatch"

**Contenuto principale:**

1. **Pre-work (10 minuti).** 
   - Creare un account admin dedicato sul computer
   - Registrare un indirizzo Gmail per l'agente (non il proprio!)
   - Installare Chrome (il browser preferito da OpenClaw per l'automazione web)

2. **Installazione.** Aprire il terminale e lanciare:
   ```
   curl -fsSL https://openclaw.ai/install.sh | bash
   ```
   Requisiti: Node.js 22+ (installato automaticamente), macOS/Linux/Windows.
   Se bloccati: installare Claude Code o Codex CLI e chiedere aiuto.

3. **Navigare l'onboarding — ogni schermata spiegata:**
   - **Avviso di sicurezza**: leggere attentamente, accettare consapevolmente
   - **Scelta del modello LLM**: Claude Opus 4.6 o Codex 5.4 consigliati. Il modello più potente disponibile al momento della lettura è la scelta migliore per un agente generale.
   - **Autenticazione**: due opzioni
     - API key (consigliata, **unica opzione affidabile dopo il ban Anthropic del 4 aprile 2026**) — ottenere da platform.claude.com o platform.openai.com. Si paga per token consumati.
     - Sottoscrizione ChatGPT ($100–200/mese) — ancora funzionante per OpenClaw, "benedetta" da OpenAI. Utile per agenti ad alto volume.
     - ~~Sottoscrizione Claude~~ — **NON PIÙ UTILIZZABILE.** Dal 4 aprile 2026, Anthropic ha bloccato l'uso delle sottoscrizioni Claude Pro e Max con tutti i tool di terze parti, incluso OpenClaw. Chi tenta riceverà un errore. Unica alternativa: API key o "extra usage" pay-as-you-go (vedi Capitolo 14 per i dettagli e le implicazioni economiche).
   - **Scelta del canale**: Telegram consigliato per iniziare (setup più semplice)
   - **Setup ricerca web**: Brave API (precaricata), Exa, Perplexity, Firecrawl — si può saltare e configurare dopo
   - **Installazione skill iniziali**: consigliare **gog** (Gmail/Calendar/Drive) e **summarize** per iniziare
   - **Abilitazione hooks**: attivare tutti e quattro, ma soprattutto **session memory** (essenziale per la continuità delle conversazioni). Gli altri (debug, ottimizzazione, etc.) sono utili per il troubleshooting.

4. **Il primo "hatch".** L'agente "nasce" nella TUI (Terminal UI) con l'iconico lobster ASCII art. Da qui si può già conversare, ma si vorrà presto passare a un canale di messaggistica.

**Prompt pronto:**
> "Ciao! Sono [nome]. Lavoro come [ruolo] e le mie sfide quotidiane sono: [elenco]. Voglio che tu sia il mio assistente personale. Il tuo nome è [nome agente]. Sei [descrizione personalità]. Scrivi il tuo IDENTITY.md e mostrami cosa hai scritto."

**(#) Debug:** Se l'installazione si blocca, i problemi più comuni sono: versione di Node.js troppo vecchia (serve 22+), firewall che blocca il download, o permessi insufficienti. Lanciare `openclaw doctor` per una diagnostica automatica.

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

[← Capitolo 4](./04-preparare-un-ambiente-sicuro-docker-sandbox.md)  ·  [Indice](../README.md)  ·  [Capitolo 6 →](./06-configurare-telegram-e-altri-canali.md)
