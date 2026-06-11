# Capitolo 4 — Preparare un ambiente sicuro: Docker, sandbox e wrapper [★★]

## Cosa imparerai

- Perché l'isolamento dell'ambiente non è un optional ma il primo passo concreto
- I sei livelli di isolamento, dal bare metal al syscall sandboxing
- Quale livello mitiga quale minaccia, in una tabella che usi come bussola
- Come costruire e firmare l'immagine sandbox con pinning per digest
- Come usare Docker Sandboxes (microVM) introdotti con Docker Desktop 4.60+
- Come scrivere un'allowlist di rete realistica con Squid o iptables
- Come tenere le API key fuori dal container con il credential proxy
- Le specificità di macOS, Windows e Linux che fanno perdere mezz'ora se non le sai
- Tre smoke test che provano davvero l'isolamento (e non solo che la rete è rotta)
- Quanto costa, in RAM, CPU e bolletta, ognuna di queste protezioni
- Cosa fare il giorno che sospetti che il sandbox sia stato compromesso

## Prerequisiti

Aver scelto dove installare OpenClaw nel [Capitolo 3](./03-scegliere-dove-installare-openclaw.md). Avere Docker Desktop ≥ 4.60 (macOS, Windows) oppure Docker Engine ≥ 27 (Linux). Sulla RAM, una precisazione: per il **Livello 1** (container per-session) bastano i 4 GB minimi del Capitolo 3; gli **8 GB disponibili per la VM Docker** servono solo se punti ai livelli con microVM o gVisor (Livello 3+). Conoscenza base del terminale: navigare fra cartelle, leggere un file YAML, seguire un `docker run` senza panico.

Verifica veloce dei prerequisiti, da incollare in un terminale:

```bash
docker --version       # Engine >= 27
# Docker Desktop: check version >= 4.60
# in Settings -> About (not in --version)
docker info | grep -i microvm
uname -m                    # arm64, x86_64
free -m | awk '/Mem:/{print $2}'
```

## Contenuto principale

### TL;DR — setup minimo per stasera

Se hai venti minuti e vuoi partire stasera al Livello 1, questi sono i cinque comandi essenziali. Il resto del capitolo è il *perché*; questi cinque comandi sono il *come*.

**(!) Attenzione:** questo capitolo si *legge* prima dell'installazione ma si *esegue* dopo: i comandi 3 e 4 presuppongono OpenClaw già installato (è il [Capitolo 5](./05-installazione-step-by-step.md) — senza, `~/.openclaw/config.yaml` non esiste e `openclaw` non è nel PATH). In più, il TL;DR usa due file creati nelle sezioni successive: `Dockerfile.sandbox` (sezione "Costruire l'immagine") e `verify-sandbox.sh` (sezione "Verificare l'isolamento"). Leggilo come anteprima del percorso; torna qui a installazione fatta, con i due file pronti.

```bash
# 1. build the hardened sandbox image
docker build -f Dockerfile.sandbox \
  -t openclaw-sandbox:bookworm-slim .

# 2. create an isolated egress network
docker network create openclaw-egress

# 3. enable the sandbox in OpenClaw config
sed -i.bak \
  's/sandbox: off/sandbox: { mode: "all" }/' \
  ~/.openclaw/config.yaml

# 4. restart and run the smoke tests
openclaw gateway restart && \
  bash verify-sandbox.sh

# 5. schedule a weekly rebuild (Fri 07:00);
#    the script wraps the build command of
#    step 1 with --no-cache (see the section
#    "Manutenzione del sandbox nel tempo")
crontab -l | { cat; echo \
  '0 7 * * 5 bash ~/.openclaw/rebuild.sh'; \
} | crontab -
```

Ora prendi un caffè e leggi il resto: ti spiega cosa è successo davvero in quei cinque comandi e perché ne mancano almeno tre per dormire tranquillo.

### Perché il sandboxing viene prima di tutto

OpenClaw, per com'è fatto, ha le chiavi di casa: filesystem, rete, comandi shell, browser, eventuali credenziali API montate nelle variabili d'ambiente. È quello che lo rende utile, ed è anche quello che lo rende pericoloso. La frase di Simon Willison — "non sono abbastanza coraggioso per farlo girare direttamente sul mio Mac" — è circolata nelle prime settimane proprio perché coglieva un sentimento comune: un agente autonomo, su una macchina personale e senza isolamento, è una bomba a orologeria silenziosa.

Il caso che ha chiuso la discussione nella community è la **CVE-2026-25253** di gennaio 2026: un'istanza non patchata, raggiungibile via WebSocket sulla porta `18789`, poteva essere compromessa in meno di 90 secondi da un attaccante che fosse riuscito a fare in modo che l'agente leggesse una singola pagina ostile. Da quel momento la documentazione ufficiale ha smesso di chiamare il sandbox "consigliato" e ha iniziato a chiamarlo "predefinito".

La regola operativa, che ripeteremo lungo tutto il capitolo, è semplice: **un container non è automaticamente un sandbox**. Lo diventa solo dopo aver chiuso almeno quattro porte: filesystem, rete, capability, secrets.

### I sei livelli di isolamento

Pensa all'isolamento come a una scala. Ogni gradino aggiunge protezione e qualche grammo di complessità. Il punto non è "salire più in alto possibile" ma "salire fino al gradino che corrisponde al tuo modello di rischio".

