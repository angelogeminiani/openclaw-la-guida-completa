# Capitolo 6 — Configurare Telegram (e altri canali) [★]

## Cosa imparerai

- Perché il canale di comunicazione è una scelta architetturale, non un dettaglio estetico, e cosa cambia davvero fra una piattaforma e l'altra.
- Come creare un bot Telegram da zero con @BotFather in cinque minuti, gestire token, mention gating e gruppi, sfruttando le novità della Bot API 9.5 e 10.0 (streaming, member tags, bot-to-bot, granular access).
- Quando scegliere WhatsApp via Baileys (rischio ban) e quando passare alla Cloud API ufficiale, alla luce della stretta Meta del 15 gennaio 2026 sui chatbot general-purpose.
- Come configurare Slack (Bolt + Socket Mode) e Discord (privileged intents, slash commands) per uso lavorativo, con gli scope minimi che ti salvano da un audit di sicurezza.
- Come collegare iMessage (plugin nativo, BlueBubbles come fallback), Signal (`signal-cli`), Matrix (appservice), WeChat (plugin Tencent), Microsoft Teams, Google Chat, Feishu, LINE e IRC.
- Come instradare più canali verso lo stesso agente con sessione condivisa, e come usare la `dmPolicy` per decidere chi può scrivergli.

## Prerequisiti

Aver completato l'installazione descritta nel [Capitolo 5](./05-installazione-step-by-step.md): l'agente è stato avviato, il Gateway risponde sulla porta `18789`, `openclaw doctor` non lamenta errori bloccanti. Devi avere il **password manager** aperto in una scheda di Chrome — useremo token sensibili — e uno **smartphone** con Telegram installato per la prima parte. Se hai pianificato di usare WhatsApp via Baileys, prevedi di avere a portata di mano un **secondo numero di telefono** (eSIM, numero virtuale o SIM dedicata): non si usa il numero personale.

Una verifica veloce prima di iniziare:

```bash
openclaw channels list
openclaw gateway status
```

Il primo comando mostra l'elenco dei canali supportati dalla tua versione (cambia di mese in mese: la documentazione ufficiale è la fonte di verità). Il secondo conferma che il Gateway è in ascolto e pronto ad accettare un nuovo canale.

## Contenuto principale

Sono le 19:00 di un mercoledì. Hai pianificato il digest serale, l'agente è acceso, il modello risponde. Manca una sola decisione: su quale chat ti scrive? Telegram impiega cinque minuti a configurarsi, WhatsApp Business tre giorni di verifica Meta, WhatsApp con Baileys due settimane prima del primo ban. Questo capitolo ti porta dalla scelta del canale al primo "ciao, ti sento" — senza fare il giro lungo.

**(i) Pro tip:** i comandi e i nomi di canale di questo capitolo si riferiscono a OpenClaw `0.18+` (la serie attiva nella primavera 2026). Prima di copia-incollare verifica con `openclaw --version` e, in caso di differenze, consulta `docs.openclaw.ai/channels` per la sintassi della tua versione. Le piattaforme esterne (Telegram Bot API, Meta, Slack, Discord) cambiano in modo indipendente e ancora più rapido.

### TL;DR — Telegram in cinque minuti

Se hai fretta e vuoi solo arrivare a "il bot risponde", questi sono i tre comandi essenziali. Tutto il resto del capitolo spiega *perché* esistono, e cosa fare quando uno di loro non si comporta come dovrebbe.

```bash
# 1. crea il bot in @BotFather sul telefono
#    /newbot -> nome -> username_bot -> copia il token

# 2. collega il token al Gateway
openclaw channels login --channel telegram

# 3. verifica che parli
openclaw channels status --channel telegram
```

Apri Telegram, cerca il tuo bot, premi `/start`. Se ricevi una risposta entro pochi secondi sei a posto: salta direttamente alla sezione *Gruppi e mention gating*. Altrimenti, prosegui con il capitolo: ogni nodo è coperto sotto.

### Costi, tempi e rischio a colpo d'occhio

Prima di entrare nel dettaglio, una mappa decisionale in quattro colonne. I costi mensili presumono uso personale o di piccolo team (~500-2000 messaggi/mese); per volumi più alti, vedi le tabelle dettagliate nelle sezioni dedicate.

| Canale | Tempo setup | Costo/mese | Rischio |
|---|---|---|---|
| Telegram | 5 min | 0 € | Basso |
| WhatsApp Baileys | 15 min | 0 € | Alto (ban 2-8 sett.) |
| WhatsApp Cloud | 1-3 giorni | 5-30 € | Basso (ufficiale) |
| Slack | 10 min | 0 € (workspace) | Basso |
| Discord | 10 min | 0 € | Basso |
| iMessage nativo | 20 min | 0 € | Medio (Mac sempre acceso) |
| Signal (signal-cli) | 30 min | 0 € | Medio (canale non ufficiale) |
| Matrix (client) | 20 min | 0 € | Basso |
| WeChat (plugin) | 1-2 giorni | 0 € | Basso (geo: Cina) |

Lettura rapida: parti da **Telegram** (costo zero, rischio zero, cinque minuti). Aggiungi **Slack o Discord** se ti serve un canale di team. Considera **WhatsApp Cloud API** solo se hai un caso d'uso *business* riconducibile a operazioni concrete (supporto, ordini, FAQ). Tutto il resto è ottimizzazione.

### Perché il canale conta più di quanto sembri

Quando si sceglie il canale di un agente personale la tentazione è di guardare solo a "quale chat uso più spesso io". È un buon punto di partenza, ma manca tre dimensioni che diventano evidenti solo dopo qualche settimana di uso reale.

La prima è **chi controlla il canale**. Telegram ha una Bot API documentata, gratuita e stabile dal 2015; il giorno in cui Telegram decide di cambiare le regole, le cambia per tutti e in modo trasparente. WhatsApp è esattamente l'opposto: Meta detiene controllo unilaterale, le regole cambiano senza preavviso, e gli strumenti non ufficiali (Baileys e simili) vivono in una zona grigia che si è ristretta moltissimo nel 2025-2026. La seconda dimensione è il **modello di interazione**: 1-a-1 (DM personale), gruppo piccolo (famiglia, team), canale broadcast (community), server multi-canale (Slack, Discord). Un agente che funziona benissimo in DM diventa rumoroso e invadente in un gruppo se non hai pensato al *mention gating*. La terza è **dove vivono i tuoi interlocutori**: una designer freelance in Italia probabilmente usa WhatsApp con i clienti, Telegram con la community, Slack con l'agenzia. Servono più canali, e il punto è farli convergere su un singolo agente che mantenga il contesto.

