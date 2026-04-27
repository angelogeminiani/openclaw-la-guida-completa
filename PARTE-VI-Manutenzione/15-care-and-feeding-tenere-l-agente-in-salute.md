# Capitolo 15 — Care and feeding: tenere il tuo agente in salute [★★]

**Cosa imparerai:**
- Come diagnosticare un agente che non risponde
- Come usare Screen Sharing e Remote Login per accesso remoto
- Come far "riparare" l'agente da solo
- Come gestire aggiornamenti e backup

**Contenuto principale:**

1. **"Hellooooo?"** L'agente smetterà di rispondere. I cron si romperanno. È normale — come con un team umano.

2. **Diagnosi.** Checklist rapida:
   - Il computer è acceso e connesso?
   - OpenClaw è in esecuzione? (`openclaw status`)
   - Il canale è connesso? (`openclaw channels status`)
   - Il cron è attivo? (`openclaw crons list`)

3. **Accesso remoto.** Per hardware fisico (Mac Mini):
   - Attivare Screen Sharing e Remote Login nelle impostazioni di sistema
   - Accedere dal laptop principale (stessa rete Wi-Fi) senza monitor/tastiera/mouse

4. **"Chiedi di ripararsi."** L'agente può diagnosticare e risolvere molti problemi da solo:
   - "Ispeziona i tuoi cron e dimmi se qualcosa è rotto"
   - "Cosa c'è nel tuo TOOLS.md? Qualcosa da aggiornare?"
   - "Scrivi nel tuo SOUL.md che devi ricordare [X]"

5. **Claude Code come "medico".** Se l'agente è veramente rotto, aprire Claude Code nella cartella `.openclaw/`, incollare i docs, e chiedere di riparare la configurazione.

6. **Aggiornamento.** `openclaw update` — prestare attenzione ai breaking changes. Leggere il changelog prima di aggiornare.

7. **Backup.** Copiare regolarmente la cartella `.openclaw/` su un disco esterno o un servizio cloud.

## Errori comuni e come risolverli

> *Sezione da rifinire in fase di stesura. Annota qui i sintomi reali che incontri seguendo il capitolo, le cause probabili e i fix verificati.*

| Sintomo | Causa probabile | Fix |
|---------|-----------------|-----|
| _TODO_ | _TODO_ | _TODO_ |

## Checklist di fine capitolo

> *Da adattare ai passi concreti coperti in questo capitolo.*

- [ ] _TODO: punto di verifica chiave 1_
- [ ] _TODO: punto di verifica chiave 2_
- [ ] _TODO: punto di verifica chiave 3_


---

[← Capitolo 14](../PARTE-V-Sicurezza-costi/14-gestire-i-costi-senza-sorprese.md)  ·  [Indice](../README.md)  ·  [Capitolo 16 →](./16-ottimizzare-la-qualita-delle-risposte.md)
