# Capitolo 3 — Scegliere dove installare OpenClaw [★]

## Cosa imparerai

- Le **tre vie** di installazione (più una "quarta" gratuita) e quando ognuna ha senso
- I requisiti minimi aggiornati a maggio 2026
- Pro, contro e **costi reali** delle tre vie, con il **TCO a 3 anni**
- Perché la portabilità del workspace rende la scelta iniziale poco vincolante
- I casi in cui la scelta più razionale è **non** installare OpenClaw, almeno per ora

## Prerequisiti

Aver letto i Capitoli [1](../PARTE-I-Capire-OpenClaw/01-cos-e-openclaw-e-perche-e-importante.md) e [2](../PARTE-I-Capire-OpenClaw/02-anatomia-di-un-agente-openclaw.md). Avere un'idea — anche vaga — di quanto vuoi spendere al mese e di cosa farai fare all'agente nelle prime due settimane.

## Contenuto principale

### La regola d'oro, prima ancora delle opzioni

C'è una sola decisione che, se sbagliata, rovina tutto il resto e che la community ripete da Clawdbot in poi: **non installare mai OpenClaw sul computer che usi per lavorare o per la vita personale**. Né sul portatile aziendale, né sul Mac di casa con cui leggi le email private, né sul desktop dove tieni la tesi di tua figlia.

OpenClaw ha accesso reale al filesystem, alla rete, ai comandi shell, al browser. Un cron mal scritto, un prompt injection, una skill di terze parti distratta — e si ritrova a cancellare cartelle o inviare email a contatti sbagliati. Anche dopo i sandbox del Cap. 4, il principio resta: **dispositivo dedicato o ambiente isolato, sempre**.

Le tre vie che vediamo adesso sono tutte modi diversi di rispettare questa regola.

### Le tre vie in trenta secondi

Non esiste una via "giusta": esiste quella più adatta a budget, tempo libero e tolleranza per la riga di comando.

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

### Requisiti minimi: cosa OpenClaw vuole davvero (maggio 2026)

I numeri di base aggiornati alla release `2026.4.27` (aggiornamento giugno 2026: dalla serie `2026.6` il terzo numero dello schema di versioning è un contatore patch mensile, es. `2026.6.11`, non più il giorno del mese):

- **Node.js 22.16+** (24.x è il default consigliato)
- **CPU**: 2 core minimi, 4 per multi-agente
- **RAM**: 4 GB minimi, **8 GB pratici**, 16 GB per browser automation o trascrizione audio
- **Disco**: 20 GB liberi (perlopiù cache di sessione)
- **Rete**: stabile, IPv4 in uscita, ≥10 Mbit; latenza < 200 ms verso il provider LLM (vedi «Latenza e regione»)
- **OS**: macOS 13+, Linux con kernel ≥ 5.15, Windows solo via WSL2

Servono da pietra di paragone per riconoscere un'offerta sottodimensionata.

**(i) Pro tip:** OpenClaw è I/O-bound, non CPU-bound: passa quasi tutto il tempo ad aspettare l'API LLM. Quattro core lenti con 8 GB di RAM battono quasi sempre due core veloci con 4 GB.

### Opzione 1 — Piattaforme hosted: tutto incluso, controllo limitato

L'hosted è il modo più rapido per avere OpenClaw funzionante in dieci minuti senza terminale: ti registri, autorizzi il canale di chat (di solito Telegram), e l'agente è già lì. Tre fasce: **all-inclusive** — un solo prezzo che include hosting, modelli LLM e canali: *OpenClaw Launch* (per esplorare), *MaxClaw* (uso personale leggero), *SimpleClaw* (onboarding in italiano, ideale per principianti italofoni); **BYOK (Bring Your Own Key)** — paghi solo l'hosting, l'LLM lo metti tu con la tua API key: *StartClaw*, *MyClaw*, *UniClaw*; **premium** — *Plus One* di Every (per content creator) e *OpenClaw Cloud*, la versione "ufficiale" della fondazione, con SLA e backup gestiti.

In cambio della comodità rinunci a parecchio: niente skill non approvate, niente modifiche profonde a `SOUL.md`, niente cron arbitrari, niente SSH sul filesystem dell'agente.

