# Capitolo 15 — Care and feeding: tenere il tuo agente in salute [★★]

## Cosa imparerai

- Come diagnosticare un agente che non risponde
- Come usare Screen Sharing e Remote Login per accesso remoto
- Come far "riparare" l'agente da solo
- Come gestire aggiornamenti e backup

## Prerequisiti

Aver fatto installazione ([Capitolo 5](../PARTE-II-Installazione/05-installazione-step-by-step.md)) e onboarding ([Capitolo 7](../PARTE-III-Primo-mese/07-prima-conversazione-onboarding-agente.md)). Il capitolo prende senso dopo almeno una settimana di uso quotidiano.

## Contenuto principale

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

**Prompt pronto:**
> "Fai una diagnosi completa di te stesso e dimmi se sei in salute. Esegui: (1) `openclaw status` e `openclaw doctor` e interpretane i risultati, (2) lista i tuoi cron attivi (`openclaw crons list`) e segnala quelli che non scattano da più di 48 ore, (3) verifica con `openclaw channels status` che tutti i canali siano connessi, (4) controlla le dimensioni del knowledge graph e segnala se c'è materiale obsoleto da archiviare. Riporta tutto in un singolo messaggio breve."

## Errori comuni e come risolverli

| Sintomo | Causa probabile | Fix |
|---------|-----------------|-----|
| L'agente non risponde da ore | Computer in sleep, connessione caduta o Gateway crashato | `openclaw status`, `openclaw channels status`, riavviare il Gateway con `openclaw start`. |
| Cron che non scatta più | Cambio DST (timezone) o file di configurazione modificato | `openclaw crons list` per verificare schedule e timezone; chiedere all'agente "ispeziona i tuoi cron". |
| Errore "out of memory" o risposte tronche | Contesto troppo grande, knowledge graph stantio | Pulire le note obsolete, archiviare conversazioni antiche, limitare la finestra di memoria. |
| Aggiornamento rompe configurazioni esistenti | Breaking changes non letti nel changelog | Sempre `openclaw update` su ambiente di test prima della produzione; leggere il CHANGELOG. |

## Checklist di fine capitolo

- [ ] So fare diagnosi rapida (`openclaw status`, `openclaw doctor`)
- [ ] Accesso remoto configurato (Screen Sharing/SSH/Tailscale) per intervenire da fuori
- [ ] Backup periodico della cartella `.openclaw/` impostato
- [ ] So aggiornare con `openclaw update` dopo aver letto il changelog
- [ ] Ho un "medico digitale" (Claude Code o altro) per debug profondi

## Link e risorse utili

- [Documentazione ufficiale](https://docs.openclaw.ai) — reference dei comandi `openclaw status`, `doctor`, `update`
- [Repository GitHub](https://github.com/openclaw/openclaw) — changelog e issue tracker per i breaking changes

Per l'elenco completo delle fonti del libro, vedi [Appendice E](../Appendici/E-risorse-e-link-utili.md).

---

[← Capitolo 14](../PARTE-V-Sicurezza-costi/14-gestire-i-costi-senza-sorprese.md)  ·  [Indice](../README.md)  ·  [Capitolo 16 →](./16-ottimizzare-la-qualita-delle-risposte.md)
