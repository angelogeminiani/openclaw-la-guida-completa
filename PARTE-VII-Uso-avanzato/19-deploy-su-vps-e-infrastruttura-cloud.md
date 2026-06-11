# Capitolo 19 — Deploy su VPS e infrastruttura cloud [★★★]

## Cosa imparerai

- Deploy su Railway, DigitalOcean, Google Cloud, Render e Hetzner
- Hardening dell'infrastruttura
- Accesso remoto sicuro con Tailscale
- NanoClaw come alternativa con container isolati

## Prerequisiti

Avere un'installazione locale funzionante ([Capitolo 5](../PARTE-II-Installazione/05-installazione-step-by-step.md)). Conoscenza base di Linux e SSH. Aver letto [Capitolo 4](../PARTE-II-Installazione/04-preparare-un-ambiente-sicuro-docker-sandbox.md) sul sandboxing e [Capitolo 13](../PARTE-V-Sicurezza-costi/13-sicurezza-la-guida-che-devi-leggere.md) sulla sicurezza.

## Contenuto principale

### Dal Mac mini sotto l'armadio al cloud sempre acceso

Per i primi due o tre mesi il posto giusto per il tuo agente è quasi sempre quello che hai scelto nel Cap. [3](../PARTE-II-Installazione/03-scegliere-dove-installare-openclaw.md): un Mac mini dietro la libreria, un vecchio laptop, un Raspberry Pi nella dispensa. Poi succede qualcosa che ti fa cambiare idea. Parti per una settimana e il router di casa decide di riavviarsi il secondo giorno. Un temporale fa saltare la corrente e l'agente resta muto fino a sera, con tre cron mancati e un cliente che aspettava il report. Oppure, semplicemente, l'agente è diventato abbastanza importante da meritare un livello di affidabilità che la rete domestica non può promettere.

È il momento della migrazione al cloud: un VPS (Virtual Private Server, una macchina virtuale Linux sempre accesa in un datacenter) che non dipende dal tuo router, dal tuo gruppo di continuità né dal gatto che passa dietro l'armadio. Steinberger stesso, prima di chiamare il suo Mac mini "il mio dipendente più affidabile", lo aveva affiancato a un VPS per i carichi che non potevano permettersi un blackout.

Vale anche la pena dire quando *non* migrare. Se hai scelto l'hardware in casa per privacy assoluta — niente cloud, niente provider — un VPS rimette i tuoi dati su un disco altrui, e nessun hardening lo cambia. E se l'agente fa solo digest mattutini e promemoria, un'ora di downtime al mese non giustifica una macchina in più da amministrare. La migrazione è per chi ha bisogno di un agente *reperibile*: always-on, raggiungibile, monitorabile.

La buona notizia, già anticipata nel Cap. [2](../PARTE-I-Capire-OpenClaw/02-anatomia-di-un-agente-openclaw.md): OpenClaw non ha un database. Tutto vive in `~/.openclaw/` — config, credenziali cifrate, sessioni e workspace. Migrare significa, in essenza, spostare una cartella e ridare le credenziali ai canali. Il resto di questo capitolo è la versione lunga e sicura di quella frase.

### Due latenze, non una

Prima di scegliere il provider c'è un errore concettuale da disinnescare, perché circola anche in guide altrimenti buone: "metti il VPS vicino al provider LLM, così tutto è più veloce". È vero a metà, e la metà sbagliata costa cara. Le latenze in gioco sono **due**, e tirano in direzioni opposte:

- **Latenza utente→VPS.** È quella che senti quando lavori in SSH, apri la dashboard o usi la TUI. Dipende dalla distanza tra *te* e il datacenter. Per chi scrive dall'Italia, un VPS a Falkenstein o Norimberga risponde in 20–35 ms; uno in Virginia in 100–130 ms, abbastanza da rendere l'editing in SSH un esercizio di pazienza.
- **Latenza VPS→LLM.** È quella che incide su quanto in fretta arrivano i token del modello. Dipende dalla distanza tra il *VPS* e l'endpoint del provider (per Anthropic e OpenAI, tipicamente `us-east`).