OpenClaw risolve questo terzo punto nativamente. Il Gateway è un *long-running process* che riceve messaggi da più piattaforme e li instrada nello stesso *session store*: se inizi una conversazione su WhatsApp e la continui su Telegram, l'agente ricorda il filo perché il contesto è condiviso. Per arrivare lì serve però aver configurato ogni canale con cura, e quasi sempre il primo è Telegram.

**(i) Pro tip:** non collegare tutti i canali nel primo pomeriggio. Aggiungi un canale per volta, lavoraci sopra una settimana, poi passa al successivo. Tre canali configurati male sono peggio di un canale configurato bene.

### Telegram — il punto di partenza consigliato

Telegram è il canale più semplice da configurare per OpenClaw, ed è quello che la documentazione ufficiale e tutte le guide indipendenti suggeriscono di provare per primo. Il motivo è banale: @BotFather genera token in 30 secondi, non c'è OAuth, non c'è approvazione, non ci sono scope, niente review di Meta o Slack. Sei tu, il bot, e basta.

#### Creare il bot con @BotFather

Apri Telegram (app o desktop) e cerca `@BotFather`. È il bot ufficiale di Telegram per gestire altri bot: ha una spunta blu, è quello con username `BotFather` esatto. Avvia una conversazione con `/start`, poi:

```
/newbot
```

BotFather chiede due informazioni in sequenza. Il **nome visibile** del bot — può contenere spazi e maiuscole, è quello che gli interlocutori vedranno nell'header della chat (es. "Polly Personal Assistant"). Lo **username** — deve terminare per `bot` o `_bot`, è univoco a livello globale e diventa parte dell'URL del bot (`t.me/polly_pa_bot`). Conviene sceglierlo coerente con il nome che darai all'agente nel `IDENTITY.md`.

Quando lo username è accettato, BotFather risponde con un messaggio che contiene una stringa di questo tipo:

```
Use this token to access the HTTP API:
8123456789:AAH9q2Wx3vK7nF8mP4...
```

Quella stringa **è il token**. Vale come una password: chi la possiede può inviare e ricevere messaggi come fosse il bot, leggere chi gli ha scritto, postare nei gruppi dove il bot è stato aggiunto. Copialo subito nel password manager, sotto la voce `OpenClaw → Telegram → Polly bot token` (o come hai chiamato il bot). **Non incollarlo in nessun file di testo, non condividerlo in chat, non screenshottarlo.**

**(!) Attenzione:** se il token finisce in un commit Git pubblico, lo trovano in pochi minuti. I bot scanner che indicizzano GitHub cercano esattamente questa pattern (`\d{9,10}:[A-Za-z0-9_-]{35}`). Quando succede, devi rigenerare immediatamente il token con `/revoke` in @BotFather e collegare il nuovo. Tutto il traffico precedente sul vecchio token è da considerare compromesso.

Mentre sei in @BotFather, conviene impostare qualche metadato:

```
/setdescription
/setabouttext
/setuserpic
/setcommands
```

`/setcommands` in particolare è utile: ti permette di registrare i comandi che l'agente accetta (`/digest`, `/status`, `/help`, ecc.), che appariranno in un menù a tendina nella chat. Per OpenClaw è consigliato registrarne almeno tre: `/start`, `/status`, `/help`.

#### Collegare il token a OpenClaw

Dal terminale dove gira il Gateway, lancia:

```bash
openclaw channels login --channel telegram
```

Il wizard chiede il token: incollalo (verrà mascherato), conferma. OpenClaw fa un test di connessione contro `api.telegram.org`, registra il bot nel proprio config (`~/.openclaw/config.yaml`, sezione `channels.telegram`), e attiva il *long polling* per ricevere i messaggi.

L'equivalente dichiarativo, senza wizard, è:

```bash
openclaw config set \
  channels.telegram.botToken \
  "8123456789:AAH9q2Wx3vK7nF8mP4..."
openclaw config set \
  channels.telegram.enabled true
openclaw gateway reload
```

Il `reload` ricarica la config senza riavviare l'intero processo: utile quando aggiungi un canale a sistema già in funzione. Se non parte, `openclaw gateway logs --tail 50` mostra il motivo (token malformato, conflitto di porte, errore di rete).

#### Il primo test di andata e ritorno

Cerca su Telegram lo username che hai scelto, apri la chat e premi `/start`. Se hai installato la skill `gog` o `personal-assistant`, l'agente risponde con un breve messaggio di benvenuto. Altrimenti scrivi semplicemente:

> Ciao, mi senti?

Se ricevi una risposta entro qualche secondo — anche solo un "Sì, ti sento, sono pronto" — il canale è operativo. Da questo momento ogni messaggio in quella chat viene processato dall'agente, ogni risposta dell'agente torna a te.

