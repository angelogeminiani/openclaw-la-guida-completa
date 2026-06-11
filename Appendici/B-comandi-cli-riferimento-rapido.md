# Appendice B — Comandi CLI di riferimento rapido

Comandi `openclaw` e affini usati nel libro, raggruppati per area. Tutti i comandi vanno lanciati nel terminale del computer su cui gira OpenClaw, salvo dove indicato.

## Installazione e bootstrap

- `curl -fsSL https://openclaw.ai/install.sh | bash` —
  installazione completa (richiede Node.js 22+). (Cap. 5)
- `./scripts/docker/setup.sh` — setup Gateway
  containerizzato in Docker Compose. (Cap. 4)
- `OPENCLAW_SANDBOX=1 ./scripts/docker/setup.sh` — setup
  containerizzato + sandbox aggiuntivo. (Cap. 4)
- `docker sandbox create --name openclaw` — sandbox
  Docker ufficiale (MicroVM, credential proxy). (Cap. 4)

## Stato e diagnostica

- `openclaw status` — stato corrente di OpenClaw
  (running/stopped). (Cap. 15)
- `openclaw gateway start|stop|restart|status` —
  controlla il processo Gateway. (Cap. 5, 14, 15)
- `openclaw doctor` — diagnostica automatica delle
  configurazioni (`--fix` ripara). (Cap. 5, 15)
- `openclaw logs --follow` — log del Gateway in tempo
  reale. (Cap. 5, 14, 15)
- `openclaw cost report --since <periodo>` — report dei
  costi LLM (richiede hook `cost-tracker`).
  (Cap. 5, 8, 14, 15)
- `openclaw sessions list` — elenca le sessioni attive.
  (Cap. 2)
- `openclaw update` — aggiorna OpenClaw alla versione più
  recente. (Cap. 13, 14, 15)

## Agenti

- `openclaw agents add <nome>` — crea un nuovo agente con
  il proprio workspace. (Cap. 10)
- `openclaw agents list` — elenca gli agenti registrati.
  (Cap. 10)

## Canali

- `openclaw channels login --channel telegram` — collega
  un bot Telegram via token. (Cap. 6, 15)
- `openclaw channels status` — stato dei canali connessi.
  (Cap. 15)

## Backup

- `openclaw backup create` — archivio `.tar.gz` di stato
  e workspace. (Cap. 5, 15)
- `openclaw backup restore <file>` — ripristina un
  archivio di backup. (Cap. 5, 15)

## Cron job

- `openclaw cron list` — elenca i cron attivi per agente.
  (Cap. 14, 15, 18)
- `openclaw cron disable <id>` — disattiva un cron (es.
  un loop impazzito). (Cap. 5, 14)
- `openclaw cron add` — crea un job (flag: `--cron`,
  `--at`, `--every`, `--tz`, `--session`, `--model`).
  (Cap. 18)
- `openclaw cron show <id>` — dettaglio del job e rotta
  di consegna. (Cap. 18)
- `openclaw cron edit <id>` — modifica prompt o modello
  del job. (Cap. 18)
- `openclaw cron run <id> --wait` — esecuzione di test
  immediata. (Cap. 18)
- `openclaw cron remove <id>` — elimina il job. (Cap. 18)
- `openclaw cron runs --id <id>` — storico esiti e durate
  dei run. (Cap. 18)
- `openclaw cron status` — stato complessivo dello
  scheduler. (Cap. 18)

## Sicurezza

- `openclaw security audit` — audit di sicurezza
  automatico. (Cap. 13)

## Skill

- `openclaw skills install <nome>` — installa una skill
  da ClawHub o sorgente locale (le globali vanno in
  `~/.openclaw/skills/`). (Cap. 17)
- `openclaw skills configure <nome>` — configura una
  skill installata (es. `gog`). (Cap. 9)
- `clawhub publish` — pubblica una skill sul registry
  ClawHub. (Cap. 17)
- `clawhub sync` — sincronizza le skill locali con
  ClawHub. (Cap. 17)

## Comandi in-channel (da inviare al bot)

- `/status` — modello, token e costi della sessione
  corrente. (Cap. 14)
- `/reload` — ricarica i file del workspace nella
  sessione corrente. (Cap. 16)

## Note

- I comandi possono cambiare tra versioni: verifica sempre con `openclaw --help` o `openclaw <sub> --help`.
- Per problemi di permessi (Docker, credenziali, sandbox) il primo passo è quasi sempre `openclaw doctor`.

---

[← Appendice A](./A-glossario.md)  ·  [Indice](../README.md)  ·  [Appendice C →](./C-template-soul-identity.md)
