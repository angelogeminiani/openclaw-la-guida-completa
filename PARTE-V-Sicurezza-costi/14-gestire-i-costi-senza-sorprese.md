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

### L'equazione dei costi

Partiamo dalla buona notizia: OpenClaw non costa niente. Il software è open-source con licenza MIT, non ha piani a pagamento, non ha funzionalità bloccate dietro un abbonamento. La notizia meno buona è che OpenClaw, da solo, non pensa: ogni volta che il tuo agente legge un messaggio, ragiona o scrive una risposta, sta chiamando un modello LLM — e il modello si paga.

L'equazione è semplice e vale la pena impararla a memoria, perché spiega ogni voce della bolletta:

```
costo = token in ingresso × prezzo input
      + token in uscita  × prezzo output
```

I *token* sono i frammenti di testo che il modello legge e produce (in italiano, grossolanamente, una parola vale 1,5–2 token). I prezzi sono espressi per milione di token e — punto cruciale — l'output costa sempre molto più dell'input, in genere quattro–cinque volte tanto.

C'è un dettaglio che sorprende tutti i principianti: l'agente non paga solo quello che *tu* scrivi. A ogni chiamata reinvia l'intero contesto della sessione — i file canonici (SOUL.md, AGENTS.md, USER.md…), le note di memoria del giorno, la storia della conversazione. Riprendi l'esempio del [Capitolo 2](../PARTE-I-Capire-OpenClaw/02-anatomia-di-un-agente-openclaw.md): quando Polly prepara il brief sul cliente Rossi consuma circa 3.500 token in ingresso e 250 in uscita. Di quei 3.500, il tuo messaggio ne pesa forse 30: tutto il resto è contesto. Costo del singolo task: circa un centesimo su Claude Sonnet 4.6. Innocuo. Ma un centesimo ripetuto da un cron in loop per una notte intera diventa una bolletta vera.

Come promesso nel Capitolo 2, ecco la contabilità trasformata in regole di budget per task (valori indicativi su Sonnet 4.6, in dollari; al cambio di maggio 2026, 1 $ ≈ 0,92 €):

| Tipo di task | Budget tipico |
|---|---|
| Messaggio semplice | < $0,02 |
| Brief con 1–2 skill | $0,02–0,12 |
| Ricerca web + sintesi | $0,05–0,15 |
| Ragionamento lungo (Opus) | $0,10–0,35 |

La regola di pollice: se un singolo task supera regolarmente un dollaro, o stai usando un modello troppo potente per quel lavoro, o la sessione si è gonfiata di contesto inutile (ne riparliamo tra poco).

Per pagare i token le strade oggi sono due, più una mezza. La **API key** (consigliata, la più affidabile): paghi esattamente i token che consumi, sul pannello del provider. Oppure la **sottoscrizione ChatGPT Pro** a $200 (~€185) al mese: una flat fee (tariffa fissa mensile) che OpenAI ha esplicitamente "benedetto" per l'uso con agenti come OpenClaw — conviene solo se consumi più di $200 equivalenti di token. La mezza strada sono i **modelli locali**, che non pagano token ma hardware ed elettricità: ci arriviamo nelle strategie. E la strada che a maggio 2026 non esiste più, la sottoscrizione Claude, merita una sezione tutta sua.

### I modelli di maggio 2026: il listino

Prima della storia, i numeri. Questa è la fotografia dei prezzi a maggio 2026, rilevata dalle dashboard dei provider: prezzi per milione di token, in dollari (1 $ ≈ 0,92 €). I listini cambiano ogni pochi mesi: usali come ordine di grandezza e verifica sempre sul pannello del tuo provider.

