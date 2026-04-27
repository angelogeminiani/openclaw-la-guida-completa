# Capitolo 18 — Cron job e automazioni avanzate [★★★]

**Cosa imparerai:**
- L'anatomia di un cron job in OpenClaw
- Pattern temporali e trigger
- Cron ricorsivi: cron che creano altri cron
- Debugging dei cron

**Contenuto principale:**

1. **Anatomia.** Un cron job è un'istruzione programmata che si ripete: orario, giornaliero, settimanale, su evento.

2. **Pattern.** Mattina (digest, check), sera (wrap-up, review), settimanale (report, audit), su evento (nuovo messaggio, nuova iscrizione).

3. **Cron ricorsivi.** L'agente può crearsi nuovi cron autonomamente. Esempio: "Ogni lunedì, verifica se ci sono nuovi competitor e, se sì, crea un cron giornaliero per monitorarli."

4. **Debugging.** `openclaw crons list` per verificare i cron attivi. Chiedere all'agente: "Ispeziona i tuoi cron e dimmi cosa è rotto."

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

[← Capitolo 17](./17-creare-skill-personalizzate.md)  ·  [Indice](../README.md)  ·  [Capitolo 19 →](./19-deploy-su-vps-e-infrastruttura-cloud.md)
