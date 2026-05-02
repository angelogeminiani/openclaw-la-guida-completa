# Capitolo 14 — Gestire i costi senza sorprese [★]

## Cosa imparerai

- Come funziona il pricing di OpenClaw (gratis + costi LLM)
- Il ban Anthropic del 4 aprile 2026: cosa è successo e cosa fare
- Stima costi per profilo d'uso
- Strategie di ottimizzazione
- Come monitorare la spesa

## Prerequisiti

Aver completato l'installazione ([Capitolo 5](../PARTE-II-Installazione/05-installazione-step-by-step.md)). Idealmente, una settimana di uso reale per avere un punto di partenza sui costi.

## Contenuto principale

1. **Come funziona.** OpenClaw è gratuito (MIT). Il costo è interamente nel modello LLM:
   - **API key** (consigliato, più affidabile): si paga per token consumati
   - **Sottoscrizione ChatGPT** ($100–200/mese): flat fee, ancora funzionante per OpenClaw — "benedetta" da OpenAI
   - **~~Sottoscrizione Claude~~**: **non più utilizzabile** (vedi punto 2)

2. **Il ban Anthropic — 4 aprile 2026.** A partire dal 4 aprile 2026 (ore 12:00 PT), Anthropic ha bloccato l'uso delle sottoscrizioni Claude Pro ($20/mese) e Max ($100–200/mese) con tutti i tool di terze parti, incluso OpenClaw. La motivazione ufficiale: i tool terzi aggiravano le ottimizzazioni di prompt caching di Anthropic, consumando molte più risorse per sessione rispetto agli strumenti proprietari (Claude Code, Cowork). Boris Cherny, responsabile di Claude Code: "Le sottoscrizioni non erano progettate per i pattern di utilizzo di questi tool terzi."
   - **La timeline dell'escalation:**
     - *9 gennaio 2026*: Anthropic blocca silenziosamente i token OAuth nelle app terze — poi fa marcia indietro dopo il backlash della community
     - *19 febbraio 2026*: Aggiornamento dei ToS — l'uso di token OAuth da piani Free/Pro/Max in prodotti terzi è formalmente vietato
     - *Marzo 2026*: Anthropic lancia Claude Code Channels (Telegram/Discord), internalizzando la feature più popolare di OpenClaw
     - *4 aprile 2026*: Enforcement tecnico — blocchi server-side attivi, le sessioni OpenClaw su sottoscrizioni Claude smettono di funzionare
   - **Come funziona il blocco tecnicamente.** Anthropic distingue i token OAuth (prefisso `sk-ant-oat-*`) dalle API key (prefisso `sk-ant-api03-*`). I blocchi server-side rifiutano i token OAuth quando provengono da sorgenti non autorizzate (tutto ciò che non è Claude.ai, Claude Code o Cowork). Errore restituito: HTTP 429 "Extra usage is required". Non è un ban dell'account — è un filtro sul tipo di credenziale.
   - **Cosa è cambiato:** Nessun periodo di transizione (meno di 24 ore di preavviso).
   - **Alternative per chi usava Claude:**
     - API key Anthropic (pay-per-token): $3/M input e $15/M output per Sonnet 4.6; $15/M e $75/M per Opus 4.6
     - "Extra usage" pay-as-you-go: addon alla sottoscrizione esistente, stesso costo per token dell'API
     - Credito una tantum pari a un mese di abbonamento (da richiedere entro il 17 aprile 2026)
     - Sconto fino al 30% su bundle "extra usage" pre-acquistati
   - **Impatto sui costi:** Un utente che girava Opus 4.6 con ~500K input e 200K output token al giorno passa da ~$200/mese (Max) a ~$675/mese (API). Aumento fino a 50x per utenti leggeri che pagavano solo $20/mese.
   - **Reazioni della community:** Steinberger ha definito la decisione "triste per l'ecosistema" e ha rivelato che lui e Dave Morin hanno cercato di convincere Anthropic, ottenendo solo un ritardo di una settimana. Garry Tan (Y Combinator): "Potrebbe rivelarsi un errore strategico o un colpo di genio." Molti utenti stanno migrando verso modelli OpenAI (Codex 5.4), modelli locali (Nemotron) o ChatGPT come provider principale.
   - **Lezione per il lettore:** Non costruire mai un workflow critico su un singolo provider. La scelta model-agnostic di OpenClaw è un punto di forza — usarla.

   **Prompt pronto:**
> "Mostrami l'analisi della tua spesa LLM dell'ultima settimana. Per ogni giorno riporta: numero di chiamate, token in ingresso/uscita, modello usato, costo stimato. Identifica: (1) il singolo task più costoso, (2) le opportunità di routing su modelli più economici (es. Haiku per heartbeat, Opus solo per ragionamento), (3) eventuali cron in loop o conversazioni stantie. Proponi un piano per ridurre la spesa del 30% senza perdere qualità."

**(!) Attenzione:** Se il tuo agente smette improvvisamente di funzionare e usavi una sottoscrizione Claude, il motivo è questo ban. Passa a una API key o cambia modello.

