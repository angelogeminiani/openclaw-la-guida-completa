# Capitolo 6 — Configurare Telegram (e altri canali) [★]

## Cosa imparerai

- Perché il canale di comunicazione è una scelta architetturale, e cosa cambia davvero fra una piattaforma e l'altra.
- Come creare un bot Telegram con @BotFather in cinque minuti, fra token, gruppi, mention gating e novità della Bot API 9.5 e 10.0.
- Quando scegliere WhatsApp via Baileys (rischio ban) e quando la Cloud API ufficiale, dopo la stretta Meta del 15 gennaio 2026.
- Come configurare Slack (Bolt + Socket Mode) e Discord (privileged intents) con scope minimi, e iMessage col plugin nativo (e perché BlueBubbles è solo legacy).
- Come instradare più canali verso lo stesso agente, unificando la sessione quando serve, con la `dmPolicy` a decidere chi può scrivergli.

## Prerequisiti

Aver completato l'installazione del [Capitolo 5](./05-installazione-step-by-step.md): agente avviato, Gateway sulla porta `18789`, `openclaw doctor` senza errori bloccanti. Tieni il **password manager** a portata di mano — useremo token sensibili — e uno **smartphone** con Telegram. Per WhatsApp via Baileys serve anche un **secondo numero di telefono** (eSIM, numero virtuale o SIM dedicata): non si usa il numero personale.

Una verifica veloce prima di iniziare:

```bash
openclaw channels list
openclaw gateway status
```

Il primo comando mostra i canali **configurati** con il loro stato (a installazione fresca la lista è vuota o quasi); l'elenco dei canali *supportati* cambia di mese in mese, e la fonte di verità è `docs.openclaw.ai/channels`. Il secondo conferma che il Gateway è in ascolto.

## Contenuto principale

Sono le 19:00 di un mercoledì. Il digest serale è pianificato, l'agente è acceso, il modello risponde. Manca una decisione: su quale chat ti scrive? Telegram si configura in cinque minuti, WhatsApp Business richiede tre giorni di verifica Meta, Baileys dura 2-8 settimane prima del primo ban. Questo capitolo ti porta dalla scelta del canale al primo "ciao, ti sento".

**(i) Pro tip:** comandi e nomi di canale si riferiscono alla serie `2026.x` di OpenClaw (primavera 2026): prima di copia-incollare verifica con `openclaw --version`. Le piattaforme esterne cambiano ancora più in fretta.

### TL;DR — Telegram in cinque minuti

I tre comandi essenziali; il resto del capitolo spiega *perché* esistono e cosa fare quando qualcosa si inceppa.

```bash
# 1. crea il bot in @BotFather sul telefono
#    /newbot -> nome -> username_bot -> copia il token

# 2. collega il token al Gateway
openclaw channels login --channel telegram

# 3. verifica che parli
openclaw channels status --channel telegram
```

Apri Telegram, cerca il tuo bot, premi `/start`. Se risponde entro pochi secondi, salta alla sezione *Gruppi e mention gating*; altrimenti prosegui.

### Costi e tempi a colpo d'occhio

Prima di entrare nel dettaglio, una mappa decisionale (costi per uso personale o piccolo team, ~500-2000 messaggi/mese).

| Canale | Tempo setup | Costo/mese |
|---|---|---|
| Telegram | 5 min | 0 € |
| WhatsApp Baileys | 15 min | 0 € |
| WhatsApp Cloud | 1-3 giorni | 5-30 € |
| Slack | 10 min | 0 € |
| Discord | 10 min | 0 € |
| iMessage nativo | 20 min | 0 € |

Sul fronte rischio: i canali ufficiali (Telegram, Slack, Discord, WhatsApp Cloud) sono a rischio basso; Baileys è ad alto rischio (ban in 2-8 settimane); iMessage a rischio medio (Mac sempre acceso, API non documentate). Lettura rapida: parti da **Telegram**; aggiungi **Slack o Discord** per il team; **WhatsApp Cloud API** solo per un caso business concreto. Il resto è ottimizzazione.

### Perché il canale conta più di quanto sembri

