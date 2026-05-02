# Capitolo 1 — Cos'è OpenClaw e perché è importante [★]

## Cosa imparerai

- Che cos'è un agente autonomo e in che cosa si distingue da un chatbot
- La storia del progetto: da Clawdbot a OpenClaw in 90 giorni
- Perché Jensen Huang l'ha definito "il rilascio software più importante di sempre"
- In che modo si differenzia da ChatGPT, Siri e Alexa

## Prerequisiti

Nessuno. Questo è il punto di ingresso del libro: ti basta una mezz'ora e voglia di capire cos'è davvero un agente autonomo.

## Contenuto principale

1. **L'era degli agenti personali.** Il 2026 è l'anno in cui l'intelligenza artificiale ha smesso di "rispondere" e ha iniziato ad "agire". OpenClaw incarna questo salto: è un framework open-source (licenza MIT) che trasforma un LLM in un dipendente digitale sempre attivo, in grado di leggere la posta, controllare il calendario, navigare il web, scrivere codice e comunicare via Telegram, WhatsApp, Slack e altri 20+ canali.

2. **La storia.** Peter Steinberger, fondatore austriaco di PSPDFKit (exit da €100 M), dopo un periodo di pausa torna a programmare nel 2025 con lo spirito del "vibe coding". A novembre 2025 pubblica Clawdbot come progetto personale su GitHub. A gennaio 2026, dopo una disputa sul marchio con Anthropic (il nome era un gioco di parole su "Claude"), il progetto diventa Moltbot e poi, tre giorni dopo, OpenClaw — perché "Moltbot non suonava bene". In 60 giorni raggiunge 247.000+ GitHub stars, il record assoluto, superando ciò che React ha impiegato dieci anni a ottenere. Il 14 febbraio 2026, Steinberger annuncia l'ingresso in OpenAI e il trasferimento del progetto a una fondazione open-source indipendente, supportata da OpenAI ma non posseduta da essa. Il 4 aprile 2026, Anthropic blocca l'uso delle sottoscrizioni Claude Pro/Max con OpenClaw e tutti i tool terzi, provocando un terremoto nella community (vedi Capitolo 14).

3. **Perché è diverso.** Confronto tassonomico: chatbot (ChatGPT, Claude chat) → assistente proattivo (Siri, Alexa) → agente autonomo (OpenClaw). Tabella comparativa con ChatGPT Agent, Siri, Alexa, Google Assistant, e agenti proprietari (Manus/Meta). OpenClaw è local-first, model-agnostic (Claude, GPT, Gemini, Nemotron, modelli locali), auto-installante (può crearsi nuove skill) e opera in background 24/7 su un computer dedicato.

4. **Il fenomeno culturale.** 343.000+ GitHub stars (aprile 2026), 67.000+ fork, oltre 200.000 agenti registrati su Moltbook (il social network per agenti AI, acquistato da Meta a marzo 2026). La mascotte del lobster, i meme, la community su Discord/X, le hosted platform (StartClaw, MyClaw, SimpleClaw, UniClaw, Plus One). La frase di Nvidia: "OpenClaw is the operating system for personal AI."

5. **Confronto con le alternative.** Tabella riepilogativa:
   - **NanoClaw**: alternativa minimalista (~700 righe di TypeScript), container Docker isolati, Claude-only, più sicuro out-of-the-box, meno integrazioni
   - **NemoClaw (Nvidia)**: wrapper di sicurezza enterprise per OpenClaw, OpenShell sandboxing a livello kernel, policy YAML, privacy router per modelli locali/cloud
   - **IronClaw (NEAR AI)**: riscrittura in Rust con focus su memory safety, zero telemetria
   - **ZeroClaw**: binary minimale (3,4 MB), deny-by-default, ideale per edge computing
   - **Moltworker**: hosting su Cloudflare, zero gestione infrastruttura
   - **Claude Code / Codex CLI**: agenti specializzati per coding, non general-purpose

**Prompt pronto:**
> "Presentati. Dimmi chi sei, cosa sai fare e quali limiti hai. Elenca i canali attraverso cui possiamo parlare e le skill che hai installate."

**(!) Attenzione:** OpenClaw ha accesso completo al computer su cui gira: filesystem, rete, comandi shell. Questo lo rende potente *e* pericoloso. Non installarlo mai su un computer in uso attivo.

## Errori comuni e come risolverli

| Sintomo | Causa probabile | Fix |
|---------|-----------------|-----|
| Confondere OpenClaw con Claude o ChatGPT | Marketing AI poco preciso, abitudine ai chatbot | OpenClaw è un *framework* che usa un LLM (Claude, GPT, Nemotron, ecc.). Il framework agisce, l'LLM ragiona. |
| Aspettarsi che l'agente "indovini" cosa fare | Mindset da chatbot conversazionale | Trattare OpenClaw come un dipendente da onboardare: serve specificare ruolo, compiti, confini (vedi Cap. 7). |
| Volerlo provare "giusto un attimo" sul portatile di lavoro | Non si percepisce ancora il rischio dell'accesso pieno al sistema | Fermarsi e leggere i Cap. 3, 4 e 13 prima di installare. La prima installazione va su un dispositivo dedicato. |

## Checklist di fine capitolo

- [ ] So spiegare in una frase la differenza tra agente autonomo e chatbot
- [ ] Conosco il modello di rilascio di OpenClaw (open-source MIT, BYOK, hosted alternatives)
- [ ] Ho memorizzato le date chiave del 2026 (ban Anthropic 4 aprile, Moltbook→Meta 10 marzo, Steinberger→OpenAI 14 febbraio)
- [ ] Ho deciso se è il caso di andare avanti col libro o fermarmi qui

## Link e risorse utili

- [Sito ufficiale di OpenClaw](https://openclaw.ai) — panoramica del progetto e link rapidi
- [OpenClaw su Wikipedia](https://en.wikipedia.org/wiki/OpenClaw) — voce enciclopedica con la cronologia
- [The Complete Guide to Building Your Personal AI Agent](https://www.lennysnewsletter.com/p/openclaw-the-complete-guide-to-building) — la guida-fiume di Claire Vo su Lenny's Newsletter
- [From Clawdbot to OpenClaw](https://www.cnbc.com/2026/02/02/openclaw-open-source-ai-agent-rise-controversy-clawdbot-moltbot-moltbook.html) — CNBC ricostruisce i 90 giorni del progetto

Per l'elenco completo delle fonti del libro, vedi [Appendice E](../Appendici/E-risorse-e-link-utili.md).

---

[← README](../README.md)  ·  [Indice](../README.md)  ·  [Capitolo 2 →](./02-anatomia-di-un-agente-openclaw.md)