| Modello | Input | Output |
|---|---|---|
| Claude Opus 4.6 | $5 | $25 |
| Claude Sonnet 4.6 | $3 | $15 |
| Claude Haiku 4.5 | $1 | $5 |
| GPT-5.1 | $2,50 | $10 |
| GPT-5.1 mini | $0,45 | $1,80 |
| Codex 5.4 | $6 | $24 |
| Gemini Pro | $2 | $8 |
| Gemini Flash | $0,30 | $1,20 |
| Kimi K2.5 | $0,60 | $2,50 |
| MiniMax M2.5 | $0,40 | $1,60 |
| Mistral Large | $2 | $6 |
| Nemotron (locale) | $0\* | $0\* |

\* I modelli locali non hanno costo per token, ma richiedono hardware adeguato (GPU consigliata) ed elettricità: vedi il confronto TCO del [Capitolo 3](../PARTE-II-Installazione/03-scegliere-dove-installare-openclaw.md).

Tre fasce, in pratica. I **premium** vanno riservati al ragionamento difficile: Opus 4.6 costa meno del doppio dei modelli medi e Codex 5.4 circa il doppio di Sonnet — premium più per posizionamento che per prezzo. I **medi** (Sonnet 4.6 — il default di questo libro —, GPT-5.1, Gemini Pro, Mistral Large) sono il cavallo da lavoro quotidiano. Gli **economici** (Haiku 4.5, Gemini Flash, GPT-5.1 mini, Kimi K2.5, MiniMax M2.5) costano centesimi e sono perfetti per heartbeat, cron e task ripetitivi. Tieni questa tabella sottomano: tutto il resto del capitolo ci torna sopra.

**(i) Pro tip — aggiornamento giugno 2026:** questo listino è la fotografia di maggio. Da allora il top di gamma si è mosso: Anthropic ha rilasciato **Opus 4.8** (sopra Opus 4.6) e un nuovo livello **Fable 5**, mentre lato OpenAI il riferimento competitivo è passato a **GPT-5.2**. Sonnet 4.6 e Haiku 4.5 restano attuali e validi per gli esempi del libro; verifica comunque i prezzi correnti sul pannello del provider.

### Il terremoto del 4 aprile 2026

Se nei mesi scorsi hai letto tutorial che consigliavano di collegare OpenClaw alla tua sottoscrizione Claude Pro o Max, dimenticali: dal 4 aprile 2026 non funzionano più. Quel giorno Anthropic ha bloccato l'uso delle sottoscrizioni Claude Pro ($20/mese, ~€18) e Max ($100–200/mese, ~€92–185) con tutti i tool di terze parti, OpenClaw incluso. La motivazione ufficiale: i tool terzi aggiravano le ottimizzazioni di prompt caching di Anthropic, consumando molte più risorse per sessione rispetto agli strumenti proprietari (Claude Code, Cowork). Boris Cherny, responsabile di Claude Code: "Le sottoscrizioni non erano progettate per i pattern di utilizzo di questi tool terzi."

Il ban non è arrivato dal nulla. La timeline dell'escalation:

- **9 gennaio 2026** — Anthropic blocca silenziosamente i token OAuth nelle app terze, poi fa marcia indietro dopo il backlash della community
- **19 febbraio 2026** — aggiornamento dei ToS: l'uso di token OAuth da piani Free/Pro/Max in prodotti terzi è formalmente vietato
- **marzo 2026** — Anthropic lancia Claude Code Channels (Telegram/Discord), internalizzando la feature più popolare di OpenClaw
- **4 aprile 2026** — enforcement tecnico: blocchi server-side attivi

E la cronologia del giorno X, ricostruita dai thread della community, è la dimostrazione di quanto poco preavviso ci sia stato — meno di 24 ore:

- **3 aprile, sera (ora del Pacifico)** — email ai sottoscrittori Pro/Max: l'accesso da tool terzi cesserà il giorno dopo
- **4 aprile, mattina** — post ufficiale sul blog di Anthropic che conferma l'enforcement
- **4 aprile, ore 12:00 PT (le 21:00 in Italia)** — i blocchi server-side si attivano; le sessioni OpenClaw su sottoscrizione smettono di rispondere
- **primo pomeriggio PT** — il Discord di OpenClaw si riempie di segnalazioni; il thread "Tell HN: Anthropic no longer allowing Claude for OpenClaw" sale in cima a Hacker News
- **in serata** — Steinberger commenta; nel giro di ore compaiono le prime guide di migrazione verso GPT-5.1, Kimi K2.5 e i modelli locali
- **5–6 aprile** — Anthropic annuncia le misure di transizione (credito una tantum, bundle scontati)
- **17 aprile** — scadenza per richiedere il credito una tantum

