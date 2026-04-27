# Capitolo 10 — Perché un solo agente non basta [★★]

**Cosa imparerai:**
- Il principio della specializzazione applicato agli agenti AI
- Come aggiungere un nuovo agente con un comando
- Come i workspace separati garantiscono isolamento
- Come trasferire conoscenza tra agenti

**Contenuto principale:**

1. **Il principio della specializzazione.** Come dice Claire Vo: "Ho scoperto che non dovresti cercare di far fare tutto a un solo agente." Un agente con identità stretta fa un lavoro migliore ed è più divertente da usare. La metafora del team: ogni agente ha un ruolo, come ogni dipendente ha una mansione.

2. **Aggiungere un agente.** Un singolo comando:
   ```
   openclaw agents add <nome_agente>
   ```
   Si ripete l'onboarding per il nuovo agente. Il nuovo agente ha workspace separato: identità, tool, cron, memoria — tutto isolato.

3. **Routing e binding.** Come instradare i canali verso agenti specifici: ogni canale (o account/peer) può essere "bindato" a un agente. Esempio: Telegram personale → Polly, Slack aziendale → Max.

4. **Trasferire conoscenza.** Far "migrare" competenze tra agenti:
   
   > "Hey Bob, ho appena creato Annie la Marketing Intern. Trasferisci tutto ciò che c'è nel tuo SOUL, nelle tue memorie e nei tuoi cron riguardo al marketing nel suo workspace, e cancellalo dal tuo."

**(i) Pro tip:** Il multi-agente è stato il vero unlock per Claire Vo. Invece di un bot che fa tutto, un team di bot specializzati produce risultati migliori, più velocemente, con meno errori.

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

[← Capitolo 9](../PARTE-III-Primo-mese/09-aggiungere-strumenti-e-integrazioni.md)  ·  [Indice](../README.md)  ·  [Capitolo 11 →](./11-progettare-il-tuo-team-di-agenti.md)
