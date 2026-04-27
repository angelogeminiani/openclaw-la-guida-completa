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
| `openclaw doctor` | Diagnostica automatica delle configurazioni | 5, 15 |
| `openclaw update` | Aggiorna OpenClaw alla versione più recente | 13, 15 |

## Agenti

| Comando | Descrizione | Capitolo |
|---------|-------------|----------|
| `openclaw agents add <nome>` | Crea un nuovo agente con il proprio workspace | 10 |
| `openclaw agents list` | Elenca gli agenti registrati | 10 |

## Canali

| Comando | Descrizione | Capitolo |
|---------|-------------|----------|
| `openclaw channels login --channel telegram` | Collega un bot Telegram via token | 6 |
| `openclaw channels status` | Stato dei canali connessi | 15 |

## Cron job

| Comando | Descrizione | Capitolo |
|---------|-------------|----------|
| `openclaw crons list` | Elenca i cron attivi per agente | 15, 18 |

## Sicurezza

| Comando | Descrizione | Capitolo |
|---------|-------------|----------|
| `openclaw security audit` | Audit di sicurezza automatico | 13 |

## Skill

| Comando | Descrizione | Capitolo |
|---------|-------------|----------|
| `openclaw plugins install` | Installa una skill da ClawHub o sorgente locale | 17 |

## Comandi in-channel (da inviare al bot)

| Comando | Descrizione | Capitolo |
|---------|-------------|----------|
| `/status` | Modello, token e costi della sessione corrente | 14 |

## Note

- I comandi possono cambiare tra versioni: verifica sempre con `openclaw --help` o `openclaw <sub> --help`.
- Per problemi di permessi (Docker, credenziali, sandbox) il primo passo è quasi sempre `openclaw doctor`.

---

[← Appendice A](./A-glossario.md)  ·  [Indice](../README.md)  ·  [Appendice C →](./C-template-soul-identity.md)
