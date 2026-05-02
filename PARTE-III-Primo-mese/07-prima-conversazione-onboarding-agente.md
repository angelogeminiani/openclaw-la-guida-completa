# Capitolo 7 — La prima conversazione: fare l'onboarding del tuo agente [★★]

## Cosa imparerai

- Cosa dire al tuo agente nei primi 10 minuti
- Come si auto-configura scrivendo i file .md
- Come dargli un nome, una personalità e un primo task
- Il mindset del "manager di agenti"

## Prerequisiti

Aver completato l'installazione ([Capitolo 5](../PARTE-II-Installazione/05-installazione-step-by-step.md)) e collegato almeno un canale ([Capitolo 6](../PARTE-II-Installazione/06-configurare-telegram-e-altri-canali.md)).

## Contenuto principale

1. **Mettersi il cappello da manager.** Come dice Claire Vo: "Come un dipendente, il tuo agente non può essere bravo in tutto. Pensa a un ruolo specifico." Assistente personale? Social media manager? Sviluppatore? Iniziare con un ruolo e aggiungerne altri dopo.

2. **I primi 10 minuti.** Cosa condividere subito:
   - Nome, ruolo/lavoro, fuso orario
   - Sfide quotidiane (scheduling, email, coordinamento famiglia, etc.)
   - Preferenze di comunicazione (tono, lingua, livello di dettaglio)
   - Cosa l'agente *non* deve fare mai (es. inviare email senza approvazione)

3. **L'auto-configurazione.** Dopo la prima conversazione, l'agente scrive automaticamente:
   - AGENTS.md — istruzioni e memoria operativa
   - SOUL.md — personalità e confini
   - IDENTITY.md — nome, emoji, vibe
   - USER.md — profilo dell'utente
   Consiglio: aprire i file e verificare che siano corretti. Editarli quando necessario.

4. **Dare un nome e una personalità.** Esempi dalla community:
   - "Polly" (personal assistant), "Felix" (business agent di Nat Eliason), "Max" (marketer)
   - Scegliere un tono: professionale, amichevole, ironico, formale
   - L'emoji identificativa (🦞, 🤖, 📋, etc.)

5. **Il primo task.** Iniziare con qualcosa di semplice e visibile:
   - "Leggi le mie ultime 10 email e fammi un riassunto"
   - "Cosa c'è nel mio calendario domani?"
   - "Cerca le ultime notizie su [argomento]"

**Prompt pronto:**
> "Il tuo nome è Polly. Sei la mia assistente personale. Il tuo tono è professionale ma caldo, conciso (3-4 frasi per risposta), orientato all'azione. Non inviare mai email senza la mia approvazione. Aggiorna il tuo SOUL.md con queste istruzioni."

## Errori comuni e come risolverli

| Sintomo | Causa probabile | Fix |
|---------|-----------------|-----|
| L'agente sembra "vuoto", senza personalità | USER.md/SOUL.md non sono stati popolati durante l'onboarding | Dedicare 30 minuti reali, condividere ruolo, sfide, preferenze, cosa NON deve mai fare. |
| Risposte generiche e prolisse | SOUL.md ancora di default | Rivedere SOUL.md: aggiungere sezione "Boundaries" con almeno 3 "non fare" e "Vibe" con tono richiesto. |
| L'agente non chiama l'utente per nome | Nome non scritto in USER.md | Dirglielo esplicitamente ("mi chiamo X, salvalo nel mio profilo") e verificare con `cat .openclaw/<nome>-workspace/USER.md`. |

## Checklist di fine capitolo

- [ ] Nome, ruolo, fuso orario e preferenze condivise con l'agente
- [ ] USER.md popolato (verificato con `cat`)
- [ ] SOUL.md ha almeno 3 regole di "non fare"
- [ ] Primo task piccolo completato dall'agente
- [ ] L'agente sa cosa NON deve mai fare in autonomia

## Link e risorse utili

- [The Complete Guide to Building Your Personal AI Agent](https://www.lennysnewsletter.com/p/openclaw-the-complete-guide-to-building) — i consigli di Claire Vo sull'onboarding
- [Use OpenClaw to Build a Business That Runs Itself](https://creatoreconomy.so/p/use-openclaw-to-build-a-business-that-runs-itself-nat-eliason) — l'approccio di Nat Eliason all'onboarding

Per l'elenco completo delle fonti del libro, vedi [Appendice E](../Appendici/E-risorse-e-link-utili.md).

---

[← Capitolo 6](../PARTE-II-Installazione/06-configurare-telegram-e-altri-canali.md)  ·  [Indice](../README.md)  ·  [Capitolo 8 →](./08-dieci-workflow-pronti-all-uso.md)
