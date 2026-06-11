# Capitolo 15 — Care and feeding: tenere il tuo agente in salute [★★]

## Cosa imparerai

- Come diagnosticare un agente che non risponde
- Come usare Screen Sharing e Remote Login per accesso remoto
- Come far "riparare" l'agente da solo
- Come gestire aggiornamenti e backup

## Prerequisiti

Aver fatto installazione ([Capitolo 5](../PARTE-II-Installazione/05-installazione-step-by-step.md)) e onboarding ([Capitolo 7](../PARTE-III-Primo-mese/07-prima-conversazione-onboarding-agente.md)). Il capitolo prende senso dopo almeno una settimana di uso quotidiano.

## Contenuto principale

### "Hellooooo?" — succederà, ed è normale

Martedì, ore 7:40. Il digest mattutino di Polly non è arrivato. Scrivi "buongiorno" su Telegram: niente. Scrivi "Hellooooo?": niente. La prima volta che succede, il pensiero corre subito al peggio — si è rotto tutto, ho perso la memoria dell'agente, devo reinstallare. Quasi mai è così.

Un agente OpenClaw è un dipendente digitale, e come ogni dipendente ogni tanto si ammala. Il computer è andato in sleep, la connessione è caduta, il Gateway è crashato dopo un aggiornamento, il token di un canale è scaduto, un cron ha smesso di scattare per il cambio di ora legale. Nella stragrande maggioranza dei casi la causa è una di queste — banale, locale, riparabile in cinque minuti. La differenza tra chi convive bene con un agente e chi lo abbandona dopo un mese non è la fortuna di non avere mai guasti: è avere un metodo per diagnosticarli senza panico e un backup per i (rari) casi in cui il guasto non è banale.

Questo capitolo è quel metodo. La buona notizia è che lo conosci già a metà: l'ossatura è la griglia dei sei elementi presentata nel [Capitolo 2](../PARTE-I-Capire-OpenClaw/02-anatomia-di-un-agente-openclaw.md).

### La griglia dei sei elementi: il tuo runbook diagnostico

Nel Capitolo 2 abbiamo descritto l'agente con sei elementi: la **scrivania** (il workspace), il **badge** (IDENTITY.md), la **cassetta degli attrezzi** (le skill), l'**agenda** (i cron), il **diario** (la memoria) e il **cuore che batte** (heartbeat e Gateway). Quando l'agente non risponde, la domanda giusta non è "quale log devo leggere?" ma "quale dei sei elementi non sta funzionando?". Ogni elemento ha un sintomo tipico e un primo controllo:

| Elemento | Primo controllo |
|----------|-----------------|
| Cuore (Gateway) | `openclaw status` |
| Scrivania (workspace) | file canonici a posto? |
| Badge (IDENTITY.md) | nome e ruolo coerenti? |
| Cassetta (skill) | TOOLS.md aggiornato? |
| Agenda (cron) | `openclaw cron list` |
| Diario (memoria) | `memory/` scrive oggi? |

L'ordine di ispezione non è casuale: si parte sempre dal cuore. Se il Gateway è giù, tutto il resto è irrilevante — l'agente più sano del mondo non risponde se il centralino è spento. Solo quando il cuore batte ha senso scendere agli altri elementi: un agente che risponde ma "non si ricorda niente" ha un problema di diario; uno che risponde ma sbaglia i comandi `gog` ha un problema di cassetta; uno che risponde ma non manda più il digest delle 7:30 ha un problema di agenda.

In forma di albero, la diagnosi dei primi cinque minuti è questa:

```text
L'agente non risponde
│
├─ Il computer è acceso e in rete?
│    no → accendi / riconnetti. Spesso finisce qui.
│
├─ openclaw status dice "running"?
│    no → openclaw gateway start
│
├─ openclaw channels status: tutto connesso?
│    no → openclaw channels login \
│           --channel telegram
│
├─ Risponde in TUI ma non sul canale?
│    sì → il problema è il canale, non l'agente
│
└─ Tutto verde ma resta muto?
     → openclaw logs --follow
     → openclaw doctor
```

Stampalo, fotografalo, mettilo nel cassetto. È il runbook che userai più spesso in assoluto.

### I cinque minuti di diagnosi, comando per comando