3. **Stima costi per profilo d'uso (post-ban, aprile 2026):**
   - **Leggero** (1 agente, task semplici, pochi cron): $6–30/mese con API key
   - **Moderato** (2–3 agenti, automazioni quotidiane): $50–150/mese (routing multi-modello consigliato)
   - **Intensivo** (5–9 agenti, business automation): $200–1.000/mese
   - Claire Vo: "Sto arrivando a spendere $1.000/mese. Per me è una spesa aziendale, molto meno costosa di un team di umani."

4. **Strategie di ottimizzazione (essenziali dopo il ban):**
   - **Routing per modello (la strategia più importante)**: usare modelli economici per task semplici (heartbeat con Gemini Flash: ~$0–5/mese), modelli medi per automazioni standard (Claude Haiku: ~$10–20/mese), modelli potenti solo per ragionamento complesso (Claude Opus o Codex 5.4: $20–50/mese per task)
   - **Sottoscrizione ChatGPT** ($100–200/mese) come provider ad alto volume — ancora flat-rate per OpenClaw
   - **Modelli locali** (Nemotron, Llama) per privacy e costo zero — richiedono hardware adeguato (GPU consigliata)
   - **Modelli alternativi economici**: Kimi K2.5, MiniMax M2.5, Mistral — la community sta scoprendo alternative competitive a costi molto inferiori
   - **Prompt cache optimization**: Anthropic ha contribuito PR per migliorare il cache hit rate di OpenClaw; aggiornare all'ultima versione riduce il costo per token via API
   - **Ridurre l'accumulo di contesto**: ogni chiamata reinvia l'intero contesto della sessione. Sessioni lunghe accumulano contesto stantio che gonfia i costi. Regola pratica: avviare sessioni nuove regolarmente, non lasciare sessioni aperte per giorni
   - Monitorare con `/status` nel canale per vedere modello + token + costi della sessione

   **(i) Pro tip — Caso studio: da $200/mese a $15/mese.** Un utente della community ha ricostruito il proprio setup dopo il ban usando: 2 VPS da $5/mese (Hostinger) per ridondanza + Kimi K2.5 come modello primario + MiniMax M2.5 come fallback economico. Totale: ~$15/mese contro i $200 precedenti. Non è la stessa qualità di Opus, ma è sufficiente per il 90% dei workflow quotidiani. La lezione: il routing multi-modello non è un'ottimizzazione opzionale — è una necessità.

5. **Monitorare la spesa.** Comando `/status`, dashboard del provider API (Anthropic Console, OpenAI Dashboard), log dei costi per agente. Impostare alert sul provider per evitare sorprese.

## Errori comuni e come risolverli

| Sintomo | Causa probabile | Fix |
|---------|-----------------|-----|
| Bolletta API raddoppiata in un giorno | Cron in loop o conversazione che cresce a dismisura | `openclaw status` per identificare l'ultimo cron attivo, fermarlo, configurare budget di iterazioni. |
| ChatGPT Plus blocca dopo poche ore | Rate limit della sottoscrizione raggiunto | Per workload pesanti passare a API a consumo o ai modelli locali (Nemotron, Kimi K2.5). |
| Opus usato per task semplici → costo elevato | Routing modello non configurato | Configurare model routing: Opus per ragionamento complesso, Haiku/Flash per heartbeat e cron. |
| Errore "insufficient quota" mid-conversazione | Hard cap del provider raggiunto | Aumentare il limite o passare a un secondo provider come fallback. |

## Checklist di fine capitolo

- [ ] Conosco il pricing del mio provider LLM (input/output, per modello)
- [ ] Ho impostato un budget mensile e un alert nel pannello del provider
- [ ] Routing modello configurato (Opus solo dove serve, Haiku/Flash per heartbeat)
- [ ] Verifico la spesa almeno una volta a settimana con `/status` o dashboard
- [ ] Ho un piano B se il provider blocca o aumenta i prezzi

## Link e risorse utili

- [Anthropic blocks OpenClaw from Claude subscriptions](https://thenextweb.com/news/anthropic-openclaw-claude-subscription-ban-cost) — cronaca del ban del 4 aprile 2026 e impatto sui costi
- [Rebuilt my OpenClaw setup for $15/month](https://medium.com/@rentierdigital/anthropic-just-killed-my-200-month-openclaw-setup-so-i-rebuilt-it-for-15-9cab6814c556) — caso studio "$200 → $15/mese" con dettagli pratici
- [Anthropic provider docs (OpenClaw)](https://docs.openclaw.ai/providers/anthropic) — configurazione di chiavi API Anthropic post-ban
- [Tell HN: Anthropic no longer allowing Claude for OpenClaw](https://news.ycombinator.com/item?id=47633396) — discussione community con alternative concrete

Per l'elenco completo delle fonti del libro, vedi [Appendice E](../Appendici/E-risorse-e-link-utili.md).

---

[← Capitolo 13](./13-sicurezza-la-guida-che-devi-leggere.md)  ·  [Indice](../README.md)  ·  [Capitolo 15 →](../PARTE-VI-Manutenzione/15-care-and-feeding-tenere-l-agente-in-salute.md)