Quando si sceglie il canale la tentazione è guardare solo a "quale chat uso più spesso io". Mancano però tre dimensioni. La prima è **chi controlla il canale**: Telegram ha una Bot API documentata, gratuita e stabile dal 2015; WhatsApp è l'opposto, con Meta in controllo unilaterale e tool non ufficiali in una zona grigia sempre più stretta. La seconda è il **modello di interazione** (1-a-1, gruppo, broadcast, server multi-canale): un agente perfetto in DM diventa invadente in un gruppo senza *mention gating*. La terza è **dove vivono i tuoi interlocutori**: una freelance italiana usa WhatsApp con i clienti, Telegram con la community, Slack con l'agenzia — servono più canali, convergenti su un singolo agente.

OpenClaw risolve il terzo punto nativamente: il Gateway instrada i messaggi di più piattaforme nello stesso *session store*. Attenzione però: di default ogni coppia canale+utente ha la **propria** sessione (`per-channel-peer`) — se inizi su WhatsApp e continui su Telegram, l'agente *non* ricorda il filo, salvo *session unification* con identità mappate (sezione "Multi-canale").

**(i) Pro tip:** un canale per volta: lavoraci una settimana, poi aggiungi il successivo. Tre canali configurati male sono peggio di uno configurato bene.

### Telegram — il punto di partenza consigliato

Telegram è il canale più semplice da configurare, ed è quello che documentazione ufficiale e guide indipendenti suggeriscono di provare per primo: @BotFather genera token in 30 secondi, senza OAuth, approvazioni, scope o review.

#### Creare il bot con @BotFather

Apri Telegram (app o desktop) e cerca `@BotFather`, il bot ufficiale per gestire altri bot (spunta blu, username `BotFather` esatto). Avvia con `/start`, poi:

```
/newbot
```

BotFather chiede due informazioni: il **nome visibile** (spazi e maiuscole ammessi, es. "Polly Personal Assistant") e lo **username**, che deve terminare per `bot` o `_bot`, è univoco a livello globale e diventa l'URL del bot (`t.me/polly_pa_bot`). Sceglilo coerente con il nome dato all'agente nell'`IDENTITY.md` del Capitolo 5.

Quando lo username è accettato, BotFather risponde così:

```
Use this token to access the HTTP API:
8123456789:AAH9q2Wx3vK7nF8mP4...
```

Quella stringa **è il token**, e vale come una password: chi la possiede può scrivere, leggere e postare come fosse il bot. Va dritta nel password manager (`OpenClaw → Telegram → Polly bot token`), **mai in file di testo, chat o screenshot**.

**(!) Attenzione:** un token in un commit Git pubblico viene trovato in pochi minuti (i bot scanner cercano la pattern `\d{9,10}:[A-Za-z0-9_-]{35}`). Rigeneralo subito con `/revoke` in @BotFather: il traffico sul vecchio token è da considerare compromesso.

Mentre sei in @BotFather, registra con `/setcommands` i comandi mostrati nel menù della chat (almeno `/start`, `/status`, `/help`) e cura descrizione e avatar (`/setdescription`, `/setabouttext`, `/setuserpic`).

#### Collegare il token a OpenClaw

Dal terminale dove gira il Gateway, lancia:

```bash
openclaw channels login --channel telegram
```

Il wizard chiede il token (mascherato), testa la connessione contro `api.telegram.org`, registra il bot in `~/.openclaw/config.yaml` (sezione `channels.telegram`) e attiva il *long polling*.

Se preferisci la via dichiarativa, imposta `channels.telegram.botToken` e `channels.telegram.enabled` con `openclaw config set`, poi `openclaw gateway reload` per ricaricare la config senza riavviare il processo. Se non parte, `openclaw logs --follow` mostra il motivo (token malformato, conflitto di porte, errore di rete).

#### Il primo test di andata e ritorno

Cerca su Telegram lo username scelto, apri la chat e premi `/start`. Con la skill `gog` o `personal-assistant` installata l'agente risponde con un benvenuto; altrimenti scrivi:

> Ciao, mi senti?

Se la risposta arriva entro qualche secondo, il canale è operativo.