Vale la pena capire *come* funziona il blocco, perché ti aiuta a diagnosticare l'errore se lo incontri. Quando autorizzi un'app con il tuo account Claude, l'app riceve un **token OAuth**: una credenziale legata alla sottoscrizione, riconoscibile dal prefisso `sk-ant-oat-`. Una **API key**, invece, è una credenziale a consumo generata dalla console sviluppatori, con prefisso `sk-ant-api03-`. Il blocco di Anthropic è un filtro sul tipo di credenziale: i token OAuth vengono rifiutati quando arrivano da sorgenti non autorizzate (tutto ciò che non è Claude.ai, Claude Code o Cowork), le API key continuano a funzionare ovunque. Il codice d'errore che vedrai è **HTTP 429** con il messaggio "Extra usage is required". Non è un ban del tuo account: è la porta che si chiude su quel tipo di chiave.

**(!) Attenzione:** Se il tuo agente smette improvvisamente di funzionare e usavi una sottoscrizione Claude, il motivo è questo ban. Passa a una API key o cambia modello.

Le alternative per chi usava Claude, coi conti esatti:

- **API key Anthropic** (pay-per-token): $3/$15 per milione di token su Sonnet 4.6, $5/$25 su Opus 4.6 — la via maestra
- **"Extra usage"**: un addon pay-as-you-go agganciato alla sottoscrizione esistente, allo stesso prezzo per token dell'API. Attenzione ai conti: la sottoscrizione non copre nessun token di OpenClaw, quindi paghi l'abbonamento *più* tutto il consumo. Ha senso solo se tieni la sottoscrizione per Claude Code o Claude.ai e ti interessa la fatturazione unificata — o se sfrutti lo sconto fino al 30% sui bundle pre-acquistati
- **Credito una tantum** pari a un mese di abbonamento (andava richiesto entro il 17 aprile 2026)

In altre parole: che tu scelga API key o extra usage, per OpenClaw — a maggio 2026 — su Claude **si paga sempre per token**. È la stessa conclusione del Capitolo 3, vista dall'altra angolazione.

L'impatto sui costi dipende interamente dal profilo. Un utente intensivo che girava Opus 4.6 con ~500K token in ingresso e 200K in uscita al giorno paga in API circa $225/mese (~€207): col listino Opus di maggio 2026, appena sopra i $200 del vecchio piano Max. Un utente moderato che pagava i $20 del piano Pro e consumava come un piano da $150 si ritrova invece un aumento di 7 volte o più. Paradossalmente, gli utenti davvero leggeri possono perfino *risparmiare*: un consumo da $6–10 al mese di API costa meno dei $20 della vecchia sottoscrizione. La sofferenza è tutta di chi consumava molto pagando un prezzo fisso basso — che era esattamente il "loophole" che Anthropic ha chiuso.

Le reazioni della community sono state immediate. Steinberger — pur ormai in OpenAI dal 14 febbraio — ha definito la decisione "triste per l'ecosistema" e ha rivelato che lui e Dave Morin avevano cercato di convincere Anthropic, ottenendo solo un ritardo di una settimana. Garry Tan (Y Combinator): "Potrebbe rivelarsi un errore strategico o un colpo di genio." Molti utenti sono migrati verso modelli OpenAI (GPT-5.1, Codex 5.4), modelli locali (Nemotron) o verso ChatGPT Pro come provider principale.

La lezione per te è una sola, e vale più di ogni tabella di prezzi: **non costruire mai un workflow critico su un singolo provider**. La natura model-agnostic di OpenClaw — il modello lo porti tu, e puoi cambiarlo — è passata in una notte da dettaglio architetturale a polizza assicurativa. Usala.

