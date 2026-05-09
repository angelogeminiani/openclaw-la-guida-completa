# Capitolo 3 — Scegliere dove installare OpenClaw [★]

## Cosa imparerai

- Le **tre vie** di installazione e quando ognuna ha senso davvero
- I requisiti minimi (Node, RAM, disco, rete) aggiornati a maggio 2026
- Pro, contro e **costi reali** di hosted, VPS cloud e hardware fisico, anche con provider italiani ed europei
- La regola d'oro che evita il 90% dei disastri raccontati nei forum
- Tre storie vere e un albero decisionale per scegliere senza più dubbi
- I casi in cui la scelta più razionale è **non** installare OpenClaw, almeno per ora

## Prerequisiti

Aver letto i Capitoli [1](../PARTE-I-Capire-OpenClaw/01-cos-e-openclaw-e-perche-e-importante.md) e [2](../PARTE-I-Capire-OpenClaw/02-anatomia-di-un-agente-openclaw.md). Avere un'idea — anche vaga — di quanto vuoi spendere al mese e di cosa farai fare all'agente nelle prime due settimane. Niente di tecnico: bastano un foglio bianco e venti minuti.

## Contenuto principale

### La regola d'oro, prima ancora delle opzioni

C'è una sola decisione che, se sbagliata, rovina tutto il resto e che la community ripete da Clawdbot in poi: **non installare mai OpenClaw sul computer che usi per lavorare o per la vita personale**. Né sul portatile aziendale, né sul Mac di casa con cui leggi le email private, né sul desktop dove tieni la tesi di tua figlia.

OpenClaw ha accesso reale al filesystem, alla rete, ai comandi shell, al browser. Un cron mal scritto, un prompt injection in una pagina che gli fai leggere, una skill di terze parti distratta — e si ritrova a cancellare cartelle, inviare email a contatti sbagliati, fare commit su repository non suoi. Anche dopo i sandbox del Cap. 4, il principio resta: **dispositivo dedicato o ambiente isolato, sempre**.

Le tre vie che vediamo adesso sono tutte modi diversi di rispettare questa regola.

### Le tre vie in trenta secondi

Quando arrivi all'installazione, hai esattamente tre famiglie di scelte. Non esiste una via "giusta": esiste quella più adatta al tuo budget, al tuo tempo libero e alla tua tolleranza per la riga di comando.

```text
┌──────────────────────────────────────────────┐
│  1. HOSTED      → ti regalano l'ambiente     │
│     (€19–60/mese, zero CLI, meno controllo)  │
├──────────────────────────────────────────────┤
│  2. VPS CLOUD   → ti affitti una macchina    │
│     (€5–25/mese, CLI obbligatoria, flessib.) │
├──────────────────────────────────────────────┤
│  3. HARDWARE    → ce l'hai in casa           │
│     (€0–800 una tantum + bollette)           │
└──────────────────────────────────────────────┘
```

Tieni a mente questo schema mentre leggi le sezioni che seguono: alla fine torneremo a una tabella decisionale che lo trasforma in una scelta concreta.

### Requisiti minimi: cosa OpenClaw vuole davvero (maggio 2026)

Indipendentemente dalla via, i numeri di base aggiornati alla release `2026.4.27` sono questi:

