# Capitolo 16 — Ottimizzare la qualità delle risposte [★★]

**Cosa imparerai:**
- Come editare SOUL.md per affinare personalità e confini
- Prompt engineering per agenti autonomi vs. chatbot
- Memory management: cosa far ricordare e cosa far dimenticare
- Come scegliere il modello giusto per ogni agente

**Contenuto principale:**

1. **Editare SOUL.md.** Il SOUL.md è il file più potente. Aggiungere sezioni: "Core Truths" (verità fondamentali), "Boundaries" (confini non negoziabili), "Vibe" (tono di comunicazione), "Continuity" (cosa ricordare tra le sessioni).

2. **Prompt engineering per agenti autonomi.** A differenza di un chatbot, l'agente deve decidere *quando* e *come* agire senza prompt dell'utente. Scrivere istruzioni come obiettivi, non come comandi: "Assicurati che nessuna email importante venga persa" è meglio di "Leggi la posta ogni ora."

3. **Memory management.** Il sistema di memoria a 3 livelli di Nat Eliason:
   - Layer 1: Knowledge graph (fatti durevoli su persone e progetti)
   - Layer 2: Note giornaliere (log di ciò che è successo)
   - Layer 3: Conoscenza tacita (preferenze, abitudini, regole)

4. **Scelta del modello (post-ban Anthropic).** Il ban del 4 aprile 2026 ha reso la scelta del modello una decisione anche economica, non solo qualitativa. Configurare il routing multi-modello per agente:
   - Claude Opus 4.6 (via API key) per ragionamento complesso e decisioni delicate — il più costoso, da usare con parsimonia
   - Claude Sonnet 4.6 o Codex 5.4 per task standard
   - Gemini Flash, Claude Haiku, Kimi K2.5, MiniMax M2.5 per heartbeat, cron e task semplici
   - Nemotron (Nvidia) o Llama per inferenza locale con privacy totale e costo zero
   - Sottoscrizione ChatGPT ($100–200/mese) come alternativa flat-rate per agenti ad alto volume

5. **Ciclo di miglioramento.** Ogni settimana: rileggere le conversazioni, identificare errori ricorrenti, aggiornare SOUL.md e TOOLS.md di conseguenza.

---

## PARTE VII — Uso avanzato

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

[← Capitolo 15](./15-care-and-feeding-tenere-l-agente-in-salute.md)  ·  [Indice](../README.md)  ·  [Capitolo 17 →](../PARTE-VII-Uso-avanzato/17-creare-skill-personalizzate.md)