**(i) Pro tip — aggiornamento giugno 2026:** dopo la chiusura della finestra temporale di questo libro, Anthropic ha parzialmente fatto marcia indietro. Dal **15 giugno 2026** le sottoscrizioni Claude Pro/Max tornano utilizzabili con tool terzi come OpenClaw attraverso un meccanismo di credito "Agent SDK": un plafond mensile (Pro $20, Max 5× $100, Max 20× $200) che assorbe il costo della minore efficienza di caching dei tool esterni, ponendo però fine al compute agentico illimitato a tariffa fissa. I conti e le strategie di questo capitolo restano validi come fotografia di maggio 2026, ma prima di scegliere tra sottoscrizione e API key verifica lo stato attuale sulla documentazione ufficiale (link in Appendice E).

### Un giorno nella vita di Polly

Le tariffe per milione di token sono astratte. Proviamo a renderle concrete seguendo Polly, l'assistente personale del libro, per una giornata di lavoro ordinaria — un solo agente, configurazione standard, heartbeat ogni 30 minuti.

| Quando | Attività | Token (in/out) |
|---|---|---|
| 24h | 48 heartbeat | 96K / 2,4K |
| 07:00 | digest mattutino (cron) | 15K / 1K |
| 09:14 | brief cliente (2 skill) | 25K / 2K |
| 09–18 | ~20 messaggi sparsi | 80K / 6K |
| 17:30 | ricerca web + sintesi | 25K / 2K |
| 22:00 | nota di memoria (cron) | 10K / 1K |

Totale: circa **250K token in ingresso e 15K in uscita al giorno**. Nota il dato controintuitivo: la voce più pesante non è il lavoro vero, sono i 48 heartbeat — il "polso" che Polly batte ogni mezz'ora anche quando non succede niente. Ogni battito ricarica i file canonici e la memoria recente: 2.000 token alla volta, 96.000 al giorno, quasi il 40% del totale.

Ora applichiamo il listino. Stessa Polly, stessa giornata, cinque modelli diversi:

| Modello | $/giorno | $/mese |
|---|---|---|
| Claude Opus 4.6 | 1,63 | ~49 (~€45) |
| Claude Sonnet 4.6 | 0,98 | ~29 (~€27) |
| GPT-5.1 | 0,78 | ~23 (~€21) |
| Claude Haiku 4.5 | 0,33 | ~10 (~€9) |
| Kimi K2.5 | 0,19 | ~6 (~€5,50) |

La stessa identica giornata costa da €5,50 a €45 al mese a seconda del modello: un fattore 8. Ed è qui che nasce l'idea più importante del capitolo: non devi *scegliere* un modello, devi *assegnare* i modelli. Se Polly usasse Haiku per i 48 heartbeat e Sonnet per tutto il resto, la giornata scenderebbe da $0,98 a circa $0,76: quasi un quarto di spesa in meno senza perdere nulla, perché rispondere `HEARTBEAT_OK` non richiede un premio Nobel. È il *routing per modello*, e lo configuriamo tra due sezioni.

### Stima costi per profilo d'uso

Mettendo insieme listino e giornate-tipo, ecco le tre fasce di spesa post-ban (aprile 2026), con API key. Prezzi in dollari; al cambio di maggio 2026, 1 $ ≈ 0,92 €.

- **Leggero** — 1 agente, task semplici, pochi cron, modello medio o economico: **$6–30/mese** (~€5,50–28). La Polly della sezione precedente su Sonnet, con routing, sta comodamente qui.
- **Moderato** — 2–3 agenti, automazioni quotidiane, qualche ricerca pesante: **$50–150/mese** (~€46–138). Il routing multi-modello qui non è consigliato, è necessario.
- **Intensivo** — 5–9 agenti, business automation, Opus per il ragionamento: **$200–1.000/mese** (~€185–920). A questo livello la spesa LLM è una voce di bilancio aziendale.