**(#) Debug:** se non arriva niente, controlla nell'ordine: (1) `openclaw channels status` indica `telegram: connected`? (2) `openclaw logs --follow` mostra messaggi in ingresso? (3) il bot esiste su `https://t.me/<username>`? (4) c'è un secondo Gateway in long-polling sullo stesso token? Telegram permette **un solo** consumatore per token — spegni quello vecchio.

#### Gruppi e mention gating

Aggiungere il bot a un gruppo è banale (*Info → Aggiungi membro → @username_del_bot*). Il problema è l'opposto: di default il bot reagisce a *qualunque* messaggio — in una chat famiglia di otto persone diventa intollerabile in mezza giornata.

Il *mention gating* risolve il problema. Si configura a livello di OpenClaw, non di Telegram: "in questa chat di gruppo intervieni solo se menzionato (`@polly_bot`) o se il messaggio comincia con un comando (`/...`)". La configurazione tipica:

```yaml
channels:
  telegram:
    groups:
      mentionGating: true
      replyTags: true
      chunking:
        enabled: true
        maxChars: 3500
```

Tradotto: parla solo se menzionato, replica col *reply tag* al messaggio originale, spezza le risposte oltre 3.500 caratteri (il limite Telegram è 4.096).

Lascia anche il default di `/setprivacy` in @BotFather (`enabled`, riceve solo le menzioni): è una difesa in più, indipendente dal mention gating di OpenClaw.

#### Cosa è cambiato con la Bot API 9.5 e 10.0

Telegram aggiorna la Bot API in media ogni 4-6 settimane; tre cambiamenti del 2026 vale la pena conoscerli.

La **Bot API 9.5** (1° marzo 2026) ha generalizzato `sendMessageDraft`, abilitando lo *streaming nativo*: l'agente scrive la risposta man mano, token per token, invece di lasciarti 12 secondi di silenzio sui modelli lenti come Opus 4.6. La 9.5 ha introdotto anche i *member tags*: etichette testuali (≤ 16 caratteri, senza emoji) per i membri di un gruppo ("admin", "ospite", "famiglia").

La **Bot API 10.0** (maggio 2026) ha aperto due scenari: la **comunicazione bot-to-bot** in contesti specifici (gruppi e business mode), che consente flussi multi-agente nativi senza dover passare dal filesystem condiviso interno; e il **granular access whitelist** via @BotFather o API, che limita a priori gli UID Telegram autorizzati a scrivere al bot — gli altri ricevono un "non disponibile". Per un agente personale è una difesa preziosa.

OpenClaw è stato il primo client a integrare lo streaming 9.5 (6 marzo 2026, cinque giorni dopo il rilascio). Si regola o disabilita nella sezione `channels.telegram.streaming` del config (`enabled`, `throttleMs`).

**(i) Pro tip:** se vedi risposte spezzate in modo strano nei gruppi, alza `throttleMs` da 250 a 500-800ms: lo streaming sub-secondo genera troppe notifiche per chi ascolta.

#### DM policy: chi può scrivere al bot

Tutti i canali condividono il pattern `dmPolicy`, che decide cosa succede quando uno *sconosciuto* scrive al bot per la prima volta:

- `pairing` (default consigliato): chi scrive deve presentarsi con un codice di accoppiamento, generato da te con `openclaw pair create`.
- `allowlist`: solo gli UID o numeri autorizzati nel config (`channels.telegram.allowlist: [123456, 234567]`).
- `open`: chiunque può scrivere. **Solo per bot pubblici progettati per esserlo** (es. assistente di vendita).
- `disabled`: il bot ignora i DM, risponde solo nei gruppi.

Per un agente personale: `pairing` su Telegram, `allowlist` su Slack/Discord. Mai `open` su un bot con accesso ai tuoi file o alla tua email.

### WhatsApp — il canale "naturale" ma pericoloso

WhatsApp è il sogno di chiunque viva in Italia — clienti, famiglia, fornitori sulla stessa app — ed è anche il canale più rischioso: Meta applica le proprie policy con rigore crescente. Le strade sono due: **Baileys** (libreria non ufficiale che parla il protocollo WhatsApp Web) e la **Cloud API ufficiale** (servizio Meta a pagamento per business).

#### Baileys: cosa è e perché è a rischio

Baileys è una libreria JavaScript open-source (WhiskeySockets) che implementa il protocollo WebSocket di WhatsApp Web: si linka come un browser via QR code e da lì invia e riceve messaggi sul numero collegato. Gratuita, semplice, supporta gruppi, media e voce — e oggi è contro i Terms of Service di WhatsApp. Nel 2025-2026 Meta ha intensificato il *fingerprinting* dei client non ufficiali: la community segnala vite medie di 2-8 settimane prima del ban permanente, che si estende all'identità del telefono (IMEI/IMSI) — una nuova SIM sullo stesso device non basta.

**(!) Attenzione:** con Baileys non collegare *mai* il numero personale. Usa un secondo numero (eSIM, VoIP con SMS, SIM dedicata): quando arriva il ban perdi un numero usa-e-getta, non dieci anni di chat con la tua famiglia.

Dal **15 gennaio 2026**, inoltre, una nuova policy AI di Meta vieta esplicitamente i chatbot AI "general-purpose" (ChatGPT, Claude, Gemini e simili) sulla piattaforma: non è una caccia automatizzata, ma è il fondamento contrattuale dei ban. Un agente riconducibile a un'azienda specifica (supporto, ordini, FAQ) rientra nell'eccezione esplicita; "un assistente personale general-purpose" è nella categoria a rischio.

#### Setup Baileys con OpenClaw

Se accetti il rischio, il setup è veloce col canale integrato:

```bash
openclaw channels login --channel whatsapp-baileys
```

Il comando stampa un QR code ASCII nel terminale. Sul telefono col numero secondario: WhatsApp → *Impostazioni* → *Dispositivi collegati* → *Collega un dispositivo* → inquadra il QR. Al *connected*, lo stato si controlla con:

```bash
openclaw channels status --channel whatsapp-baileys
```

Lo stesso comando rivela quando il link si rompe (WhatsApp scollega i dispositivi inattivi da 14 giorni o col traffico sospetto): rifai il QR scan. Se il numero è bannato, l'errore è `403 Forbidden: account banned` e nessun retry serve.

Tre regole per limitare il rischio: (1) **bassa frequenza** — niente burst, distanzia tutto di 30-60 secondi; (2) **scope ristretto** — solo i tuoi contatti (`dmPolicy: allowlist`); (3) **niente broadcast** — la *broadcast list* è il modo più rapido per farsi bannare in mezza giornata.

#### Cloud API ufficiale: l'unica strada a prova di ban

Se hai un caso d'uso *business* (azienda, freelance con partita IVA, e-commerce), la strada giusta è la **WhatsApp Business Cloud API**: a pagamento, con un *Business Service Provider* registrato (Twilio, MessageBird, 360dialog, Meta diretto) e verifica del numero, ma ufficiale e senza rischi. Per un **privato senza attività registrata** è di fatto inaccessibile — la verifica Meta richiede una partita IVA o un'azienda: le opzioni reali restano Baileys (coi rischi visti) o, meglio, un altro canale.

Il pricing è cambiato: dal **1° luglio 2025** Meta fattura *per-messaggio* (non più a conversazione), con tariffe per nazione del *destinatario* e per categoria. I messaggi **marketing** sono i più cari ($0,01–0,14, ~€0,01–0,13); **utility** e **authentication** costano l'80-90% in meno; le risposte **service** nella *customer service window* sono gratuite, come le *click-to-WhatsApp* per 72 ore. Per un supporto e-commerce italiano le utility costano centesimi a messaggio: poche decine di euro al mese.

OpenClaw espone il canale come `whatsapp-cloud`:

```bash
openclaw channels login --channel whatsapp-cloud
```

Il wizard chiede *Phone Number ID*, *WABA ID* (WhatsApp Business Account), *Permanent Access Token* dalla console Meta e URL del webhook, e genera un *verify token* da incollare nella console per validarlo.

**(i) Pro tip:** se non vuoi la console Meta (lunga, in inglese, UX da business platform di dieci anni fa), Twilio offre un'astrazione molto più semplice: piccolo *markup* sui messaggi, mezza giornata di configurazione risparmiata.

### Slack — per il lavoro di team

Slack è il canale per i team: un agente che vive in `#ops` o `#growth` e risponde quando menzionato cambia il ritmo del lavoro. OpenClaw lo integra via **Bolt + Socket Mode**, il pattern moderno consigliato da Slack: niente webhook pubblico, niente reverse proxy, niente porte aperte — il bot apre una WebSocket *outbound* e riceve gli eventi da lì.

#### Creare l'app Slack

Vai su `api.slack.com/apps`, *Create New App* → *From scratch*: nome dell'app (es. "Polly"), workspace di destinazione. Poi tre sezioni da configurare nell'ordine.

**Socket Mode**: attiva il toggle nella sezione omonima. Slack chiede di generare un *App-Level Token*: *Generate*, un nome (es. "openclaw-socket"), scope `connections:write`. Il token inizia con `xapp-...`: copialo subito nel password manager, è mostrato una sola volta.

**Bot Token**: su *OAuth & Permissions → Bot Token Scopes* aggiungi gli scope minimi. Per un agente standard:

- `chat:write` — inviare messaggi
- `app_mentions:read` — menzioni `@polly`
- `im:history`, `im:read`, `im:write` — DM
- `commands` — slash commands `/...`
- `files:read` — allegati
- `channels:history`, `groups:history` — solo se deve leggere i messaggi nei canali

Aggiunti gli scope, clicca *Install to Workspace*: Slack genera il *Bot User OAuth Token* che inizia con `xoxb-...` — di nuovo, password manager.

**Event Subscriptions**: attiva e aggiungi gli eventi da ricevere: `app_mention` (essenziale), `message.im` (DM), eventualmente `message.channels` per i canali pubblici.

**(!) Attenzione:** gli scope `*.history` danno accesso alla cronologia delle conversazioni, e gli IT manager seri li auditano. Parti dal minimo, aggiungi al bisogno: richiede di re-installare l'app, ma è veloce.

#### Collegare a OpenClaw

```bash
openclaw channels login --channel slack
```

Il wizard chiede i due token (`xapp-...` e `xoxb-...`) e il *Signing Secret* (su *Basic Information → App Credentials*). Poi:

```bash
openclaw channels status --channel slack
```

Atteso: `slack: connected (socket mode)`. Invita il bot in un canale (`/invite @polly`) e menzionalo: `@polly status`. Risponde in pochi secondi.

#### Slash commands e routing canali → agenti

Slack supporta gli *slash commands*: comandi globali (`/digest`, `/standup`, `/lead`) attivi anche fuori dai canali dove il bot è invitato. Si configurano nella sezione *Slash Commands*; OpenClaw li mappa a *intent*:

```yaml
channels:
  slack:
    slashCommands:
      - command: /digest
        intent: morning_digest
      - command: /standup
        intent: team_standup
        channels:
          allowlist: ["C0123456789"]  # only #team-ops
```

Nel multi-agente (vedi [Capitolo 12](../PARTE-IV-Multi-agente/12-comunicazione-e-coordinamento-tra-agenti.md)) puoi anche fare *channel binding*: il canale `#sales` parla con l'agente Sam, il canale `#support` con l'agente Holly, e così via. Tutti sullo stesso bot Slack, instradati dietro le quinte.

### Discord — per community, gaming, progetti laterali

Discord ha una logica diversa: Slack è per il lavoro asincrono di un team chiuso, Discord è la lingua franca di community pubbliche, open-source e gaming. Un agente in un server Discord può fare moderazione, FAQ, contenuti, supporto.

#### Privileged intents: il punto critico

Dal 2022 Discord limita l'accesso ai dati con i **Privileged Gateway Intents**: `GUILD_PRESENCES` (stato online), `GUILD_MEMBERS` (lista membri) e `MESSAGE_CONTENT` (testo dei messaggi). Per OpenClaw l'unico critico è **MESSAGE_CONTENT**: senza, il bot riceve solo metadati (chi, quando, dove), non il testo. Per attivarlo: `discord.com/developers/applications` → seleziona l'app → *Bot* → *Privileged Gateway Intents* → attiva *MESSAGE CONTENT INTENT* → *Save Changes*.

**Soglia dei 100 server**: sotto i 100 server attivi gli intent senza review; oltre, serve una *verification* manuale di 2-6 settimane. Per un bot personale non è un problema.

**(i) Pro tip:** dal 2024 Discord spinge le *application commands* come alternativa al `MESSAGE_CONTENT`: se l'agente lavora su comandi (`/ask`, `/summarize`, `/digest`), farne a meno riduce la compliance ed evita la verifica oltre i 100 server.

#### Creare il bot Discord

Su `discord.com/developers/applications`, *New Application*: nome, accetta i termini. Poi *Bot* → *Reset Token* (alla prima volta è *Add Bot*): il *Bot Token* va nel password manager. Infine *OAuth2* → *URL Generator*: scope `bot` e `applications.commands`, permission minime (`Send Messages`, `Read Message History`, `Use Slash Commands`). Discord genera un URL di invito: aprilo, scegli il server, autorizza.

Collegamento a OpenClaw:

```bash
openclaw channels login --channel discord
```

Token + application ID, conferma. Verifica scrivendo nel server: l'agente risponde.

### iMessage — l'ecosistema Apple [★★]

iMessage è ostico perché è chiuso: nessuna Bot API ufficiale Apple, nessun endpoint cloud. L'unico modo per pilotarlo è un **Mac fisico** dove iMessage è loggato, più un layer software che intercetti i messaggi.

OpenClaw supporta due strade. La prima è il **plugin nativo iMessage**, introdotto nel 2025 e diventato default nel 2026: legge i database SQLite di Messages.app, invia via AppleScript, gestisce immagini e tapback. Richiede macOS Sequoia 15.4+ e il *Full Disk Access* concesso a OpenClaw. È la scelta consigliata per ogni nuovo setup.

La seconda è **BlueBubbles**, server open-source usato storicamente per il bridging di iMessage verso Android/Linux/Windows (REST API). Funziona ancora, ma il progetto è fermo (ultima release: 16 maggio 2025) e la doc ufficiale OpenClaw lo indica come deprecato per i nuovi setup. Se l'hai già configurato continua a funzionare; se parti oggi, usa il plugin nativo.

```bash
openclaw channels login --channel imessage
# native plugin (default on macOS 15.4+)

openclaw channels login --channel imessage-bluebubbles
# legacy bridge, requires bluebubbles-server running
```

**(!) Attenzione:** Apple non garantisce stabilità sui database di Messages.app: aggiornamenti minori di macOS hanno già rotto il plugin nativo in passato. Tieni `openclaw update` aggiornato e controlla il changelog dopo ogni update di macOS.

### Gli altri canali in mezza pagina [★★]

Telegram, WhatsApp e Slack/Discord coprono il 95% dei casi. Per il resto, OpenClaw supporta una lunga coda di canali con lo stesso pattern: `openclaw channels login --channel <nome>` e credenziali della piattaforma. Tre meritano una nota.

**WeChat** è il canale necessario per utenti o clienti in Cina. Da **marzo 2026** Tencent ha un plugin ufficiale per OpenClaw (WeChat → *Impostazioni* → *Plugin* → *ClawBot*). Le restrizioni governative (vedi [Capitolo 21](../PARTE-VIII-Visione-futuro/21-ecosistema-openclaw.md)) impongono inferenza su modelli autorizzati dalla CAC: niente OpenAI o Anthropic, in pratica Kimi K2.5, MiniMax M2.5 o DeepSeek-V3.

**Microsoft Teams** è la scelta obbligata negli ambienti corporate Microsoft: passa per Bot Framework e Graph API e richiede l'approvazione del tenant da parte dell'IT.

**Signal** è il canale per chi tiene davvero alla privacy: si appoggia a `signal-cli` (CLI non ufficiale ma stabile, manutentore AsamK) in daemon mode, con link via QR. Setup tecnico, niente ecosistema bot: tipicamente un canale secondario.

Per gli altri, una riga ciascuno: **Matrix** si collega a un homeserver come client o appservice; **Google Chat** passa per Workspace; **Feishu** copre l'area APAC; **LINE** domina Giappone, Taiwan e Thailandia; **IRC** resta vivo nelle community open-source. Guide dedicate su `docs.openclaw.ai/channels`.

### Multi-canale: stesso agente, contesto condiviso

Lo stesso Gateway gestisce più canali sopra un unico *session store*: configuri Telegram, WhatsApp e Slack e lo stesso agente risponde su tutti e tre — e, con la *session unification*, con la stessa memoria. Visivamente:

```
   Telegram ─┐
   WhatsApp ─┼──► Gateway ──► Session Store
   Slack    ─┘    (router)    (memoria
                              condivisa)
```

I canali entrano nel Gateway con identità distinte (UID Telegram, numero WhatsApp, user ID Slack); il *router* le riconduce alla stessa sessione solo se la *unification* è attiva. La risposta esce dal canale da cui è arrivata la richiesta: niente cross-posting automatico. In pratica:

```bash
openclaw sessions list
# session_id   channel    last_seen
# s_a1b2c3     telegram   2 min ago
# s_d4e5f6     slack      1 hour ago
```

Le sessioni sono normalmente *per-canale + per-utente*; per farle convergere (es. "Polly sa che mi sono lamentato del traffico sia su WhatsApp che su Telegram") si configura la *session unification* sull'identità dell'utente:

```yaml
sessions:
  unification:
    enabled: true
    strategy: by-user-identity
```

L'unificazione richiede di aver mappato esplicitamente le identità al medesimo utente nel file `USER.md`: senza la mappa, Polly tratta le tre identità come tre persone diverse.

### Migrare da un canale all'altro

Capita spesso: si parte con Telegram, poi il team vive su Slack; o si lavora con Baileys finché un ban impone la Cloud API. Raramente è un *cutover* netto: i due canali convivono qualche settimana. Tre punti da non perdere di vista.

**Storico delle conversazioni.** OpenClaw archivia i messaggi *per sessione*, non per canale: lo storico non si trasferisce. Prima di chiudere il vecchio canale, chiedi all'agente un *briefing di passaggio* in `MEMORY.md` o nelle note giornaliere — chi sei, su cosa lavorate, le decisioni recenti: quello viaggia con la memoria persistente.

**Mappare le identità.** Se uso Telegram come UID `123456` e Slack come `U0ABCDEF`, l'agente vede *due persone diverse* — a meno che tu non glielo dica nel `USER.md` (o nella sezione *identities* del config):

```yaml
users:
  - id: <tuo-id-utente>
    identities:
      telegram: "123456"
      slack: "U0ABCDEF"
      whatsapp: "+39 3xx xxxxxxx"
```

Da quel momento le tre identità collassano sull'utente `<tuo-id-utente>` e la *session unification* funziona davvero.

**Cutover graduale.** Tieni il vecchio canale attivo due-quattro settimane, spostando un cron alla volta e verificando che tutto funzioni sul nuovo. Quando sei sicuro:

```bash
openclaw channels disable --channel whatsapp-baileys
# disconnects but keeps config

openclaw channels remove --channel whatsapp-baileys
# permanently removes config
```

`disable` è reversibile (`channels enable`); `remove` cancella la config e richiede di rifare il login.

### Sicurezza dei canali: cose da non dimenticare

Quattro regole valide per tutti i canali.

**Token nel password manager, mai in chiaro.** I file di config che contengono token (es. `~/.openclaw/secrets.env`) vanno protetti con `chmod 600` ed esclusi da ogni sincronizzazione cloud non cifrata.

**Webhook secrets dove servono.** WhatsApp Cloud, Slack e Teams firmano i payload con *signing secret* o *verify token*: senza, chiunque conosca il webhook URL può inviarti messaggi finti. OpenClaw verifica le firme, ma solo se il secret è nel config.

**Rotazione periodica.** Almeno una volta all'anno ruota i token senza scadenza: `/revoke` in BotFather, rigenerazione su Slack, *Reset Token* su Discord (rompe il bot finché non aggiorni la config). Segna la data in calendario.

**Mention gating e DM policy sempre.** Mai `dmPolicy: open` su un bot con accesso a tool sensibili; nei gruppi, mention gating sempre attivo: una notifica per ogni messaggio è il modo migliore per farsi disattivare in una settimana.

## Prompt pronti all'uso

Da incollare in chat con l'agente appena il primo canale (di solito Telegram) è collegato, per validare la configurazione.

**Prompt 1 — onboarding di un gruppo Telegram:**

> "Sto per aggiungerti a un gruppo Telegram famigliare di otto persone. Prima: (1) attiva `mentionGating` e `replyTags` sul canale Telegram, (2) imposta `chunking.maxChars` a 3500, (3) registra in AGENTS.md la regola operativa che in questo gruppo sei conciso e non parli mai se non menzionato direttamente. Conferma quando hai applicato tutto e mostrami il diff del config."

**Prompt 2 — passaggio da Baileys a WhatsApp Cloud:**

> "Voglio migrare da `whatsapp-baileys` a `whatsapp-cloud`. Spiegami nell'ordine: (1) cosa preparare lato Meta Business Suite, (2) quali credenziali servono (Phone Number ID, WABA ID, Permanent Token, verify token), (3) come fare il cutover senza perdere lo storico, (4) quali costi mensili aspettarmi per ~500 messaggi utility verso utenti italiani. Niente preamboli."

**Prompt 3 — verifica e audit dei canali:**

> "Audit dei canali collegati: per ognuno dimmi (a) lo stato e gli errori nei log delle ultime 24 ore, (b) quale `dmPolicy` è attiva, (c) se i signing secret sono configurati, (d) se l'allowlist è popolata, (e) quando è stato ruotato l'ultima volta il token. Se qualcosa è sotto-standard, proponimi il fix con il comando esatto."

## Errori comuni e come risolverli

Errori di Telegram e WhatsApp:

**Sintomo:** il bot non risponde.
Causa: token errato o secondo Gateway in long-polling.
Fix: `openclaw channels status`; rigenerare token;
spegnere il duplicato.

**Sintomo:** bot risponde a tutto in gruppo.
Causa: mention gating off + privacy off.
Fix: `/setprivacy` su `enabled` + `mentionGating: true`.

**Sintomo:** account bannato (Baileys).
Causa: traffico eccessivo, fingerprinting.
Fix: numero secondario, meno frequenza, Cloud API.

**Sintomo:** webhook Cloud API non riceve.
Causa: verify token mancante o URL non HTTPS.
Fix: verificare nella console Meta; serve HTTPS pubblico
o tunnel.

Errori di Slack/Discord/iMessage:

**Sintomo:** Slack: `not_authed`.
Causa: token `xapp-...` o `xoxb-...` non valido.
Fix: rigenerare i token o reinstallare l'app.

**Sintomo:** Discord: bot non legge i messaggi.
Causa: MESSAGE_CONTENT intent non attivo.
Fix: Developer Portal → Bot → attivare l'intent.

**Sintomo:** iMessage nativo non funziona.
Causa: Full Disk Access non concesso.
Fix: macOS → Privacy → Full Disk Access → OpenClaw.

## Checklist di fine capitolo

- [ ] Almeno un canale collegato e verificato (`openclaw channels status`)
- [ ] Test di andata e ritorno: risposta ricevuta in pochi secondi
- [ ] `dmPolicy` su `pairing` o `allowlist` (mai `open`) sul canale principale
- [ ] Mention gating attivo se il bot è in almeno un gruppo
- [ ] Tutti i token in password manager, fuori da Git
- [ ] Signing secret / verify token configurati dove applicabile
- [ ] Streaming Telegram (Bot API 9.5+) scelto coscientemente
- [ ] Se uso WhatsApp: Baileys solo con numero secondario, allowlist e bassa frequenza; Cloud con budget stimato
- [ ] In calendario la prossima rotazione dei token (entro 12 mesi)

## Link e risorse utili

Le fonti del capitolo; la raccolta completa è nell'[Appendice E](../Appendici/E-risorse-e-link-utili.md).

Telegram — [Bot API changelog ufficiale](https://core.telegram.org/bots/api-changelog), [Bot API reference](https://core.telegram.org/bots/api), [GramIO 9.5 changelog](https://gramio.dev/changelogs/2026-03-02).

WhatsApp — [WhatsApp Business API pricing 2026 (EngageLab)](https://www.engagelab.com/blog/whatsapp-business-api-pricing), [WhatsApp Chatbot Rules 2026 (Conferbot)](https://www.conferbot.com/blog/whatsapp-chatbot-rules-2026), [Meta blocks third-party AI chatbots (Chatboq)](https://chatboq.com/blogs/third-party-ai-chatbots-ban), [Baileys repository (WhiskeySockets)](https://github.com/WhiskeySockets/Baileys).

Slack — [Slack Bolt for JavaScript docs](https://tools.slack.dev/bolt-js/concepts/socket-mode/), [Socket Mode reference](https://api.slack.com/apis/socket-mode), [App-Level Tokens](https://api.slack.com/authentication/token-types#app-level).

Discord — [Privileged Gateway Intents FAQ (Discord)](https://support-dev.discord.com/hc/en-us/articles/4404772028055-Message-Content-Privileged-Intent-FAQ), [Discord Intents 2026 practical guide (Space-Node)](https://space-node.net/blog/discord-gateway-intents-message-content-2026).

iMessage / Signal / Matrix — [OpenClaw BlueBubbles docs](https://docs.openclaw.ai/channels/bluebubbles), [signal-cli wiki (AsamK)](https://github.com/AsamK/signal-cli/wiki/Quickstart), [matrix-appservice-bridge](https://github.com/matrix-org/matrix-appservice-bridge).

OpenClaw — [Configuration reference](https://docs.openclaw.ai/gateway/configuration), [Multi-channel setup (LumaDock)](https://lumadock.com/tutorials/openclaw-multi-channel-setup), [Channel integration guide (YingTu)](https://yingtu.ai/en/blog/openclaw-messaging-channel-integration-guide).

---

[← Capitolo 5](./05-installazione-step-by-step.md)  ·  [Indice](../README.md)  ·  [Capitolo 7 →](../PARTE-III-Primo-mese/07-prima-conversazione-onboarding-agente.md)
