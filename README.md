# OpenClaw: Guida Completa 🦞

> *Dal primo "hatch" al team multi-agente: tutto ciò che serve per padroneggiare il lobster digitale più virale del 2026.*

Questo repository contiene il manoscritto completo del libro **OpenClaw: Guida Completa**, suddiviso capitolo per capitolo in file Markdown. È pensato per essere letto direttamente su GitHub, clonato in locale, esportato in PDF/ePub o riusato come base per una documentazione viva.

> 📖 Cerchi solo l'elenco lineare di tutti i capitoli? Vai a [INDICE.md](./INDICE.md).

---

## A chi è rivolta questa guida

Tre livelli di lettore, segnalati su ogni capitolo:

| Simbolo | Livello | Per chi |
|---------|---------|---------|
| `[★]` | Base | Non ha mai usato il terminale, vuole un assistente AI personale |
| `[★★]` | Intermedio | Ha già installato OpenClaw o tool simili, vuole sbloccarne il pieno potenziale |
| `[★★★]` | Avanzato | Sviluppatore o power user: skill custom, deploy VPS, architettura interna |

---

## Come è strutturato il libro

La guida è divisa in **otto parti** + **cinque appendici**. Ogni parte ha la sua sottocartella e un breve README di indice. I capitoli sono numerati progressivamente da 1 a 22.

### 📁 [PARTE I — Capire OpenClaw](./PARTE-I-Capire-OpenClaw/)

Le fondamenta concettuali. Cos'è un agente autonomo, come funziona OpenClaw e qual è la sua anatomia interna.