Vediamo l'albero in azione sul caso di apertura: Polly muta alle 7:40.

**Passo 1 — il computer.** Sembra offensivo scriverlo, ma è la causa numero uno: il Mac mini è andato in sleep dopo un aggiornamento di macOS che ha resettato le impostazioni di risparmio energetico, oppure il router ha riavviato il Wi-Fi alle 4 di notte. Se hai configurato l'accesso remoto (sezione successiva), un ping basta a capirlo:

```bash
ping -c 3 macmini.local
```

**Passo 2 — il Gateway.** Connesso alla macchina, chiedi lo stato:

```bash
openclaw status
```

Le risposte possibili sono due. `running` significa che il processo è vivo e si passa al passo 3. `stopped` significa che il Gateway è morto — crash, riavvio del computer senza riavvio automatico, aggiornamento interrotto — e la cura è ripartire:

```bash
openclaw gateway start
```

**Passo 3 — i canali.** Gateway vivo ma agente muto su Telegram? Lo stato dei canali dice se il problema è lì:

```bash
openclaw channels status
```

Un canale `disconnected` con il Gateway `running` indica quasi sempre credenziali scadute o revocate: il token del bot Telegram rigenerato per errore da @BotFather, la sessione WhatsApp invalidata dopo troppi giorni offline. Si ripara ricollegando il canale con `openclaw channels login --channel <nome>`.

**Passo 4 — l'agenda.** Se l'agente risponde ma "ha saltato un appuntamento" — il digest non arrivato è esattamente questo — il sospettato è un cron:

```bash
openclaw cron list
```

Guarda due cose: che il job esista ancora e che l'ultima esecuzione (`last run`) sia recente. Un cron che non scatta da giorni con lo schedule giusto è spesso vittima del cambio di **ora legale** (in inglese DST, daylight saving time): se il job è definito senza timezone esplicita, lo spostamento delle lancette può farlo scattare un'ora prima, un'ora dopo, o mai. Il [Capitolo 18](../PARTE-VII-Uso-avanzato/18-cron-job-e-automazioni-avanzate.md) tratta i cron in profondità.

**Passo 5 — log e dottore.** Se tutto è verde ma l'agente resta muto, servono gli strumenti pesanti:

```bash
openclaw logs --follow
openclaw doctor
```

Il primo mostra in tempo reale cosa sta facendo (o non facendo) il Gateway: errori di autenticazione verso il provider LLM, rate limit, eccezioni nelle skill. Il secondo esegue una batteria di controlli automatici su config, credenziali, permessi e versioni, e per molti problemi propone direttamente la riparazione con `openclaw doctor --fix`.

**(#) Debug:** un sintomo subdolo è l'agente che risponde ai messaggi ma ha l'heartbeat silenzioso: nessun controllo proattivo, nessun digest, nessuna iniziativa. In `openclaw logs --follow` cerca le righe heartbeat: se non compaiono ogni 30 minuti (il default), verifica che HEARTBEAT.md esista nel workspace e che non sia stato compromesso da un edit dell'agente stesso.

**(i) Pro tip:** la diagnosi più economica è quella che non devi fare tu. Un servizio di uptime monitoring gratuito (UptimeRobot, Better Stack — vedi Appendice E) che pinga la macchina ogni cinque minuti ti avvisa che qualcosa è giù prima che te ne accorga dal silenzio dell'agente.

### Accesso remoto: riparare senza monitor né tastiera

Tutto quanto sopra presuppone di poter aprire un terminale sulla macchina dell'agente. Se OpenClaw gira su un Mac mini headless — senza monitor, tastiera né mouse, com'è tipico — l'accesso remoto non è un optional: è l'unico modo di curarlo.

Su Mac la configurazione richiede due minuti, **da fare il giorno dell'installazione**, non il giorno del guasto: Impostazioni di Sistema → Generali → Condivisione, e qui attivi due voci. **Condivisione Schermo** (Screen Sharing) ti dà il desktop remoto: dal laptop, nel Finder, Vai → Connessione al server e inserisci `vnc://macmini.local` (o l'IP della macchina). **Accesso remoto** (Remote Login) ti dà SSH, cioè il terminale:

```bash
ssh tuo-utente@macmini.local
```