Claire Vo, che gestisce il team di nove agenti del [Capitolo 11](../PARTE-IV-Multi-agente/11-progettare-il-tuo-team-di-agenti.md), sta nella fascia alta per scelta: "Sto arrivando a spendere $1.000/mese. Per me è una spesa aziendale, molto meno costosa di un team di umani."

Su base annua — la tabella promessa nel Capitolo 5 — i numeri fanno più impressione, ed è il modo giusto di guardarli quando decidi il budget:

| Profilo | $/mese | $/12 mesi |
|---|---|---|
| Leggero | 6–30 | 72–360 |
| Moderato | 50–150 | 600–1.800 |
| Intensivo | 200–1.000 | 2.400–12.000 |

Due avvertenze sulle fasce. Primo: il passaggio da una fascia all'altra non è graduale ma a gradini — il giorno in cui aggiungi il secondo agente, o il primo cron con ricerca web, la spesa salta. Secondo: il multi-agente costa più della somma delle parti. Come visto nel [Capitolo 12](../PARTE-IV-Multi-agente/12-comunicazione-e-coordinamento-tra-agenti.md), ogni delega tra agenti raddoppia il contesto pagato: se Polly delega a Kelly, paghi i file canonici e la memoria di entrambi. Tienine conto quando passi dal profilo leggero al moderato.

### Strategie di ottimizzazione costi

Le strategie sono sei, in ordine di impatto. La prima vale da sola più delle altre cinque messe insieme.

**1. Routing per modello.** L'abbiamo visto coi numeri di Polly: assegnare il modello giusto a ogni tipo di lavoro è la leva più potente che hai. Modelli economici per i task meccanici (heartbeat con Gemini Flash o Haiku: ~$0–5/mese), modelli medi per le automazioni standard (Sonnet 4.6 o Haiku: ~$10–20/mese), modelli potenti solo per il ragionamento complesso (Opus 4.6 o Codex 5.4: $20–50/mese per i task che li richiedono davvero). Ed ecco, finalmente, come si configura. Il routing vive nella config del Gateway:

```yaml
# ~/.openclaw/config.yaml — model routing
agents:
  defaults:
    model: claude-sonnet-4-6      # workhorse
    models:
      heartbeat: claude-haiku-4-5 # 48 beat/day
      cron: claude-haiku-4-5      # light crons
      reasoning: claude-opus-4-6  # on demand
```

E per dare a ogni agente del team il suo modello, in base al volume e alla delicatezza del ruolo:

```yaml
agents:
  polly:
    model: claude-sonnet-4-6      # PA, quality
  finn:
    model: kimi-k2-5              # high volume
```

Dopo la modifica, `openclaw gateway restart` e verifica con `/status` nel canale che il modello attivo sia quello atteso. Lo schema esatto della sezione `models` evolve da una versione all'altra: verifica con `openclaw --version` e con la Configuration reference della documentazione ufficiale (link in Appendice E).

**2. ChatGPT Pro come flat-rate.** La sottoscrizione ChatGPT Pro ($200/mese, ~€185) resta utilizzabile con OpenClaw come provider ad alto volume — OpenAI l'ha "benedetta" esplicitamente. Il conto è banale: se il tuo consumo API supererebbe i $200/mese, la tariffa fissa conviene; sotto, no.

**3. Modelli alternativi economici.** Kimi K2.5, MiniMax M2.5, Mistral: la community post-ban ha scoperto che per la maggior parte dei task quotidiani le alternative a basso costo sono più che adeguate. Non hanno la finezza di ragionamento di Opus, ma a un decimo del prezzo la domanda giusta è: questo task la richiede davvero?

**4. Modelli locali.** Nemotron, Llama: zero costo per token e massima privacy, in cambio di hardware adeguato (GPU consigliata) e qualità inferiore sui task complessi. Sensati come tassello di un routing — i task ripetitivi in locale, il ragionamento in cloud — più che come soluzione unica.

