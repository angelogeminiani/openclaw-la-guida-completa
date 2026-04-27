# Appendice A — Glossario

Voci alfabetiche dei termini tecnici usati nel libro. Le definizioni sono volutamente sintetiche: per il dettaglio rimandano al capitolo di riferimento.

**A2UI** — Agent-to-UI. Capacità dell'agente di creare interfacce visive dinamiche in tempo reale (Cap. 20).

**AGENTS.md** — Il *contratto di lavoro* dell'agente: istruzioni operative, memoria contestuale, regole di ingaggio. Letto a ogni avvio.

**API key** — Credenziale per accedere al provider LLM (Anthropic, OpenAI, ecc.). Inizia con un prefisso identificativo (es. `sk-ant-api03-*`). Da gestire come segreto. Vedi Cap. 14.

**Binding** — Associazione tra un canale (o un account/peer) e un agente specifico. Determina quale agente risponde quando arriva un messaggio. Vedi Cap. 10.

**BYOK** — Bring Your Own Key. Modello in cui l'utente fornisce le proprie API key al tool, anziché pagare il tool che a sua volta paga il provider. È il modello di OpenClaw.

**Canale** — Mezzo di comunicazione tra utente e agente: Telegram, WhatsApp, Slack, Discord, Signal, iMessage, Matrix, WeChat, e oltre 20 supportati. Vedi Cap. 6.

**ClawHub** — Il registry ufficiale delle skill della community (`clawhub.com`). 700+ skill, ma con noti problemi di sicurezza (~20% identificate come malevole). Vedi Cap. 13, 17.

**CLI** — Command-Line Interface. L'interfaccia a riga di comando di OpenClaw (`openclaw …`).

**Cron job** — Istruzione programmata che si ripete (orario, giornaliero, settimanale, su evento). Vedi Cap. 18.

**Gateway** — Il control plane di OpenClaw, esposto come WebSocket locale (`ws://127.0.0.1:18789`). Gestisce sessioni, canali, tool ed eventi. Tutto ciò che entra ed esce passa di qui (Cap. 20).

**Heartbeat** — Il *battito* periodico dell'agente (default ~30 min): si sveglia, controlla i cron, processa la coda dei messaggi, torna in attesa.

**IDENTITY.md** — Il *biglietto da visita* dell'agente: nome, emoji, vibe, descrizione breve.

**IronClaw** — Riscrittura di OpenClaw in Rust (NEAR AI) con focus su memory safety e zero telemetria. Vedi Cap. 4.

**Knowledge graph** — Layer 1 del memory system di Nat Eliason: fatti durevoli su persone e progetti, organizzati in cartelle PARA. Vedi Cap. 8, 16.

**Live Canvas** — Funzione correlata ad A2UI per la creazione e la modifica live di interfacce.

**LLM** — Large Language Model. Modello AI generativo come Claude, GPT, Gemini, Nemotron. OpenClaw è model-agnostic.

**Lobster (workflow shell)** — Shell di workflow nativa di OpenClaw: pipeline composabili tipizzate, local-first. Trasforma skill e tool in automazioni sicure.

**Moltbook** — Social network in stile Reddit dove solo agenti AI possono postare; gli umani osservano. Lanciato il 28 gennaio 2026, acquistato da Meta il 10 marzo 2026. Vedi Cap. 21.

**NanoClaw** — Alternativa minimalista (~700 righe TypeScript) con container Docker isolati per ogni chat. Solo Claude come modello. Vedi Cap. 4, 19.

**NemoClaw** — Wrapper di sicurezza enterprise di Nvidia attorno a OpenClaw: OpenShell sandboxing kernel-level, policy YAML, privacy router. Vedi Cap. 4.

**OpenShell** — Sandbox a livello kernel di NemoClaw (Nvidia). Usa Linux Security Modules per isolare l'agente a livello OS, non solo container.

**PARA system** — Metodo di organizzazione di Tiago Forte: Projects, Areas, Resources, Archives. Usato come struttura del knowledge graph nel memory system.

**Prompt injection** — Tecnica di attacco in cui istruzioni malevole sono nascoste in email, pagine web o contenuti che l'agente processa, e l'agente le esegue come se fossero istruzioni dell'utente. Vedi Cap. 13.

**Routing** — Logica del Gateway che instrada i messaggi in arrivo verso l'agente corretto in base al binding configurato.

**Session** — Unità di conversazione tra utente e agente. Tipi: main (chat 1:1), group isolation, activation modes, queue modes, reply-back. Vedi Cap. 2, 20.

**Skill** — Una directory contenente un file `SKILL.md` con metadati e istruzioni. Le skill possono essere bundled (incluse), globali (installate dall'utente) o di workspace (specifiche per un agente — priorità massima). Vedi Cap. 17.

**SKILL.md** — File markdown che descrive una skill: nome, scopo, dipendenze, esempi d'uso. Letto dall'agente quando deve usare la skill.

**SOUL.md** — La *personalità* dell'agente: tono, limiti, valori, confini etici. È qui che si definisce cosa l'agente *non* deve mai fare.

**Submolt** — Termine colloquiale per gli agenti registrati su Moltbook (analogo a *redditor* su Reddit).

**Token** — Unità minima di testo processata da un LLM (~3-4 caratteri). Il pricing API è espresso in $/M token (input e output separatamente).

**TOOLS.md** — Il *manuale d'uso*: note su come l'agente deve usare ciascuno strumento a disposizione.

**TUI** — Terminal User Interface. Interfaccia testuale base di OpenClaw post-installazione. Mostra il lobster ASCII art al primo *hatch*.

**USER.md** — Il *dossier sull'utente*: tutto ciò che l'agente sa di te (nome, ruolo, sfide, preferenze).

**VPS** — Virtual Private Server. Server cloud in affitto (Railway, DigitalOcean, Hostinger, ecc.). Una delle tre opzioni di installazione. Vedi Cap. 3.

**Webhook** — Endpoint HTTP che riceve eventi in tempo reale da un servizio esterno. Alcuni canali e integrazioni usano webhook.

**Workspace** — Cartella dedicata di un agente (`.openclaw/[nome]-workspace`) che contiene identità, tool, cron e memoria. Ogni agente ha il proprio workspace isolato.

**ZeroClaw** — Binary minimale (3,4 MB), deny-by-default, ideale per edge computing.

---

[← Capitolo 22](../PARTE-VIII-Visione-futuro/22-futuro-del-lavoro-con-gli-agenti.md)  ·  [Indice](../README.md)  ·  [Appendice B →](./B-comandi-cli-riferimento-rapido.md)
