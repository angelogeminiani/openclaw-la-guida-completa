# Capitolo 4 — Preparare un ambiente sicuro: Docker, sandbox e wrapper [★★]

**Cosa imparerai:**
- Perché l'isolamento dell'ambiente è il primo passo, non un optional
- Le tre strategie di sandboxing: Docker nativo, NanoClaw, NemoClaw/OpenShell
- Come scegliere il livello di isolamento giusto per il tuo caso d'uso
- Setup pratico di Docker sandbox per OpenClaw

**Prerequisiti:** Aver scelto dove installare (Capitolo 3). Conoscenza base del terminale.

**Contenuto principale:**

1. **Perché il sandboxing viene prima di tutto.** OpenClaw ha accesso completo al sistema operativo: filesystem, rete, comandi shell, browser. Come ha scritto Simon Willison: "Non sono abbastanza coraggioso per farlo girare direttamente sul mio Mac." La containerizzazione non è un extra per paranoici — è il modo responsabile di usare un agente autonomo. CVE-2026-25253 ha dimostrato che un'istanza non patchata poteva essere compromessa in meno di 90 secondi via WebSocket.

2. **I livelli di isolamento — dalla minima alla massima protezione:**
   - **Livello 0 — Installazione diretta (bare metal):** L'agente gira sullo stesso OS dell'utente. Massima flessibilità, massimo rischio. Accettabile solo su dispositivo dedicato (Mac Mini, vecchio laptop) che non contiene dati sensibili.
   - **Livello 1 — Docker sandbox per-session (consigliato per iniziare):** Il Gateway gira sull'host, ma ogni tool/skill dell'agente viene eseguito in un container Docker isolato. L'agente può leggere/scrivere solo nelle directory montate esplicitamente. È il miglior compromesso tra usabilità e sicurezza.
   - **Livello 2 — Gateway containerizzato completo:** L'intero OpenClaw (Gateway + agenti) gira dentro Docker. Nessuna installazione sull'host. Ideale per VPS e per chi vuole un ambiente "usa e getta".
   - **Livello 3 — NanoClaw (container per-chat):** Alternativa minimalista (~700 righe di TypeScript). Ogni chat gira nel proprio container Docker isolato. Permission gate obbligatori, audit log integrato. Limite: solo Claude, ecosistema ridotto.
   - **Livello 4 — NemoClaw/OpenShell (sandboxing a livello kernel):** Nvidia OpenShell usa Linux Security Modules per isolare l'agente a livello OS, non solo container. Policy YAML deny-by-default: ogni azione è bloccata se non esplicitamente permessa. Policy engine out-of-process (l'agente non può disattivarla). Privacy router per tenere i dati sensibili su modelli locali. Ideale per uso enterprise e dati sensibili.
   - **Livello 5 — gVisor (runsc):** Runtime container che intercetta le syscall. Riduce drasticamente la superficie d'attacco anche se l'agente sfrutta una vulnerabilità. Overhead di performance minimo per i workload tipici di OpenClaw.