| Piano | Costo/mese | Modelli LLM |
|---|---|---|
| OpenClaw Launch | €6 (primo a €3) | inclusi |
| MaxClaw | €19 | inclusi |
| SimpleClaw | €15 | inclusi |
| StartClaw / MyClaw | €9–15 + token | BYOK |
| Plus One (Every) | €60 | inclusi |
| OpenClaw Cloud | €59 (primo a €29) | inclusi |

I prezzi cambiano ogni paio di mesi: usali come ordine di grandezza. Quasi tutti offrono un free trial di 7–14 giorni.

**(!) Attenzione:** dopo il **ban Anthropic del 4 aprile 2026** le sottoscrizioni Claude Pro/Max non sono più utilizzabili con strumenti di terze parti come OpenClaw. Se un piano "BYOK" promette di accettare la tua subscription Claude, sta vendendo qualcosa che non funziona più. Solo **API key pay-as-you-go** sono utilizzabili oggi. Vedi anche Cap. [13](../PARTE-V-Sicurezza-costi/13-sicurezza-la-guida-che-devi-leggere.md) e Cap. [14](../PARTE-V-Sicurezza-costi/14-gestire-i-costi-senza-sorprese.md).

> *Claire Vo, dopo aver provato cinque hosted nella prima settimana del 2026:* "Sono slick, partono in dieci minuti, ma su qualunque cosa volessi davvero personalizzare mi sono sempre bloccata. Per chi vuole solo un assistente al volo, perfetto. Per chi vuole un dipendente digitale, no."

### Opzione 2 — VPS cloud: il giusto compromesso

Il VPS è il modo in cui gira oggi la maggior parte degli agenti OpenClaw "seri": una macchina virtuale Linux sempre accesa, con OpenClaw dentro un container Docker.

**Hetzner Cloud** è la scelta predefinita della community europea. Il piano *CX32* (4 vCPU, 8 GB RAM, 80 GB NVMe) costa **€7,40/mese** e regge un agente con 5–10 cron e tre canali; il *CX42* (8 vCPU, 16 GB) sta sotto i €15/mese ed è il candidato per multi-agente o trascrizione audio. Datacenter in Germania e Finlandia, 2–3× più economico dei concorrenti.

**DigitalOcean** dal 24 gennaio 2026 ha un'immagine 1-Click ufficiale dal Marketplace a **$12 (~€11)/mese**: droplet hardened (container non-root, firewall, token Gateway unico). Costa più di Hetzner ma "parte sicuro by default": se è il tuo primo VPS parti da qui; migrare poi è un'ora di lavoro.

**Le alternative**, in breve: **Railway** (fatturazione al minuto: $10/GB di RAM (~€9) e $20/vCPU (~€18) al mese — ideale per testare, caro su workload sempre attivi), **Render** (piani fissi, prevedibile ma sotto-dimensionato), **Hostinger** (per il primissimo esperimento), **Google Cloud / AWS / OVH** (overkill per il lettore tipico).

| Piano | Costo/mese | Nota |
|---|---|---|
| Hetzner CX32 | €7,40 | favorito UE |
| Hetzner CX42 | €14,90 | multi-agente |
| DigitalOcean 1-Click | $12 (~€11) | hardened |
| Railway (uso) | €15–40 | usage-based |
| Render | da $7 (~€6,50) | always-on |
| Hostinger KVM 2 | €4,99 | low-cost |

Vanno **sommati i token LLM**: $6–30 (~€5,50–28)/mese per un uso leggero, $50–150 (~€46–138) per uno moderato (le fasce del Cap. [14](../PARTE-V-Sicurezza-costi/14-gestire-i-costi-senza-sorprese.md)).

**La quarta via nascosta: i free tier.** **Oracle Cloud Free Tier** regala in perpetuo un'instance ARM fino a **4 OCPU + 24 GB di RAM** in regioni come Francoforte: su carta, meglio di un CX42 a costo zero. I cavilli: Oracle si riprende le istanze quasi inattive (un cron con un piccolo carico periodico ti mette al riparo — i dettagli della anti-idle policy sono nel Cap. [19](../PARTE-VII-Uso-avanzato/19-deploy-su-vps-e-infrastruttura-cloud.md)), l'account va aperto almeno una volta al mese, e la disponibilità al provisioning è capricciosa. Perfetto per imparare, ma il SLA "best effort" non è production-grade; gli altri free tier sono troppo piccoli o a scadenza.