**5. Prompt cache e batching.** Il prompt caching fa pagare a tariffa ridotta le parti di contesto già viste dal provider (i file canonici, per esempio, che sono identici a ogni chiamata). Anthropic ha contribuito PR per migliorare il cache hit rate di OpenClaw: tenere l'installazione aggiornata con `openclaw update` riduce il costo per token via API senza che tu debba fare altro. Il batching è il complemento: raggruppare i task non urgenti — il digest serale, la nota di memoria, i report settimanali — in un'unica esecuzione, invece di lasciare che ognuno ricarichi da zero il proprio contesto. Tre cron che girano insieme pagano i file canonici una volta sola; tre cron sparsi nella giornata li pagano tre volte.

**6. Ridurre il contesto stantio.** Ogni chiamata reinvia l'intero contesto della sessione: una conversazione lasciata aperta per giorni accumula storia morta che paghi a ogni messaggio. Regola pratica: avvia sessioni nuove regolarmente e non usare una chat infinita come archivio — per ricordare le cose c'è la memoria persistente, che costa molto meno della storia di sessione.

**(i) Pro tip — Caso studio: da $200/mese a $15/mese.** Un utente della community ha ricostruito il proprio setup dopo il ban usando: 2 VPS da €4,99/mese di listino (Hostinger) per ridondanza + Kimi K2.5 come modello primario + MiniMax M2.5 come fallback economico. Totale: ~$15/mese (~€14) contro i $200 (~€185) precedenti. Non è la stessa qualità di Opus, ma è sufficiente per il 90% dei workflow quotidiani. La lezione: il routing multi-modello non è un'ottimizzazione opzionale — è una necessità.

### Monitorare la spesa

L'ottimizzazione senza monitoraggio è cieca. Tre strumenti, dal più immediato al più completo.

Il comando **`/status`**, scritto direttamente nel canale (Telegram o altro), risponde con modello attivo, token consumati e costo stimato della sessione corrente. È il check da 5 secondi: prendi l'abitudine di lanciarlo quando un task ti sembra durato troppo. Per la vista d'insieme c'è **`openclaw cost report --since 7d`** da terminale (richiede l'hook `cost-tracker` abilitato nel wizard del Capitolo 5), che aggrega i costi per agente e per giorno. La fonte di verità finale, però, è la **dashboard del provider** (Anthropic Console, OpenAI Dashboard): è lì che vive la bolletta vera, ed è lì che vanno impostati due numeri prima ancora del primo cron in produzione: un **alert** via email a una soglia intermedia (per esempio a metà budget) e un **hard cap** — il tetto di spesa invalicabile oltre il quale il provider smette di servire richieste. L'hard cap a volte interrompe l'agente a metà conversazione, ed è esattamente quello che vuoi: meglio un task fallito che una sorpresa a quattro cifre.

