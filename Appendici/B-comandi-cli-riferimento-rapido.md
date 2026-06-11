# Appendice B — Comandi CLI di riferimento rapido

Comandi `openclaw` e affini usati nel libro, raggruppati per area. Tutti i comandi vanno lanciati nel terminale del computer su cui gira OpenClaw, salvo dove indicato.

## Installazione e bootstrap

| Comando | Descrizione | Capitolo |
|---------|-------------|----------|
| `curl -fsSL https://openclaw.ai/install.sh \| bash` | Installazione completa (richiede Node.js 22+) | 5 |
| `./scripts/docker/setup.sh` | Setup Gateway containerizzato in Docker Compose | 4 |
| `OPENCLAW_SANDBOX=1 ./scripts/docker/setup.sh` | Setup containerizzato + sandbox aggiuntivo | 4 |
| `docker sandbox create --name openclaw` | Sandbox Docker ufficiale (MicroVM, credential proxy) | 4 |

## Stato e diagnostica

| Comando | Descrizione | Capitolo |
|---------|-------------|----------|
| `openclaw status` | Stato corrente di OpenClaw (running/stopped) | 15 |
| `openclaw gateway start\|stop\|restart\|status` | Controlla il processo Gateway | 5, 14, 15 |
| `openclaw doctor` | Diagnostica automatica delle configurazioni (`--fix` ripara) | 5, 15 |
| `openclaw logs --follow` | Log del Gateway in tempo reale | 5, 14, 15 |
| `openclaw cost report --since <periodo>` | Report dei costi LLM (richiede hook `cost-tracker`) | 5, 8, 14, 15 |
| `openclaw sessions list` | Elenca le sessioni attive | 2 |
| `openclaw update` | Aggiorna OpenClaw alla versione più recente | 13, 14, 15 |

## Agenti

| Comando | Descrizione | Capitolo |
|---------|-------------|----------|
| `openclaw agents add <nome>` | Crea un nuovo agente con il proprio workspace | 10 |
| `openclaw agents list` | Elenca gli agenti registrati | 10 |

## Canali

| Comando | Descrizione | Capitolo |
|---------|-------------|----------|
| `openclaw channels login --channel telegram` | Collega un bot Telegram via token | 6, 15 |
| `openclaw channels status` | Stato dei canali connessi | 15 |

## Backup

| Comando | Descrizione | Capitolo |
|---------|-------------|----------|
| `openclaw backup create` | Archivio `.tar.gz` di stato e workspace | 5, 15 |
| `openclaw backup restore <file>` | Ripristina un archivio di backup | 5, 15 |

## Cron job

| Comando | Descrizione | Capitolo |
|---------|-------------|----------|
| `openclaw cron list` | Elenca i cron attivi per agente | 14, 15, 18 |
| `openclaw cron disable <id>` | Disattiva un cron (es. un loop impazzito) | 5, 14 |
| `openclaw cron add` | Crea un job (flag: `--cron`, `--at`, `--every`, `--tz`, `--session`, `--model`) | 18 |
| `openclaw cron show <id>` | Dettaglio del job e rotta di consegna | 18 |
| `openclaw cron edit <id>` | Modifica prompt o modello del job | 18 |
| `openclaw cron run <id> --wait` | Esecuzione di test immediata | 18 |
| `openclaw cron remove <id>` | Elimina il job | 18 |
| `openclaw cron runs --id <id>` | Storico esiti e durate dei run | 18 |
| `openclaw cron status` | Stato complessivo dello scheduler | 18 |

## Sicurezza

| Comando | Descrizione | Capitolo |
|---------|-------------|----------|
| `openclaw security audit` | Audit di sicurezza automatico | 13 |

## Skill

| Comando | Descrizione | Capitolo |
|---------|-------------|----------|
| `openclaw skills install <nome>` | Installa una skill da ClawHub o sorgente locale (le globali vanno in `~/.openclaw/skills/`) | 17 |
| `openclaw skills configure <nome>` | Configura una skill installata (es. `gog`) | 9 |
| `clawhub publish` | Pubblica una skill sul registry ClawHub | 17 |
| `clawhub sync` | Sincronizza le skill locali con ClawHub | 17 |

## Comandi in-channel (da inviare al bot)

| Comando | Descrizione | Capitolo |
|---------|-------------|----------|
| `/status` | Modello, token e costi della sessione corrente | 14 |
| `/reload` | Ricarica i file del workspace nella sessione corrente | 16 |

## Note

- I comandi possono cambiare tra versioni: verifica sempre con `openclaw --help` o `openclaw <sub> --help`.
- Per problemi di permessi (Docker, credenziali, sandbox) il primo passo è quasi sempre `openclaw doctor`.

---

[← Appendice A](./A-glossario.md)  ·  [Indice](../README.md)  ·  [Appendice C →](./C-template-soul-identity.md)
