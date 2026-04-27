# Capitolo 2 — L'anatomia di un agente OpenClaw [★]

**Cosa imparerai:**
- Come "pensa" un agente: heartbeat, cron, sessioni e memoria persistente
- I cinque file d'identità (AGENTS.md, SOUL.md, IDENTITY.md, TOOLS.md, USER.md)
- Il ciclo di vita di un task dall'arrivo del messaggio al report finale
- Come funzionano i canali di comunicazione

**Contenuto principale:**

1. **Il modello mentale.** Pensare a OpenClaw come a un dipendente digitale con una scrivania (il workspace), un badge (l'identità), una cassetta degli attrezzi (le skill/tool), un'agenda (i cron job) e un diario (la memoria). Ogni 30 minuti il "cuore batte" (heartbeat): l'agente si sveglia, controlla i cron, processa i messaggi in coda, e si rimette in attesa.

2. **I file d'identità.** Descrizione approfondita di ciascun file .md nella cartella `.openclaw/[agent-name]-workspace`:
   - **AGENTS.md** — Il "contratto di lavoro": istruzioni operative, memoria contestuale, regole di ingaggio. Viene letto ad ogni avvio.
   - **SOUL.md** — La "personalità": tono, limiti, valori, confini etici. È qui che definisci cosa l'agente *non* deve mai fare.
   - **IDENTITY.md** — Il "biglietto da visita": nome, emoji, vibe, descrizione breve.
   - **TOOLS.md** — Il "manuale d'uso": note su come l'agente deve usare ogni strumento a disposizione.
   - **USER.md** — Il "dossier sull'utente": tutto ciò che l'agente sa su di te — nome, ruolo, sfide, preferenze.

3. **Il ciclo di vita di un task.** Diagramma del flusso: Messaggio in arrivo (canale) → Gateway → Routing verso l'agente giusto → Sessione → Ragionamento (LLM) → Esecuzione (skill, browser, shell, API) → Report al canale → Memoria persistente.

4. **Canali di comunicazione.** Elenco completo con note:
   - Telegram (grammY) — consigliato per iniziare
   - WhatsApp (Baileys) — il più naturale per uso personale
   - Slack (Bolt) e Discord (discord.js) — ideali per team
   - Signal (signal-cli), iMessage (BlueBubbles o legacy imsg), Microsoft Teams, Matrix, Google Chat, Feishu, LINE, IRC, Mattermost, Nextcloud Talk, Nostr, Synology Chat, Tlon, Twitch, Zalo, WeChat (plugin ufficiale Tencent), WebChat
   - TUI (Terminal UI) — l'interfaccia di base post-installazione

5. **Session model.** Tipi di sessione: main (chat 1:1), group isolation, activation modes, queue modes, reply-back. Regole per i gruppi: mention gating, reply tags, chunking per canale.

**Prompt pronto:**
> "Mostrami il contenuto del tuo SOUL.md e IDENTITY.md. Ci sono regole o limiti che vorresti che aggiornassi?"

**(i) Pro tip:** Il file SOUL.md è il tuo strumento più potente. Un agente con un SOUL.md generico darà risposte generiche. Investi tempo a scriverlo bene: definisci cosa l'agente deve fare, cosa *non* deve mai fare, e con quale tono comunicare.

---

## PARTE II — Installazione e primo setup

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

[← Capitolo 1](./01-cos-e-openclaw-e-perche-e-importante.md)  ·  [Indice](../README.md)  ·  [Capitolo 3 →](../PARTE-II-Installazione/03-scegliere-dove-installare-openclaw.md)