**(#) Debug:** se non arriva niente, controlla nell'ordine: (1) `openclaw channels status` indica `telegram: connected`? (2) `openclaw gateway logs --tail 100` mostra messaggi in ingresso quando scrivi? (3) il bot esiste davvero su `https://t.me/<username>`? (4) non hai per caso un secondo Gateway che fa long-polling sullo stesso token? Telegram permette **un solo** consumatore per token: se due processi cercano di leggere in parallelo, ognuno ruba i messaggi dell'altro. Spegni quello vecchio prima di accendere il nuovo.

#### Gruppi e mention gating

Aggiungere il bot a un gruppo è banale: nel gruppo, *Info → Aggiungi membro → @username_del_bot*. Il problema è quello opposto: appena il bot è nel gruppo, di default reagisce a *qualunque* messaggio. In una chat famiglia di otto persone diventa intollerabile in mezza giornata.

Il *mention gating* risolve il problema. Si configura a livello di OpenClaw, non di Telegram, e dice all'agente: "in questa chat di gruppo, intervieni solo se vieni menzionato esplicitamente (`@polly_bot`) o se il messaggio comincia con un comando (`/...`)". La configurazione tipica:

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

Tradotto: l'agente parla solo se menzionato, replica al messaggio originale con il *reply tag* (così è chiaro a chi sta rispondendo), e spezza in più messaggi le risposte oltre 3.500 caratteri (il limite Telegram è 4.096, ma teniamoci un margine).

In @BotFather c'è anche un'impostazione speculare: `/setprivacy` permette di scegliere se il bot riceve "tutti i messaggi" o "solo quelli che lo menzionano direttamente". Lascia il default (`enabled` = privacy on, riceve solo le menzioni): è una difesa in più, indipendente dal mention gating di OpenClaw.

#### Cosa è cambiato con la Bot API 9.5 e 10.0

Telegram rilascia aggiornamenti della Bot API in media ogni 4-6 settimane. Tre cambiamenti del 2026 vale la pena conoscerli, perché ognuno apre uno scenario che prima non era possibile.

La **Bot API 9.5** (1° marzo 2026) ha generalizzato `sendMessageDraft` a tutti i bot, abilitando lo *streaming nativo* delle risposte: l'agente non aspetta di aver completato la risposta per inviarla, ma la scrive a parole come farebbe un umano. Per OpenClaw questo significa che, su modelli lenti come Opus 4.6, vedi la risposta apparire token per token invece di aspettare 12 secondi di silenzio. La 9.5 ha introdotto anche i *member tags*: l'agente può attribuire etichette testuali (≤ 16 caratteri, senza emoji) ai membri di un gruppo, utili per ruoli ("admin", "ospite", "famiglia").

La **Bot API 10.0** (maggio 2026) ha aperto due scenari: la **comunicazione bot-to-bot** in contesti specifici (gruppi e business mode), che consente flussi multi-agente nativi senza dover passare dal filesystem condiviso interno; e il **granular access whitelist** impostabile via @BotFather o API, che restringe chi può anche solo scrivere al bot. Per un agente personale è una difesa preziosa: limiti a priori la lista degli UID Telegram autorizzati, e qualunque altro utente riceve un messaggio di "non disponibile".

OpenClaw è stato il primo client a integrare lo streaming 9.5 in modo completo (l'aggiornamento è arrivato il 6 marzo 2026, cinque giorni dopo il rilascio della Bot API). Se vuoi disabilitarlo per usare bot più "tradizionali", c'è una flag:

```yaml
channels:
  telegram:
    streaming:
      enabled: true   # default da Bot API 9.5+
      throttleMs: 250 # min delay between chunks
```

**(i) Pro tip:** se ti capita di vedere risposte spezzate in modo strano nei gruppi, alza `throttleMs` a 500-800ms. Lo streaming sub-secondo nei gruppi grandi genera notifiche multiple sul telefono di chi ascolta, e l'esperienza diventa fastidiosa.

#### DM policy: chi può scrivere al bot

Tutti i canali in OpenClaw condividono lo stesso pattern di `dmPolicy`, che decide cosa succede quando uno *sconosciuto* scrive al bot per la prima volta. I valori sono quattro:

- `pairing` (default consigliato): chi scrive deve presentarsi con un codice di accoppiamento, che generi tu con `openclaw pair create`. È il modo più sicuro: solo chi ha ricevuto il codice da te può aprire un canale 1-a-1.
- `allowlist`: solo gli UID o numeri esplicitamente autorizzati nel config (`channels.telegram.allowlist: [123456, 234567]`) possono scrivere.
- `open`: chiunque può scrivere. **Da usare solo se il bot è pubblico e progettato per esserlo** (es. assistente di vendita di un'azienda).
- `disabled`: il bot ignora del tutto i DM, risponde solo nei gruppi a cui è stato aggiunto.

Per un agente personale, la combinazione tipica è `pairing` su Telegram e `allowlist` su Slack/Discord. Mai `open` su un bot che ha accesso ai tuoi file o alla tua email.

### WhatsApp — il canale "naturale" ma pericoloso

WhatsApp è il sogno di chiunque viva in Italia: chat con i clienti, gruppo della famiglia, fornitori, condominio, tutto sulla stessa app. È anche, di gran lunga, il canale più rischioso da configurare per un agente. Non perché sia tecnicamente difficile, ma perché Meta è entrata in una fase di applicazione molto più rigida delle proprie policy, e le scelte fatte oggi possono diventare obsolete fra sei mesi.

Esistono due strade concettualmente opposte: **Baileys** (libreria non ufficiale che parla il protocollo WhatsApp Web) e la **Cloud API ufficiale** (servizio Meta a pagamento per business). Capire perché esistono entrambe è metà del lavoro.

#### Baileys: cosa è e perché è a rischio

Baileys è una libreria JavaScript open-source (WhiskeySockets) che implementa il protocollo WebSocket di WhatsApp Web: si "linka" come fosse un browser, scansiona un QR code, e da quel momento riceve e invia messaggi sul numero linkato. È gratuita, semplice, supporta gruppi, media e voce. È anche, oggi, contro i Terms of Service di WhatsApp.

Nel 2025 e 2026 Meta ha intensificato il *fingerprinting* dei client non ufficiali: protocollo, *message velocity*, pattern comportamentali. Le segnalazioni della community indicano che gli account che usano Baileys vivono mediamente 2-8 settimane prima di essere bannati in modo permanente. I numeri non vanno né recuperati né riabilitati: il ban è definitivo e si estende all'identità del telefono (IMEI/IMSI), quindi una semplice nuova SIM sullo stesso device non basta.

**(!) Attenzione:** se usi Baileys, non collegare *mai* il tuo numero personale di WhatsApp. Prendi un secondo numero — eSIM di un operatore virtuale, numero VoIP che supporti SMS per verifica, SIM dedicata in un telefono usato come server — e linka quello. Quando arriva il ban, perdi un numero usa-e-getta, non l'archivio degli ultimi dieci anni di chat con la tua famiglia.

A complicare lo scenario, dal **15 gennaio 2026** è entrata in vigore una nuova policy AI di Meta che vieta esplicitamente i chatbot AI "general-purpose" (ChatGPT, Claude, Gemini e simili) sulla piattaforma. Non è una caccia automatizzata, ma è il fondamento contrattuale che giustifica i ban. Se il tuo agente fa cose riconducibili a un'azienda specifica — supporto clienti, ordini, FAQ, tracking — la policy esplicita un'eccezione. Se invece è "un assistente personale general-purpose che ti aiuta in tutto", sei nella categoria a rischio.

#### Setup Baileys con OpenClaw

Detto tutto questo, se hai bisogno di WhatsApp e accetti il rischio, il setup è veloce. OpenClaw ha un canale `whatsapp-baileys` integrato:

```bash
openclaw channels login --channel whatsapp-baileys
```

Il comando stampa un QR code ASCII nel terminale. Sul telefono che possiede il numero secondario: WhatsApp → *Impostazioni* → *Dispositivi collegati* → *Collega un dispositivo* → inquadra il QR. Quando il link è stabilito, OpenClaw avvisa con un *connected* e da quel momento il numero è pilotato dall'agente. Lo stato del link si controlla con:

```bash
openclaw channels status --channel whatsapp-baileys
```

Lo stesso comando rivela quando il link si rompe (succede regolarmente: WhatsApp scollega i dispositivi che non vengono usati per 14 giorni, o quando rileva traffico sospetto). In quel caso devi rifare il QR scan. Se il numero viene bannato, l'errore è `403 Forbidden: account banned` e nessun retry serve.

Per limitare il rischio, applica almeno tre regole: (1) **bassa frequenza** — niente messaggi automatici in burst, distanzia tutto di almeno 30-60 secondi; (2) **scope ristretto** — solo chi è già nei tuoi contatti può scrivere al bot (`dmPolicy: allowlist`); (3) **niente broadcast** — la *broadcast list* è il modo più rapido per farsi bannare in mezza giornata, evitala completamente.

#### Cloud API ufficiale: l'unica strada a prova di ban

Se hai un caso d'uso *business* (azienda, freelance con partita IVA, e-commerce, support clienti), la strada giusta è la **WhatsApp Business Cloud API**. È a pagamento, richiede un *Business Service Provider* registrato (Twilio, MessageBird, 360dialog, Meta diretto) e un processo di verifica del numero, ma in cambio non rischi nulla: è il canale ufficiale, supportato e documentato.

Il pricing è cambiato sostanzialmente. Dal **1° luglio 2025** Meta è passata da un modello a *conversazione* a un modello *per-messaggio*: ogni template inviato si paga singolarmente. Le tariffe variano per nazione del *destinatario* (non del mittente) e per categoria del messaggio:

- **Marketing** — la più cara, indicativamente $0,01–0,14 per messaggio a seconda del paese.
- **Utility / Authentication** — circa 80-90% meno costosa del marketing.
- **Service** — gratuite se inviate entro la *customer service window* aperta da un messaggio del cliente.
- **Click-to-WhatsApp** — gratuite per 72 ore dopo un messaggio iniziato da un annuncio.

Dal **1° gennaio 2026** Meta ha rivisto al ribasso le tariffe marketing per Francia ed Egitto, al rialzo per India, mentre utility e authentication sono scese in Nord America. Per un caso italiano standard (supporto clienti su un e-commerce) le utility costano centesimi a messaggio: poche decine di euro al mese per volumi medi.

OpenClaw espone il canale come `whatsapp-cloud`:

```bash
openclaw channels login --channel whatsapp-cloud
```

Il wizard chiede il *Phone Number ID*, il *WABA ID* (WhatsApp Business Account), il *Permanent Access Token* generato dalla console Meta, e l'URL del webhook. OpenClaw genera anche un *verify token* casuale che devi incollare nella console Meta per validare il webhook.

**(i) Pro tip:** se non vuoi rapportarti direttamente con la console Meta (lunga, in inglese, con UX da business platform di dieci anni fa), Twilio offre un'astrazione molto più semplice e una console italiana. Costa un piccolo *markup* sui messaggi ma ti risparmia mezza giornata di configurazione.

### Slack — per il lavoro di team

Slack è il canale per i team. Bot personali servono a poco lì (nessuno guarda DM con un bot privato durante la giornata), ma un agente che vive in un canale `#ops` o `#growth` e risponde quando viene menzionato cambia il ritmo del lavoro.

OpenClaw integra Slack tramite **Bolt + Socket Mode**, che è il pattern moderno consigliato da Slack stessa: niente webhook pubblico, niente reverse proxy, niente porte aperte. Il bot apre una WebSocket *outbound* verso Slack e riceve gli eventi da lì.

#### Creare l'app Slack

Vai su `api.slack.com/apps` e clicca *Create New App* → *From scratch*. Nome dell'app (es. "Polly"), workspace di destinazione. Dopodiché, nel menu laterale dell'app, ci sono tre sezioni da configurare nell'ordine.

**Socket Mode**: vai su *Socket Mode* (menu a sinistra) e attiva il toggle. Slack ti chiede di generare un *App-Level Token*: clicca *Generate*, dagli un nome (es. "openclaw-socket"), aggiungi lo scope `connections:write`, conferma. Slack mostra un token che inizia con `xapp-...`: copialo subito nel password manager. È mostrato una sola volta.

**Bot Token**: vai su *OAuth & Permissions*. Nella sezione *Scopes → Bot Token Scopes* aggiungi gli scope minimi per il tuo caso d'uso. Per un agente standard servono almeno:

- `chat:write` — inviare messaggi
- `app_mentions:read` — ricevere menzioni `@polly`
- `im:history`, `im:read`, `im:write` — DM
- `channels:history`, `groups:history` — se vuoi leggere i messaggi nei canali (non sempre necessario, dipende da come usi l'agente)
- `commands` — slash commands `/...`
- `files:read` — se gli mandi allegati

Una volta aggiunti gli scope, clicca *Install to Workspace*. Slack genera il *Bot User OAuth Token* che inizia con `xoxb-...`: di nuovo, password manager.

**Event Subscriptions**: vai su *Event Subscriptions* e attiva. Aggiungi gli eventi che vuoi che il bot riceva: `app_mention` (essenziale), `message.im` (per i DM), eventualmente `message.channels` se vuoi che ascolti i canali pubblici dove è invitato.

**(!) Attenzione:** gli scope `*.history` sono potenti — danno accesso alla cronologia di conversazioni — e gli IT manager seri li auditano. Parti dal minimo (`chat:write` + `app_mentions:read` + `commands`), poi aggiungi al bisogno. Aggiungere uno scope dopo l'installazione richiede di re-installare l'app, ma è veloce.

#### Collegare a OpenClaw

```bash
openclaw channels login --channel slack
```

Il wizard chiede i due token (`xapp-...` e `xoxb-...`) e il *Signing Secret* (che trovi su *Basic Information → App Credentials*). Una volta inseriti, prova:

```bash
openclaw channels status --channel slack
```

Risultato atteso: `slack: connected (socket mode)`. Sul workspace Slack, invita il bot in un canale (`/invite @polly`), poi menzionalo: `@polly status`. Risponde in pochi secondi.

#### Slash commands e routing canali → agenti

Slack supporta gli *slash commands*: comandi globali (`/digest`, `/standup`, `/lead`) che chiamano il tuo bot ovunque tu sia, anche fuori dai canali dove è invitato. Si configurano nella sezione *Slash Commands* dell'app. OpenClaw li mappa automaticamente a *intent* dell'agente; per personalizzarli:

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

Discord ha una logica diversa da Slack. Slack è ottimizzato per il lavoro asincrono di un team chiuso; Discord è la lingua franca delle community pubbliche, dei progetti open-source e degli ambienti gaming. Un agente OpenClaw che vive in un server Discord può fare moderazione, FAQ, generazione di contenuti, supporto.

#### Privileged intents: il punto critico

Dal 2022 Discord ha introdotto i **Privileged Gateway Intents** per limitare l'accesso ai dati. Tre intent sono "privilegiati":

- `GUILD_PRESENCES` — stato online/offline degli utenti
- `GUILD_MEMBERS` — lista membri di un server
- `MESSAGE_CONTENT` — il contenuto testuale dei messaggi

Per OpenClaw l'unico critico è **MESSAGE_CONTENT**: senza di lui il bot riceve solo metadati dei messaggi (chi, quando, dove), non il testo. Per attivarlo: `discord.com/developers/applications` → seleziona l'app → *Bot* → scorri fino a *Privileged Gateway Intents* → attiva *MESSAGE CONTENT INTENT* → *Save Changes*.

**Soglia dei 100 server**: se il bot è in meno di 100 server, puoi attivare gli intent senza review. Da 100 server in su, Discord richiede una *verification* manuale che può durare 2-6 settimane. Per un bot personale o di una piccola community non è un problema; per un bot pensato per scalare, pianifica in anticipo.

**(i) Pro tip:** dal 2024 Discord spinge verso le *application commands* (slash commands e context menu) come alternativa al `MESSAGE_CONTENT`. Se il tuo agente lavora prevalentemente su comandi (`/ask`, `/summarize`, `/digest`), valuta seriamente di farne a meno: riduci la superficie di compliance e non hai più bisogno della verifica oltre i 100 server.

#### Creare il bot Discord

Su `discord.com/developers/applications`, *New Application*. Dai un nome, accetta i termini. Nel menu laterale, *Bot* → *Reset Token* (alla prima volta è *Add Bot*). Discord mostra il *Bot Token* (inizia con `MT...` o stringa lunga): nel password manager. Poi *OAuth2* → *URL Generator*: seleziona lo scope `bot` e `applications.commands`, e le permission che ti servono (`Send Messages`, `Read Message History`, `Use Slash Commands` come minimo). Discord genera un URL di invito: aprilo, scegli il server, autorizza.

Collegamento a OpenClaw:

```bash
openclaw channels login --channel discord
```

Token + application ID, conferma, fatto. Verifica nello stesso modo di Slack: scrivi nel server, l'agente risponde.

### iMessage — l'ecosistema Apple [★★]

iMessage è ostico perché è chiuso. Non esiste una Bot API ufficiale Apple, non c'è un endpoint cloud. L'unico modo per pilotarlo è avere un **Mac fisico** dove iMessage è loggato, e un layer software che intercetti i messaggi.

OpenClaw supporta due strade.

La prima è il **plugin nativo iMessage** introdotto nel 2025 e diventato default nel 2026: legge i database SQLite di Messages.app, invia messaggi tramite AppleScript, gestisce immagini e tapback. Funziona solo su macOS recenti (Sequoia 15.4+) e richiede di concedere a OpenClaw l'accesso a *Full Disk Access* nelle impostazioni Privacy e Sicurezza. È la scelta consigliata per ogni nuovo setup.

La seconda è **BlueBubbles**, un server open-source storicamente molto usato per fare bridging di iMessage verso Android/Linux/Windows. OpenClaw parla a BlueBubbles tramite REST API. Funziona ancora, ma il progetto non è stato aggiornato negli ultimi mesi: l'ultima release server è del 16 maggio 2025, e la documentazione ufficiale OpenClaw indica BlueBubbles come deprecato per nuovi setup. Se l'hai già configurato continua a funzionare; se stai partendo oggi, usa il plugin nativo.

```bash
openclaw channels login --channel imessage
# native plugin (default on macOS 15.4+)

openclaw channels login --channel imessage-bluebubbles
# legacy bridge, requires bluebubbles-server running
```

**(!) Attenzione:** Apple non garantisce stabilità sui database di Messages.app. Aggiornamenti minori di macOS (15.4.1 → 15.4.2) hanno rotto il plugin nativo in passato. Tieni `openclaw update` aggiornato e monitora il changelog dopo ogni aggiornamento di macOS.

### Signal — privacy massima, setup tecnico [★★]

Signal non ha bot API. Esiste però `signal-cli`, una CLI non ufficiale ma stabile (manutentore: AsamK, attiva dal 2017) che parla il protocollo Signal e si integra via JSON-RPC o D-Bus. OpenClaw la usa come backend del canale `signal`.

Il setup ha tre fasi. Prima si **installa** `signal-cli` (su macOS via Homebrew, su Linux via pacchetto o JAR). Poi si **linka** un account Signal al device — analogo al QR di WhatsApp: si genera un `sgnl://linkdevice?...` URI, lo si trasforma in QR (`qrencode -t ANSIUTF8`), si scansiona dal telefono dove Signal è già installato. Infine si avvia `signal-cli` in **daemon mode** con D-Bus, in modo che OpenClaw possa parlarci.

```bash
signal-cli link -n "openclaw" | \
  qrencode -t ANSIUTF8

signal-cli -a +391234567890 daemon \
  --socket --dbus
```

Collegamento a OpenClaw:

```bash
openclaw channels login --channel signal
```

Signal è ottimo per chi tiene molto alla privacy o ha interlocutori che usano solo Signal. È meno adatto come canale primario per un agente personale: non supporta gruppi business, non ha l'ecosistema bot di Telegram, e il setup è molto più tecnico. Tipicamente diventa un canale secondario, attivato per pubblici specifici.

### Matrix — open-source e self-hosted [★★]

Matrix è il protocollo aperto di messaggistica federata (Element è il client più diffuso). Per OpenClaw c'è un canale `matrix` che si collega a un homeserver via API client-server, oppure si registra come *appservice* (più potente, ma richiede modifiche alla config dell'homeserver).

Per uso personale la strada veloce è la modalità *client*: registri un account utente per il bot sull'homeserver (`@polly:matrix.org` o sul tuo homeserver), generi un access token, lo passi a OpenClaw.

```bash
openclaw channels login --channel matrix
# asks for homeserver URL, user, access token
```

La modalità *appservice* serve quando il bot deve impersonare *namespace* di utenti (es. bridging avanzato): richiede di scrivere un *registration YAML* e di registrarlo nell'homeserver. Vale la pena solo se gestisci il tuo homeserver e vuoi integrazioni avanzate.

Matrix è la scelta giusta se: (1) hai già un homeserver, (2) lavori con community open-source che vivono lì, (3) la federazione è un requisito (un agente che parla con utenti su homeserver diversi).

### WeChat — il mercato cinese

WeChat è il canale necessario se hai utenti, clienti o team in Cina. Da **marzo 2026** Tencent ha rilasciato un plugin ufficiale per OpenClaw (WeChat → *Impostazioni* → *Plugin* → *ClawBot*), che evita la zona grigia degli automation tool non ufficiali. È l'unico canale dove la collaborazione con la piattaforma è ufficiale e benedetta.

Limitazioni: il plugin funziona solo per account WeChat *Personal* registrati in Cina o per account *Business* con licenza. Restrizioni governative (vedi [Capitolo 21](../PARTE-VIII-Visione-futuro/21-ecosistema-openclaw.md)) impongono che l'inferenza dell'agente avvenga su modelli LLM autorizzati dalla CAC; questo esclude OpenAI e Anthropic, e tipicamente significa appoggiarsi a Kimi K2.5, MiniMax M2.5 o DeepSeek-V3.

### Microsoft Teams, Google Chat, Feishu, LINE, IRC [★★]

OpenClaw supporta nativamente anche **Microsoft Teams** (via Bot Framework, scope Graph API), **Google Chat** (per Workspace), **Feishu** (l'edizione internazionale di Lark, molto usato in APAC), **LINE** (Giappone, Taiwan, Thailandia), **IRC** (storico, ma ancora vivissimo nelle community open-source). Il pattern è uguale per tutti: `openclaw channels login --channel <nome>`, il wizard chiede i token/credenziali specifiche della piattaforma, OpenClaw li registra. La differenza è solo nel processo lato piattaforma: Teams richiede approvazione di tenant, Google Chat passa per Workspace Marketplace, LINE ha la console *LINE Developers*.

Se ti serve uno di questi canali in modo serio, la documentazione ufficiale (`docs.openclaw.ai/channels`) ha guide dedicate per ognuno. Per la quasi totalità dei lettori italiani di questo libro, Telegram + WhatsApp + Slack/Discord copre il 95% dei casi.

### Multi-canale: stesso agente, contesto condiviso

Una delle caratteristiche distintive di OpenClaw è che lo stesso Gateway gestisce contemporaneamente più canali, mantenendo un *session store* condiviso. Configuri Telegram, WhatsApp e Slack: lo stesso agente risponde su tutti e tre, e la memoria dell'interazione è la stessa.

Visivamente, il flusso ha questa forma:

```
   Telegram ─┐
   WhatsApp ─┼──► Gateway ──► Session Store
   Slack    ─┘    (router)    (memoria
                              condivisa)
```

I tre canali entrano nel Gateway con identità distinte (UID Telegram, numero WhatsApp, user ID Slack); il *router* le riconduce alla stessa sessione utente se la *unification* è attiva, altrimenti le tiene separate. La risposta dell'agente esce dal canale da cui è arrivata la richiesta — non c'è cross-posting automatico: se chiedi qualcosa su Telegram, l'agente risponde su Telegram.

In pratica:

```bash
openclaw channels list
# telegram   connected
# whatsapp   connected (baileys)
# slack      connected

openclaw sessions list
# session_id   channel    last_seen
# s_a1b2c3     telegram   2 min ago
# s_d4e5f6     slack      1 hour ago
```

Le sessioni sono normalmente *per-canale + per-utente*, ma se vuoi che convergano (es. "Polly sa che oggi mi sono lamentato del traffico sia su WhatsApp che su Telegram") puoi configurare la *session unification* sull'identità dell'utente:

```yaml
sessions:
  unification:
    enabled: true
    strategy: by-user-identity
```

L'unificazione richiede che tu abbia mappato esplicitamente le identità (UID Telegram, numero WhatsApp, user ID Slack) al medesimo utente nel file `USER.md`. Senza la mappa, Polly tratta le tre identità come tre persone diverse.

### Tabella decisionale "qual è il canale giusto per te"

Per non sovraccaricare con una matrice gigante, ho spezzato la decisione in tre tabelle compatte (A5-friendly: 3 colonne max).

Tabella 1 — **uso personale**:

| Caso d'uso | Canale consigliato | Note |
|---|---|---|
| Assistente personale 1-a-1 | Telegram | Setup più veloce |
| Famiglia (gruppo) | WhatsApp Cloud | Niente Baileys con i tuoi cari |
| Privacy massima | Signal | Setup tecnico, gestione tua |

Tabella 2 — **uso lavorativo**:

| Caso d'uso | Canale consigliato | Note |
|---|---|---|
| Team interno | Slack | Bolt + Socket Mode |
| Community / open-source | Discord | Slash commands meglio di MESSAGE_CONTENT |
| Corporate enterprise | Teams | Bot Framework + Graph API |

Tabella 3 — **casi specifici**:

| Caso d'uso | Canale consigliato | Note |
|---|---|---|
| Ecosistema Apple | iMessage nativo | Mac sempre acceso |
| Mercato cinese | WeChat (plugin Tencent) | Modello LLM CAC-approved |
| Federazione open | Matrix | Homeserver tuo |

### Migrare da un canale all'altro

Capita più spesso di quanto pensi. Si parte con Telegram da soli, poi si entra in un team che vive su Slack e bisogna replicarci l'agente. Oppure si lavora con Baileys da mesi finché un ban annuncia che è il momento di passare a WhatsApp Cloud. La migrazione è raramente un *cutover* netto: di solito i due canali convivono per qualche settimana, poi quello vecchio viene spento. Tre punti da non perdere di vista.

**Storico delle conversazioni.** OpenClaw archivia i messaggi *per sessione*, non per canale. Quando aggiungi un nuovo canale lo storico esistente *non* si trasferisce automaticamente: l'agente sa cosa avete detto su Telegram, ma su Slack parte da zero. Per spianare la transizione, prima di chiudere il vecchio canale chiedi all'agente di scrivere un *briefing di passaggio* nel file `MEMORY.md` o nelle note giornaliere — un riepilogo di chi sei, su cosa state lavorando, le decisioni recenti. Quello viaggia con la memoria persistente e l'agente lo ritroverà sul nuovo canale.

**Mappare le identità.** Se uso Telegram come UID `123456` e Slack come `U0ABCDEF`, l'agente vede *due persone diverse* — a meno che tu non glielo dica. Nel `USER.md` (o nella sezione *identities* del config) puoi mappare esplicitamente l'identità unica:

```yaml
users:
  - id: gian-angelo
    identities:
      telegram: "123456"
      slack: "U0ABCDEF"
      whatsapp: "+39 333 1234567"
```

Da quel momento le tre identità collassano sull'utente `gian-angelo` e la *session unification* (vista nella sezione precedente) funziona davvero.

**Cutover graduale.** Tieni il vecchio canale attivo per due-quattro settimane in parallelo al nuovo. Sposta un cron alla volta (es. prima il digest mattutino, poi le notifiche, poi i task interattivi), e monitora che tutto funzioni sul nuovo prima di disattivare il vecchio. Quando sei sicuro:

```bash
openclaw channels disable --channel whatsapp-baileys
# disconnects but keeps config

openclaw channels remove --channel whatsapp-baileys
# permanently removes config
```

`disable` è reversibile in qualunque momento (`channels enable`); `remove` cancella la configurazione e richiede di rifare il login per riabilitare il canale.

### Sicurezza dei canali: cose da non dimenticare

Quattro regole che valgono per tutti i canali, e che fanno la differenza fra un setup amatoriale e uno difensivo.

**Token nel password manager, mai in chiaro.** Telegram, Slack, Discord, WhatsApp Cloud, Matrix: tutti generano credenziali. Tutte devono vivere in un password manager. Quando lavori con file di config che contengono token (es. `~/.openclaw/secrets.env`), proteggi i file con permessi restrittivi (`chmod 600`) e *escludili* da qualunque sincronizzazione cloud non cifrata.

**Webhook secrets dove servono.** WhatsApp Cloud, Slack (signing secret), Microsoft Teams: usano *signing secret* o *verify token* per firmare i payload in arrivo. Senza la verifica della firma, chiunque conosca il tuo webhook URL può inviarti messaggi finti. OpenClaw verifica le firme automaticamente, ma solo se hai inserito il secret nel config.

**Rotazione periodica.** Almeno una volta all'anno, ruota i token che non hanno scadenza naturale: BotFather permette `/revoke`, Slack permette di revocare il token e generarne uno nuovo, Discord ha *Reset Token* (occhio: rompe il bot fino a quando non aggiorni la config). Segna l'evento in calendario.

**Mention gating e DM policy sempre.** Nessun bot OpenClaw dovrebbe vivere con `dmPolicy: open` se ha accesso a tool sensibili. Nei gruppi, *sempre* mention gating attivo: una notifica push del bot per ogni messaggio è il modo migliore per essere disattivato da chi ti circonda nel giro di una settimana.

## Prompt pronti all'uso

I prompt che seguono sono pensati per essere incollati direttamente in chat con l'agente, una volta che il primo canale (di solito Telegram) è collegato. Usali nei primi minuti per validare la configurazione.

**Prompt 1 — verifica del setup canali:**

> "Fai un controllo dei canali collegati: lista quelli attivi, lo stato di ognuno, l'ultimo messaggio ricevuto per canale, e qualunque errore visibile nei log delle ultime 24 ore. Se trovi un canale in stato `disconnected` o `error`, dimmi come ripararlo passo per passo."

**Prompt 2 — onboarding di un gruppo Telegram:**

> "Sto per aggiungerti a un gruppo Telegram famigliare di otto persone. Prima di farlo, voglio che tu: (1) attivi `mentionGating` e `replyTags` sul canale Telegram, (2) imposti `chunking.maxChars` a 3500, (3) registri in IDENTITY.md la nota che in questo gruppo devi essere conciso e mai parlare se non menzionato direttamente. Confermami quando hai applicato tutto e mostrami il diff del config."

**Prompt 3 — passaggio da Baileys a WhatsApp Cloud:**

> "Voglio migrare dal canale `whatsapp-baileys` a `whatsapp-cloud`. Spiegami nell'ordine: (1) cosa devo preparare lato Meta Business Suite, (2) quali credenziali servono (Phone Number ID, WABA ID, Permanent Token, verify token), (3) come faccio il cutover senza perdere lo storico delle conversazioni, (4) quali costi mensili devo aspettarmi per ~500 messaggi utility al mese verso utenti italiani. Niente preamboli."

**Prompt 4 — verifica sicurezza canali:**

> "Audit di sicurezza sui canali collegati: per ogni canale dimmi (a) quale `dmPolicy` è attiva, (b) se i secret/signing secret sono configurati, (c) se l'allowlist degli UID/numeri è popolata, (d) quando è stato ruotato l'ultima volta il token. Se qualcosa è sotto-standard, proponimi il fix con il comando esatto da lanciare."

## Errori comuni e come risolverli

Tabella spezzata in due per leggibilità su A5.

Errori di Telegram:

| Sintomo | Causa probabile | Fix |
|---|---|---|
| Il bot non risponde | Token errato o secondo Gateway in long-polling | `openclaw channels status`; rigenerare token in @BotFather; spegnere il Gateway duplicato |
| Risposte tagliate a metà nei gruppi | `chunking` non attivo | Attivare `chunking.enabled: true`, `maxChars: 3500` |
| Bot risponde a ogni messaggio in gruppo | Mention gating off + privacy off | `/setprivacy` su `enabled` in BotFather + `mentionGating: true` in config |

Errori di WhatsApp:

| Sintomo | Causa probabile | Fix |
|---|---|---|
| QR Baileys scade | Tempo limite stretto | Avere lo smartphone in mano prima del comando, ripetere |
| Account bannato (Baileys) | Eccesso di traffico, fingerprinting | Numero secondario, ridurre frequenza, valutare Cloud API |
| Webhook Cloud API non riceve | Verify token mancante o URL HTTPS non valido | Verificare la verify nella console Meta; OpenClaw richiede HTTPS pubblico o tunnel |

Errori di Slack/Discord:

| Sintomo | Causa probabile | Fix |
|---|---|---|
| Slack: `not_authed` | Token `xapp-...` o `xoxb-...` non valido | Rigenerare in *App-Level Tokens* o reinstallare app nel workspace |
| Discord: bot non legge i messaggi | MESSAGE_CONTENT intent non attivo | Developer Portal → Bot → attivare l'intent; valutare passaggio a slash commands |
| Discord: necessità di verifica >100 server | Bot cresciuto oltre soglia | Sottomettere la verifica oppure migrare a slash commands |

Errori di iMessage/Signal/Matrix:

| Sintomo | Causa probabile | Fix |
|---|---|---|
| iMessage nativo non funziona | Full Disk Access non concesso | macOS → Privacy → Full Disk Access → aggiungere OpenClaw |
| Signal `signal-cli` non riceve | Daemon non attivo, account non linkato | Rilanciare `signal-cli ... daemon --dbus`; rifare link |
| Matrix: 401 Unauthorized | Access token scaduto | Rigenerare dall'account bot sull'homeserver |

## Checklist di fine capitolo

- [ ] Almeno un canale collegato e verificato (`openclaw channels status`)
- [ ] Test di andata e ritorno: ho mandato un messaggio e ho ricevuto risposta entro pochi secondi
- [ ] `dmPolicy` impostata su `pairing` o `allowlist` (mai `open`) sul canale principale
- [ ] Mention gating attivo se ho aggiunto il bot in almeno un gruppo
- [ ] Tutti i token (Telegram, Slack, Discord, WhatsApp, ecc.) salvati in password manager, fuori da Git
- [ ] Signing secret / verify token configurati dove applicabile (Slack, WhatsApp Cloud, Teams)
- [ ] Streaming Telegram (Bot API 9.5+) attivo o disattivo coscientemente, non per default ignorato
- [ ] Se uso WhatsApp Baileys: numero secondario, allowlist attiva, frequenza messaggi sotto controllo
- [ ] Se uso WhatsApp Cloud: pricing previsto a mente, budget mensile stimato
- [ ] Annotata in calendario la prossima rotazione dei token (entro 12 mesi)

## Link e risorse utili

Le fonti citate in questo capitolo. La raccolta completa di tutte le fonti del libro si trova nell'[Appendice E](../Appendici/E-risorse-e-link-utili.md).

Telegram — [Bot API changelog ufficiale](https://core.telegram.org/bots/api-changelog), [Bot API reference](https://core.telegram.org/bots/api), [Telegram Mini Apps](https://core.telegram.org/bots/webapps), [GramIO 9.5 changelog](https://gramio.dev/changelogs/2026-03-02).

WhatsApp — [WhatsApp Business API pricing 2026 (EngageLab)](https://www.engagelab.com/blog/whatsapp-business-api-pricing), [WhatsApp Chatbot Rules 2026 (Conferbot)](https://www.conferbot.com/blog/whatsapp-chatbot-rules-2026), [Meta blocks third-party AI chatbots (Chatboq)](https://chatboq.com/blogs/third-party-ai-chatbots-ban), [Baileys repository (WhiskeySockets)](https://github.com/WhiskeySockets/Baileys).

Slack — [Slack Bolt for JavaScript docs](https://tools.slack.dev/bolt-js/concepts/socket-mode/), [Socket Mode reference](https://api.slack.com/apis/socket-mode), [App-Level Tokens](https://api.slack.com/authentication/token-types#app-level).

Discord — [Privileged Gateway Intents FAQ (Discord)](https://support-dev.discord.com/hc/en-us/articles/4404772028055-Message-Content-Privileged-Intent-FAQ), [Discord Intents 2026 practical guide (Space-Node)](https://space-node.net/blog/discord-gateway-intents-message-content-2026).

iMessage / Signal / Matrix — [OpenClaw BlueBubbles docs](https://docs.openclaw.ai/channels/bluebubbles), [signal-cli wiki (AsamK)](https://github.com/AsamK/signal-cli/wiki/Quickstart), [matrix-appservice-bridge](https://github.com/matrix-org/matrix-appservice-bridge).

OpenClaw — [Configuration reference](https://docs.openclaw.ai/gateway/configuration), [Multi-channel setup (LumaDock)](https://lumadock.com/tutorials/openclaw-multi-channel-setup), [Channel integration guide (YingTu)](https://yingtu.ai/en/blog/openclaw-messaging-channel-integration-guide).

---

[← Capitolo 5](./05-installazione-step-by-step.md)  ·  [Indice](../README.md)  ·  [Capitolo 7 →](../PARTE-III-Primo-mese/07-prima-conversazione-onboarding-agente.md)
