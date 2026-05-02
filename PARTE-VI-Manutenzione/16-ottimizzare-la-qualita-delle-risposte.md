# Capitolo 16 — Ottimizzare la qualità delle risposte [★★]

## Cosa imparerai

- Come editare SOUL.md per affinare personalità e confini
- Prompt engineering per agenti autonomi vs. chatbot
- Memory management: cosa far ricordare e cosa far dimenticare
- Come scegliere il modello giusto per ogni agente

## Prerequisiti

Aver fatto l'onboarding del tuo agente ([Capitolo 7](../PARTE-III-Primo-mese/07-prima-conversazione-onboarding-agente.md)) e averlo manutenuto per qualche settimana ([Capitolo 15](./15-care-and-feeding-tenere-l-agente-in-salute.md)). Devi avere abbastanza risposte reali da poter giudicare cosa migliorare.

## Contenuto principale

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

**Prompt pronto:**
> "Aiutami a migliorare il tuo SOUL.md. Analizza le ultime 20 risposte che mi hai dato e identifica: (1) dove sei stato troppo prolisso, (2) dove hai usato un tono inappropriato (troppo formale, troppo casual, troppo apologetico), (3) dove hai violato un mio confine implicito. Proponi 3-5 aggiunte concrete al SOUL.md, mostrandomi il diff esatto da applicare e spiegandomi il perché di ognuna."

## Errori comuni e come risolverli

| Sintomo | Causa probabile | Fix |
|---------|-----------------|-----|
| Risposte ancora generiche dopo aver editato SOUL.md | SOUL.md non riletto in sessione corrente | Forzare reload (`/reload` o restart agente) e verificare che le modifiche siano in `.openclaw/<nome>-workspace/SOUL.md`. |
| L'agente "ricorda" cose vecchie sbagliate | Knowledge graph stantio, note obsolete non archiviate | Pulizia mensile: archiviare invece di cancellare per non perdere il contesto storico. |
| Cambio modello peggiora le risposte | SOUL.md tarato sul modello precedente | Rivedere SOUL.md per il nuovo modello (Claude e GPT rispondono diversamente agli stessi prompt). |
| Difficile capire quali iterazioni hanno migliorato | Nessun test set di prompt di riferimento | Tenere un set di 5-10 prompt-tipo da rilanciare dopo ogni modifica per confronto. |

## Checklist di fine capitolo

- [ ] SOUL.md versionato in Git (anche solo locale)
- [ ] Almeno una iterazione settimanale di affinamento prevista
- [ ] Memory management attivo: so cosa salvare, cosa archiviare, cosa eliminare
- [ ] Modello scelto in modo consapevole per ogni agente (non solo "il più potente")
- [ ] Ho un set di 5-10 prompt-tipo per testare le iterazioni

## Link e risorse utili

- [Use OpenClaw to Build a Business That Runs Itself](https://creatoreconomy.so/p/use-openclaw-to-build-a-business-that-runs-itself-nat-eliason) — come Nat Eliason scrive i SOUL.md dei suoi agenti
- [Documentazione ufficiale](https://docs.openclaw.ai) — best practice di prompt e memoria a tre livelli

Per l'elenco completo delle fonti del libro, vedi [Appendice E](../Appendici/E-risorse-e-link-utili.md).

---

[← Capitolo 15](./15-care-and-feeding-tenere-l-agente-in-salute.md)  ·  [Indice](../README.md)  ·  [Capitolo 17 →](../PARTE-VII-Uso-avanzato/17-creare-skill-personalizzate.md)
