# Capitolo 17 — Creare skill personalizzate [★★★]

## Cosa imparerai

- L'anatomia di una skill: directory + SKILL.md
- Come scrivere una skill da zero
- Come pubblicare su ClawHub
- Sicurezza delle skill: code review e sandboxing

## Prerequisiti

Aver già installato e usato qualche skill esistente ([Capitolo 9](../PARTE-III-Primo-mese/09-aggiungere-strumenti-e-integrazioni.md)). Conoscenza di base di Markdown e YAML. Per le skill con script, dimestichezza con un linguaggio di scripting (Python, Node, bash).

## Contenuto principale

La terza volta che chiedi a Max di trasformare le note di un lancio in un post LinkedIn, ti accorgi di una cosa: gli stai ripetendo le stesse sette istruzioni della settimana scorsa. Niente emoji, massimo 1.300 caratteri, apertura con un dato concreto, chiusura con una domanda, mai il gergo "rivoluzionario". Le avevi anche messe in TOOLS.md, ma in mezzo alle note su Home Assistant e sull'API del gestionale si sono perse, e Max le applica una volta sì e due no. Quello che ti serve non è un'altra nota: è un *pacchetto* — una procedura con un nome, delle istruzioni che si caricano solo quando servono, magari uno script. Quello che ti serve, in OpenClaw, si chiama skill. Questo capitolo ti insegna a costruirla, testarla, pubblicarla e — soprattutto, dopo quello che hai letto nel [Capitolo 13](../PARTE-V-Sicurezza-costi/13-sicurezza-la-guida-che-devi-leggere.md) — a non farti male.

### I segnali che ti serve una skill custom

Una skill non è il primo strumento da impugnare: è il terzo o il quarto. I segnali che è arrivato il momento sono ricorrenti e facili da riconoscere.

Il primo è la **ripetizione**: stai dando all'agente le stesse istruzioni multi-passo per la terza volta, oppure la stessa scheda di TOOLS.md è cresciuta fino a occupare metà del file. Il secondo è il **determinismo**: una parte del compito non dovrebbe essere "ragionata" dall'LLM ma eseguita uguale ogni volta — una chiamata API con i parametri giusti, un calcolo, una conversione di formato. Ogni volta che l'agente "reinventa" quel passaggio rischia di sbagliarlo, e uno script da 20 righe lo farebbe sempre giusto, gratis. Il terzo è la **condivisione**: vuoi che la stessa capacità sia disponibile a più agenti del tuo team (Cap. 10–12), o vuoi regalarla alla community. Il quarto è il **contesto**: le istruzioni sono diventate così lunghe che tenerle in TOOLS.md — che l'agente carica sempre — costa token a ogni sessione, anche quando non servono. Come vedremo tra poco, le skill hanno un meccanismo di caricamento progressivo che TOOLS.md non ha.

Se nessuno di questi segnali è scattato, probabilmente una skill è troppo: la tabella che segue è la bussola.

| Il problema è… | Strumento giusto |
|---|---|
| come si comporta l'agente | SOUL.md / AGENTS.md |
| dove sta un'API, due note d'uso | TOOLS.md |
| servizio con server ufficiale | MCP |
| procedura ripetibile, script, riuso | skill |

La riga di confine più sottile è quella tra TOOLS.md e skill. La regola pratica: TOOLS.md è il post-it, la skill è il manuale d'officina. Se le istruzioni stanno in dieci righe e servono spesso, post-it. Se superano la pagina, hanno bisogno di codice o servono solo in certi compiti, manuale. E rispetto a MCP: un server MCP espone *operazioni* (l'elenco grezzo di ciò che un servizio sa fare), una skill incapsula *competenza* (come usare bene quelle operazioni, con quali regole e in che ordine). Non a caso le due cose convivono: esistono skill che insegnano all'agente a usare bene un server MCP.

### Anatomia: una cartella con un SKILL.md dentro

Una skill non è un plugin compilato, non è un pacchetto npm, non è un binario: è una **directory con dentro un file `SKILL.md`** e, facoltativamente, tre sottocartelle. Il formato deriva dagli AgentSkills di Anthropic, che il Capitolo 2 ha già introdotto. Tutto qui — ed è il motivo per cui scrivere skill è alla portata di chiunque sappia scrivere Markdown.