3. **Docker sandbox nativo di OpenClaw — setup pratico.** OpenClaw supporta il sandboxing Docker out-of-the-box con due modalità:
   - **Agent Sandbox (per-session):** Il Gateway resta sull'host, i tool girano in container.
     - Costruire l'immagine base: `openclaw-sandbox:bookworm-slim`
     - Abilitare nella config: `agents.defaults.sandbox.mode = "all"` (o `"non-main"` per iniziare)
     - Scope: `"session"` (un container per sessione) o `"agent"` (un container per agente)
     - `workspaceAccess`: `"none"` (più sicuro), `"ro"`, o `"rw"`
   - **Containerized Gateway:** L'intero OpenClaw in Docker Compose.
     - Script: `./scripts/docker/setup.sh`
     - Volumi montati: `~/.openclaw` (config) e `~/openclaw/workspace` (file dell'agente)
     - Con sandbox aggiuntivo: `OPENCLAW_SANDBOX=1 ./scripts/docker/setup.sh`
   - **Docker Sandboxes (integrazione Docker ufficiale):** `docker sandbox create --name openclaw` — isolamento in MicroVM, proxy per le credenziali (le API key non entrano nel container), rete filtrata.

4. **NanoClaw — quando la semplicità è priorità.**
   - ~700 righe di codice auditabili in un pomeriggio
   - Ogni chat = un container Docker isolato
   - Permission gate obbligatori (non opzionali come in OpenClaw)
   - Audit log per ogni azione
   - Limite: solo Claude come modello, niente multi-model routing, ecosistema skill ridotto
   - Ideale per: team piccoli, compliance, chi vuole capire cosa fa ogni riga di codice

5. **NemoClaw/OpenShell — il livello enterprise.**
   - Si installa sopra OpenClaw con un singolo comando
   - OpenShell: sandbox a livello kernel (non container), policy YAML per network/filesystem/processi
   - Privacy router: query complesse → cloud, dati sensibili → Nemotron locale
   - Policy engine out-of-process: l'agente compromesso non può disattivare le regole
   - Partnership: Cisco, CrowdStrike, Google, Microsoft Security
   - Stato: alpha (marzo 2026). Da usare in produzione solo dopo maturazione.

6. **IronClaw — la terza via (Rust).**
   - Riscrittura da zero in Rust (memory safety a compile time)
   - Zero telemetria, zero dipendenze esterne non necessarie
   - Ideale per chi lavora con dati altamente confidenziali
   - Ecosistema ancora giovane, community più piccola

7. **Tabella decisionale — quale livello scegliere.**

   | Profilo | Livello consigliato | Perché |
   |---------|-------------------|--------|
   | Hobbyist su Mac Mini dedicato | Livello 1 (Docker sandbox per-session) | Buon compromesso, facile da configurare |
   | Developer su VPS | Livello 2 (Gateway containerizzato) | Ambiente usa-e-getta, niente installato sull'host |
   | Uso personale con dati sensibili | Livello 3 (NanoClaw) | Container isolati, audit log, auditabile |
   | Business / startup | Livello 4 (NemoClaw) | Policy granulari, privacy router |
   | Enterprise / compliance | Livello 4+5 (NemoClaw + gVisor) | Massimo isolamento, audit trail completo |
   | Privacy assoluta, no cloud | Livello 6 (IronClaw) | Zero telemetria, Rust, tutto locale |

8. **Hardening aggiuntivo per qualsiasi livello.**
   - Eseguire il container come utente non-root (uid 1000)
   - `--cap-drop=ALL` per rimuovere tutte le Linux capability
   - Egress filtering: allowlist esplicita per i domini raggiungibili
   - Disabilitare mDNS dentro la rete Docker per prevenire lateral movement
   - Profilo seccomp personalizzato per limitare le syscall
   - `read_only: true` sul filesystem del container dove possibile

**(!) Attenzione:** "Un container non è automaticamente un sandbox." La configurazione di default di Docker non protegge da tutto. Senza egress filtering, un agente compromesso può esfiltare dati verso qualsiasi host esterno. Senza `--cap-drop=ALL`, il container ha più permessi del necessario.

**(i) Pro tip:** Per chi inizia, il percorso più pratico è: installazione su Mac Mini/VPS dedicato → Docker sandbox per-session (Livello 1) → quando ci si sente pronti, passare al Gateway containerizzato (Livello 2). Aggiungere NemoClaw solo quando si hanno dati business reali da proteggere.

**(#) Debug:** Se il sandbox Docker non parte, verificare: Docker Desktop/Engine è in esecuzione? L'immagine `openclaw-sandbox:bookworm-slim` è stata costruita? Il socket Docker è montato correttamente? Su Linux, i permessi del volume sono di uid 1000? Lanciare `openclaw doctor` per diagnostica automatica.

**Checklist di fine capitolo:**
- [ ] Ho scelto il livello di isolamento adatto al mio caso d'uso
- [ ] Docker Desktop/Engine è installato e funzionante
- [ ] Ho costruito l'immagine sandbox (se uso Docker sandbox)
- [ ] Ho configurato il livello di `workspaceAccess` appropriato
- [ ] Ho verificato che il container gira come non-root
- [ ] Ho configurato egress filtering se espongo il sistema a internet

## Errori comuni e come risolverli

> *Sezione da rifinire in fase di stesura. Annota qui i sintomi reali che incontri seguendo il capitolo, le cause probabili e i fix verificati.*

| Sintomo | Causa probabile | Fix |
|---------|-----------------|-----|
| _TODO_ | _TODO_ | _TODO_ |


---

[← Capitolo 3](./03-scegliere-dove-installare-openclaw.md)  ·  [Indice](../README.md)  ·  [Capitolo 5 →](./05-installazione-step-by-step.md)