**Italia ed Europa.** Per chi legge in italiano: **Aruba Cloud** (datacenter in Italia, da €4,20 a ~€30/mese, fatturazione e supporto in italiano), **Seeweb** (Milano e Frosinone, ~€10/mese, energia 100% rinnovabile), **OVHcloud** e **Scaleway** (Francia, da €3,50/mese). Con vincoli stretti di **GDPR / data residency** (clienti pubblici, sanità, legale), il dato in Italia o in UE semplifica molto la documentazione di trattamento; per chi cerca solo prezzo e latenza, **Hetzner Falkenstein o Helsinki** restano imbattibili — e sono comunque in UE.

**Latenza e regione.** Un VPS a Singapore con il modello LLM in Virginia ti regala 350 ms di andata e ritorno per ogni token: terribile. Regola pratica: **stesso continente del provider LLM** (per Anthropic e OpenAI di solito `us-east-1`; per Mistral e Cohere c'è l'Europa). Hetzner regge comunque: i ~90–110 ms tra Germania e `us-east` stanno sotto la soglia dei 200 ms. La regola serve a evitare i casi estremi, non a squalificare l'Europa.

**(#) Debug:** se un agente "ragiona" lentamente ma `htop` sul VPS mostra CPU al 5%, la causa è quasi sempre **latenza verso il provider LLM**. Verifica rapida:

```bash
curl -s -o /dev/null -w "%{time_total}\n" \
  -X POST https://api.anthropic.com/v1/messages \
  -H 'x-api-key: <la-tua-key>'
```

Sopra i 400 ms, hai sbagliato regione del VPS. Attento a non confondere le due soglie: i 200 ms dei requisiti minimi sono il solo **RTT di rete** verso il provider, i 400 ms qui sono il **tempo totale della richiesta** (handshake TLS e risposta inclusi).

**Accesso sicuro: niente porte aperte.** Il Gateway di OpenClaw apre il control plane WebSocket su `127.0.0.1:18789`. Quella porta **non va mai esposta su internet**, nemmeno per pochi minuti. Per accedere alla TUI o al dashboard del tuo VPS dal laptop, la community usa **Tailscale**: rete mesh WireGuard, gratuita fino a 100 dispositivi. La configuri in tre comandi, la aggiungi a telefono e laptop, e l'agente è raggiungibile come fosse in LAN — senza che il resto del mondo veda nulla. Di Tailscale usa la modalità *Serve* (visibile solo ai tuoi device), mai *Funnel* (che espone a internet pubblico) sul control plane. Il setup completo è nel Cap. [19](../PARTE-VII-Uso-avanzato/19-deploy-su-vps-e-infrastruttura-cloud.md): è la risposta giusta a "come ci accedo da fuori?".

```bash
# minimal Tailscale install on a fresh VPS
curl -fsSL https://tailscale.com/install.sh | sh
sudo tailscale up --ssh --hostname openclaw-vps
```

### Opzione 3 — Hardware fisico: il piacere del ferro

L'hardware fisico è l'opzione più "meme-worthy" della cultura OpenClaw — dal post di Steinberger che chiama il suo Mac mini "il mio dipendente più affidabile" alle foto di Raspberry Pi nascosti nelle dispense — ed è quella che dà più controllo, privacy e soddisfazione.

**Mac mini M4 (consigliato).** Lo standard di fatto. Modello base a maggio 2026: M4 a 10 core, 16 GB, 512 GB SSD, **$799 (~€949 di listino in Italia, IVA inclusa)** — Apple ha alzato il prezzo da $599 il 1° maggio 2026 dopo il ritiro della versione 256 GB e la carenza di chip di memoria dovuta alla domanda AI. Consumo a riposo 2,6–4 W, silenzioso, performance eccessive per un agente personale. Per chi vuole **privacy assoluta**: niente cloud, tutto in casa.

**Vecchio laptop o mini-PC.** Qualsiasi macchina con Node 22+, 8 GB di RAM e SSD funziona: un MacBook Air 2018, un mini-PC N100 a €170, un ThinkPad ricondizionato. Zero costo per chi ha già il pezzo nel cassetto.

**Raspberry Pi 5 16 GB.** Per workload leggeri (cron testuali, riassunti, digest) il Pi è perfetto: ~€110 la board, ~€20 case e alimentatore, ~€25 un NVMe da 256 GB — il vero cambio di marcia rispetto alla microSD. Per browser automation o trascrizione è sotto-dimensionato: chi ce lo prova se ne pente subito.

**Cosa serve oltre al ferro.** Tre cose che si scoprono al primo blackout:

1. **UPS (gruppo di continuità)**. Un APC Back-UPS o simile (€120–180) dà al Mac mini il tempo di uno spegnimento controllato via USB. Senza, ogni temporale rischia di corrompere il workspace.
2. **IP fisso o DDNS**. Il router di casa cambia IP a piacimento: la soluzione più semplice è Tailscale (vedi sopra), in alternativa un DDNS gratuito (DuckDNS, Cloudflare Tunnel).
3. **Backup regolari**. Tutto OpenClaw vive in un'unica cartella: `~/.openclaw/`. Un `rsync` notturno verso un NAS o un cloud storage è sufficiente. Senza backup, perdere quella cartella = perdere l'agente.

```bash
# nightly workspace backup (run via launchd or cron)
rsync -av --delete \
  ~/.openclaw/ \
  /Volumes/backup/openclaw-$(date +%F)/
```

**Bolletta elettrica.** ~10 W medi per 8.760 ore = ~88 kWh/anno: a 0,30 €/kWh sono **~€26 l'anno**, poco più di €2 al mese (il Pi 5: ~€10–18/anno).

**Avvio automatico.** Su macOS conviene un `LaunchAgent` plist (non `cron`); su Linux una unit `systemd --user` con `Restart=on-failure` (il Cap. [19](../PARTE-VII-Uso-avanzato/19-deploy-su-vps-e-infrastruttura-cloud.md) la mostra). Il cuore del plist, da salvare come `ai.openclaw.gateway.plist` in `~/Library/LaunchAgents/` dentro il consueto boilerplate XML:

```xml
<key>ProgramArguments</key>
<array>
  <string>/usr/local/bin/openclaw</string>
  <string>gateway</string>
  <string>start</string>
</array>
<key>RunAtLoad</key><true/>
<key>KeepAlive</key><true/>
```

Lo carichi con `launchctl load` e dopo ogni reboot il Gateway riparte da solo.

**Monitoraggio.** Anche un agente in casa può cadere mentre sei in ferie. **UptimeRobot** e **Better Stack** hanno piani gratuiti: un monitor su un endpoint di health interno (solo via Tailscale, mai su internet) ti avvisa se l'agente è muto. Vedi anche il Cap. [15](../PARTE-VI-Manutenzione/15-care-and-feeding-tenere-l-agente-in-salute.md).

**(!) Attenzione:** chiunque ti convincerà a mettere OpenClaw "tanto per provare" sul tuo MacBook quotidiano avrà torto. Se proprio vuoi provarlo senza nuovo hardware, usa un'utenza macOS dedicata senza permessi di amministrazione. Ma è un palliativo: un Mac mini di seconda mano costa €300 ed è una scelta migliore.

### Tre storie vere (in versione anonima)

A fissare la scelta servono persone: tre profili reali raccolti dai forum e dai meet-up dei primi mesi del 2026.

**Anna, copywriter freelance, Milano.** Vuole un agente che le legga le email del mattino, metta in coda i task e scriva la bozza di newsletter. Zero terminale. Ha cominciato con *MaxClaw* a €19/mese a inizio marzo; a fine aprile un consulente (€150 una tantum) l'ha migrata su Mac mini ricondizionato (€420). Primo mese: €19. Mesi successivi: €30 di media (~€12 di ammortamento del Mac su 3 anni + ~€18 di LLM e API di ricerca). Tempo dedicato: due ore/settimana il primo mese, mezz'ora dopo.

**Marco, ingegnere meccanico, Bologna.** Sa usare Linux, vuole privacy. Ha comprato un Mac mini M4 16/512 a **€902 (listino €949 meno il 5% di sconto Apple Education)**, messo dietro la libreria con UPS, Tailscale e backup notturno su un NAS che già aveva. Tre mesi dopo ha quattro agenti attivi (casa, moglie, lavoro, un esperimento per l'asilo della figlia). Costo medio: €40/mese di LLM + €2 di bolletta. Frustrazione: il primo blackout, prima dell'UPS, gli era costato due ore di memoria persistente da ricostruire.

**Luca, sviluppatore SaaS, Torino.** Vuole un agente "serio", anche per i clienti, always-on, citabile nei termini di servizio. *Hetzner CX42* (€14,90/mese) hardenizzato a mano, SSH solo via Tailscale, NemoClaw (Cap. 4) per le query con dati clienti. Costo: €15 infra + €60 LLM + €10 monitoring. L'hosted era fuori discussione: avrebbe dovuto firmare DPA con il provider. Il VPS gli risolve il problema in tre clausole.

Morale: **la via giusta è quella che minimizza l'attrito tra te e l'agente**. Anna non avrebbe retto un Hetzner, Marco si sarebbe annoiato con MaxClaw, Luca sarebbe esploso al primo problema di reperibilità.

### L'albero delle decisioni: tre domande in ordine

Tre domande in ordine: ognuna esclude un'intera famiglia di opzioni.

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

Se ti fermi al primo "SÌ" sei nei panni di Anna; se rispondi "NO" e poi "SÌ, e ho budget" sei Marco; con tre "NO" di fila sei Luca.

### Tabella decisionale: quale via fa per te

| Profilo | Via consigliata |
|---|---|
| Provarlo oggi, senza CLI | Hosted *Launch* / *MaxClaw* |
| Italofono alle prime armi | *SimpleClaw* o Mac mini |
| Tecnico, budget < €15/mese | VPS Hetzner CX32 |
| Sicurezza by default | DigitalOcean 1-Click |
| Privacy assoluta, no cloud | Mac mini M4 in casa |
| Hobbyista, solo testo | Raspberry Pi 5 + NVMe |
| Multi-agente, business | Hetzner CX42 o M4 Pro |
| Compliance, dati sensibili | VPS + NemoClaw (Cap. 4) |

Una scelta non è per sempre: molti partono hosted e migrano su VPS o Mac mini entro tre mesi.

### Migrazione tra vie: il vantaggio nascosto del "filesystem-only"

OpenClaw non usa un database: tutto vive in file (identità, skill, cron, memoria, log). La cartella `~/.openclaw/` pesa qualche decina di megabyte, e questo cambia il rapporto col rischio della scelta sbagliata: **una migrazione è quasi sempre una copia di file**. Lo scenario tipo è quello di Anna.

1. **Esporta il workspace** dal provider hosted (comando `export` o download via dashboard).
2. **Installa OpenClaw** sulla nuova destinazione (Cap. [5](./05-installazione-step-by-step.md)).
3. **Riposiziona la cartella** in `~/.openclaw/workspace/` (o `workspace-<nome>`).
4. **Ridai le credenziali ai canali** — token Telegram, sessioni WhatsApp, OAuth Slack: l'unica parte non automatica.
5. **Avvia il Gateway** e fai `openclaw doctor`.

Prima migrazione: 60–90 minuti, di cui 50 di documentazione; la seconda, 15.

```bash
# moving an agent workspace from old host to new host
rsync -avz --progress \
  old-host:~/.openclaw/workspace-polly/ \
  ~/.openclaw/workspace-polly/
```

Non si trasferiscono da sole le sessioni dei canali, le API key e i secret nelle skill custom: tieni a parte un `secrets.txt` cifrato (Cap. [13](../PARTE-V-Sicurezza-costi/13-sicurezza-la-guida-che-devi-leggere.md)). Il guadagno: la paura di scegliere male diventa irrilevante — cambiare via è il lavoro di un pomeriggio. Il Cap. [19](../PARTE-VII-Uso-avanzato/19-deploy-su-vps-e-infrastruttura-cloud.md) descrive la procedura passo passo.

### Calcolare il costo totale (e perché non è solo il prezzo del piano)

Il costo mensile reale è la somma di tre voci; saltarne una significa perdere il controllo del bilancio.

```text
COSTO TOTALE = INFRASTRUTTURA + LLM + EXTRA
```

- **Infrastruttura**: la riga del provider o l'ammortamento dell'hardware (Mac mini da €949 su 3 anni = ~€26/mese + ~€2 di energia).
- **LLM**: i token consumati. Da €15/mese per un agente leggero a €150 con browser automation aggressiva (Cap. [14](../PARTE-V-Sicurezza-costi/14-gestire-i-costi-senza-sorprese.md)).
- **Extra**: ricerca web (Brave Search API: gratis entro i crediti inclusi, poi $5 (~€4,60) ogni 1.000 query), trascrizione, backup.

Per un agente personale di livello intermedio:

- **Hetzner CX32**: €7,40 infra + €30 LLM + €5 search ≈ **€42/mese**
- **Mac mini M4**: €28 (ammortamento + luce) + €30 + €5 ≈ **€63/mese**
- **MaxClaw**: €19 (modelli inclusi) + €5 search ≈ **€24/mese**

Sui costi puri l'hosted vince spesso, ma controllo, privacy e multi-agente fanno pendere la bilancia verso VPS o hardware per chi pensa di restare oltre i primi 60 giorni.

**TCO a 3 anni.** La fotografia di un mese inganna. Spalmando l'investimento su 36 mesi con criterio uniforme — €30 LLM + €5 search al mese per tutti; per gli all-inclusive (MaxClaw, OpenClaw Cloud) i modelli sono inclusi e si somma solo la search — il quadro cambia.

| Via | 12 mesi | 36 mesi |
|---|---|---|
| Oracle Free Tier + €35 | €420 | €1 260 |
| MaxClaw €19 + €5 search | €288 | €864 |
| Hetzner CX32 + €35 | €509 | €1 526 |
| DO 1-Click (~€11) + €35 | €552 | €1 656 |
| OpenClaw Cloud €59 + €5 | €738 | €2 274 |
| Mac mini M4 + €35 | €1 543 | €2 431 |

(Mac mini: €949 di listino + €150 di UPS + €72 di elettricità su 36 mesi. OpenClaw Cloud: il primo mese a €29 è già scontato nei totali. Oracle: hardware €0, ma LLM ed extra restano.)

Tre letture: *hosted vince finché l'uso resta dentro i suoi limiti* (con browser automation aggressiva salti su BYOK e i conti si avvicinano a Hetzner); *Hetzner è l'opzione "incolore" più ragionevole* — €1 526 su 3 anni per un agente pienamente customizzabile vince sui forum tecnici per una ragione; *il Mac mini è una scelta affettiva, non economica* — lo si sceglie per privacy, per il piacere del ferro o per il multi-agente (4 agenti su un Mac mini costano come 1, su MaxClaw costerebbero €76/mese).

**(i) Pro tip — il pattern "due agenti":** una pratica diffusa è tenere un "agente di prova" (hosted o VPS da €5) per sperimentare skill e modelli nuovi, e un "agente serio" (Mac mini, Hetzner CX32+) per le cose che contano. Costa €5–10 in più al mese ma evita di romperti l'agente principale durante un esperimento delle 23 (Cap. [8](../PARTE-III-Primo-mese/08-dieci-workflow-pronti-all-uso.md) e [15](../PARTE-VI-Manutenzione/15-care-and-feeding-tenere-l-agente-in-salute.md)).

### Quando NON installare OpenClaw (sii adulto con te stesso)

Tre situazioni in cui la scelta più razionale è non installarlo affatto, almeno non oggi.

**Non hai due ore alla settimana per i primi due mesi.** OpenClaw non è "imposta e dimentica": per le prime settimane vorrai ritoccare `IDENTITY.md`, log e cron. L'agente che non curi diventa un agente che ti propone idiozie convinto di servirti.

**Tratti dati altamente regolamentati senza budget.** Avvocati, medici, commercialisti devono mettere in conto almeno €40/mese (VPS hardenizzato + NemoClaw + monitoring + DPA con il provider LLM) e qualche ora di consulenza. L'agente "sul portatile, total privacy" è il modo più rapido per finire in un guaio serio.

**Sei alle prime armi col terminale e senza un riferimento.** Prima o poi servirà cambiare un file `.md`, configurare un canale, leggere un log. Senza qualcuno a cui chiedere — un collega, un canale Discord italiano — la frustrazione arriva alla seconda settimana: meglio cominciare da Claude o ChatGPT come **assistente** (Cap. 1) e tornare più avanti.

### FAQ — casi particolari

**"Posso installarlo su un NAS Synology?"** Sì, come container Docker su un modello con CPU decente e 4 GB+ di RAM, ma solo per agenti testuali leggeri: il filesystem dei NAS soffre sui tanti file piccoli della memoria persistente.

**"Ho già un VPS dove gira un blog: posso aggiungere OpenClaw lì?"** Solo se restano **liberi** 2 vCPU e 4 GB di RAM e lo isoli in un container separato. In dubbio, VPS dedicato da €5/mese.

**"Uso Windows, posso installarlo in WSL2?"** Sì, supporto ufficiale. **Importantissimo**: workspace dentro il filesystem Linux (`/home/<user>/.openclaw/`), mai in `/mnt/c/` — le performance cross-OS sui file piccoli sono catastrofiche.

**"Vivo in un paese con elettricità instabile?"** Hardware in casa no: dove salta la corrente salta anche la connessione. VPS in UE o USA, con backup periodico in locale.

**"Il mio router fa Carrier-Grade NAT, Tailscale funziona?"** Sì: ripiega sui suoi relay DERP con 30–80 ms in più, trascurabili. Dettagli nel Cap. [19](../PARTE-VII-Uso-avanzato/19-deploy-su-vps-e-infrastruttura-cloud.md).

**(i) Pro tip — impronta ambientale:** Hetzner e Seeweb usano energia 100% rinnovabile e un Mac mini consuma pochissimo. Ma il 90% della differenza la fai sui modelli LLM, non sull'host: usa modelli più piccoli quando bastano (Haiku invece di Opus per le query semplici) — il Cap. [14](../PARTE-V-Sicurezza-costi/14-gestire-i-costi-senza-sorprese.md) affronta lo stesso tema sul piano economico.

### Cosa controllare ogni mese (cinque punti, dieci minuti)

Imposta una mezz'ora al mese — la prima domenica funziona bene — per cinque verifiche ricorrenti.

1. **Spesa.** Pannello del provider LLM e dell'host contro il budget: sopra il 30%, qualcosa è cambiato (cron impazzito, skill che chatta troppo).
2. **Backup recente.** Verifica il `rsync` notturno. Un backup mai testato non è un backup.
3. **Versione aggiornata.** `openclaw update` se sei più di una minor release indietro: le patch correggono spesso bug di sicurezza (vedi la CVE-2026-25253, alias ClawJacked, nel Cap. 4).
4. **Log puliti.** `openclaw doctor` non deve emettere warning; pattern strani nei log vanno indagati subito.
5. **Token e segreti.** API key e token dei canali andrebbero ruotati almeno una volta l'anno: mettiti un promemoria.

Costi nel Cap. [14](../PARTE-V-Sicurezza-costi/14-gestire-i-costi-senza-sorprese.md), salute dell'agente nel Cap. [15](../PARTE-VI-Manutenzione/15-care-and-feeding-tenere-l-agente-in-salute.md).

### Anteprima Cap. 4: la sicurezza non è un optional

Qualunque via tu scelga, il prossimo capitolo affronta una domanda che non puoi rimandare: **come isolare l'agente dal sistema operativo**? Docker per-session, NanoClaw, NemoClaw, gVisor — i livelli di sandboxing da scegliere prima del primo `openclaw gateway start`. Sull'hosted se ne occupa il provider; su VPS o hardware è una decisione tua.

## Prompt pronti all'uso

> **Prompt pronto — scelta personalizzata:**
> "Aiutami a scegliere dove installare OpenClaw. Dati su di me: budget mensile €X tutto incluso (infra + LLM + extra), competenze tecniche [nessuna / base / intermedie / avanzate], uso principale [descrivi in 2 frasi], priorità tra costo / privacy / facilità / controllo. Confronta hosted, VPS Hetzner CX32, DigitalOcean 1-Click e Mac mini M4 nel mio caso. Dammi una raccomandazione motivata in massimo 200 parole, con un piano di migrazione se cambio idea entro 3 mesi."

> **Prompt pronto — stima costo realistica:**
> "Stimami il costo mensile totale di OpenClaw: infrastruttura [hosted X / VPS Y / hardware Z], modello [Claude Sonnet 4.6 / GPT-5.1], uso atteso [N messaggi/giorno, M cron, browser automation sì/no], più ricerca web e backup. Dammi un range minimo–massimo, con le tre voci che pesano di più."

## Errori comuni e come risolverli

**Sintomo:** "lo metto sul MacBook di lavoro per provare".
Causa: sottovalutazione dell'accesso pieno al sistema.
Fix: mai. Mac mini dedicato, VPS o utenza isolata. La
regola d'oro vince sempre.

**Sintomo:** bolletta VPS triplicata in due settimane.
Causa: bandwidth a consumo o LLM verboso.
Fix: imposta budget alert sul provider LLM.

**Sintomo:** l'agente "lagga".
Causa: VPS in regione lontana dal modello LLM.
Fix: stesso continente del provider LLM (per Anthropic =
`us-east`).

**Sintomo:** il piano BYOK non accetta la mia Claude Pro.
Causa: ban Anthropic del 4 aprile 2026.
Fix: API key pay-as-you-go o piano all-inclusive
(MaxClaw, OpenClaw Cloud).

**Sintomo:** Raspberry Pi inutilizzabile dopo qualche
giorno.
Causa: workload pesante o microSD lenta.
Fix: NVMe USB 3.0 (~€25); per browser automation, Mac
mini o VPS.

**Sintomo:** Mac mini spento dal temporale, workspace
corrotto.
Causa: niente UPS, niente backup.
Fix: UPS via USB + `rsync` notturno verso storage
esterno.

**Sintomo:** aperta la porta 18789 sul VPS "per debug".
Causa: esposizione del control plane.
Fix: chiudi subito (`ufw delete allow 18789`) e usa
Tailscale. Considera l'istanza compromessa.

## Checklist di fine capitolo

- [ ] Ho capito la **regola d'oro** e ho escluso il computer in uso attivo
- [ ] Ho scelto fra hosted, VPS cloud o hardware fisico in modo motivato
- [ ] Ho calcolato un budget realistico (infra + LLM + extra) e il **TCO a 3 anni**
- [ ] Il dispositivo o il VPS NON contiene dati personali o di lavoro sensibili
- [ ] Il provider LLM ha API key pay-as-you-go (non solo subscription)
- [ ] Se VPS: regione coerente con il provider LLM, accesso solo via Tailscale
- [ ] Se hardware: UPS, backup notturno del workspace, autostart (launchd / systemd)
- [ ] Ho letto il TOS del provider; se tratto dati personali, provider UE e DPA valutato
- [ ] Ho previsto un monitor di uptime (UptimeRobot, Better Stack) sul Gateway
- [ ] Ho onestamente verificato di **avere il tempo** per i primi due mesi
- [ ] So che `~/.openclaw/` è portabile: la scelta iniziale non è un vincolo definitivo
- [ ] Ho fissato in agenda un check mensile (spesa, backup, update, log, segreti)
- [ ] Ho dato un'occhiata al [Cap. 4](./04-preparare-un-ambiente-sicuro-docker-sandbox.md) sul sandboxing

## Link e risorse utili

- [OpenClaw — Documentazione ufficiale: Install](https://docs.openclaw.ai/install/) — la fonte primaria
- [DigitalOcean Marketplace 1-Click OpenClaw](https://marketplace.digitalocean.com/apps/openclaw) — droplet hardened a $12/mese
- [DigitalOcean — Technical Deep Dive sull'immagine hardened](https://www.digitalocean.com/blog/technical-dive-openclaw-hardened-1-click-app)
- [Raspberry Pi Foundation — OpenClaw sul Pi](https://www.raspberrypi.com/news/turn-your-raspberry-pi-into-an-ai-agent-with-openclaw/) — guida ufficiale
- [Apple raises Mac Mini's starting price to $799](https://fortune.com/2026/05/02/apple-mac-minis-starting-price-hike-799-ai-demand-supply-shortage/) — l'aumento di maggio 2026
- [Anthropic ban — terzi e subscription Claude](https://thenextweb.com/news/anthropic-openclaw-claude-subscription-ban-cost) — il ban del 4 aprile 2026
- [Tailscale — Self-host a local AI stack](https://tailscale.com/blog/self-host-a-local-ai-stack) — pattern di accesso remoto
- [Aruba Cloud — VPS Italia](https://www.cloud.it/vps/) e [Seeweb — Cloud Server](https://www.seeweb.it/prodotti/cloud-server) — dato in Italia
- [UptimeRobot](https://uptimerobot.com/) e [Better Stack](https://betterstack.com/) — monitoraggio gratuito del Gateway
- [Jeff Geerling — M4 Mac mini's efficiency](https://www.jeffgeerling.com/blog/2024/m4-mac-minis-efficiency-incredible/) — misure reali del consumo
- [Oracle Cloud Free Tier — FAQ](https://www.oracle.com/cloud/free/faq/) — la quarta via gratuita
- [Hetzner — Sustainability report](https://www.hetzner.com/unternehmen/umweltschutz/) — datacenter 100% rinnovabili dal 2021

Per l'elenco completo delle fonti del libro, vedi [Appendice E](../Appendici/E-risorse-e-link-utili.md).

---

[← Capitolo 2](../PARTE-I-Capire-OpenClaw/02-anatomia-di-un-agente-openclaw.md)  ·  [Indice](../README.md)  ·  [Capitolo 4 →](./04-preparare-un-ambiente-sicuro-docker-sandbox.md)