```text
fattura-lookup/
├── SKILL.md       # manifest + istruzioni
├── scripts/       # codice eseguibile
│   └── lookup.py
├── references/    # doc caricata on-demand
│   └── api-gestionale.md
└── assets/        # template, immagini, font
```

Il `SKILL.md` ha due parti. In testa, un **frontmatter YAML** con i metadati; sotto, un **corpo Markdown** con le istruzioni che l'agente leggerà quando attiva la skill. I campi essenziali del frontmatter sono tre: `name` (l'identificatore), `description` (la frase con cui l'agente *scopre* la skill — ci torniamo, perché è il campo più importante di tutti) e `allowed-tools`, che restringe quali tool l'agente può usare mentre la skill è attiva: una skill di sola consultazione non ha motivo di poter scrivere file. A questi si aggiunge un blocco `metadata` con i requisiti dichiarati: binari necessari (`bins`) e variabili d'ambiente attese (`env`), tipicamente la chiave API che lo script userà. Dichiararli non è burocrazia: è ciò che permette a OpenClaw di avvisare l'utente *prima* che la skill fallisca in silenzio, e agli scanner di sicurezza di confrontare ciò che la skill dichiara con ciò che fa davvero.

Le tre sottocartelle hanno ruoli precisi. `scripts/` contiene il codice eseguibile — Python, Node, bash — che l'agente lancia con il tool shell; è la parte deterministica del pacchetto. `references/` contiene documentazione aggiuntiva che l'agente legge **solo quando le istruzioni lo mandano lì**: la reference completa di un'API, venti esempi di output, una guida di stile estesa. `assets/` contiene materiali passivi: template, immagini, font.

**Dove vivono le skill.** OpenClaw le cerca in tre posti, in ordine di precedenza crescente:

- **bundled** — incluse nell'installazione di OpenClaw (arrivano e si aggiornano con `openclaw update`); non si modificano;
- **globali** — in `~/.openclaw/skills/`, installate da te con `openclaw skills install <nome>`; visibili a tutti gli agenti del Gateway;
- **workspace** — in `~/.openclaw/workspace/skills/` (o `workspace-<nome>/skills/` per gli agenti aggiuntivi); le vede solo quell'agente, e a parità di nome **vincono** su globali e bundled.

La precedenza del workspace è una funzione, non un dettaglio: ti permette di prendere una skill pubblica e farne una variante personalizzata per un solo agente senza toccare l'originale — e, in fase di sviluppo, di testare la versione nuova su un agente solo mentre gli altri usano quella stabile.

**(i) Pro tip:** la `description` è il tuo SEO interno. L'agente non legge il corpo della skill quando decide se usarla: legge solo nome e description. Una description scritta come un riassunto ("helper per i documenti") non verrà mai scelta; una scritta come la domanda dell'utente ("usala quando l'utente chiede stato, importo o scadenza di una fattura") sì. Scrivi la description *dopo* aver immaginato le cinque frasi con cui chiederesti quella cosa in chat.

### Le Rules: il caso Nano Banana Pro

Dentro il corpo del SKILL.md c'è una sezione che merita un discorso a parte: **Rules**. È l'elenco dei comportamenti non negoziabili — ciò che la skill deve sempre o non deve mai fare — e la sua importanza l'ha resa evidente una skill famosa: **nano-banana-pro**, pubblicata da Peter Steinberger nel repository ufficiale delle skill, che incapsula la generazione di immagini con il modello Nano Banana Pro di Google (la famiglia Gemini). Il problema osservato sul campo: quando l'API del modello "pro" falliva o tardava, gli agenti tendevano a ripiegare in autonomia su un modello simile più economico, producendo immagini di qualità diversa da quella che l'utente aveva pagato e chiesto. La soluzione non è stata codice, ma una riga di Rules: "Only use the google/nano-banana-pro model. Never fall back to other models." La lezione vale per ogni skill che scriverai: **se un comportamento conta, va scritto esplicitamente nelle Rules** — l'agente non può rispettare un vincolo che esiste solo nella tua testa. Divieti di scrittura, gestione degli errori ("se l'API non risponde, dillo: non inventare dati"), riservatezza dei token: tutto lì, in bullet brevi e inequivocabili.

### Il modello a tre livelli di caricamento (e quanto ti costa)

Il design più intelligente delle skill è ciò che *non* viene caricato. Il meccanismo ha tre livelli, e capirlo cambia sia come scrivi le skill sia quanto spendi — è la spiegazione promessa dal pro tip del Capitolo 9.

**Livello 1 — name + description, sempre.** Di ogni skill installata, l'agente vede a ogni sessione solo nome e description: poche decine di token l'una. È il catalogo che gli permette di "sapere di sapere".

**Livello 2 — il corpo del SKILL.md, all'attivazione.** Solo quando l'agente decide che il compito richiede quella skill, carica l'intero corpo: istruzioni, Rules, comandi. È qui che la skill smette di essere una voce di catalogo e diventa competenza operativa.

**Livello 3 — `references/`, on-demand.** I file in `references/` non vengono caricati nemmeno all'attivazione: l'agente li legge solo se e quando le istruzioni del corpo lo mandano lì ("per i filtri avanzati leggi `references/api-gestionale.md`"). È il posto giusto per tutto ciò che serve raramente ma, quando serve, serve per intero.

Le conseguenze economiche sono dirette. Il livello 1 è un costo fisso: quaranta skill installate con description da 60 token sono ~2.400 token *a ogni sessione*, che tu le usi o no — moltiplicati per decine di sessioni e heartbeat al giorno, a fine mese si vedono in bolletta (la contabilità completa è nel [Capitolo 14](../PARTE-V-Sicurezza-costi/14-gestire-i-costi-senza-sorprese.md)). Il livello 2 si paga solo all'uso. Il livello 3 quasi mai. La morale per chi scrive skill: description asciutta, corpo essenziale, tutto il resto in `references/`. E la morale per chi le installa: poche e buone.

### La prima skill, passo per passo

Costruiamo l'esempio del primo tipo classico: il **wrapper di un'API** — il gestionale aziendale di cui hai già una scheda in TOOLS.md (Capitolo 9), cresciuta troppo. La promozione a skill avviene in cinque passi.

**Passo 1 — la cartella.** Lavora in una directory di appoggio, non direttamente nel workspace:

```bash
mkdir -p fattura-lookup/scripts
mkdir -p fattura-lookup/references
```

**Passo 2 — il SKILL.md minimo funzionante.**

```markdown
---
name: fattura-lookup
description: >
  Cerca fatture nel gestionale aziendale per
  numero, cliente o data. Usala quando l'utente
  chiede stato, importo o scadenza di una
  fattura, o l'elenco delle fatture non pagate.
allowed-tools: [shell]
metadata:
  requires:
    bins: [python3]
    env: [GESTIONALE_API_TOKEN]
---

# Fattura lookup

Per cercare una fattura esegui:

    python3 scripts/lookup.py --query "<termine>"

L'output è JSON: numero, cliente, importo in
euro, stato, scadenza. Riassumilo in prosa,
non incollare il JSON in chat.

## Rules

- Sola lettura: mai creare, modificare o
  cancellare fatture.
- Non mostrare il token in chat o nei log.
- Se l'API non risponde, dillo: non inventare
  dati di fattura.

Per filtri avanzati e paginazione leggi
references/api-gestionale.md (solo se la
query base non basta).
```

**Passo 3 — lo script.** La parte deterministica, in `scripts/lookup.py`. Nota che il token arriva da una variabile d'ambiente — dichiarata nel frontmatter, servita dallo store cifrato o dal credential proxy del Capitolo 4 — e non compare da nessuna parte nel codice:

```python
#!/usr/bin/env python3
# Query the ERP invoice API, print JSON to stdout.
import json
import os
import sys
import urllib.parse
import urllib.request

BASE = "https://gestionale.example.com/api/v1"
TOKEN = os.environ["GESTIONALE_API_TOKEN"]


def search(query):
    qs = urllib.parse.quote(query)
    req = urllib.request.Request(
        f"{BASE}/invoices?q={qs}",
        headers={"Authorization": f"Bearer {TOKEN}"},
    )
    with urllib.request.urlopen(req, timeout=20) as r:
        return json.load(r)


if __name__ == "__main__":
    print(json.dumps(search(sys.argv[-1])))
```

**Passo 4 — il test locale.** Copia la cartella nel workspace dell'agente che fa da cavia — `~/.openclaw/workspace/skills/fattura-lookup/` — e poi fai il test che conta davvero, quello di *discovery*: non nominare la skill, chiedi la cosa. "Qual è lo stato della fattura 2026-114?" Se l'agente attiva la skill e risponde con i dati giusti, il pacchetto funziona. Se invece arranca o risponde a memoria, il problema è quasi sempre la description: riscrivila con le parole che hai usato tu nella domanda. Con `openclaw logs --follow` in un terminale a fianco vedi in diretta l'attivazione della skill e l'esecuzione dello script.

**Passo 5 — il loop di iterazione.** Le skill si affinano come il SOUL.md: a piccoli passi osservati. Usa la skill nel lavoro vero per qualche giorno; ogni volta che l'agente la usa male, chiediti se manca una Rule (comportamento sbagliato), se la description è ambigua (attivazione mancata o a sproposito) o se il corpo è poco chiaro (esecuzione confusa). Correggi un file, riprova, ripeti. Quando non la tocchi più da una settimana, è pronta per essere promossa da workspace a globale — o pubblicata.

**(#) Debug:** lo script funziona lanciato a mano ma fallisce quando lo lancia l'agente? Tre sospetti in ordine: la variabile d'ambiente non arriva nel contesto di esecuzione (controlla il blocco `requires` e lo store delle credenziali), il sandbox non ha le dipendenze (un `requirements.txt` in `scripts/` e l'immagine va ricostruita), l'egress filtering del Capitolo 4 blocca il dominio dell'API (aggiungilo all'allowlist).

### Gli altri due esempi: trasformare contenuti, automatizzare la vita

Il secondo tipo classico è la **content transform** — ed è la soluzione del problema di Max in apertura. La skill `post-linkedin` non ha bisogno di nessuno script: è competenza pura. Il corpo del SKILL.md contiene il processo (estrai il dato più concreto dalle note, apri con quello, chiudi con una domanda) e le Rules contengono i divieti (niente emoji, mai "rivoluzionario", massimo 1.300 caratteri). Le venti migliori aperture già pubblicate e la guida estesa alla voce del brand vivono in `references/voce-del-brand.md`, caricate solo quando Max scrive davvero un post. Da quando esiste la skill, le sette istruzioni non le ripeti più: dici "fammi il post del lancio" e il risultato è uniforme — e se un giorno la voce del brand cambia, la aggiorni in un file solo.

Il terzo tipo è la **personal automation**: la skill che incapsula un rito personale. L'esempio minimo è `nota-spese` per Polly: uno script `scripts/log.py` di dieci righe che appende una riga (data, importo in euro, categoria, nota) a un CSV nel workspace, e un corpo che spiega quando usarla ("quando l'utente dice ho speso X per Y") e come rispondere (conferma in una riga, niente commenti sul merito della spesa). Da sola è una banalità; combinata con un cron mensile che legge il CSV e produce il riepilogo (il [Capitolo 18](./18-cron-job-e-automazioni-avanzate.md) è dedicato a questo), diventa un sistema di tracciamento spese costruito in mezz'ora. È il pattern più sottovalutato del capitolo: skill piccola + cron = automazione personale completa.

### Pubblicare su ClawHub: versioni, changelog, rollback

ClawHub è il registry pubblico delle skill — al primo audit indipendente di febbraio 2026 contava poco meno di tremila pacchetti, due settimane dopo aveva già superato quota diecimila, e da allora ha continuato a crescere. Pubblicare è semplice; pubblicare *bene* richiede tre abitudini.

Il registry ha una CLI dedicata, `clawhub`, separata dalla CLI di OpenClaw:

```bash
npm install -g clawhub
clawhub login
```

La login passa da GitHub, e non per comodità: dopo l'ondata di skill malevole di inizio 2026, ClawHub usa l'anzianità dell'account GitHub come barriera d'ingresso contro gli account usa-e-getta. La pubblicazione vera e propria:

```bash
clawhub skill publish ./fattura-lookup \
  --slug fattura-lookup \
  --name "Fattura lookup" \
  --version 1.0.0 \
  --changelog "Initial release"
```

Prima abitudine: il **versioning**. Le skill su ClawHub usano il semver classico (`1.0.0`, `1.1.0`, `2.0.0`) — da non confondere con il calendar versioning di OpenClaw stesso. Ogni publish crea una versione nuova e il registry conserva la storia completa: chi installa può vedere cosa è cambiato tra una versione e l'altra, ed è una proprietà di *sicurezza*, non solo di ordine — un aggiornamento che cambia comportamento senza changelog è esattamente il pattern con cui le skill malevole si sono infilate nei workspace altrui. Per gli aggiornamenti di routine c'è la scorciatoia che confronta le tue cartelle locali con il registry e pubblica solo ciò che è cambiato:

```bash
clawhub sync --bump minor \
  --changelog "Add date range filters"
```

Seconda abitudine: il **changelog onesto**, sempre, anche di una riga. Terza: saper tornare indietro. I tag del registry (come `latest`) puntano a una versione e **si possono spostare**: se la 1.2.0 rompe qualcosa, riporti `latest` alla 1.1.0 e chi installa riceve di nuovo la versione sana mentre tu sistemi con calma. Chi invece *usa* la tua skill e viene morso da un aggiornamento può sempre reinstallare la versione precedente dalla storia del registry.

Dal lato di chi installa, il comando è quello canonico che conosci dal Capitolo 9 — `openclaw skills install <nome>` — e funziona anche con un repo Git arbitrario al posto del nome, per le skill che non vuoi pubblicare su un registry pubblico.

**(!) Attenzione:** una skill pubblicata è codice che gira a casa di sconosciuti. Prima del primo publish rileggi gli script con gli occhi di chi non si fida: niente percorsi assoluti tuoi, niente telemetria non dichiarata, niente segreti hardcoded (il token nello script d'esempio arriva via env proprio per questo), dipendenze minime e dichiarate. Il maintainer distratto è il primo anello della supply chain di cui parla la prossima sezione.

### Sicurezza: dopo ClawHavoc, Clawdex e Clawvet

Il Capitolo 13 ha raccontato ClawHavoc per esteso: oltre trecento skill malevole pubblicate su ClawHub da una rete coordinata — il primo audit indipendente del registry, a febbraio 2026, ne contò 341 malevole su 2.857 totali (aggiornamento giugno 2026: con la crescita del registry oltre le 10.700 skill, le malevole individuate sono salite a circa 824, fino a ~1.184 secondo analisi successive). Qui interessa il dopo: come si crea e si installa una skill in un ecosistema dove quella campagna è già successa.

La risposta della community sono stati i due scanner promessi nei Capitoli 4 e 13: **Clawdex** e **Clawvet**. Si puntano alla cartella di una skill — prima dell'installazione, o prima del publish se la skill è tua — e la analizzano da due angoli complementari. Il primo guarda soprattutto il *codice*: script che leggono file sensibili (`~/.ssh/`, `credentials/`), chiamate di rete verso domini non dichiarati nel manifest, comandi shell offuscati. Il secondo guarda soprattutto il *testo*: istruzioni nel corpo del SKILL.md che tentano prompt injection ("ignora le regole precedenti…"), incoerenze tra ciò che la description promette e ciò che le istruzioni fanno fare, richieste di permessi senza giustificazione. Nessuno dei due è infallibile e si sovrappongono in parte: usali entrambi, e trattali come un metal detector, non come un certificato — un esito pulito abbassa il rischio, non lo azzera.

Il protocollo completo per una skill di terze parti, in ordine: leggi il SKILL.md (description, Rules, cosa chiede in `requires`), leggi gli script se ci sono (venti righe di Python si leggono in due minuti; se sono duemila righe offuscate, è già una risposta), passa la cartella a Clawdex e Clawvet, e infine **provala in sandbox** (Capitolo 4) con un agente di test prima di darla all'agente che ha accesso alla tua email. Per le tue skill vale il protocollo speculare: scansiona prima di pubblicare — trovare una vulnerabilità nella propria skill dopo che cento persone l'hanno installata è un pessimo modo di conoscere la community.

### Gli otto anti-pattern (e come rimediare)

Otto errori coprono la quasi totalità delle skill che funzionano male. In ordine di frequenza:

1. **La description vaga.** "Helper per i documenti" non verrà mai scoperta. Fix: scrivi la description con le parole delle domande reali degli utenti, casi d'uso inclusi.
2. **La skill-tuttofare.** Una skill che fa fatture, preventivi e solleciti si attiva male e si mantiene peggio. Fix: una skill, una competenza; tre skill piccole battono una grande.
3. **Il corpo enciclopedico.** Cinquanta esempi nel SKILL.md significano cinquanta esempi caricati a ogni attivazione. Fix: nel corpo l'essenziale, il resto in `references/`.
4. **Le dipendenze implicite.** Funziona sulla tua macchina perché tu hai `jq` e `pandas`; nel sandbox di chiunque altro, no. Fix: dichiara `bins` ed `env` nel frontmatter, aggiungi `requirements.txt` o `package.json` in `scripts/`.
5. **I segreti nel pacchetto.** Un token in chiaro nel SKILL.md o nello script finisce su un registry pubblico. Fix: solo variabili d'ambiente dichiarate in `requires.env`, chiavi nello store cifrato.
6. **Reinventare l'esistente.** Una skill che rifà il tool nativo di web search, o che incarta a mano un servizio con server MCP ufficiale. Fix: prima di scrivere, cerca — su ClawHub e tra gli MCP (la bussola è nel Capitolo 9).
7. **I comportamenti critici impliciti.** Il fallback silenzioso di Nano Banana Pro insegna: ciò che non è nelle Rules non esiste. Fix: ogni "mai" e ogni "sempre" che ti importa va scritto, in bullet, nella sezione Rules.
8. **Il publish senza rete di sicurezza.** Versione unica, niente changelog, mai testata in sandbox. Fix: semver, changelog a ogni release, test in sandbox prima del publish — e il tag pronto da spostare indietro se la release morde.

### Superpowers e le meta-skill: skill che generano skill

C'è un ultimo piano, quello meta. Il framework più influente in questo spazio è **Superpowers** di Jesse Vincent — veterano dell'open source, già release manager di Perl 5 — nato nell'ecosistema Claude Code e adattato dalla community a OpenClaw: lo descrive come "an agentic skills framework & software development methodology that works". L'idea è che le skill non siano solo capacità isolate ma un *metodo* componibile, e che la prima skill da dare a un agente sia quella che gli insegna a usare (e a scrivere) le altre — nella collezione è la meta-skill di authoring, accompagnata dalla regola dell'1%: se c'è anche solo una probabilità minima che una skill sia rilevante per il compito, l'agente deve consultarla.

Su ClawHub la stessa idea circola in forma più artigianale: meta-skill con nomi come skill-factory, skill-engineer e skill-father che guidano l'agente nella generazione di nuove skill a partire da una descrizione in linguaggio naturale — "osservami fare questa cosa tre volte e impacchettala". È il punto in cui il cerchio del capitolo si chiude: dopo aver scritto a mano la tua prima skill, la seconda puoi fartela proporre dall'agente stesso. Con un'avvertenza che a questo punto del libro suona familiare: una skill generata è codice generato, e il fatto che l'abbia scritta *il tuo* agente non la esenta da niente — code review, scanner e sandbox si applicano esattamente come a una skill scaricata da internet. Un agente che si scrive i propri strumenti è l'immagine più potente di OpenClaw; un agente che si scrive i propri strumenti *senza che nessuno li legga* è l'inizio di una war story del Capitolo 13.

**Prompt pronto:**
> "Voglio creare una skill custom che [descrivi cosa deve fare, es. "estrae i prezzi dei voli da Skyscanner per una rotta e date"]. Aiutami a: (1) scrivere il SKILL.md con frontmatter completo (`name`, `description` con keyword chiare, `allowed-tools`), (2) scegliere se serve uno script in `scripts/` e in quale linguaggio, (3) testare la skill in sandbox prima di abilitarla, (4) decidere se pubblicarla su ClawHub o tenerla privata."

**Prompt pronto:**
> "Ho scaricato la skill [nome] da ClawHub ma non l'ho ancora installata. Fai una revisione di sicurezza della cartella: (1) confronta la description con ciò che le istruzioni fanno fare davvero, (2) elenca ogni lettura di file e ogni chiamata di rete negli script, segnalando quelle non dichiarate nel frontmatter, (3) cerca tentativi di prompt injection nel testo, (4) dimmi se la proveresti in sandbox o la scarteresti, e perché."

## Errori comuni e come risolverli

**Sintomo:** la skill custom non viene "scoperta"
dall'agente.
Causa: description nel SKILL.md poco specifica
(parole chiave assenti).
Fix: riscrivere la description con parole chiave
concrete legate ai casi d'uso, usando le parole
delle domande reali.

**Sintomo:** la skill funziona localmente ma
fallisce in container.
Causa: dipendenze non installate nel sandbox.
Fix: aggiungere `requirements.txt` o
`package.json` in `scripts/`, dichiarare `bins`
ed `env` nel frontmatter, ricostruire l'immagine
sandbox.

**Sintomo:** skill da ClawHub non si installa:
"signature verification failed".
Causa: skill non firmata o checksum che non
corrisponde.
Fix: NON forzare l'installazione; segnalare al
maintainer o cercare un'alternativa firmata.

**Sintomo:** skill troppo "chiacchierona" nelle
risposte.
Causa: body di SKILL.md verboso, molti esempi
caricati a ogni attivazione.
Fix: compattare il body, spostare gli esempi
lunghi in `references/` (caricati on-demand).

**Sintomo:** la skill si attiva ma l'agente fa
una cosa vietata (es. ripiega su un altro modello
o servizio).
Causa: comportamento critico assente dalla
sezione Rules.
Fix: scrivere il vincolo in modo esplicito nelle
Rules ("mai…", "sempre…"), come nel caso
Nano Banana Pro.

**Sintomo:** due agenti rispondono in modo diverso
con la "stessa" skill.
Causa: una copia di workspace ha la precedenza
sulla versione globale in uno dei due workspace.
Fix: controllare `skills/` nei workspace coinvolti
e rimuovere o allineare la copia locale.

**Sintomo:** `clawhub skill publish` viene
rifiutato.
Causa: account GitHub troppo recente per il gate
anti-abuso, slug già occupato o versione non in
formato semver.
Fix: verificare login e anzianità dell'account,
scegliere uno slug libero, usare una versione
`X.Y.Z`.

## Checklist di fine capitolo

- [ ] Almeno una skill custom funzionante in locale
- [ ] SKILL.md con frontmatter completo (name + description con keyword)
- [ ] Code review fatta sull'eventuale codice in `scripts/`
- [ ] Skill testata in sandbox prima di abilitarla in produzione
- [ ] Ho deciso se pubblicarla su ClawHub o tenerla privata
- [ ] Comportamenti critici scritti nella sezione Rules
- [ ] Esempi e doc lunghi spostati in `references/`, non nel body
- [ ] Dipendenze dichiarate (`bins`, `env`) e nessun segreto nel pacchetto
- [ ] Skill di terze parti passate a Clawdex/Clawvet prima dell'installazione
- [ ] Se pubblico: versione semver e changelog a ogni release

## Link e risorse utili

- [Documentazione ufficiale](https://docs.openclaw.ai) — reference completo del formato SKILL.md
- [Skills — reference ufficiale](https://docs.openclaw.ai/tools/skills) — formato, frontmatter, posizioni e precedenza
- [Creating skills — guida ufficiale](https://docs.openclaw.ai/tools/creating-skills) — il loop di sviluppo consigliato dal progetto
- [ClawHub (skill registry)](https://clawhub.com) — registry ufficiale per cercare e pubblicare skill
- [ClawHub CLI](https://github.com/openclaw/clawhub) — repo del registry, comandi `publish` e `sync`
- [Superpowers](https://github.com/obra/superpowers) — il framework di skill componibili di Jesse Vincent
- [OpenClaw vs NemoClaw vs NanoClaw Security](https://dev.to/_46ea277e677b888e0cd13/openclaw-vs-nemoclaw-vs-nanoclaw-ai-agent-platform-security-comparison-i3k) — rischi delle skill di terze parti e come mitigarli

Per l'elenco completo delle fonti del libro, vedi [Appendice E](../Appendici/E-risorse-e-link-utili.md).

---

[← Capitolo 16](../PARTE-VI-Manutenzione/16-ottimizzare-la-qualita-delle-risposte.md)  ·  [Indice](../README.md)  ·  [Capitolo 18 →](./18-cron-job-e-automazioni-avanzate.md)