Per il 90% delle riparazioni basta SSH: i comandi del runbook sono tutti da terminale. Lo Screen Sharing serve nei casi in cui devi interagire con la GUI — un dialogo di macOS che blocca tutto, un browser da sbloccare, un aggiornamento di sistema in attesa di click.

Entrambe le soluzioni funzionano senza configurazione finché laptop e Mac mini sono sulla stessa rete. Per intervenire da fuori casa — sei in vacanza e Polly è muta — la strada giusta è **Tailscale**, la VPN leggera già incontrata nel [Capitolo 3](../PARTE-II-Installazione/03-scegliere-dove-installare-openclaw.md) (sezione «Accesso sicuro: niente porte aperte»): crea una rete privata tra i tuoi dispositivi e ti permette di fare SSH al Mac mini da qualsiasi posto, senza aprire porte sul router. Se l'agente gira su un VPS, l'accesso è SSH per definizione e il discorso è già stato fatto: la configurazione completa è nel [Capitolo 19](../PARTE-VII-Uso-avanzato/19-deploy-su-vps-e-infrastruttura-cloud.md).

**(!) Attenzione:** l'accesso remoto sicuro passa da SSH o Tailscale, mai dall'esposizione diretta del Gateway. La porta 18789 (il control plane WebSocket) non va mai aperta sul router o sul firewall "per comodità": chiunque la raggiunga controlla il tuo agente. Se l'hai fatto, chiudila e considera l'istanza compromessa (vedi [Capitolo 13](../PARTE-V-Sicurezza-costi/13-sicurezza-la-guida-che-devi-leggere.md)).

### Prevenire è meglio che diagnosticare

Riguarda l'albero di diagnosi: il primo ramo — computer in sleep o spento — è anche la causa più frequente in assoluto. Ed è interamente prevenibile, con dieci minuti di configurazione il giorno dell'installazione.

Su un Mac headless la prima mossa è dire al sistema di non addormentarsi mai e di riaccendersi da solo dopo un blackout:

```bash
# never sleep, restart after power failure
sudo pmset -a sleep 0
sudo pmset -a autorestart 1
```

Le stesse opzioni esistono in Impostazioni di Sistema → Energia, ma il terminale ha un vantaggio: `pmset -g` ti mostra in un colpo la configurazione corrente, ed è il controllo da rifare **dopo ogni aggiornamento maggiore di macOS** — gli update di sistema ogni tanto resettano le impostazioni di risparmio energetico, ed è esattamente il guasto della scena di apertura.

La seconda mossa è assicurarsi che il Gateway riparta da solo quando la macchina si riavvia: su Mac, l'app o il comando di avvio di OpenClaw tra gli elementi di login dell'utente dedicato; su Linux e VPS, una unit systemd — la configurazione completa è nel Capitolo 19. Il test è banale e va fatto una volta: riavvia la macchina e cronometra dopo quanto l'agente risponde su Telegram senza che tu abbia toccato nulla. Se la risposta è "mai", hai appena trovato un guasto futuro a costo zero.

### "Chiedi di ripararsi": l'agente è il primo tecnico di se stesso

C'è una categoria di guasti che non richiede nemmeno il terminale: quelli in cui l'agente risponde, ma si comporta male. Sbaglia account email, ignora una skill, ha dimenticato una preferenza, un cron produce risultati strani. In questi casi il primo tecnico da chiamare è l'agente stesso: ha accesso ai propri file, ai propri cron e ai propri log, e ispezionarli è un task come un altro.

Una conversazione reale, via Telegram, suona così:

> **Tu:** Il digest di stamattina non è arrivato. Ispeziona i tuoi cron e dimmi cosa è successo.
>
> **Polly:** Ho controllato. Il cron `morning-digest` esiste ed è attivo, ma l'ultima esecuzione risale a 3 giorni fa. Lo schedule è `30 7 * * *` senza timezone esplicita: col passaggio all'ora legale potrebbe essere il problema. Vuoi che aggiunga `timezone: Europe/Rome` e faccia un test?
>
> **Tu:** Sì, procedi e mandami il digest di prova.