```text
        ┌──────────────────────────────────┐
  L5    │  NemoClaw / OpenShell (LSM)      │
        │  policy engine out-of-process    │
        ├──────────────────────────────────┤
  L4    │  gVisor / MAGI (syscall)         │
        │  user-space kernel "Sentry"      │
        ├──────────────────────────────────┤
  L3    │  Docker Sandboxes (microVM)      │
        │  kernel guest dedicato           │
        ├──────────────────────────────────┤
  L2    │  Gateway containerizzato         │
        │  l'intero OpenClaw in compose    │
        ├──────────────────────────────────┤
  L1    │  Docker per-session (consigliato)│
        │  ogni tool in container effimero │
        ├──────────────────────────────────┤
  L0    │  Bare metal — nessun isolamento  │
        │  solo su dispositivo dedicato    │
        └──────────────────────────────────┘
              host kernel + hardware
```

**Livello 0 — Installazione diretta (bare metal).** L'agente gira sullo stesso OS dell'utente. Massima flessibilità, massimo rischio. Accettabile solo su un dispositivo dedicato — Mac Mini, vecchio laptop riformattato — che non contiene dati personali né credenziali di lavoro.

**Livello 1 — Docker sandbox per-session.** Il Gateway gira sull'host, ma ogni tool e ogni skill dell'agente vengono eseguiti in un container Docker isolato e a vita breve. L'agente legge e scrive solo nelle directory montate esplicitamente. È il miglior compromesso tra usabilità e sicurezza, ed è il punto di partenza consigliato dal libro.

**Livello 2 — Gateway containerizzato completo.** L'intero OpenClaw, Gateway compreso, gira dentro Docker Compose. Nessuna installazione sull'host. È la scelta naturale per VPS e per chi vuole un ambiente "usa e getta" che si ricostruisce da zero in trenta secondi.

**Livello 3 — Docker Sandboxes (microVM).** Da Docker Desktop 4.60+ in poi, ogni sandbox può girare dentro una microVM Firecracker o equivalente, con un kernel Linux dedicato. Boot time intorno ai 125 ms, overhead dell'hypervisor sotto i 5 MiB per VM (il footprint runtime complessivo resta sui ~250 MB: vedi la tabella dei costi più avanti). È isolamento *hardware-grade*: anche un container compromesso non vede l'host.

**Livello 4 — gVisor (runsc) e MAGI.** Runtime container che intercetta le syscall in user space (il "Sentry") e le re-implementa, dimezzando la superficie d'attacco anche se l'agente sfrutta una vulnerabilità del kernel. **MAGI** (Multi-Agent gVisor Isolation), pubblicato da Google ad aprile 2026, aggiunge isolamento per-agente all'interno dello stesso processo Sentry: ideale quando un team di agenti gira sulla stessa macchina e non vuoi che un agente compromesso veda gli altri.