**(#) Debug:** spesa anomala e improvvisa? Nell'ordine: `/status` per vedere la sessione corrente; `openclaw cron list` per scovare cron in loop (e `openclaw cron disable <id>` per fermare il colpevole); `openclaw logs --follow` per guardare le chiamate in tempo reale. Nove volte su dieci il colpevole è un cron che ritenta all'infinito o una sessione gonfia di contesto.

**Prompt pronto:**
> "Mostrami l'analisi della tua spesa LLM dell'ultima settimana. Per ogni giorno riporta: numero di chiamate, token in ingresso/uscita, modello usato, costo stimato. Identifica: (1) il singolo task più costoso, (2) le opportunità di routing su modelli più economici (es. Haiku per heartbeat, Opus solo per ragionamento), (3) eventuali cron in loop o conversazioni stantie. Proponi un piano per ridurre la spesa del 30% senza perdere qualità."

L'abitudine giusta è settimanale: cinque minuti, ogni lunedì, dashboard del provider più il prompt qui sopra. Il budget di un agente si gestisce come quello di un dipendente — non controllandolo ogni ora, ma non scoprendo a fine trimestre che ha comprato un'auto aziendale.

## Errori comuni e come risolverli

**Sintomo:** bolletta API raddoppiata in un giorno.
Causa: cron in loop o conversazione che cresce a dismisura.
Fix: `openclaw cron list` per identificare il cron sospetto,
`openclaw cron disable <id>` per fermarlo, poi configurare
un budget di iterazioni.

**Sintomo:** errore HTTP 429 "Extra usage is required" su un
setup che prima funzionava.
Causa: token OAuth (`sk-ant-oat-*`) di una sottoscrizione
Claude, bloccata dal 4 aprile 2026.
Fix: generare una API key (`sk-ant-api03-*`) dalla console
Anthropic, o cambiare provider.

**Sintomo:** ChatGPT Pro blocca dopo poche ore.
Causa: rate limit della sottoscrizione raggiunto.
Fix: per workload pesanti passare ad API a consumo, a modelli
alternativi economici (Kimi K2.5) o a modelli locali
(Nemotron).

**Sintomo:** Opus usato per task semplici → costo elevato.
Causa: routing modello non configurato.
Fix: configurare la sezione `models` nella config del Gateway
(vedi sopra): Opus per ragionamento complesso, Haiku/Flash
per heartbeat e cron.

**Sintomo:** errore "insufficient quota" a metà conversazione.
Causa: hard cap (tetto di spesa) del provider raggiunto.
Fix: aumentare il limite o passare a un secondo provider come
fallback.

## Checklist di fine capitolo

- [ ] Conosco il pricing del mio provider LLM (input/output, per modello)
- [ ] Ho impostato un budget mensile e un alert nel pannello del provider
- [ ] Routing modello configurato (Opus solo dove serve, Haiku/Flash per heartbeat)
- [ ] Verifico la spesa almeno una volta a settimana con `/status` o dashboard
- [ ] Ho un piano B se il provider blocca o aumenta i prezzi
- [ ] Non ho più token OAuth (`sk-ant-oat-*`) in giro: solo API key
- [ ] So stimare a occhio il costo di un task con la tabella del listino

## Link e risorse utili

- [Anthropic blocks OpenClaw from Claude subscriptions](https://thenextweb.com/news/anthropic-openclaw-claude-subscription-ban-cost) — cronaca del ban del 4 aprile 2026 e impatto sui costi
- [Anthropic cuts off Claude subscriptions with OpenClaw](https://venturebeat.com/technology/anthropic-cuts-off-the-ability-to-use-claude-subscriptions-with-openclaw-and) — ricostruzione dell'escalation e delle reazioni
- [Anthropic reinstates OpenClaw on Claude subscriptions](https://venturebeat.com/technology/anthropic-reinstates-openclaw-and-third-party-agent-usage-on-claude-subscriptions-with-a-catch) — la parziale marcia indietro di giugno 2026 (credito Agent SDK)
- [Claude Code subscribers need extra for OpenClaw](https://techcrunch.com/2026/04/04/anthropic-says-claude-code-subscribers-will-need-to-pay-extra-for-openclaw-support/) — i dettagli dell'opzione "extra usage"
- [Rebuilt my OpenClaw setup for $15/month](https://medium.com/@rentierdigital/anthropic-just-killed-my-200-month-openclaw-setup-so-i-rebuilt-it-for-15-9cab6814c556) — caso studio "$200 → $15/mese" con dettagli pratici
- [Anthropic provider docs (OpenClaw)](https://docs.openclaw.ai/providers/anthropic) — configurazione di chiavi API Anthropic post-ban
- [Tell HN: Anthropic no longer allowing Claude for OpenClaw](https://news.ycombinator.com/item?id=47633396) — discussione community con alternative concrete

Per l'elenco completo delle fonti del libro, vedi [Appendice E](../Appendici/E-risorse-e-link-utili.md).

---

[← Capitolo 13](./13-sicurezza-la-guida-che-devi-leggere.md)  ·  [Indice](../README.md)  ·  [Capitolo 15 →](../PARTE-VI-Manutenzione/15-care-and-feeding-tenere-l-agente-in-salute.md)