- **Node.js 22.14+** (24.x è il default consigliato; 22 LTS regge bene per chi ha pipeline aziendali ancorate a quella versione)
- **CPU**: 2 core minimi, 4 consigliati per multi-agente
- **RAM**: 4 GB minimi, **8 GB pratici**, 16 GB se prevedi browser automation o trascrizione audio frequenti
- **Disco**: 20 GB liberi (la maggior parte sono cache di sessione e file scaricati dall'agente)
- **Rete**: connessione stabile, IPv4 in uscita, ≥10 Mbit; latenza < 200 ms verso il provider LLM (vedi sezione 3 di questo capitolo)
- **OS**: macOS 13+, qualsiasi Linux mainstream con kernel ≥ 5.15, Windows solo via WSL2

Se i numeri ti suonano strani, non preoccuparti: nessuna delle tre vie ti chiederà di calcolarli a mano. Te li hanno già calcolati i provider e i venditori di hardware. Servono solo come pietra di paragone per riconoscere un'offerta sottodimensionata quando la vedi.

**(i) Pro tip:** OpenClaw è I/O-bound, non CPU-bound. Passa quasi tutto il tempo ad aspettare risposte da un'API LLM o da un canale di chat. Quattro core lenti con 8 GB di RAM sono quasi sempre meglio di due core veloci con 4 GB.

### Opzione 1 — Piattaforme hosted: tutto incluso, controllo limitato

L'hosted è il modo più rapido per dire "voglio provare OpenClaw" e averlo funzionante in dieci minuti senza toccare un terminale. Ti registri, scegli un piano, autorizzi il canale di chat (di solito Telegram), e l'agente è già lì.

Il panorama 2026 si è assestato su tre fasce:

**Fascia base "all-inclusive"** — un solo prezzo che include hosting, modelli LLM, canali, alcune skill: *OpenClaw Launch* (€6/mese dopo il primo mese a €3), *MaxClaw* (€19/mese piatto, lanciato da MiniMax a fine febbraio 2026), *SimpleClaw* (€15/mese, onboarding guidato in italiano).

**Fascia intermedia "BYOK" (Bring Your Own Key)** — paghi l'hosting, l'LLM lo metti tu con la tua API key: *StartClaw*, *MyClaw*, *UniClaw*. Costo dell'hosting €9–15/mese, più €10–100 di token a seconda dell'uso.

**Fascia premium / editoriale** — *Plus One* di Every (every.to), pensata per scrittori e content creator, integrata con la newsletter e con tool di pubblicazione: €60/mese, modelli inclusi, supporto umano. *OpenClaw Cloud* (€59/mese dopo il primo a €29) è la versione "ufficiale" della fondazione, con SLA e backup gestiti.

Cosa ottieni davvero. Una dashboard web per monitorare l'agente, un'app mobile o un bot Telegram pre-configurato, aggiornamenti gestiti dal provider, supporto via chat. Cosa **non** ottieni: la libertà di installare skill non approvate, di modificare a fondo `SOUL.md`, di scrivere cron arbitrari, di accedere al filesystem dell'agente con SSH.

| Piano tipo | Costo/mese | Modelli LLM | Per chi |
|---|---|---|---|
| OpenClaw Launch | €6 | inclusi | esplorare in 10 min |
| MaxClaw | €19 | inclusi | uso personale leggero |
| SimpleClaw | €15 | BYOK | italofoni, principianti |
| StartClaw / MyClaw | €9–15 + token | BYOK | curiosi tecnici |
| Plus One (Every) | €60 | inclusi | content creator |
| OpenClaw Cloud | €29 → €59 | inclusi | chi vuole l'ufficiale |

I prezzi cambiano ogni paio di mesi: usali come ordine di grandezza, non come listino. Tutti i provider della tabella offrono un free trial di 7–14 giorni: usalo per capire il flusso prima di abbonarti.

**(!) Attenzione:** dopo il **ban Anthropic del 4 aprile 2026** le sottoscrizioni Claude Pro/Max non sono più utilizzabili con strumenti di terze parti come OpenClaw. Se un piano "BYOK" promette di accettare la tua subscription Claude, sta vendendo qualcosa che non funziona più. Solo **API key pay-as-you-go** sono utilizzabili oggi. Vedi anche Cap. [13](../PARTE-V-Sicurezza-costi/13-sicurezza-la-guida-che-devi-leggere.md) e Cap. [14](../PARTE-V-Sicurezza-costi/14-gestire-i-costi-senza-sorprese.md).

> *Claire Vo, dopo aver provato cinque hosted nella prima settimana del 2026:* "Sono slick, partono in dieci minuti, ma su qualunque cosa volessi davvero personalizzare mi sono sempre bloccata. Per chi vuole solo un assistente al volo, perfetto. Per chi vuole un dipendente digitale, no."

### Opzione 2 — VPS cloud: il giusto compromesso

Il VPS è il modo in cui gira oggi la maggior parte degli agenti OpenClaw "seri" che non vivono su hardware fisico. Una macchina virtuale Linux, sempre accesa, dietro una connessione decente, con OpenClaw dentro un container Docker.

Il panorama 2026 è dominato da due nomi e da una mezza dozzina di alternative.

**Hetzner Cloud** è la scelta predefinita della community europea. Il piano *CX32* (4 vCPU, 8 GB RAM, 80 GB SSD NVMe, 20 TB di traffico) costa **€7,40/mese** e regge senza fatica un agente con 5–10 cron, browser automation moderata e tre canali. Il fratello maggiore *CX42* (8 vCPU, 16 GB, 160 GB) sta sotto i €15/mese ed è il candidato giusto per multi-agente o per skill che fanno trascrizione audio. Datacenter in Germania e Finlandia, latenza ottima verso i modelli europei, 2–3× più economico rispetto ai concorrenti diretti per le stesse specifiche.

**DigitalOcean** dal 24 gennaio 2026 ha un'immagine 1-Click ufficiale dal Marketplace, oggi a **$12/mese** (prima era a $24): droplet hardened, OpenClaw `2026.1.24-1` pre-installato, container Docker non-root, firewall `ufw` già configurato, rate limit attivi, token Gateway unico per istanza. È la scelta giusta se vuoi qualcosa che "parta sicuro by default" senza dover hardenizzare tu. Costa di più di Hetzner ma ti regala due ore di lavoro.

**Le alternative**, ognuna con la sua nicchia:

- **Railway** — 1-Click deploy, fatturazione al minuto (€10/GB di RAM/mese, €20/vCPU/mese). Ideale per testare; diventa caro su workload sempre attivi (un piccolo OpenClaw può finire a €30–50/mese).
- **Render** — piani fissi a partire da $7/mese (0,5 vCPU, 512 MB), più predicibile di Railway per servizi always-on, ma sotto-dimensionato rispetto al CX32 di Hetzner.
- **Hostinger** — VPS Docker da €4,99/mese, buono per il primissimo esperimento, networking meno performante di Hetzner.
- **Google Cloud / AWS / OVH** — sono opzioni reali ma rivolte a chi ha già un account aziendale e sa cosa cerca; per il lettore tipico di questo libro sono overkill.

**Tabella sintetica VPS — quanto costa veramente in un mese tipico:**

| Provider | Piano | Costo | Nota |
|---|---|---|---|
| Hetzner | CX32 (4/8/80) | €7,40 | community favorite UE |
| Hetzner | CX42 (8/16/160) | €14,90 | multi-agente |
| DigitalOcean | 1-Click | $12 | hardened by default |
| Railway | Hobby + uso | €15–40 | usage-based, attenzione |
| Render | Standard | $7–25 | always-on prevedibile |
| Hostinger | KVM 2 | €4,99 | low-cost, limitato |

A questi importi vanno **sommati i token LLM**: per un agente personale "normale" si stima €15–80/mese di API (vedi Cap. [14](../PARTE-V-Sicurezza-costi/14-gestire-i-costi-senza-sorprese.md)).

**Italia ed Europa: provider locali e dato in casa.** Per chi legge in italiano, vale la pena conoscere anche le opzioni "vicine":

- **Aruba Cloud** (Italia, datacenter Arezzo, Bergamo, Milano, Roma) — VPS Smart Cloud da €4,20/mese (1 vCPU, 1 GB) fino a €30/mese per i tagli che reggono OpenClaw bene (4 vCPU, 8 GB). Pro: dato in territorio italiano, fatturazione in IVA italiana, supporto in italiano. Contro: networking meno performante di Hetzner, console web più datata.
- **Seeweb** (Italia, datacenter Milano, Lugano, Frosinone, Sesto San Giovanni) — Cloud Server da circa €10/mese per 2 vCPU/4 GB. Sotto il 100% rinnovabile, una delle poche realtà cloud italiane con questa promessa.
- **OVHcloud** (Francia, datacenter Strasburgo, Gravelines, Roubaix) — VPS Value da €3,50/mese, ottimo rapporto prezzo/specs, latenza ~25 ms da Milano.
- **Scaleway** (Francia, datacenter Parigi, Amsterdam, Varsavia) — STARDUST da €0,01/ora (~€7,30/mese always-on per Stardust 2 vCPU/2 GB), interfaccia molto curata, comunità developer attiva.

Quando sceglierli rispetto a Hetzner: se hai vincoli di **GDPR / data residency** stretti (clienti pubblici, sanità, settore legale), tenere il VPS in Italia o quanto meno in UE è una semplificazione enorme della documentazione di trattamento dati. Se invece sei un privato che vuole solo il prezzo migliore e bassa latenza dall'Italia, **Hetzner Falkenstein o Helsinki** restano imbattibili — i datacenter Hetzner sono in UE e quindi il GDPR è comunque rispettato dalle clausole standard.

**(#) Debug:** se ti accorgi che un agente "ragiona" lentamente ma `htop` sul VPS mostra CPU al 5% e rete tranquilla, la causa è quasi sempre **latenza verso il provider LLM**, non il VPS. Fai una verifica rapida: `curl -w "%{time_total}\n" -o /dev/null -s https://api.anthropic.com/v1/messages -X POST -H 'x-api-key: …' …`. Se ottieni più di 400 ms di tempo totale, hai sbagliato regione del VPS o stai colpendo un endpoint geograficamente sbagliato.

**Latenza e regione.** Un VPS di Singapore con il modello LLM in Virginia ti regala 350 ms di andata e ritorno per ogni token. Per un agente conversazionale, è terribile. Regola pratica: **stesso continente del tuo provider LLM**. Per Anthropic e OpenAI è di solito `us-east-1`; per Mistral e Cohere c'è scelta in Europa; per Qwen e Moonshot meglio Singapore o Tokyo.

**Accesso sicuro: niente porte aperte.** Il Gateway di OpenClaw apre il control plane WebSocket su `127.0.0.1:18789`. Quella porta **non va mai esposta su internet**, nemmeno per pochi minuti. Per accedere alla TUI o al dashboard del tuo VPS dal laptop, la community usa **Tailscale**: rete WireGuard mesh, NAT traversal automatico, MagicDNS, gratuito fino a 100 dispositivi. Lo configuri in tre comandi sul VPS, lo aggiungi al tuo telefono e al laptop, e l'agente è raggiungibile come fosse in LAN — senza che il resto del mondo veda nulla. Il setup completo è nel Cap. [19](../PARTE-VII-Uso-avanzato/19-deploy-su-vps-e-infrastruttura-cloud.md); per ora basta sapere che esiste e che è la risposta giusta a "come ci accedo da fuori?".

```bash
# minimal Tailscale install on a fresh VPS
curl -fsSL https://tailscale.com/install.sh | sh
sudo tailscale up --ssh --hostname openclaw-vps
```

**(i) Pro tip — Tailscale Serve vs Funnel.** Tailscale ha due modi diversi di esporre un servizio. *Serve* lo rende raggiungibile **solo dalla tua tailnet** (i tuoi device): è l'opzione di default ed è quella giusta nel 99% dei casi. *Funnel* lo apre invece a internet pubblico via i relay Tailscale (con HTTPS gestito). Per OpenClaw **non usare mai Funnel** sul control plane (`:18789`): ti basta Serve. Funnel può avere senso solo per webhook in ingresso ben specifici, e va sempre accoppiato a un token segreto.

**(i) Pro tip:** se è la prima volta che metti mano a un VPS, parti dal 1-Click DigitalOcean a $12. Costa il 60% più di Hetzner ma evita di passare il primo giorno a configurare `ufw`, `fail2ban`, `sshd_config` e utenti non-root. Una volta che capisci come si muove un agente in cloud, migrare a Hetzner è un'ora di lavoro.

### Opzione 3 — Hardware fisico: il piacere del ferro

L'hardware fisico è l'opzione più "meme-worthy" della cultura OpenClaw — dal post di Steinberger che chiama il suo Mac mini "il mio dipendente più affidabile" alle foto di Raspberry Pi nascosti nelle dispense. Ma è anche l'opzione che dà più controllo, più privacy e, nel lungo periodo, più soddisfazione.

**Mac mini M4 (consigliato).** È diventato lo standard di fatto. Modello base in vendita ad aprile 2026: M4 a 10 core, 16 GB di memoria unificata, 512 GB SSD, **$799** (Apple ha alzato il prezzo da $599 il 1° maggio 2026 dopo il ritiro della versione 256 GB e una carenza globale di chip di memoria dovuta alla domanda AI). Consumo a riposo 2,6–4 W misurati da utenti indipendenti, picco multi-core ~21 W, dimensioni 13×13 cm, rumorosità impercettibile, performance largamente eccessive per un agente personale. Ottimo per chi vuole **privacy assoluta**: niente cloud, niente provider, tutto in casa.

**Vecchio laptop o mini-PC.** Qualsiasi macchina con Node 22+, 8 GB di RAM e SSD funziona benissimo. Un MacBook Air 2018, un mini-PC Intel N100 nuovo a €170, un ThinkPad ricondizionato sotto i €250 — sono tutti candidati validi. Vantaggio: zero costo per chi ha già il pezzo nel cassetto. Svantaggio: spesso senza autospegnimento dopo un blackout (vedi sotto).

**Raspberry Pi 5 16 GB.** Per workload leggeri (cron testuali, riassunti, digest mattutino, ricerca web) il Pi è perfetto e costa poco: ~€110 per la board, ~€20 per case e alimentatore, **~€25 per un NVMe SSD da 256 GB** che è il vero cambio di marcia rispetto alla microSD. Limite reale: il Pi non può eseguire modelli LLM locali grossi, quindi va abbinato a un'API cloud. Per browser automation pesante o trascrizione audio è sotto-dimensionato — promesso a se stessi al volo, ci si pente subito.

**Cosa serve oltre al ferro.** Tre cose che chi installa in casa scopre solo al primo blackout o al primo cambio di IP del router:

1. **UPS (gruppo di continuità)**. Un APC Back-UPS BX950U o simile (€120–180) tiene su il Mac mini per 30–40 minuti, abbastanza perché macOS faccia uno spegnimento controllato via cavo USB. Senza UPS, ogni temporale rischia di corrompere il workspace dell'agente.
2. **IP fisso o DDNS**. Il router di casa cambia IP pubblico a piacimento. Le soluzioni: Tailscale (vedi sezione 3) — la più semplice, oppure un servizio DDNS gratuito (DuckDNS, Cloudflare Tunnel) se vuoi un nome stabile.
3. **Backup regolari**. Il workspace di OpenClaw è una cartella: `~/.openclaw/`. Un `rsync` notturno verso un NAS o un cloud storage è sufficiente. Senza backup, perdere il workspace = perdere l'agente.

```bash
# nightly workspace backup (run via launchd or cron)
rsync -av --delete \
  ~/.openclaw/ \
  /Volumes/backup/openclaw-$(date +%F)/
```

**Bolletta elettrica: quanto costa davvero tenere acceso il Mac mini.** Con un consumo medio realistico di ~10 W (mix idle + brevi picchi quando l'agente lavora) e 8.760 ore in un anno, sono **~88 kWh/anno**. Al prezzo medio italiano residenziale di 0,30 €/kWh siamo a **~€26 all'anno**, cioè poco più di **€2 al mese** in bolletta. Il Raspberry Pi 5 sta ancora più in basso (3–7 W, ~€10–18/anno). Se sommi questo all'ammortamento dell'hardware su 3 anni, vedi nella sezione costi più avanti che il Mac mini in casa resta competitivo con un VPS Hetzner.

**Avvio automatico: l'agente parte con il computer.** Su macOS conviene un `LaunchAgent` plist (questo, non `cron`, è il modo "giusto" di tenere un demone su Mac). Su Linux si usa `systemd --user`. Esempio macOS:

```xml
<!-- ~/Library/LaunchAgents/ai.openclaw.gateway.plist -->
<?xml version="1.0" encoding="UTF-8"?>
<plist version="1.0">
  <dict>
    <key>Label</key><string>ai.openclaw.gateway</string>
    <key>ProgramArguments</key>
    <array>
      <string>/usr/local/bin/openclaw</string>
      <string>gateway</string>
    </array>
    <key>RunAtLoad</key><true/>
    <key>KeepAlive</key><true/>
    <key>StandardOutPath</key>
    <string>/tmp/openclaw.out.log</string>
    <key>StandardErrorPath</key>
    <string>/tmp/openclaw.err.log</string>
  </dict>
</plist>
```

Carichi il plist con `launchctl load ~/Library/LaunchAgents/ai.openclaw.gateway.plist` e dopo ogni reboot il Gateway riparte da solo. La stessa idea su Linux è una unit `systemd --user` con `Restart=on-failure` (il Cap. [19](../PARTE-VII-Uso-avanzato/19-deploy-su-vps-e-infrastruttura-cloud.md) la mostra in dettaglio).

**Monitoraggio: sapere che è giù prima di te.** Anche un agente in casa può cadere mentre sei al lavoro o in ferie. Due servizi gratuiti coprono il 90% dei casi: **UptimeRobot** (50 monitor gratis, controllo ogni 5 minuti, alert via email/Telegram) e **Better Stack** (10 monitor gratis, alert più ricchi). Punti il monitor su un endpoint di health interno (esposto solo via Tailscale, non su internet) e ricevi un push se l'agente è muto da più di 10 minuti. Vedi anche il Cap. [15](../PARTE-VI-Manutenzione/15-care-and-feeding-tenere-l-agente-in-salute.md) sulla diagnostica e la salute dell'agente.

**(!) Attenzione:** chiunque ti convincerà a mettere OpenClaw "tanto per provare" sul tuo MacBook quotidiano avrà torto. Se vuoi davvero provarlo subito senza nuovo hardware, usa un'utenza macOS dedicata (`System Settings → Users & Groups → Add User`) con i permessi di amministrazione disabilitati, in modo che almeno l'agente non possa modificare i file della tua utenza principale. Ma è un palliativo: un Mac mini di seconda mano costa €300 ed è una scelta migliore.

### Tre storie vere (in versione anonima)

Le tabelle aiutano, ma a fissare la scelta servono persone. Tre profili reali raccolti dai forum e dai meet-up del primo trimestre 2026, ridotti all'essenziale.

**Anna, copywriter freelance, Milano.** Ha sentito parlare di OpenClaw da una collega e vuole un agente che le legga le email del mattino, le metta in coda i task della giornata, le scriva la prima bozza di newsletter ogni martedì. Zero terminale, zero voglia di imparare. Ha cominciato con *MaxClaw* a €19/mese a inizio marzo, ha capito il flusso in due settimane, e a fine aprile ha pagato un consulente €150 una tantum per migrarla su Mac mini ricondizionato (€420). Costo totale del primo mese: €19. Costo medio dei mesi successivi: €25 (LLM + API ricerca + ammortamento Mac). Tempo dedicato: due ore/settimana per i primi 30 giorni, mezz'ora/settimana dopo.

**Marco, ingegnere meccanico, Bologna.** Sa usare Linux, vuole privacy, non gli interessa risparmiare 7 €/mese sul cloud. Ha comprato un Mac mini M4 16/512 a €949 con il 5% di sconto Apple Education, lo ha messo in studio dietro la libreria, attaccato a un APC Back-UPS, con Tailscale e backup notturno su un NAS Synology che già aveva. Tre mesi dopo ha quattro agenti attivi (uno per la casa, uno per la moglie, uno per il lavoro, uno sperimentale per l'asilo della figlia). Costo medio: €40/mese di LLM + €2 di bolletta. Soddisfazione: alta. Frustrazione: il primo blackout senza UPS, prima dell'acquisto, gli era costato due ore per ricostruire una memoria persistente.

**Luca, sviluppatore SaaS, Torino.** Vuole un agente "serio", lo userà anche per i clienti, deve essere always-on, vuole poter scriverlo nei termini di servizio del suo prodotto. Ha messo OpenClaw su un *Hetzner CX42* (€14,90/mese) a Falkenstein, hardenizzato a mano (UFW, fail2ban, utenti non-root, certificati Let's Encrypt per le webhook), accesso SSH solo via Tailscale. NemoClaw sopra (Cap. 4) per le query con dati clienti, privacy router locale per il resto. Costo: €15 infra + €60 LLM + €10 monitoring (Better Stack a pagamento). Per Luca, l'hosted era fuori discussione: avrebbe dovuto firmare DPA con il provider e infilarli nel suo contratto. Il VPS gli risolve il problema in tre clausole.

Le tre storie raccontano la stessa morale: **la via giusta è quella che minimizza l'attrito tra te e l'agente**. Anna non avrebbe mai resistito a un Hetzner. Marco si sarebbe annoiato in tre giorni con MaxClaw. Luca su Mac mini in casa sarebbe esploso al primo problema di reperibilità.

### L'albero delle decisioni: tre domande in ordine

Se le storie e le tabelle ti hanno lasciato indeciso, prova a rispondere a tre domande in ordine. Ognuna esclude tutta una famiglia di opzioni.

```text
1) Hai paura del terminale o non hai 2 ore/settimana
   da dedicarci nei primi due mesi?
        SÌ ─► HOSTED (Launch / MaxClaw / SimpleClaw)
                                    fine
        NO ─► passa a 2)

2) Tratti dati sensibili (clienti, medici, legali)
   o vuoi privacy assoluta?
        SÌ, e ho budget ─► HARDWARE in casa (Mac mini)
        SÌ, ma niente budget ─► VPS UE + NemoClaw (Cap. 4)
        NO ─► passa a 3)

3) Stai a casa la maggior parte del tempo,
   con buona connessione e un angolo asciutto?
        SÌ ─► HARDWARE (Mac mini o vecchio laptop)
        NO ─► VPS (Hetzner CX32 o DO 1-Click)
```

Tre domande, una scelta. Se la prima risposta fosse "SÌ, no, no", saresti nei panni di Anna; se fosse "NO, sì-budget, sì", saresti Marco; "NO, no, no" è il profilo di Luca.

### Tabella decisionale: quale via fa per te

Le tre dimensioni che decidono la scelta sono budget, competenze tecniche, uso previsto. La tabella le incrocia in modo diretto.

| Profilo | Via consigliata |
|---|---|
| Voglio provarlo oggi, senza CLI | Hosted *Launch* o *MaxClaw* |
| Italofono alle prime armi | *SimpleClaw* o Mac mini usato |
| Tecnico curioso, budget < €15/mese | VPS Hetzner CX32 |
| Sviluppatore, vuole sicurezza by default | DigitalOcean 1-Click |
| Privacy assoluta, niente cloud | Mac mini M4 in casa |
| Hobbyista, workload solo testuali | Raspberry Pi 5 + NVMe |
| Multi-agente, business | Hetzner CX42 o Mac mini M4 Pro |
| Compliance / dati sensibili | VPS hardened + NemoClaw (Cap. 4) |

Una scelta non è per sempre. La maggior parte degli utenti fa una **migrazione** entro i primi tre mesi: parte hosted per capire il flusso, poi sposta tutto su VPS o su Mac mini quando ha le idee chiare. La cartella `~/.openclaw/` è portabile: il Cap. [19](../PARTE-VII-Uso-avanzato/19-deploy-su-vps-e-infrastruttura-cloud.md) descrive la procedura passo passo.

### Calcolare il costo totale (e perché non è solo il prezzo del piano)

Il costo mensile reale di OpenClaw è la somma di tre voci. Saltarne una è il modo più rapido per ritrovarsi col bilancio fuori controllo.

```text
COSTO TOTALE = INFRASTRUTTURA + LLM + EXTRA
```

- **Infrastruttura**: la riga del provider (€7,40 per Hetzner, $12 per DO, €19 per MaxClaw…) o l'ammortamento dell'hardware (un Mac mini da $799 spalmato su 3 anni = ~€20/mese di ammortamento + ~€3 di energia elettrica per chi è in Italia con 0,30 €/kWh).
- **LLM**: i token consumati dal modello. Variabile crudele: un agente conversazionale leggero sta sui €15/mese, un agente con browser automation aggressiva può arrivare a €150. Vedi Cap. [14](../PARTE-V-Sicurezza-costi/14-gestire-i-costi-senza-sorprese.md) per il calcolo dettagliato.
- **Extra**: ricerca web (Brave Search API €5/mese, Exa €10–25, Firecrawl pay-per-page), eventuali servizi di trascrizione, storage di backup, dominio per HTTPS.

Esempio realistico per un singolo agente personale, livello intermedio:

| Voce | Hetzner CX32 | Mac mini M4 | MaxClaw |
|---|---|---|---|
| Infra | €7,40 | €23 (ammort.) | €19 |
| LLM | €30 | €30 | inclusi |
| Search | €5 | €5 | €5 |
| **Totale** | **~€42** | **~€58** | **~€24** |

Sembra che hosted vinca sempre. Sui costi puri, spesso sì. Ma controllo, personalizzazione, privacy e capacità di crescere con multi-agente fanno pendere la bilancia in direzione VPS o hardware per chi pensa di restare con OpenClaw oltre i primi 60 giorni.

**Setup di prova vs setup serio: il pattern "due agenti".** Una pratica diffusa nella community è tenere **due ambienti separati** dopo il primo mese: un "agente di prova" (su hosted o su un VPS Hostinger da €5) dove provi skill nuove, prompt aggressivi e modelli sconosciuti, e un "agente serio" (Mac mini, Hetzner CX32+, NemoClaw) che gestisce le cose che contano davvero — calendario, email, automazioni vincolate. Costa €5–10 in più al mese ma ti evita di romperti l'agente principale durante un esperimento delle 23. Ne riparliamo nei capitoli sui workflow (Cap. [8](../PARTE-III-Primo-mese/08-dieci-workflow-pronti-all-uso.md)) e sulla manutenzione (Cap. [15](../PARTE-VI-Manutenzione/15-care-and-feeding-tenere-l-agente-in-salute.md)).

### Quando NON installare OpenClaw (sii adulto con te stesso)

Un libro onesto non finge che OpenClaw sia per chiunque. Ci sono almeno tre situazioni in cui la scelta più razionale è non installarlo affatto, almeno non oggi.

**Non hai due ore alla settimana per i primi due mesi.** OpenClaw non è "imposta una volta e dimentica". Per le prime sei-otto settimane vorrai modificare `IDENTITY.md`, leggere log, riavviare il Gateway, regolare cron. Se hai un periodo di lavoro o vita che non te le concede, aspetta: l'agente che non riesci a curare diventa un agente che ti propone idiozie convinto di servirti.

**Tratti dati altamente regolamentati senza budget per fare le cose bene.** Avvocati, medici, commercialisti che maneggiano dati di clienti devono accettare un costo minimo di €40/mese per VPS hardenizzato + NemoClaw + monitoring + DPA con il provider LLM, e qualche ora con un consulente. Provare a risparmiare facendo girare un agente "sul portatile, total privacy" è il modo più rapido per ritrovarsi in un guaio serio dopo la prima query mal scritta.

**Sei totalmente alle prime armi col terminale e non hai un amico smanettone a portata di mano.** Per quanto MaxClaw e Launch abbiano abbassato l'asticella, prima o poi servirà cambiare un file `.md` in cartella `~/.openclaw/`, configurare un canale Telegram, leggere un log. Senza un riferimento — un familiare, un collega, un canale Discord di lingua italiana — la frustrazione arriva alla seconda settimana. In questi casi il consiglio è: cominciare da Claude o ChatGPT come **assistente** (Cap. 1) e tornare a OpenClaw quando hai più dimestichezza.

In tutti gli altri casi, prosegui senza esitazioni. Le prossime pagine dànno per scontato che tu abbia fatto la tua scelta.

### Anteprima Cap. 4: la sicurezza non è un optional

Qualunque via tu scelga, il prossimo capitolo affronta una domanda che non puoi rimandare: **come isolare l'agente dal resto del sistema operativo**? Docker per-session, container Gateway, NanoClaw, NemoClaw, gVisor — sono i livelli di sandboxing tra cui scegliere prima di lanciare il primo `openclaw gateway`. Se sei sull'hosted, te ne occupa il provider; se sei su VPS o hardware, è una decisione tua.

## Prompt pronti all'uso

> **Prompt pronto — scelta personalizzata:**
> "Aiutami a scegliere dove installare OpenClaw. Dati su di me: budget mensile €X tutto incluso (infra + LLM + extra), competenze tecniche [nessuna / base / intermedie / avanzate], uso principale [descrivi in 2 frasi], priorità tra costo / privacy / facilità / controllo. Confronta hosted, VPS Hetzner CX32, DigitalOcean 1-Click e Mac mini M4 nel mio caso. Dammi una raccomandazione motivata in massimo 200 parole, con un piano di migrazione se cambio idea entro 3 mesi."

> **Prompt pronto — stima costo realistica:**
> "Stimami il costo mensile totale di OpenClaw nel mio scenario. Infrastruttura scelta: [hosted X / VPS Y / hardware Z]. Modello LLM previsto: [Claude Sonnet 4.5 / GPT-5 / Mistral Medium]. Uso atteso: [N messaggi/giorno, M cron giornalieri, browser automation sì/no, trascrizione audio sì/no]. Includi anche ricerca web e storage di backup. Dammi un range minimo–massimo, indicando le tre voci che peserebbero di più sul totale."

## Errori comuni e come risolverli

| Sintomo | Causa probabile | Fix |
|---|---|---|
| "Lo metto sul mio MacBook di lavoro tanto per provare" | Sottovalutazione dell'accesso pieno al sistema | Mai. Mac mini dedicato, vecchio laptop, VPS o utenza macOS isolata. La regola d'oro vince sempre. |
| Bolletta VPS triplicata in due settimane | Provider con bandwidth a consumo o LLM verboso | Hetzner/DO hanno traffico generoso incluso; imposta `Spend Cap` sul provider e budget alert sul provider LLM. |
| Latenza dei messaggi orribile, l'agente "lagga" | VPS in regione lontana dal modello LLM | Stesso continente del provider LLM. Per Anthropic = `us-east`; per modelli UE = Hetzner Falkenstein o Helsinki. |
| Il piano BYOK non accetta la mia Claude Pro | Ban Anthropic del 4 aprile 2026 | Passa ad API key pay-as-you-go o scegli un piano all-inclusive (MaxClaw, OpenClaw Cloud). |
| Raspberry Pi inutilizzabile dopo qualche giorno | Workload troppo pesante o microSD lenta | Aggiungi un NVMe USB 3.0 (~€25). Per browser automation o trascrizione, passa a Mac mini o VPS. |
| Mac mini si spegne durante un temporale, workspace corrotto | Niente UPS, niente backup | UPS APC Back-UPS (€120–180) collegato via USB + `rsync` notturno verso storage esterno. |
| Aperto la porta 18789 sul firewall del VPS "per debug" | Esposizione del control plane | Chiudi subito (`ufw delete allow 18789`) e usa Tailscale per l'accesso remoto. Considera l'istanza compromessa. |

## Checklist di fine capitolo

- [ ] Ho capito la **regola d'oro** e ho escluso il computer in uso attivo
- [ ] Ho scelto fra hosted, VPS cloud o hardware fisico in modo motivato
- [ ] Ho calcolato un budget mensile realistico (infra + LLM + extra)
- [ ] Il dispositivo o il VPS NON contiene dati personali o di lavoro sensibili
- [ ] Il provider LLM ha API key pay-as-you-go disponibili (non solo subscription)
- [ ] Se VPS: regione coerente con il provider LLM, accesso solo via Tailscale
- [ ] Se hardware: UPS pianificato, backup notturno del workspace, rete stabile, autostart configurato (launchd / systemd)
- [ ] Ho letto il TOS del provider per verificare che gli agenti AI siano consentiti
- [ ] Se tratto dati personali: il provider è UE / Italia, ho valutato un DPA
- [ ] Ho previsto un monitor di uptime (UptimeRobot, Better Stack) sul Gateway
- [ ] Ho onestamente verificato di **avere il tempo** per i primi due mesi di curva di apprendimento
- [ ] Ho dato un'occhiata al [Cap. 4](./04-preparare-un-ambiente-sicuro-docker-sandbox.md) sul sandboxing prima di passare all'installazione

## Link e risorse utili

- [OpenClaw — Documentazione ufficiale: Install](https://docs.openclaw.ai/install/) — la fonte primaria per tutti i percorsi
- [DigitalOcean Marketplace 1-Click OpenClaw](https://marketplace.digitalocean.com/apps/openclaw) — droplet hardened a $12/mese
- [Technical Deep Dive: How we Created a Security-hardened 1-Click Deploy OpenClaw](https://www.digitalocean.com/blog/technical-dive-openclaw-hardened-1-click-app) — cosa c'è dentro l'immagine DO
- [Hetzner Cloud — OpenClaw deployment guide](https://docs.openclaw.ai/install/hetzner) — guida community per CX32/CX42
- [openclaw-hetzner — repo Pulumi](https://github.com/miguelff/openclaw-hetzner) — IaC ready-to-deploy a meno di $7
- [Raspberry Pi Foundation — Turn your Raspberry Pi into an AI agent with OpenClaw](https://www.raspberrypi.com/news/turn-your-raspberry-pi-into-an-ai-agent-with-openclaw/) — guida ufficiale Pi
- [Apple raises Mac Mini's starting price to $799](https://fortune.com/2026/05/02/apple-mac-minis-starting-price-hike-799-ai-demand-supply-shortage/) — cronaca dell'aumento di maggio 2026
- [Anthropic ban — terzi e subscription Claude](https://thenextweb.com/news/anthropic-openclaw-claude-subscription-ban-cost) — il punto sul ban del 4 aprile 2026
- [Tailscale — Self-host a local AI stack](https://tailscale.com/blog/self-host-a-local-ai-stack) — pattern di accesso remoto consigliato
- [Aruba Cloud — VPS Italia](https://www.cloud.it/vps/) — alternativa con dato in territorio italiano
- [Seeweb — Cloud Server](https://www.seeweb.it/prodotti/cloud-server) — provider italiano sostenibile (energia rinnovabile)
- [OVHcloud — VPS Value](https://www.ovhcloud.com/it/vps/) — alternativa francese a basso costo
- [UptimeRobot](https://uptimerobot.com/) e [Better Stack](https://betterstack.com/) — monitoraggio gratuito del Gateway
- [Jeff Geerling — M4 Mac mini's efficiency is incredible](https://www.jeffgeerling.com/blog/2024/m4-mac-minis-efficiency-incredible/) — misure reali del consumo energetico

Per l'elenco completo delle fonti del libro, vedi [Appendice E](../Appendici/E-risorse-e-link-utili.md).

---

[← Capitolo 2](../PARTE-I-Capire-OpenClaw/02-anatomia-di-un-agente-openclaw.md)  ·  [Indice](../README.md)  ·  [Capitolo 4 →](./04-preparare-un-ambiente-sicuro-docker-sandbox.md)