Se segui il consiglio sbagliato e metti il VPS in USA East "per stare vicino a Claude", ottimizzi la seconda latenza massacrando la prima: l'agente risponde uguale, ma ogni tua sessione SSH diventa molasses. La regola corretta per un lettore europeo è quella già vista nel Cap. 3: **VPS vicino a te, stesso continente "a buon senso" col provider LLM solo per evitare i casi estremi**. I ~90–110 ms tra Germania e `us-east` stanno sotto la soglia di percezione per un agente conversazionale; i 350 ms tra Singapore e Virginia no. Datacenter europeo per te, e nessun rimorso verso il modello.

**(#) Debug:** se l'agente "ragiona" lento ma `htop` sul VPS è tranquillo, misura la tratta VPS→LLM prima di incolpare la macchina: il comando `curl -w` con `time_total` mostrato nel box Debug del Cap. 3 (sezione "Latenza e regione") funziona identico qui. Sopra i 400 ms, hai sbagliato continente — del VPS o dell'endpoint.

### La matrice di scelta dei provider

Il panorama 2026 dei deploy OpenClaw in cloud si è assestato su cinque nomi ricorrenti, più una manciata di alternative regionali già viste nel Cap. 3 (Aruba, Seeweb, OVHcloud, Scaleway, Hostinger). La matrice:

| Provider | Costo/mese | Per chi |
|---|---|---|
| Hetzner CX32 | €7,40 | miglior costo/prestazioni |
| DigitalOcean | $12 (~€11) | sicuro by default |
| Railway | €15–40 | provare in 5–8 minuti |
| Render | $7–25 (~€6–23) | always-on prevedibile |
| Google Cloud | variabile | chi è già su GCP |

La logica di scelta sta in tre domande. Vuoi *provare* il deploy cloud senza impegno? Railway, oggi pomeriggio. Vuoi un VPS che parta già hardenizzato senza lavoro manuale? DigitalOcean. Vuoi il miglior prezzo, datacenter UE e pieno controllo, accettando un'ora di hardening fatto da te? Hetzner — ed è la strada che questo capitolo percorre per intero, dal server vuoto al Gateway in produzione. Google Cloud e Render coprono nicchie precise che vediamo tra poco. A qualunque cifra della tabella vanno **sommati i token LLM** (€15–80/mese per un agente personale tipico — Cap. [14](../PARTE-V-Sicurezza-costi/14-gestire-i-costi-senza-sorprese.md)).

### Railway: in cloud in 5–8 minuti

Railway è il modo più rapido in assoluto per vedere OpenClaw girare in cloud: un template 1-Click, nessun server da amministrare, fatturazione al minuto. Il flusso reale, cronometrato dalla community tra i 5 e gli 8 minuti:

1. Apri il template "OpenClaw" su Railway e fai "Deploy".
2. Nelle variabili d'ambiente imposta **`SETUP_PASSWORD`**: è la password che protegge il wizard di primo avvio esposto via web. Senza, chiunque trovi l'URL del tuo deploy può configurarsi *il tuo* agente — con le tue API key.
3. Aggiungi un **volume persistente** montato su **`/data`**: è lì che il container scrive lo stato (`config.yaml`, credenziali, workspace). Senza volume, ogni redeploy riparte da zero: agente amnesico, onboarding da rifare.
4. Apri l'URL del servizio, inserisci la `SETUP_PASSWORD`, completa l'onboarding con la tua API key.

**(i) Pro tip:** il volume su `/data` non è un'opzione, è *la* differenza tra un giocattolo e un deploy. Verificalo subito: riavvia il servizio dalla dashboard Railway e controlla che l'agente ricordi il nome che gli hai dato. Se non lo ricorda, il volume non è montato dove crede lui.

Il limite di Railway è il modello di costo: paghi RAM e vCPU al minuto (~€10/GB di RAM/mese, ~€20/vCPU/mese), perfetto per servizi che dormono, penalizzante per un agente con heartbeat ogni 30 minuti e cron sparsi che non dorme mai. Un piccolo OpenClaw sempre attivo finisce facilmente a €30–50/mese: il triplo di Hetzner per metà delle risorse. E i piani free/hobby hanno limiti di esecuzione che troncano i task lunghi (browser automation, trascrizioni). Usalo per quello in cui eccelle — capire in un pomeriggio se il cloud fa per te — e poi trasloca: la procedura di migrazione qui sotto vale anche in uscita da Railway.

### DigitalOcean Marketplace: sicuro by default

Dal **24 gennaio 2026** il Marketplace DigitalOcean ha un'immagine 1-Click **ufficiale** di OpenClaw, oggi a $12 (~€11)/mese. Non è un semplice "OpenClaw preinstallato": è una *hardened image*, un droplet che esce dalla fabbrica con le difese già alzate — container Docker non-root, firewall `ufw` preconfigurato, rate limit attivi sulle API esposte, token del Gateway unico per istanza generato al provisioning. Il dettaglio tecnico è documentato nel "Technical Deep Dive" ufficiale di DigitalOcean (Appendice E).

Il flusso: Marketplace → "OpenClaw" → scegli il droplet (il taglio base regge bene un agente singolo) → region (Francoforte o Amsterdam per chi sta in Italia — vale la regola delle due latenze) → aggiungi la tua chiave SSH → Create. Al primo login un messaggio di benvenuto ti guida all'onboarding via CLI, identico a quello del Cap. [5](../PARTE-II-Installazione/05-installazione-step-by-step.md).

Rispetto a Hetzner costa circa il 50% in più a parità di fascia, ma ti regala le due ore di hardening manuale e — per chi non ha mai amministrato un server — soprattutto ti toglie la possibilità di sbagliarlo. È il consiglio già dato nel Cap. 3: prima esperienza su DigitalOcean, migrazione a Hetzner quando hai capito come si muove un agente in cloud.

### Google Cloud e Render: per chi ci vive già

**Google Cloud** ha senso quasi solo se la tua infrastruttura è già lì. Le due strade documentate nella guida ufficiale (sezione install della documentazione — Appendice E) sono **GKE** (Kubernetes gestito: overkill per un agente, sensato se ne orchestri una flotta) e **Cloud Run**. Su Cloud Run serve un avvertimento grosso: è una piattaforma *scale-to-zero*, progettata per spegnere i container inattivi. Un agente OpenClaw non è mai "inattivo" nel senso di Cloud Run — ha l'heartbeat ogni 30 minuti, cron notturni, sessioni WebSocket persistenti — quindi devi forzare un'istanza sempre attiva (min-instances = 1), e a quel punto paghi come una VM rinunciando ai vantaggi del serverless. Se non hai vincoli aziendali su GCP, un VPS semplice è la scelta più onesta.

**Render** sta a metà: piani fissi da $7 (~€6,50) a $25 (~€23)/mese, esperienza "serverless-like" (deploy da repository, zero gestione OS) ma con servizi always-on prevedibili nel costo, al contrario di Railway. Anche qui la persistenza non è scontata: serve un *persistent disk* collegato al servizio, o lo stato evapora a ogni deploy. Il piano da $7 (0,5 vCPU, 512 MB) è sotto i requisiti visti nel Cap. 3: per un agente vero parti almeno dal taglio intermedio.

### Hetzner end-to-end: dal VPS vuoto al Gateway in produzione

Questa è la procedura completa, dall'account appena creato all'agente che risponde su Telegram dal datacenter. È quella che ha seguito Luca, lo sviluppatore torinese del Cap. 3, per il suo CX42; qui usiamo il CX32 (€7,40/mese), che basta a un agente singolo con cron e browser automation moderata. Tempo realistico la prima volta: 60–90 minuti. La parola che incontrerai più spesso è **hardening** — letteralmente "indurimento": l'insieme di interventi che riducono la superficie d'attacco di una macchina esposta a internet. Un VPS appena nato riceve i primi tentativi di accesso automatizzati nel giro di minuti, non di giorni: l'hardening non è paranoia, è igiene.

**Passo 0 — checklist pre-migrazione (sulla macchina vecchia).** Prima di toccare il cloud, congela lo stato di partenza:

```bash
# 1. snapshot of current health, kept for later
openclaw doctor > ~/doctor-before.txt

# 2. full backup: engine state + workspace
openclaw backup create \
  --output ~/Backups \
  --include-workspace

# 3. stop the old gateway
openclaw gateway stop
```

E tre verifiche a mano: i token dei canali sono recuperabili (il token BotFather di Telegram, le OAuth Slack)? Le API key dei provider sono salvate anche fuori da `~/.openclaw/` (password manager)? Hai letto l'output di `doctor` e sistemato i warning *prima* di migrare? Migrare un'installazione malata trapianta anche la malattia.

**(!) Attenzione:** da questo momento e fino a fine migrazione il vecchio Gateway deve restare **spento** (e il daemon disabilitato, se l'avevi installato). Due Gateway accesi con lo stesso token Telegram si rubano i messaggi a vicenda: l'agente risponde due volte, o a metà, e il debugging è da manicomio.

**Passo 1 — crea il server.** Dalla console Hetzner Cloud: nuovo progetto → Add Server → location **Falkenstein** o **Norimberga** (UE, GDPR, 20–35 ms dall'Italia) → immagine **Ubuntu 24.04 LTS** → tipo **CX32** (4 vCPU, 8 GB, 80 GB NVMe) → **SSH key**: incolla la tua chiave pubblica (`~/.ssh/id_ed25519.pub`). Non scegliere l'accesso via password: la chiave SSH è il primo mattone dell'hardening, ed è gratis. In 30 secondi hai un IP.

**Passo 2 — utente non-root.** Il primo login è `root`; il primo gesto è smettere di usarlo:

```bash
adduser claw
usermod -aG sudo claw

# copy the SSH key to the new user
rsync --archive --chown=claw:claw \
  ~/.ssh /home/claw/
```

D'ora in poi entri come `claw` e usi `sudo` quando serve. Un processo compromesso sotto un utente normale fa molti meno danni di uno sotto root — è lo stesso principio del container non-root del Cap. 4, un piano più in basso.

**Passo 3 — hardening base.** Tre interventi, dieci minuti:

```bash
sudo apt update && sudo apt -y upgrade
sudo apt -y install ufw fail2ban

# firewall: inbound SSH only
sudo ufw allow OpenSSH
sudo ufw enable
```

`ufw` è il firewall: la regola sopra dice "in ingresso solo SSH, tutto il resto chiuso" — e nota cosa *non* apriamo: nessuna porta per il Gateway, ci pensa Tailscale tra poco. **fail2ban** è un demone che legge i log di autenticazione e banna temporaneamente gli IP che sbagliano password in raffica: con la config di default copre SSH senza che tu debba toccare nulla. Terzo intervento, chiudere l'accesso via password in `/etc/ssh/sshd_config`:

```text
# /etc/ssh/sshd_config — key lines
PasswordAuthentication no
PermitRootLogin no
```

Poi `sudo systemctl restart ssh`. Da adesso si entra solo con la chiave, e mai come root. (Se vuoi andare oltre — porta SSH non standard, 2FA — la checklist dell'[Appendice D](../Appendici/D-checklist-sicurezza.md) ha la lista completa.)

**Passo 4 — swap e Docker.** La **swap** è un file su disco usato come RAM di emergenza: con 8 GB non la userai quasi mai, ma il giorno che una trascrizione audio sfora, fa la differenza tra un rallentamento e un processo ucciso dal kernel:

```bash
sudo fallocate -l 2G /swapfile
sudo chmod 600 /swapfile
sudo mkswap /swapfile && sudo swapon /swapfile
echo '/swapfile none swap sw 0 0' | \
  sudo tee -a /etc/fstab
```

Se sul laptop usavi il sandbox Docker del Cap. 4 — e dovresti — il VPS non è il posto dove rinunciarci: installa Docker (`sudo apt -y install docker.io`, poi `sudo usermod -aG docker claw`), porta con te il tuo `Dockerfile.sandbox` e ricostruisci l'immagine sul server con `docker build --no-cache`. L'hardening guadagnato nel Cap. 4 (container non-root, egress allowlist, credential proxy) viaggia tutto dentro file di config: la migrazione non te lo toglie, a patto di non "semplificare temporaneamente" per far prima. Le semplificazioni temporanee sui server sono permanenti.

**Passo 5 — Node 22.16+ e OpenClaw.** Ubuntu 24.04 non ha di serie un Node abbastanza recente; usa NodeSource come nel Cap. 5:

```bash
curl -fsSL https://deb.nodesource.com/setup_22.x \
  | sudo -E bash -
sudo apt -y install nodejs
node --version   # must be >= 22.16

# install OpenClaw (official script)
curl -fsSL https://openclaw.ai/install.sh | bash
```

Quando l'installer ti propone l'onboarding, puoi fermarti: non serve creare un agente nuovo, stai per trapiantare il tuo.

**Passo 6 — ripristina il backup.** Porta l'archivio sul VPS e ripristinalo:

```bash
# from your laptop
scp ~/Backups/openclaw-backup-*.tar.gz \
  claw@<ip-del-vps>:~/

# on the VPS
openclaw backup restore \
  ~/openclaw-backup-2026-05-13-0900.tar.gz
```

Il restore ricrea `~/.openclaw/` per intero: `config.yaml`, credenziali cifrate, sessioni, e — grazie al `--include-workspace` del Passo 0 — anche la "scrivania": SOUL.md, IDENTITY.md, memoria, skill, cron. Il tuo agente si sveglia sul server con tutti i ricordi al loro posto.

**Passo 7 — il Gateway come servizio systemd.** Sul laptop ci pensava `openclaw onboard --install-daemon`; su un server headless conviene sapere cosa c'è dentro. La unit promessa nel Cap. 3, per esteso:

```ini
# ~/.config/systemd/user/openclaw-gateway.service
[Unit]
Description=OpenClaw Gateway
After=network-online.target

[Service]
ExecStart=/usr/local/bin/openclaw gateway start
Restart=on-failure
RestartSec=5

[Install]
WantedBy=default.target
```

`Restart=on-failure` è la riga che vale il biglietto: se il Gateway muore, systemd lo rialza dopo 5 secondi, alle 3 di notte come a mezzogiorno. Attivazione:

```bash
systemctl --user enable --now openclaw-gateway
sudo loginctl enable-linger claw
```

Il secondo comando è il dettaglio che frega tutti sui server: senza *linger*, i servizi `--user` partono solo quando l'utente ha una sessione di login attiva — cioè mai, su una macchina dove entri una volta al mese. Con il linger, il Gateway parte al boot e sopravvive ai tuoi logout.

**Passo 8 — doctor post e confronto.** Chiudi il cerchio aperto al Passo 0:

```bash
openclaw doctor > ~/doctor-after.txt
diff ~/doctor-before.txt ~/doctor-after.txt
```

Il `diff` è il collaudo della migrazione: l'ideale è vuoto o quasi. Ogni riga nuova è qualcosa che la migrazione ha rotto e che vedi *adesso*, in mezz'ora di lucidità, invece che fra tre settimane quando un cron fallisce in silenzio. Il sospetto più frequente: canali disconnessi — qualche sessione (WhatsApp in particolare) non sopravvive al cambio macchina. La cura è ri-autenticare: `openclaw channels login --channel <nome>`. Poi scrivi all'agente su Telegram: se risponde — una volta sola — la migrazione è finita.

**(i) Pro tip:** prima di dichiarare vittoria, fai uno **snapshot** del VPS dalla console Hetzner (costa centesimi). È la foto della macchina appena migrata e funzionante: il giorno che un esperimento di hardening va storto, torni lì in un click invece di rifare i Passi 1–7.

### Tailscale: accesso al Gateway senza porte aperte

Resta il problema dell'accesso remoto. Il control plane del Gateway vive su `127.0.0.1:18789` e — vale la pena ripeterlo con la formula del Cap. 3 — quella porta **non va mai esposta su internet**, nemmeno per pochi minuti, nemmeno "tanto c'è il token". La risposta della community è **Tailscale**: una rete privata WireGuard tra i tuoi dispositivi, con NAT traversal automatico e zero porte aperte. Il setup completo, promesso nel Cap. 3, sono quattro comandi:

```bash
# on the VPS
curl -fsSL https://tailscale.com/install.sh | sh
sudo tailscale up --ssh --hostname openclaw-vps

# expose the dashboard inside the tailnet only
sudo tailscale serve --bg 18789
```

Poi installi il client Tailscale su laptop e telefono (stessa utenza) e il gioco è fatto: `openclaw-vps` diventa un nome raggiungibile da tutti i tuoi dispositivi — e da nessun altro al mondo. Il flag `--ssh` aggiunge l'SSH via Tailscale, con due bonus: puoi chiudere del tutto la porta 22 pubblica (`sudo ufw delete allow OpenSSH` — fail2ban va in pensione, non c'è più niente da bannare) e l'autenticazione passa per l'identità Tailscale invece che per la chiave. `tailscale serve` pubblica la dashboard del Gateway **solo dentro la tailnet**, con HTTPS automatico: dal telefono, in treno, apri la dashboard come se il VPS fosse in LAN.

Sulla differenza tra *Serve* (solo tailnet — quello che vuoi) e *Funnel* (internet pubblico — quello che non vuoi sul Gateway), vale il pro tip "Tailscale Serve vs Funnel" del Cap. 3: la regola corta è che Funnel sul control plane non si usa mai. Il pattern completo VPS + Tailscale + agente AI è documentato anche sul blog ufficiale Tailscale (Appendice E).

### NanoClaw: un container per ogni chat

Chiusura con l'alternativa radicale. **NanoClaw** è una reimplementazione minimalista dell'idea OpenClaw: ~700 righe di TypeScript leggibili in una serata, nessun ecosistema di plugin, e una scelta architetturale netta — **ogni chat vive nel suo container Docker**. Non un sandbox condiviso da tutto l'agente come nel Cap. 4: un container *per conversazione*, con filesystem e permessi propri. Una prompt injection che scappa da una chat trova i muri del container, non i tuoi dati.

I limiti sono il prezzo della purezza: supporta solo Claude come modello, niente ClawHub, niente community di skill, canali ridotti all'osso. La regola di scelta è onesta: se in questo capitolo hai pensato "tutto qui l'hardening?", NanoClaw non fa per te — ti mancherà l'ecosistema in una settimana. Se invece hai pensato "troppa superficie d'attacco, troppi pezzi", NanoClaw su un CX32 Hetzner è la combinazione più tranquilla del 2026: poco codice da fidarsi, isolamento per-chat, e un confronto dettagliato con OpenClaw e NemoClaw nelle analisi della community (Appendice E).

**Prompt pronto:**
> "Voglio spostarti dal Mac Mini di casa a un VPS [DigitalOcean / Railway / Hetzner]. Aiutami nella migrazione: (1) checklist pre-migrazione (cosa fare sul Mac prima di spegnerlo), (2) scelta della region più vicina al mio provider LLM, (3) hardening base del VPS (SSH key-only, firewall, fail2ban), (4) configurazione di Tailscale per accesso senza esporre la porta del Gateway su internet, (5) `openclaw doctor` post-migrazione per confermare che tutto funzioni."

## Errori comuni e come risolverli

**Sintomo:** deploy Railway funziona ma timeout sui task lunghi.
Causa: limite di esecuzione del piano free/hobby.
Fix: passare a piano superiore o a VPS dedicato
(DigitalOcean, Hetzner).

**Sintomo:** SSH lentissimo, comandi che bloccano.
Causa: VPS in una region lontana **da te** (la latenza
SSH dipende dalla tratta utente→VPS).
Fix: dall'Italia, scegliere una region europea
(Falkenstein, Norimberga, Francoforte, Amsterdam).

**Sintomo:** l'agente risponde lento, token col contagocce.
Causa: VPS in un continente diverso dal provider LLM
(latenza VPS→LLM, da non confondere con quella SSH).
Fix: stesso continente del provider nei casi estremi;
dall'Europa verso `us-east` i ~100 ms non si percepiscono
(vedi "Latenza e regione" nel Cap. 3).

**Sintomo:** Docker non parte sul VPS.
Causa: kernel troppo vecchio o swap insufficiente.
Fix: verificare `uname -r`, aggiungere swap
(`fallocate -l 2G /swapfile`).

**Sintomo:** espongo accidentalmente il Gateway su internet.
Causa: porta 18789 aperta sul firewall pubblico.
Fix: MAI esporre la porta del Gateway. Usare Tailscale
Serve/Funnel per accesso remoto sicuro.

**Sintomo:** l'agente risponde due volte a ogni messaggio.
Causa: il vecchio Gateway di casa è ancora acceso con lo
stesso token di canale.
Fix: `openclaw gateway stop` sulla macchina vecchia e
disabilitare il daemon (launchd/systemd).

**Sintomo:** dopo la migrazione `doctor` segnala canali
disconnessi.
Causa: alcune sessioni di canale (es. WhatsApp) non
sopravvivono al cambio di macchina.
Fix: ri-autenticare con
`openclaw channels login --channel <nome>`.

**Sintomo:** il Gateway muore al logout SSH dal VPS.
Causa: unit `systemd --user` senza linger attivo.
Fix: `sudo loginctl enable-linger <utente>`.

## Checklist di fine capitolo

- [ ] Provider scelto e VPS provisionato
- [ ] Hardening base completato: SSH key-only, firewall attivo, fail2ban
- [ ] Tailscale (o equivalente) per accesso senza esporre porte pubbliche
- [ ] Backup periodico della cartella `.openclaw/` su storage esterno
- [ ] `openclaw doctor` non segnala warning
- [ ] Backup `--include-workspace` creato PRIMA della migrazione
- [ ] Output di `doctor` pre/post migrazione confrontati con `diff`
- [ ] Unit systemd attiva e `loginctl enable-linger` impostato
- [ ] Vecchio Gateway spento e daemon disabilitato (niente doppie risposte)

## Link e risorse utili

- [Railway 1-Click Deploy](https://railway.com/deploy/openclaw) — la via più rapida per spostare OpenClaw in cloud
- [How to Run OpenClaw with DigitalOcean](https://www.digitalocean.com/community/tutorials/how-to-run-openclaw) — guida ufficiale DigitalOcean (Marketplace dal 24 gennaio 2026)
- [DigitalOcean Marketplace 1-Click](https://marketplace.digitalocean.com/apps/openclaw) — l'immagine ufficiale hardened
- [DigitalOcean Technical Deep Dive](https://www.digitalocean.com/blog/technical-dive-openclaw-hardened-1-click-app) — cosa c'è dentro la hardened image
- [Install — indice ufficiale di tutti i percorsi](https://docs.openclaw.ai/install/) — incluse le guide GCP, Render e Hetzner
- [Hetzner — guida community OpenClaw](https://docs.openclaw.ai/install/hetzner) — il riferimento per la procedura end-to-end
- [openclaw-hetzner (Pulumi IaC)](https://github.com/miguelff/openclaw-hetzner) — la stessa procedura come infrastructure-as-code
- [Hostinger VPS per OpenClaw](https://www.hostinger.com/vps/docker/openclaw) — opzione low-cost con Docker preconfigurato
- [Tailscale — Self-host a local AI stack](https://tailscale.com/blog/self-host-a-local-ai-stack) — il pattern VPS + tailnet spiegato da Tailscale
- [OpenClaw Docker: Hardening for Production 2026](https://advenboost.com/openclaw-docker-hardening-your-ai-sandbox-for-production-2026/) — hardening per VPS pubblici
- [OpenClaw vs NanoClaw vs NemoClaw](https://collabnix.com/the-claw-wars-openclaw-vs-nanoclaw-vs-nemoclaw/) — il confronto tra le tre "claw"

Per l'elenco completo delle fonti del libro, vedi [Appendice E](../Appendici/E-risorse-e-link-utili.md).

---

[← Capitolo 18](./18-cron-job-e-automazioni-avanzate.md)  ·  [Indice](../README.md)  ·  [Capitolo 20 →](./20-architettura-del-gateway.md)