**Livello 5 — NemoClaw / OpenShell.** Sandboxing a livello kernel via Linux Security Modules, policy YAML deny-by-default, policy engine *out-of-process* (l'agente non può disattivarlo nemmeno se viene compromesso). È il livello enterprise: documentazione granulare, audit trail, partnership Cisco/CrowdStrike/Microsoft.

C'è poi un livello "0.5" non numerato — **NanoClaw** — che vive fuori da questa scala perché non è un livello di OpenClaw ma una *riscrittura minimalista*: ~700 righe di TypeScript, container per-chat, permission gate obbligatori, audit log integrato. È un Livello 1 con una superficie di codice talmente piccola che puoi leggertela in un pomeriggio.

### Glossario rapido (per non interrompere la lettura)

I termini che ricorrono nelle prossime pagine, in una riga ciascuno:

- **Capability (Linux):** permesso granulare del kernel (es. `CAP_NET_ADMIN`); `--cap-drop=ALL` li rimuove tutti.
- **Seccomp:** filtro che decide quali syscall un processo può chiamare; profilo JSON.
- **AppArmor / SELinux:** Linux Security Modules che applicano policy di accesso a livello kernel.
- **KVM:** ipervisore Linux su cui si appoggiano Firecracker e Docker Sandboxes.
- **MicroVM:** VM minima (kernel + initrd, niente userland completo) che boota in millisecondi.
- **Sentry (gVisor):** processo user-space che intercetta e re-implementa le syscall del container.
- **CapEff:** il bitmask delle capability *effective* di un processo, leggibile in `/proc/self/status`.

### Mappa minacce → livello minimo

Usa questa tabella come bussola: per ogni minaccia che ti preoccupa, sali fino al livello che la mitiga davvero. Tutto quello che è sotto è insufficiente.

| Minaccia | Livello minimo |
|---|---|
| Cron scritto male che cancella file utente | L1 |
| Skill di terze parti che esfiltra dati | L1 + egress filtering |
| Prompt injection che esegue comandi shell | L1 + cap-drop |
| API key letta dall'agente e spedita fuori | L1 + credential proxy |
| Lateral movement nella LAN di casa | L1 + rete Docker isolata |
| Container escape via bug del runtime | L3 (microVM) o L4 (gVisor) |
| Kernel exploit (CVE del kernel host) | L3 o L4 |
| Agente compromesso che vede gli altri agenti | L4 (MAGI) |
| Agente che disattiva la propria policy | L5 (out-of-process) |
| Manomissione dell'immagine base | pinning + `cosign verify` |

### Docker sandbox nativo di OpenClaw — setup pratico

OpenClaw supporta il sandboxing Docker out-of-the-box con tre modalità, e la configurazione vive in `~/.openclaw/config.yaml`.

**Agent Sandbox (per-session, Livello 1):** il Gateway resta sull'host, i tool girano in container.

```yaml
# ~/.openclaw/config.yaml
agents:
  defaults:
    sandbox:
      mode: "all"          # "all" | "non-main" | "off"
      scope: "session"     # "session" | "agent"
      image: "openclaw-sandbox:bookworm-slim"
      workspaceAccess: "ro"  # "none" | "ro" | "rw"
      network:
        egress: "allowlist"
        allow:
          - "api.anthropic.com"
          - "api.openai.com"
          - "api.brave.com"
```

`mode: "non-main"` è il punto di ingresso più morbido: il main agent gira senza container, ma ogni sub-agent che esegue codice o naviga il web è isolato. Quando ti senti pronto, passa a `mode: "all"`.

**Containerized Gateway (Livello 2):** l'intero OpenClaw in Docker Compose. Lo script ufficiale fa il grosso del lavoro:

```bash
# clone the repo and bootstrap
git clone https://github.com/openclaw/openclaw.git
cd openclaw
./scripts/docker/setup.sh
```

Il setup monta come volume un solo albero: `~/.openclaw/` — lo stato (config, credenziali, log) e, al suo interno, `~/.openclaw/workspace/` con i file dell'agente. Per attivare anche il sandbox per-session *dentro* il Gateway containerizzato:

```bash
OPENCLAW_SANDBOX=1 ./scripts/docker/setup.sh
```

**Docker Sandboxes (Livello 3):** integrazione ufficiale Docker, con isolamento microVM e proxy delle credenziali.

```bash
docker sandbox create --name openclaw \
  --runtime microvm \
  --memory 4g \
  --network openclaw-egress
```

Le API key non entrano nel container: vengono iniettate via *credential proxy* (vedi sezione dedicata più avanti). La rete `openclaw-egress` è una rete Docker custom con allowlist; la creiamo nella sezione successiva.

### Costruire l'immagine — pinning per digest e firma

L'immagine di default è essenziale per definizione: Debian 12 *slim*, Node.js 22, qualche utility minimale, niente compilatori, niente shell interattive comode (no `vim`, no `htop`). Se serve di più, lo aggiungi *consapevolmente*.

Tre regole non negoziabili nel Dockerfile: **utente non-root**, **base image pinnata per digest** (non solo per tag), **firma verificata** prima del build.

```dockerfile
# Dockerfile.sandbox
# Pin the base image by digest, not just by tag.
# Tags can be re-pushed; digests can't.
FROM debian:bookworm-slim@sha256:155280b00ee0133250\
f7159d6ae9d62efb6b25b5a0b9b4c0b8c4cf2ffb6e0d87

# Install only what is strictly needed
RUN apt-get update && apt-get install -y \
      --no-install-recommends \
      ca-certificates curl git \
      python3 python3-pip nodejs npm \
    && rm -rf /var/lib/apt/lists/*

# Create a non-root user with a stable uid
RUN useradd -m -u 1000 -s /bin/bash claw

USER claw
WORKDIR /home/claw/work
ENTRYPOINT ["/usr/bin/timeout", "300"]
CMD ["bash"]
```

Se il publisher dell'immagine base firma con `cosign` (Sigstore), verifica la firma prima di farla entrare nella tua build. L'esempio che segue è **generico**: identity e issuer corretti li trovi nella documentazione di firma del publisher (non tutte le immagini ufficiali, Debian inclusa, pubblicano firme cosign — in quel caso il pinning per digest resta la tua difesa principale):

```bash
# generic example — adapt identity/issuer
# to the publisher's signing docs
cosign verify \
  --certificate-identity \
    '<signer-identity>' \
  --certificate-oidc-issuer \
    '<oidc-issuer-url>' \
  <image>:<tag>
```

Build e tag locali:

```bash
docker build -f Dockerfile.sandbox \
  -t openclaw-sandbox:bookworm-slim .
```

Verifica veloce che giri *davvero* come `uid 1000` e senza capability:

```bash
docker run --rm \
  --user 1000:1000 \
  --cap-drop=ALL \
  --read-only \
  --tmpfs /tmp:size=64m \
  openclaw-sandbox:bookworm-slim \
  bash -c 'id; cat /proc/self/status | grep CapEff'
```

Se vedi `uid=1000(claw)` e `CapEff: 0000000000000000` (cioè zero capability *effective*), sei a posto.

**(i) Pro tip:** versiona il `Dockerfile.sandbox` nello stesso repo dei tuoi prompt e dei tuoi cron. Quando un giorno l'agente si comporterà in modo strano, vorrai poter tornare all'immagine di sei mesi fa con un solo `git checkout`.

### Configurare Docker Sandboxes (Docker Desktop 4.60+)

Da Docker Desktop 4.60 in poi, i sandbox possono girare dentro microVM dedicate. La differenza pratica rispetto a un container "normale" è che il kernel è separato da quello dell'host: una vulnerabilità del kernel ospite non si propaga.

```bash
# enable microvm runtime once
docker sandbox configure \
  --runtime microvm --boot 2gb

# create the sandbox used by openclaw
docker sandbox create \
  --name openclaw \
  --image openclaw-sandbox:bookworm-slim \
  --memory 4g --cpu 2 \
  --network openclaw-egress \
  --read-only-root \
  --tmpfs /tmp:size=128m \
  --tmpfs /run:size=8m
```

Puntare OpenClaw a usare il sandbox via config:

```yaml
agents:
  defaults:
    sandbox:
      driver: "docker-sandboxes"
      name: "openclaw"
```

**Note specifiche per OS.** I dettagli che fanno perdere mezz'ora se non li sai:

- **macOS (Apple Silicon).** In *Settings → General* attiva "Use Virtualization framework" e "Use Rosetta for x86/amd64 emulation": la prima abilita il microVM, la seconda fa girare immagini `linux/amd64` su M1–M4 senza riscrivere niente. Il file di config Docker vive in `~/Library/Group Containers/group.com.docker/settings-store.json`.
- **Windows.** Docker Desktop su Windows si appoggia a WSL2; il microVM funziona ma richiede *nested virtualization* abilitata nel BIOS. Su Hyper-V puro (Server) le funzioni AI sono limitate. Verifica con `wsl --status` e `systeminfo | findstr Hypervisor`.
- **Linux.** Considera **rootless Docker** (`dockerd-rootless-setuptool.sh install`): il demone Docker stesso gira come tuo utente, e una *escape* dal container non scala a root sull'host. È la singola mossa che, su Linux, ti dà più sicurezza per zero euro.

### Egress filtering: la rete è il vettore principale

Statisticamente, quando un agente fa danni reali è quasi sempre via rete: scarica una skill malevola, esfiltra dati verso un host non previsto, manda email a contatti sbagliati. Bloccare l'egress *per default* ed esporre solo una allowlist è la singola misura con il miglior rapporto fra protezione ottenuta e fatica spesa.

Approccio 1 — **rete Docker isolata + Squid come proxy uscente**:

```yaml
# docker-compose.egress.yaml
services:
  squid:
    image: ubuntu/squid:latest
    networks: [openclaw-egress]
    volumes:
      - ./squid.conf:/etc/squid/squid.conf:ro
    ports: ["3128:3128"]

networks:
  openclaw-egress:
    driver: bridge
    internal: false   # squid needs the outside
```

Il file `squid.conf` con un'allowlist minimale per OpenClaw:

```text
# squid.conf — minimal allowlist
acl allowed_domains dstdomain "/etc/squid/allow.txt"
http_access allow allowed_domains
http_access deny all
http_port 3128
```

E `allow.txt` con i domini realmente necessari:

```text
.anthropic.com
.openai.com
.brave.com
.exa.ai
.github.com
.openclaw.ai
api.telegram.org
```

Il container OpenClaw imposta `HTTP_PROXY` e `HTTPS_PROXY` su `http://squid:3128` e perde la capacità di parlare con qualunque altro dominio.

Approccio 2 — **iptables sull'host** quando vuoi una difesa a livello kernel anche sopra Docker. Una premessa: i bridge Docker hanno nomi auto-generati (`br-<id>`); per usare un nome stabile come `br-openclaw` devi fissarlo alla creazione della rete, oppure ricavare quello reale:

```bash
# option A: fix the bridge name at creation
docker network create openclaw-egress \
  -o com.docker.network.bridge.name=br-openclaw

# option B: derive the auto-generated name
NET_ID=$(docker network inspect \
  openclaw-egress -f '{{.Id}}')
BRIDGE="br-${NET_ID:0:12}"

# default deny on the openclaw-egress bridge
sudo iptables -I FORWARD -i br-openclaw -j DROP
sudo iptables -I FORWARD -i br-openclaw \
  -d $(dig +short api.anthropic.com \
       | head -1) -j ACCEPT
```

Questa seconda strada è meno elegante (gli IP cambiano), ma è quella che ti salva quando il proxy stesso viene compromesso.

**(!) Attenzione:** quando aggiungi un dominio alla allowlist, chiediti sempre *quale risorsa specifica serve*. "GitHub" in allowlist significa anche "qualunque repo malevolo su GitHub". Se possibile, restringi a path o a sottodomini (`raw.githubusercontent.com` solo per i repo che ti aspetti).

### Credential proxy: niente API key dentro il container

L'errore classico è mettere `ANTHROPIC_API_KEY=sk-…` come variabile d'ambiente del container. È comodo, è veloce, ed è esattamente il modo in cui le API key finiscono in pastebin pubblici quando l'agente decide, in piena buona fede, di "stampare l'environment per debug".

OpenClaw ≥ 2026.4 supporta un *credential proxy* che vive sull'host e firma le richieste *al posto dell'agente*. Il container vede solo un endpoint locale — `http://credstore.local:7777` — e fa richieste come se l'API fosse pubblica. La key non entra mai nello spazio di indirizzamento dell'agente.

```yaml
# ~/.openclaw/config.yaml — credential proxy
credentials:
  mode: "proxy"
  endpoint: "http://credstore.local:7777"
  providers:
    anthropic:
      keyEnv: "ANTHROPIC_API_KEY"
    openai:
      keyEnv: "OPENAI_API_KEY"
```

Verifica che dentro il container non ci sia traccia delle key:

```bash
docker exec openclaw env | \
  grep -iE 'key|secret|token'
# expected: empty output
```

Se vedi qualcosa, fermati, ruota le key, rimettile *solo* sull'host, riavvia.

### NanoClaw — quando la semplicità è priorità

NanoClaw vale la pena di essere conosciuto anche se non lo userai. È un esercizio di stile: ~700 righe di TypeScript, una sola dipendenza significativa (Docker), nessun runtime nascosto. Ogni chat gira nel proprio container, le permission sono *richieste* per ogni azione (non opzionali), l'audit log è on per default e non si può spegnere.

Il limite è dichiarato: solo Claude come modello, niente multi-model routing, ecosistema skill ridotto a quelle ufficiali. È perfetto per: team piccoli con requisiti di compliance, persone che vogliono capire ogni riga di codice prima di farla girare a casa, ricercatori di sicurezza che usano OpenClaw come bersaglio e NanoClaw come *control group*.

### NemoClaw / OpenShell — il livello enterprise

NemoClaw si installa sopra OpenClaw con un singolo comando e introduce **OpenShell**, un sandbox a livello kernel basato su Linux Security Modules (AppArmor/SELinux), con policy YAML scrivibili a mano:

```yaml
# openshell-policy.yaml — example
default: deny
filesystem:
  read:  ["/home/claw/work/**"]
  write: ["/home/claw/work/output/**"]
network:
  egress:
    - "api.anthropic.com:443"
    - "api.openai.com:443"
process:
  exec: ["python3", "node", "git"]
```

Il policy engine gira *out-of-process*: anche un agente compromesso non può modificare il file di policy né disattivare il modulo. In più, il **privacy router** instrada le query "facili" verso il cloud e le query con dati sensibili verso un Nemotron locale, riducendo l'esposizione di dati personali ai provider esterni.

Stato a maggio 2026: alpha avanzata, partnership annunciate con Cisco, CrowdStrike, Google e Microsoft Security. Da mettere in produzione quando avrai dati di business reali da proteggere, non prima.

### IronClaw — la terza via (Rust)

IronClaw è una riscrittura da zero in Rust: memory safety a compile time, zero telemetria, zero dipendenze non strettamente necessarie. È pensato per chi lavora con dati altamente confidenziali — ricerca medica, legale, intelligence — e accetta in cambio un ecosistema più giovane e una community di un ordine di grandezza più piccola di OpenClaw.

Se la tua azienda non ti permette di mandare dati ad Anthropic o OpenAI, IronClaw + Nemotron locale è oggi la combinazione realisticamente percorribile.

### gVisor (runsc) e MAGI: isolamento a livello di syscall

gVisor non sostituisce Docker: lo *avvolge*. Il binario `runsc` si registra come runtime alternativo e intercetta tutte le syscall del container in un processo user-space chiamato Sentry, che le re-implementa parzialmente prima di passarle al kernel. Il risultato: la superficie d'attacco contro il kernel host crolla.

Configurazione tipica su Linux:

```bash
# install runsc
curl -fsSL https://gvisor.dev/install.sh \
  | sudo bash

# register the runtime in /etc/docker/daemon.json
sudo tee /etc/docker/daemon.json <<'EOF'
{
  "runtimes": {
    "runsc": { "path": "/usr/local/bin/runsc" }
  }
}
EOF
sudo systemctl restart docker
```

E poi, per un singolo container:

```bash
docker run --rm --runtime=runsc \
  openclaw-sandbox:bookworm-slim \
  python3 -c 'print("hello from gvisor")'
```

L'overhead è di circa il 10–30% sui workload I/O-pesanti (lettura/scrittura file, rete intensiva) e quasi nullo sui carichi compute-bound. Qui serve onestà: OpenClaw è un carico prevalentemente **I/O-bound** — legge file, scrive log, parla in rete con i provider — quindi quell'overhead lo paghi davvero. Su un agente personale resta quasi impercettibile (i colli di bottiglia veri sono la latenza del modello e della rete), ma su workload intensi di filesystem — build npm, sync di cartelle — si sente: vedi anche la riga `runsc` nella tabella "Errori comuni". **MAGI** estende questo modello: un singolo Sentry ospita più agenti, ognuno con la propria *security context*, e impedisce a un agente compromesso di vedere lo stato degli altri. È particolarmente utile in setup multi-agente (parte IV).

### Tabella decisionale — quale livello scegliere

| Profilo | Livello | Perché |
|---|---|---|
| Hobbyist su Mac Mini | 1 | Compromesso, facile setup |
| Developer su VPS | 2 | Usa-e-getta, niente sull'host |
| Dati personali sensibili | 3 | microVM, kernel separato |
| Multi-agente serio | 4 (gVisor/MAGI) | Isolamento syscall |
| Business / startup | 5 (NemoClaw) | Policy granulari |
| Enterprise / compliance | 4 + 5 | Difesa a strati |
| Privacy assoluta, no cloud | IronClaw | Rust, zero telemetria |

### Hardening aggiuntivo per qualsiasi livello

Indipendentemente dal livello scelto, queste sei mosse vanno fatte sempre:

1. Container come utente non-root (`uid 1000`).
2. `--cap-drop=ALL` e poi, eventualmente, `--cap-add` solo le capability strettamente necessarie.
3. `--read-only` sul filesystem del container, con `tmpfs` per `/tmp` e `/run`.
4. Profilo seccomp personalizzato (parti dal default Docker e *toglie* syscall, non aggiunge).
5. Disabilitare mDNS per prevenire lateral movement: si fa **sull'host** (`/etc/avahi/avahi-daemon.conf` → `disable-publishing=yes`); le immagini slim del container non hanno Avahi a bordo.
6. `--pids-limit=512` e `--memory=2g` per evitare che un agente impazzito esaurisca le risorse dell'host.

Il file `compose.override.yaml` finale, per chi usa Docker Compose, somiglia a questo:

```yaml
services:
  agent:
    user: "1000:1000"
    read_only: true
    cap_drop: ["ALL"]
    pids_limit: 512
    mem_limit: 2g
    tmpfs:
      - /tmp:size=128m
      - /run:size=8m
    security_opt:
      - "no-new-privileges:true"
      - "seccomp=./seccomp-openclaw.json"
    networks: [openclaw-egress]
```

**Prima e dopo, nello stesso comando.** Per capire cosa cambia davvero, confronta un `docker run` ingenuo con la versione hardened:

```bash
# BEFORE — naive, do NOT copy
docker run -d --name openclaw \
  -e ANTHROPIC_API_KEY=$KEY \
  -v /home:/home \
  --network host \
  openclaw-sandbox

# AFTER — hardened
docker run -d --name openclaw \
  --user 1000:1000 \
  --cap-drop=ALL \
  --read-only \
  --tmpfs /tmp:size=128m \
  --pids-limit=512 \
  --memory=2g \
  --security-opt=no-new-privileges:true \
  --network openclaw-egress \
  -v ~/.openclaw/workspace:/home/claw/work:rw \
  openclaw-sandbox:bookworm-slim
```

Le differenze in chiaro: niente API key in env (arrivano via credential proxy), niente accesso a `/home`, niente `--network host`, niente capability extra, niente filesystem scrivibile, limiti di processi e memoria, immagine *pinnata* per tag (e per digest nel Dockerfile). Una nota sul mount del workspace: qui è `rw` perché l'esempio mostra un agente già operativo, ma il livello effettivo lo decide `workspaceAccess` nella config — parti da `ro` come consigliato sopra e passa a `rw` solo quando sai perché ti serve.

### Verificare l'isolamento: tre smoke test

Un sandbox è utile quanto la tua fiducia che funzioni. Ogni volta che lo riconfiguri, esegui questi tre test prima di tornare a usare l'agente sul serio.

**Test 1 — il container non può scrivere fuori dal workspace:**

```bash
docker exec openclaw \
  bash -c 'touch /etc/should_not_exist \
    && echo BAD || echo OK'
# expected: OK
```

**Test 2 — l'allowlist di rete fa il suo lavoro in entrambe le direzioni.** Una sola riga non basta: una rete spenta restituirebbe lo stesso `000` di un blocco funzionante. Verifica *insieme* che l'host fuori allowlist sia bloccato e che l'host in allowlist risponda.

```bash
# 2a. blocked domain — must NOT connect
docker exec openclaw \
  curl -sS -o /dev/null -w 'blocked=%{http_code}\n' \
    --max-time 3 https://example.com

# 2b. allowed domain — must connect
docker exec openclaw \
  curl -sS -o /dev/null -w 'allowed=%{http_code}\n' \
    --max-time 5 https://api.anthropic.com
# expected: blocked=000 or 403, allowed=2xx or 401
```

`401` su `api.anthropic.com` è un *successo*: significa che la connessione TLS è andata a buon fine e il server ha risposto "manca l'autenticazione". È esattamente quello che vogliamo — la rete funziona, l'allowlist passa, le credenziali (giustamente) no.

**Test 3 — le API key non sono presenti nell'environment dell'agente:**

```bash
docker exec openclaw env | \
  grep -iE 'sk-|key|secret|token' \
  && echo LEAK || echo OK
# expected: OK
```

Salva i tre test in uno script `verify-sandbox.sh` e lancialo dopo ogni `openclaw update`.

**Prompt pronto — generare la verifica con OpenClaw stesso:**

> "Genera uno script bash chiamato `verify-sandbox.sh` che esegua tre controlli sul mio container OpenClaw: (1) verifica che il container giri come uid 1000 e con `CapEff` a zero; (2) verifica che `curl https://example.com` venga bloccato dall'egress filtering *e* che `curl https://api.anthropic.com` arrivi a un 2xx/401; (3) verifica che nelle variabili d'ambiente non compaiano stringhe simili ad API key (`sk-…`, `secret`, `token`). Lo script deve uscire con codice 0 se tutto è ok e 1 al primo errore, e stampare un riepilogo leggibile a colori."

### Costi nascosti: memoria, CPU e bolletta

Tenere conto dei costi del sandbox evita la frustrazione del "perché va così piano". Numeri orientativi misurati su un Mac Mini M4 base (16 GB RAM) con OpenClaw 2026.4 e una sessione tipica di lavoro:

| Setup | RAM extra | CPU | Boot |
|---|---|---|---|
| Bare metal | 0 | 0 | 0 ms |
| Docker per-session | ~120 MB | 1–3% | ~600 ms |
| Gateway containerizzato | ~350 MB | 2–4% | ~3 s |
| Docker Sandboxes (microVM) | ~250 MB | 3–6% | ~125 ms |
| gVisor (runsc) | ~80 MB | 10–30% I/O | ~400 ms |
| NemoClaw / OpenShell | ~500 MB | 5–8% | ~5 s |

Sul Mac Mini base 16 GB la combinazione "Gateway containerizzato + microVM" sta comoda. Se vai su un Raspberry Pi 5 (8 GB), tieniti al solo Livello 1 e disattiva il sandbox sul main agent.

**Bolletta.** Un Mac Mini M4 con OpenClaw acceso 24/7 e Gateway containerizzato consuma in media 8–10 W in più rispetto a idle (misurato a parete con un Shelly Plug). In Italia, a tariffa media 0,30 €/kWh, sono circa **2,00–2,50 € al mese**. Su un VPS, il costo del livello "microVM" si traduce in genere in uno scatto di taglia (1 vCPU → 2 vCPU): conta 2–4 € al mese in più sui provider europei mainstream.

### Manutenzione del sandbox nel tempo

Un sandbox non è un setup "una tantum": invecchia. Tre abitudini che pagano, e questa volta con i comandi pronti per automatizzarle.

**Ogni venerdì, ricostruisci da zero.** Le base image accumulano CVE; un rebuild settimanale chiude la finestra. Tre versioni dello stesso comando, una per OS:

```bash
# create the rebuild script used by the TL;DR
cat > ~/.openclaw/rebuild.sh <<'EOF'
#!/usr/bin/env bash
# weekly sandbox rebuild + smoke test
cd ~/.openclaw
docker build --no-cache \
  -f Dockerfile.sandbox \
  -t openclaw-sandbox:bookworm-slim .
bash verify-sandbox.sh
EOF
chmod +x ~/.openclaw/rebuild.sh

# Linux — cron, weekly Friday at 07:00
crontab -e
# add the following line:
0 7 * * 5 bash ~/.openclaw/rebuild.sh \
  >> ~/.openclaw/logs/rebuild.log 2>&1
```

```ini
# Linux — systemd timer, alternative to cron
# /etc/systemd/system/openclaw-rebuild.timer
[Unit]
Description=Weekly OpenClaw sandbox rebuild
[Timer]
OnCalendar=Fri 07:00
Persistent=true
[Install]
WantedBy=timers.target
```

```xml
<!-- macOS — launchd, ~/Library/LaunchAgents/ai.openclaw.rebuild.plist -->
<plist version="1.0"><dict>
  <key>Label</key><string>ai.openclaw.rebuild</string>
  <key>ProgramArguments</key>
  <array>
    <string>/bin/bash</string>
    <string>-lc</string>
    <string>cd ~/.openclaw &amp;&amp; \
      docker build --no-cache \
      -f Dockerfile.sandbox \
      -t openclaw-sandbox:bookworm-slim .</string>
  </array>
  <key>StartCalendarInterval</key>
  <dict>
    <key>Weekday</key><integer>5</integer>
    <key>Hour</key><integer>7</integer>
  </dict>
</dict></plist>
```

Carica con `launchctl load ~/Library/LaunchAgents/ai.openclaw.rebuild.plist` (macOS) o `systemctl --user enable --now openclaw-rebuild.timer` (Linux).

**Dopo ogni `openclaw update`,** leggi il changelog cercando le voci con tag `[security]` o `[breaking]`. Se la nuova versione cambia il default di `agents.defaults.sandbox.mode`, lo sai prima e non dopo.

**Una volta al mese,** lancia `openclaw security audit` (introdotto nella release `2026.3.x`): genera un report che confronta la tua config con i baseline noti e segnala scostamenti.

**(!) Attenzione:** non fidarti del fatto che "fino a ieri funzionava". Le best practice di sandboxing sono cambiate tre volte tra novembre 2025 e maggio 2026 (Docker Sandboxes, MAGI, credential proxy ufficiale). Quello che era "sicuro" sei mesi fa potrebbe non esserlo più oggi. Il sandbox più pericoloso è quello che hai installato e dimenticato.

**(#) Debug:** se il sandbox Docker non parte, in ordine di probabilità: (1) Docker Desktop/Engine non in esecuzione; (2) immagine `openclaw-sandbox:bookworm-slim` non costruita; (3) socket Docker non montato (su Linux verifica `/var/run/docker.sock`); (4) permessi del volume di workspace di `uid` diverso da 1000; (5) firewall dell'host che blocca la rete `openclaw-egress`. `openclaw doctor` esegue una diagnostica automatica e nel 90% dei casi dice già lui dove guardare.

### Playbook: sospetto compromissione

Tutto il capitolo finora è stato sulla prevenzione. Questo paragrafo è sulla cura: cosa fare quando, una mattina, qualcosa non torna — l'agente ha mandato un'email che non avrebbe dovuto, il consumo di token è raddoppiato senza motivo, vedi connessioni uscenti verso un dominio sconosciuto.

Cinque passi, in quest'ordine, senza saltarne nessuno.

1. **Stop al Gateway**, subito. Il primo riflesso giusto è togliere all'agente la capacità di fare altri danni. Niente "indagine in corso, lascialo acceso così vediamo che fa": prima si ferma, poi si guarda.

   ```bash
   openclaw gateway stop
   docker stop openclaw && \
     docker network disconnect openclaw-egress \
     openclaw 2>/dev/null || true
   ```

2. **Snapshot del workspace e dei log**, prima di toccare qualunque cosa. Vuoi una fotografia della scena del crimine, non un pavimento ripulito.

   ```bash
   tar czf ~/openclaw-incident-$(date +%F).tgz \
     ~/.openclaw/logs/audit.log \
     ~/.openclaw/config.yaml \
     ~/.openclaw/workspace
   ```

3. **Ruota tutte le credenziali** che l'agente ha potuto vedere: API key Anthropic/OpenAI, token GitHub/GitLab, secret di skill terze, password di servizi a cui avesse accesso via `gog`. Considera "viste" anche quelle che pensavi protette dal credential proxy: in dubbio, ruota.

4. **Ispeziona l'audit log** cercando in quest'ordine: (a) nuovi cron creati nelle ultime 24–72 ore; (b) chiamate di rete verso domini fuori dall'allowlist; (c) `exec` di processi diversi dal solito (`bash`, `python3`, `node` sono normali; `curl | sh`, no); (d) modifiche a `SOUL.md`, `TOOLS.md`, o ai file di policy.

5. **Ricostruisci da zero**, non da backup recente. Il backup di tre giorni fa potrebbe già contenere la skill o il cron compromesso. Riparti da: nuovo `Dockerfile.sandbox` (rebuild senza cache), nuova `~/.openclaw/config.yaml` da template pulito, nuove key, nuovi token. Reimporta solo i `SOUL.md` e i prompt che hai versionato in Git e di cui puoi vedere la storia.

Quando hai finito, scrivi quattro righe di postmortem: cosa è successo, come l'hai notato, cosa l'avrebbe prevenuto, cosa cambi nella config. Tre mesi dopo non te lo ricorderai e tornerà utile.

### Cosa leggere dopo

Il sandbox è la base della sicurezza, ma non la copre tutta. Tre direzioni naturali:

- [Capitolo 13 — Sicurezza: la guida che devi leggere](../PARTE-V-Sicurezza-costi/13-sicurezza-la-guida-che-devi-leggere.md): il modello di rischio completo, prompt injection, supply chain delle skill, gestione `.env`, checklist operativa stampabile.
- [Capitolo 17 — Creare skill personalizzate](../PARTE-VII-Uso-avanzato/17-creare-skill-personalizzate.md): come scrivere skill che restano sicure, code review interna, sandboxing per skill non fidate, gli scanner Clawdex e Clawvet.
- [Capitolo 19 — Deploy su VPS e infrastruttura cloud](../PARTE-VII-Uso-avanzato/19-deploy-su-vps-e-infrastruttura-cloud.md): portare il sandbox dal laptop a un'infrastruttura cloud (Railway, DigitalOcean, Hetzner) senza perdere l'hardening guadagnato in questo capitolo.

## Errori comuni e come risolverli

| Sintomo | Causa probabile | Fix |
|---|---|---|
| Container exit code 1 al primo avvio | Immagine sandbox non costruita o non aggiornata | `docker build -f Dockerfile.sandbox` e verifica con `docker images`. |
| L'agente non scrive nel workspace | `workspaceAccess: "none"` o `"ro"` di default | Cambia in `"rw"` solo quando hai capito le implicazioni. |
| Chiamate ad API esterne falliscono | Egress allowlist incompleta | Aggiungi il dominio in `allow.txt` o nella allowlist Squid; ricarica. |
| Container gira come root | Manca `USER 1000` nel Dockerfile o override del compose | Aggiungi `USER 1000` e `chown -R 1000:1000` al volume montato. |
| `env` dentro il container espone le API key | Credential proxy disattivato o variabili passate via `-e` | Attiva `credentials.mode: "proxy"`, rimuovi `-e ANTHROPIC_API_KEY`. |
| microVM non parte su macOS | Docker Desktop < 4.60 o Virtualization framework disattivato | Aggiorna Docker Desktop, abilita "Use Virtualization framework" nelle Preferences. |
| `runsc` lento in modo anomalo | Workload I/O-pesante (build npm, sync Drive) | Limita gVisor agli agent secondari; lascia il main agent su runc. |
| Ogni `openclaw update` rompe il sandbox | Override del config su file con permessi sbagliati | Versiona `~/.openclaw/config.yaml` in Git e ripristina il diff dopo l'update. |
| `cosign verify` fallisce sull'immagine base | Tag re-pushato o firma scaduta | Aggiorna il digest nel `FROM`, ri-verifica, ricostruisci. |
| WSL2 non vede la microVM | Nested virtualization disattivata nel BIOS | Abilita VT-x/AMD-V e "Virtualization in firmware" nel BIOS, riavvia. |

## Checklist di fine capitolo

- [ ] Ho scelto il livello di isolamento adatto al mio modello di rischio
- [ ] Docker Desktop ≥ 4.60 (o Engine ≥ 27) installato e funzionante
- [ ] Ho letto la mappa minacce → livelli e capito quale livello mi copre
- [ ] Immagine `openclaw-sandbox:bookworm-slim` costruita con `FROM ... @sha256:` (digest)
- [ ] `cosign verify` superato sulla base image (se il publisher pubblica firme Sigstore)
- [ ] Container verificato girare come `uid 1000` con `CapEff: 0`
- [ ] `workspaceAccess` configurato al livello minimo che fa funzionare l'agente
- [ ] Egress filtering attivo via Squid o iptables, allowlist scritta a mano
- [ ] Credential proxy abilitato; `env` dentro al container non mostra API key
- [ ] Tre smoke test eseguiti e tutti `OK` (incluso il test 2 con allowed + blocked)
- [ ] Script `verify-sandbox.sh` aggiunto al repo dei dotfiles
- [ ] Rebuild settimanale schedulato via cron / systemd timer / launchd
- [ ] `openclaw security audit` eseguito e archiviato il report
- [ ] Playbook "sospetto compromissione" stampato e tenuto a portata di mano

## Link e risorse utili

- [Run OpenClaw Securely in Docker Sandboxes](https://www.docker.com/blog/run-openclaw-securely-in-docker-sandboxes/) — post ufficiale Docker sull'integrazione
- [Docker Sandboxes documentation](https://docs.docker.com/ai/sandboxes/) — reference dei comandi `docker sandbox`
- [Sandboxing — documentazione ufficiale OpenClaw](https://docs.openclaw.ai/gateway/sandboxing) — modalità di sandbox e config
- [How to sandbox AI agents in 2026: MicroVMs, gVisor & isolation strategies](https://northflank.com/blog/how-to-sandbox-ai-agents) — panoramica indipendente
- [Multi-Agent gVisor Isolation (MAGI)](https://gvisor.dev/blog/2026/04/15/magi-multi-agent-gvisor-isolation/) — annuncio Google MAGI
- [Your Container Is Not a Sandbox (2026)](https://emirb.github.io/blog/microvm-2026/) — perché Docker da solo non basta
- [Sandboxing Claude Code in Docker: From Naive to Hardened](https://www.rasha.me/blog/sandboxing-claude-code-in-docker) — guida pratica all'hardening progressivo
- [Trail of Bits — claude-code-devcontainer](https://github.com/trailofbits/claude-code-devcontainer) — riferimento per devcontainer hardened
- [Sigstore / cosign — Verifying Container Images](https://docs.sigstore.dev/cosign/verifying/verify/) — firmare e verificare le immagini base
- [Rootless mode (Docker docs)](https://docs.docker.com/engine/security/rootless/) — come far girare il demone Docker senza root
- [Running OpenClaw in Docker (Simon Willison TIL)](https://til.simonwillison.net/llms/openclaw-docker) — setup pratico
- [OpenClaw Docker: Hardening for Production 2026](https://advenboost.com/openclaw-docker-hardening-your-ai-sandbox-for-production-2026/) — hardening per ambienti reali
- [NemoClaw Explained: Enterprise Security](https://particula.tech/blog/nvidia-nemoclaw-openclaw-enterprise-security) — approfondimento Nvidia OpenShell

Per l'elenco completo delle fonti del libro, vedi [Appendice E](../Appendici/E-risorse-e-link-utili.md).

---

[← Capitolo 3](./03-scegliere-dove-installare-openclaw.md)  ·  [Indice](../README.md)  ·  [Capitolo 5 →](./05-installazione-step-by-step.md)