- [Capitolo 1 — Cos'è OpenClaw e perché è importante `[★]`](./PARTE-I-Capire-OpenClaw/01-cos-e-openclaw-e-perche-e-importante.md)
- [Capitolo 2 — L'anatomia di un agente OpenClaw `[★]`](./PARTE-I-Capire-OpenClaw/02-anatomia-di-un-agente-openclaw.md)

### 📁 [PARTE II — Installazione e primo setup](./PARTE-II-Installazione/)

Tutto quello che serve per portare il tuo primo lobster digitale online: scelta dell'ambiente, sandboxing, installazione e collegamento ai canali.

- [Capitolo 3 — Scegliere dove installare OpenClaw `[★]`](./PARTE-II-Installazione/03-scegliere-dove-installare-openclaw.md)
- [Capitolo 4 — Preparare un ambiente sicuro: Docker, sandbox e wrapper `[★★]`](./PARTE-II-Installazione/04-preparare-un-ambiente-sicuro-docker-sandbox.md)
- [Capitolo 5 — Installazione step-by-step `[★]`](./PARTE-II-Installazione/05-installazione-step-by-step.md)
- [Capitolo 6 — Configurare Telegram (e altri canali) `[★]`](./PARTE-II-Installazione/06-configurare-telegram-e-altri-canali.md)

### 📁 [PARTE III — Il primo mese con OpenClaw](./PARTE-III-Primo-mese/)

Dall'onboarding del tuo agente ai primi 10 workflow pronti, fino al collegamento con Gmail, GitHub, Notion e altri strumenti.

- [Capitolo 7 — La prima conversazione: fare l'onboarding del tuo agente `[★★]`](./PARTE-III-Primo-mese/07-prima-conversazione-onboarding-agente.md)
- [Capitolo 8 — 10 workflow pronti all'uso `[★★]`](./PARTE-III-Primo-mese/08-dieci-workflow-pronti-all-uso.md)
- [Capitolo 9 — Aggiungere strumenti e integrazioni `[★★]`](./PARTE-III-Primo-mese/09-aggiungere-strumenti-e-integrazioni.md)

### 📁 [PARTE IV — Setup multi-agente](./PARTE-IV-Multi-agente/)

Quando un solo agente non basta: progettazione di un team specializzato, routing tra agenti, comunicazione e coordinamento.

- [Capitolo 10 — Perché un solo agente non basta `[★★]`](./PARTE-IV-Multi-agente/10-perche-un-solo-agente-non-basta.md)
- [Capitolo 11 — Progettare il tuo team di agenti `[★★]`](./PARTE-IV-Multi-agente/11-progettare-il-tuo-team-di-agenti.md)
- [Capitolo 12 — Comunicazione e coordinamento tra agenti `[★★★]`](./PARTE-IV-Multi-agente/12-comunicazione-e-coordinamento-tra-agenti.md)

### 📁 [PARTE V — Sicurezza e costi](./PARTE-V-Sicurezza-costi/)

Il modello di rischio di OpenClaw, come difendersi, e come gestire la spesa LLM dopo il ban Anthropic del 4 aprile 2026.

- [Capitolo 13 — Sicurezza: la guida che devi leggere `[★]`](./PARTE-V-Sicurezza-costi/13-sicurezza-la-guida-che-devi-leggere.md)
- [Capitolo 14 — Gestire i costi senza sorprese `[★]`](./PARTE-V-Sicurezza-costi/14-gestire-i-costi-senza-sorprese.md)

### 📁 [PARTE VI — Manutenzione e ottimizzazione](./PARTE-VI-Manutenzione/)

Care and feeding del tuo agente: diagnosi, riparazione, backup, e affinamento di SOUL.md e prompt.

- [Capitolo 15 — Care and feeding: tenere il tuo agente in salute `[★★]`](./PARTE-VI-Manutenzione/15-care-and-feeding-tenere-l-agente-in-salute.md)
- [Capitolo 16 — Ottimizzare la qualità delle risposte `[★★]`](./PARTE-VI-Manutenzione/16-ottimizzare-la-qualita-delle-risposte.md)

### 📁 [PARTE VII — Uso avanzato](./PARTE-VII-Uso-avanzato/)

Skill personalizzate, cron job complessi, deploy su cloud, e l'architettura del Gateway WebSocket.

- [Capitolo 17 — Creare skill personalizzate `[★★★]`](./PARTE-VII-Uso-avanzato/17-creare-skill-personalizzate.md)
- [Capitolo 18 — Cron job e automazioni avanzate `[★★★]`](./PARTE-VII-Uso-avanzato/18-cron-job-e-automazioni-avanzate.md)
- [Capitolo 19 — Deploy su VPS e infrastruttura cloud `[★★★]`](./PARTE-VII-Uso-avanzato/19-deploy-su-vps-e-infrastruttura-cloud.md)
- [Capitolo 20 — L'architettura del Gateway `[★★★]`](./PARTE-VII-Uso-avanzato/20-architettura-del-gateway.md)

### 📁 [PARTE VIII — Visione e futuro](./PARTE-VIII-Visione-futuro/)

L'ecosistema attorno a OpenClaw (Moltbook, hosted platforms, fondazione) e cosa significa lavorare con un agente come collega digitale.

- [Capitolo 21 — L'ecosistema OpenClaw `[★]`](./PARTE-VIII-Visione-futuro/21-ecosistema-openclaw.md)
- [Capitolo 22 — Il futuro del lavoro con gli agenti `[★]`](./PARTE-VIII-Visione-futuro/22-futuro-del-lavoro-con-gli-agenti.md)

### 📁 [Appendici](./Appendici/)

Materiali di riferimento rapido da tenere a portata di mano:

- [Appendice A — Glossario](./Appendici/A-glossario.md)
- [Appendice B — Comandi CLI di riferimento rapido](./Appendici/B-comandi-cli-riferimento-rapido.md)
- [Appendice C — Template SOUL.md e IDENTITY.md](./Appendici/C-template-soul-identity.md)
- [Appendice D — Checklist di sicurezza](./Appendici/D-checklist-sicurezza.md)
- [Appendice E — Risorse e link utili](./Appendici/E-risorse-e-link-utili.md)

---

## Percorsi di lettura consigliati

Non sei obbligato a leggere tutto in ordine. Ecco tre percorsi a seconda del tuo profilo:

### 🟢 Percorso "Voglio installare OpenClaw oggi" (3-4 ore)

1 → 2 → 3 → 5 → 6 → 7 → 8 → 13 → 14

Salti il capitolo Docker/sandbox (Cap. 4) per arrivare prima all'agente funzionante, ma leggi **subito** sicurezza e costi prima di lasciarlo correre da solo.

### 🟡 Percorso "Voglio un setup robusto" (1 settimana)

1 → 2 → 3 → 4 → 5 → 6 → 7 → 8 → 9 → 13 → 14 → 15

Aggiungi il capitolo sandbox e quello sulle integrazioni: la base solida prima di automatizzare la tua vita.

### 🔴 Percorso "Voglio un team di agenti che lavora per me" (2-4 settimane)

Tutti i capitoli, in ordine. Più Appendice C per i template SOUL.md.

---

## Schema standard di ogni capitolo

Ogni capitolo segue la stessa struttura:

1. **Titolo + livello di difficoltà**
2. **Cosa imparerai** — 3-5 punti chiave
3. **Prerequisiti** — cosa devi aver già fatto
4. **Contenuto principale** — passi numerati dove appropriato
5. **Prompt pronti all'uso** — testi copia-incolla da inviare all'agente
6. **Errori comuni** — diagnostica e fix
7. **Checklist di fine capitolo**

I capitoli che non hanno ancora le sezioni "Errori comuni" e "Checklist" contengono **placeholder strutturati** (tabelle e bullet vuoti marcati `_TODO_`) come traccia per la stesura definitiva.

### Box ricorrenti

| Box | Significato |
|-----|-------------|
| `(!) Attenzione` | Avviso su sicurezza, costi o azioni irreversibili |
| `(i) Pro tip` | Trucco che si scopre solo con l'esperienza |
| `(#) Debug` | Diagnostica e riparazione quando qualcosa si rompe |
| `Prompt pronto` | Blocco copia-incolla da inviare direttamente all'agente |

---

## Come usare questo repository

### Leggere online

Naviga le cartelle direttamente su GitHub: ogni file `.md` viene renderizzato automaticamente. I link tra capitoli funzionano sia su GitHub sia in locale.

### Clonare e leggere in locale

```bash
git clone https://github.com/<tuo-utente>/openclaw-guida.git
cd openclaw-guida
```

Aprilo in [Obsidian](https://obsidian.md), VS Code, o qualsiasi editor Markdown. Obsidian è particolarmente comodo: crea automaticamente il grafo delle pagine collegate.

### Esportare in PDF / ePub

Con [Pandoc](https://pandoc.org):

```bash
# PDF unico (richiede LaTeX installato)
pandoc README.md PARTE-*/[0-9]*.md Appendici/*.md \
  -o openclaw-guida.pdf --toc --toc-depth=2

# ePub
pandoc README.md PARTE-*/[0-9]*.md Appendici/*.md \
  -o openclaw-guida.epub --toc --toc-depth=2 \
  --metadata title="OpenClaw: Guida Completa"
```

### Contribuire

I refusi e le imprecisioni si correggono via pull request. Per aggiunte sostanziali (nuovi capitoli, nuovi workflow, casi d'uso) apri prima una issue per discuterne.

OpenClaw evolve molto velocemente — se trovi informazioni datate (versioni di tool, prezzi LLM, link rotti) segnalale: aiuti la community.

---

## Date e versioning

- **Versione di riferimento**: aprile 2026
- **Eventi inclusi**: ban Anthropic del 4 aprile 2026, acquisizione Moltbook da parte di Meta (10 marzo 2026), ingresso di Steinberger in OpenAI (14 febbraio 2026)
- **Software**: OpenClaw v.x.y al momento della stesura. La CLI può cambiare: verifica sempre con `openclaw --version` e leggi il changelog ufficiale.

OpenClaw evolve rapidamente. Verifica i comandi e i prezzi prima di seguirli alla lettera.

---

## Avvertenza importante

> **(!) OpenClaw ha accesso completo al computer su cui gira.** Filesystem, rete, comandi shell, browser, email, calendario. Questo lo rende potente *e* pericoloso. **Non installarlo mai su un computer in uso attivo o che contiene dati sensibili.** Usa sempre un dispositivo dedicato o un VPS isolato. Leggi il [Capitolo 13](./PARTE-V-Sicurezza-costi/13-sicurezza-la-guida-che-devi-leggere.md) **prima** di esporlo a internet o di dargli accesso a integrazioni in scrittura.

---

## Licenza

Vedi [`LICENSE`](./LICENSE) nel repository. I contenuti sono distribuiti sotto Creative Commons BY-SA 4.0.

---

## Crediti e fonti

Il libro si basa su documentazione ufficiale, articoli pubblici, podcast e testimonianze della community OpenClaw. L'elenco completo delle fonti consultate è nell'[Appendice E](./Appendici/E-risorse-e-link-utili.md).

---

*Buona lettura — e attenzione alle chele.* 🦞
