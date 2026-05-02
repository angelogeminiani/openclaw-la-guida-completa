# Capitolo 5 — Installazione step-by-step [★]

## Cosa imparerai

- Come preparare il computer per l'installazione
- Come completare l'onboarding senza errori
- Come scegliere modello LLM, autenticazione e canale
- Come effettuare il primo "hatch"

## Prerequisiti

Aver letto il [Capitolo 3](./03-scegliere-dove-installare-openclaw.md) e scelto dove installare OpenClaw. Per un setup sicuro è caldamente consigliato il [Capitolo 4](./04-preparare-un-ambiente-sicuro-docker-sandbox.md). Ti serve: account utente dedicato, terminale, Chrome installato, una Gmail dedicata.

## Contenuto principale

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

| Sintomo | Causa probabile | Fix |
|---------|-----------------|-----|
| Lo script `curl … install.sh` fallisce | Rete dietro proxy aziendale o certificate pinning | Scaricare lo script (`curl -O`), ispezionarlo, lanciarlo manualmente con `bash install.sh`. |
| Errore "Anthropic API key invalid" | Tentativo di usare la sottoscrizione Claude Pro/Max (bloccata dal 4 aprile 2026) invece di una API key | Generare una API key dal pannello Anthropic e usarla. Vedi Cap. 14 per le alternative al ban. |
| La TUI non parte dopo l'installazione | Terminale non TTY (es. SSH senza `-t`) | Lanciare in un vero terminale o aggiungere `-t` allo `ssh`. |
| Onboarding completo ma `openclaw status` dice "stopped" | Il Gateway non è stato avviato dopo l'installazione | `openclaw start` o riavviare il servizio se installato come daemon. |

## Checklist di fine capitolo

- [ ] Account utente dedicato e Gmail dedicata creati
- [ ] OpenClaw installato senza errori (`openclaw --version` risponde)
- [ ] Modello LLM configurato con API key valida (NON sottoscrizione)
- [ ] Almeno un canale collegato (`openclaw channels status` lo conferma)
- [ ] Primo "hatch" completato e l'agente risponde
- [ ] `openclaw status` mostra "running"

## Link e risorse utili

- [Documentazione ufficiale di installazione](https://docs.openclaw.ai) — guide step-by-step e troubleshooting
- [How to install OpenClaw without getting banned](https://www.shareuhack.com/en/posts/openclaw-setup-tutorial-2026) — tutorial aggiornato post-ban Anthropic
- [Anthropic provider docs (OpenClaw)](https://docs.openclaw.ai/providers/anthropic) — come configurare la chiave API Anthropic dopo il 4 aprile 2026

Per l'elenco completo delle fonti del libro, vedi [Appendice E](../Appendici/E-risorse-e-link-utili.md).

---

[← Capitolo 4](./04-preparare-un-ambiente-sicuro-docker-sandbox.md)  ·  [Indice](../README.md)  ·  [Capitolo 6 →](./06-configurare-telegram-e-altri-canali.md)