Lo stesso schema funziona per la cassetta degli attrezzi ("Cosa c'è nel tuo TOOLS.md? C'è qualcosa di obsoleto da aggiornare?") e per la personalità ("Scrivi nel tuo SOUL.md che non devi mai inviare email senza farmele leggere"). L'agente che si auto-ripara è uno dei momenti più sorprendenti della convivenza con OpenClaw — ed è anche il motivo per cui la manutenzione ordinaria costa così poco tempo.

Due avvertenze, però. La prima: l'auto-diagnosi funziona solo se l'agente risponde — se è muto, sei nel runbook della sezione precedente, e nessun prompt può aiutarti. La seconda: l'agente può sbagliare la diagnosi con la stessa sicurezza con cui sbaglia qualsiasi altra cosa. Se ti dice "ho sistemato il cron" e il giorno dopo il digest non arriva di nuovo, smetti di chiedere a lui e verifica con i tuoi occhi (`openclaw cron list`). Fidarsi del paziente che si autocertifica guarito non è medicina, è ottimismo.

**(i) Pro tip:** rendi l'auto-ispezione un'abitudine, non un'emergenza: un cron settimanale che chiede all'agente di controllare i propri cron, lo stato delle skill e le dimensioni della memoria, e di mandarti un rapporto di una riga. I dettagli su come costruirlo sono nel Capitolo 18.

### Claude Code come "medico" dell'agente

Quando l'agente è troppo confuso per auto-ripararsi ma il problema è chiaramente nei suoi file — configurazione corrotta, workspace incoerente dopo un update, file canonici pasticciati da un esperimento — lo strumento giusto è un secondo AI che operi il primo. Nella community lo chiamano "il medico": in pratica, Claude Code (o un tool equivalente) aperto sulla cartella di OpenClaw.

La procedura è questa. Per prima cosa **fai un backup** (sezione più avanti): mai operare un paziente senza poterlo riportare allo stato precedente. Poi, sulla macchina dell'agente (anche via SSH):

```bash
cd ~/.openclaw
claude
```

Claude Code vede così l'intera anatomia: `config.yaml`, i workspace, i cron, i log. Il contesto che gli serve e che non ha sono le convenzioni di OpenClaw: dagli in pasto le due pagine giuste della documentazione ufficiale, cioè la guida di **troubleshooting** e la **reference di configurazione** del Gateway (titoli esatti e indirizzi in Appendice E) — copiandole nel prompt o salvandole come file `docs-troubleshooting.md` e `docs-config.md` nella cartella, così può leggerle da solo.

Il prompt di apertura che funziona meglio è descrittivo e prudente:

> **Prompt pronto (per Claude Code, non per l'agente):**
> "Questa cartella è l'installazione OpenClaw del mio agente personale. Sintomo: [descrivi: es. 'dopo openclaw update il Gateway parte ma Telegram resta disconnected']. Ho allegato la documentazione ufficiale di troubleshooting e configurazione. Leggi config.yaml e i log recenti in logs/, formula una diagnosi e proponi le correzioni **senza applicarle**: voglio rivedere ogni modifica prima. Non toccare credentials/ e auth.token."

Il vincolo "proponi senza applicare" non è pignoleria: un medico che opera senza consenso è esattamente il tipo di rischio che il Capitolo 13 ti ha insegnato a non correre. Rivedi le modifiche proposte, applicale, riavvia con `openclaw gateway restart` e verifica con `openclaw doctor`.

**(!) Attenzione:** usare Claude Code per riparare i file di OpenClaw è un uso normale della tua sottoscrizione Claude: il ban di Anthropic del 4 aprile 2026 (vedi [Capitolo 14](../PARTE-V-Sicurezza-costi/14-gestire-i-costi-senza-sorprese.md)) riguarda l'uso delle sottoscrizioni come motore LLM *dentro* OpenClaw, non l'editing dei suoi file dall'esterno.

### Quando smettere di riparare

C'è un ultimo gradino nella scala dell'escalation, e nominarlo esplicitamente ti farà risparmiare serate intere: **smettere di riparare**. La regola pratica: se dopo trenta minuti di runbook, log e medico non hai una diagnosi — non una soluzione, proprio una *diagnosi* — la strada più rapida non è insistere, è reinstallare pulito e ripristinare l'ultimo backup. Con la procedura di ripristino testata della sezione sul backup, sono venti minuti a esito certo, contro ore di tentativi a esito ignoto.

Prima di farlo, sposta la cartella malata da parte (`mv ~/.openclaw ~/.openclaw.broken`) invece di cancellarla: è l'autopsia. Quando l'agente è di nuovo vivo, con calma, puoi darla in pasto al medico per capire cosa era successo — o buttarla e non pensarci più. Accanirsi sulla riparazione è un istinto da sistemista; avere backup testati serve esattamente a non doverlo seguire.

### Aggiornare senza farsi male

OpenClaw evolve in fretta — le versioni seguono il calendario, `2026.4.x`, `2026.5.x` — e gli aggiornamenti portano patch di sicurezza che non vuoi saltare. Il comando è uno:

```bash
openclaw update
```

Ma il comando è la parte facile. La disciplina che evita i guai è attorno: **prima** dell'update leggi il changelog sul repository GitHub cercando le righe marcate `[breaking]` e `[security]` — le prime ti dicono cosa dovrai cambiare a mano, le seconde perché non puoi rimandare. **Subito prima** dell'update fai un backup (un comando, vedi sotto): è il tuo pulsante "annulla". **Dopo** l'update lancia `openclaw doctor --fix`, che intercetta e ripara automaticamente gli schema mismatch della configurazione, e verifica che i canali siano su e che l'agente risponda — il Capitolo 5 fornisce uno script `verify-install.sh` che fa tutto in un colpo.

E scegli il momento: mai aggiornare cinque minuti prima di un cron importante o uscendo di casa. L'aggiornamento giusto è quello fatto quando hai mezz'ora davanti per accorgerti che qualcosa si è rotto e ripararlo con calma.

### Backup: cosa salvare, quanto spesso, e la prova del ripristino

Tutto ciò che il tuo agente è — identità, memoria, configurazione, credenziali — vive in **un'unica cartella**: `~/.openclaw/`. Non c'è un database nascosto, non c'è stato nel cloud. Questa è la mappa di cosa contiene e di cosa è davvero critico:

```text
~/.openclaw/
├── config.yaml       # config Gateway: CRITICO
├── credentials/      # credenziali canali: CRITICO
├── auth.token        # token control plane
├── workspace/        # scrivania + memoria: CRITICO
├── workspace-polly/  # idem, per ogni agente
├── sessions/         # sessioni (ricostruibili)
├── channels/         # stato canali (ricostruibile)
└── logs/             # log (sacrificabili)
```

I tre elementi marcati critici sono insostituibili: la configurazione rappresenta ore di messa a punto, le credenziali sono le chiavi dei canali, e i workspace contengono ciò che nessun reinstall può ridarti — la memoria, la personalità, i mesi di note giornaliere del tuo agente. Log e sessioni invece si rigenerano da soli: perderli costa zero.

Il comando di backup è quello già visto nel Capitolo 5, e la forma giusta include sempre i workspace:

```bash
openclaw backup create \
  --output ~/Backups \
  --include-workspace \
  --rotate 8
```

Produce un archivio `openclaw-backup-YYYY-MM-DD-HHMM.tar.gz` e conserva gli ultimi otto. La frequenza giusta: **settimanale automatico** (un cron di sistema la domenica alle 3, come nel Capitolo 5) più **uno manuale prima di ogni update**. E l'archivio deve finire *fuori* dalla macchina dell'agente — disco esterno, NAS, cloud — perché un backup sullo stesso disco che muore non è un backup, è un epitaffio.

Poi c'è la parte che quasi tutti saltano e che è l'unica che conta: **provare il ripristino**. Un backup non testato è una speranza, non un'assicurazione. La procedura completa, da eseguire almeno una volta (e idealmente ogni tre mesi):

1. Su una macchina di prova — o sulla stessa, dopo aver
   spostato altrove la cartella corrente — installa
   OpenClaw alla **stessa versione** del backup.
2. Ferma il Gateway: `openclaw gateway stop`.
3. Ripristina l'archivio:

```bash
openclaw backup restore \
  ~/Backups/openclaw-backup-2026-05-31-0300.tar.gz
```

4. Lancia `openclaw doctor` e correggi eventuali
   segnalazioni.
5. Riavvia: `openclaw gateway start`.
6. Manda un messaggio di prova e fai la domanda di
   verità: "cosa ci siamo detti la settimana scorsa?"
   Se risponde ricordando, la memoria c'è e il
   ripristino è completo.

Cronometra l'esercizio la prima volta: sapere che "da zero a Polly viva" sono venti minuti trasforma ogni futuro disastro da emergenza a fastidio.

**(!) Attenzione:** l'archivio di backup contiene `credentials/` e `auth.token`: chi lo possiede può impersonare il tuo agente su tutti i canali. Trattalo come tratteresti un portafoglio di password — storage cifrato, mai in una cartella condivisa o su un repo Git.

### Il workspace sotto Git: il tagliando continuo

Il backup fotografa tutto periodicamente; per la parte più viva dell'agente — il workspace — c'è uno strumento complementare e più fine, promesso nel Capitolo 2: **Git**. Il workspace è solo testo, ed è il candidato perfetto al versionamento:

```bash
cd ~/.openclaw/workspace-polly
git init
printf "attachments/\n.openclaw/\n" > .gitignore
git add -A
git commit -m "polly: baseline"
```

Il `.gitignore` esclude gli allegati scaricati dai canali (pesanti e rigenerabili) e lo stato interno. Da qui in poi, un commit ogni tanto — dopo un ritocco al SOUL.md, dopo una settimana densa, prima di un esperimento — e ottieni tre cose che il backup non dà. Primo, il **diff**: `git diff` ti mostra esattamente cosa l'agente ha cambiato nei propri file, riga per riga — il modo più concreto di "vederlo crescere" e di accorgerti se ha scritto nel posto sbagliato. Secondo, il **rollback chirurgico**: l'agente ha pasticciato il SOUL.md? `git checkout SOUL.md` e torna quello di ieri, senza toccare il resto. Terzo, la **copia off-site dell'anima**: un repo remoto *privato* come specchio, così la parte insostituibile dell'agente vive anche fuori casa.

**(!) Attenzione:** sotto Git va il *workspace*, mai la radice `~/.openclaw/`: `credentials/`, `auth.token` e ogni `.env` non devono finire in nessun repository, nemmeno privato. Se per errore hai committato un segreto, rigeneralo subito: rimuoverlo dalla history non basta.

### Il tagliando settimanale: cinque minuti che evitano tutto il resto

Quasi tutto questo capitolo descrive cosa fare *dopo* un guasto. L'ultima abitudine da costruire lo rende in gran parte inutile: un tagliando fisso, cinque minuti, stesso giorno ogni settimana — il sabato mattina col caffè funziona bene. Il giro completo:

1. `openclaw doctor` — zero warning?
2. `openclaw cron list` — tutti i job sono
   scattati quando dovevano?
3. Il backup di domenica scorsa **esiste davvero**
   nella cartella di destinazione? (Guardarlo, non
   presumerlo.)
4. `openclaw cost report --since 7d` — la spesa è
   in linea con la settimana tipo? (Vedi Capitolo 14:
   un costo che raddoppia senza motivo è un sintomo,
   non una bolletta.)
5. Un messaggio all'agente: come da Pro tip della
   sezione sull'auto-riparazione, può fare lui
   l'ispezione interna — il prompt qui sotto è
   pensato esattamente per questo.

Cinque minuti a settimana sembrano burocrazia finché non li confronti con l'alternativa: accorgerti dei problemi quando l'agente è muto, il backup non esiste e la spesa è triplicata da dieci giorni.

**(i) Pro tip:** la manutenzione fin qui è meccanica — tenere l'agente *vivo*. Tenerlo *bravo* è un mestiere diverso: la cura della memoria (cosa ricordare, cosa dimenticare, quando compattare) e l'affinamento della personalità sono il tema del [Capitolo 16](./16-ottimizzare-la-qualita-delle-risposte.md), dove trovi anche il significato preciso di termini come "knowledge graph" usati nel prompt qui sotto.

**Prompt pronto:**
> "Fai una diagnosi completa di te stesso e dimmi se sei in salute. Esegui: (1) `openclaw status` e `openclaw doctor` e interpretane i risultati, (2) lista i tuoi cron attivi (`openclaw cron list`) e segnala quelli che non scattano da più di 48 ore, (3) verifica con `openclaw channels status` che tutti i canali siano connessi, (4) controlla le dimensioni del knowledge graph e segnala se c'è materiale obsoleto da archiviare. Riporta tutto in un singolo messaggio breve."

## Errori comuni e come risolverli

**Sintomo:** l'agente non risponde da ore.
Causa: computer in sleep, connessione caduta o Gateway crashato.
Fix: `openclaw status` e `openclaw channels status`; se il Gateway è giù, `openclaw gateway restart`.

**Sintomo:** un cron non scatta più.
Causa: cambio di ora legale (DST) con timezone non esplicita, o file di configurazione modificato.
Fix: `openclaw cron list` per verificare schedule, timezone e ultima esecuzione; chiedere all'agente "ispeziona i tuoi cron"; aggiungere `timezone: Europe/Rome` al job.

**Sintomo:** errore "out of memory" o risposte tronche.
Causa: contesto troppo grande, memoria stantia mai compattata.
Fix: pulire le note obsolete, archiviare conversazioni antiche, limitare la finestra di memoria (tecniche nel Capitolo 16).

**Sintomo:** l'aggiornamento rompe configurazioni esistenti.
Causa: breaking changes non letti nel changelog.
Fix: leggere il CHANGELOG (tag `[breaking]`) prima di `openclaw update`; backup immediatamente prima; dopo, `openclaw doctor --fix`; nel peggiore dei casi, `openclaw backup restore`.

**Sintomo:** il ripristino di un backup fallisce o produce errori di schema.
Causa: versione di OpenClaw diversa tra backup e installazione.
Fix: ripristinare sulla **stessa versione** del backup, poi eventualmente aggiornare; `openclaw doctor --fix` per gli schema mismatch residui.

**Sintomo:** l'agente "muore" ogni notte più o meno alla stessa ora e resuscita quando tocchi il computer.
Causa: sleep di sistema attivo, spesso ri-abilitato da un aggiornamento di macOS.
Fix: `pmset -g` per verificare; `sudo pmset -a sleep 0` per disattivare; ricontrollare dopo ogni update di sistema.

**Sintomo:** Screen Sharing o SSH non raggiungono più il Mac mini.
Causa: IP cambiato dal router, o nome `.local` (mDNS) non risolto sulla rete.
Fix: usare l'IP diretto al posto del nome; soluzione definitiva: Tailscale, che dà un indirizzo stabile (Capitolo 3).

## Checklist di fine capitolo

- [ ] So fare diagnosi rapida (`openclaw status`, `openclaw doctor`)
- [ ] Accesso remoto configurato (Screen Sharing/SSH/Tailscale) per intervenire da fuori
- [ ] Backup periodico della cartella `.openclaw/` impostato
- [ ] So aggiornare con `openclaw update` dopo aver letto il changelog
- [ ] Ho un "medico digitale" (Claude Code o altro) per debug profondi
- [ ] Ho eseguito (e cronometrato) almeno una prova di ripristino completa
- [ ] Il workspace è sotto Git, con i segreti fuori dal repository
- [ ] Sleep disattivato e riavvio automatico configurato sulla macchina dell'agente
- [ ] Tagliando settimanale fissato (stesso giorno, cinque minuti)

## Link e risorse utili

- [Documentazione ufficiale](https://docs.openclaw.ai) — reference dei comandi `openclaw status`, `doctor`, `update`
- [Repository GitHub](https://github.com/openclaw/openclaw) — changelog e issue tracker per i breaking changes
- "General troubleshooting" (OpenClaw Docs) — la guida ufficiale da dare in pasto al "medico"
- "What Does `openclaw doctor --fix` Do?" (Stack Junkie) — ogni warning del doctor spiegato
- "OpenClaw Backup Guide" (LumaDock) — backup di stato, impostazioni e memoria
- "Self-host a local AI stack" (Tailscale) — il pattern di accesso remoto consigliato

Per l'elenco completo delle fonti del libro (con gli URL estesi), vedi [Appendice E](../Appendici/E-risorse-e-link-utili.md).

---

[← Capitolo 14](../PARTE-V-Sicurezza-costi/14-gestire-i-costi-senza-sorprese.md)  ·  [Indice](../README.md)  ·  [Capitolo 16 →](./16-ottimizzare-la-qualita-delle-risposte.md)
