# Capitolo 12 — Comunicazione e coordinamento tra agenti [★★★]

**Cosa imparerai:**
- L'architettura multi-agente: workspace, binding, routing
- Pattern di collaborazione su progetti condivisi
- Gestire conflitti e sovrapposizioni di competenza
- Pattern di escalation: quando un agente chiede aiuto a un altro

**Contenuto principale:**

1. **Architettura.** Ogni agente ha il proprio workspace (cartella `.openclaw/[nome]-workspace`), le proprie skill, i propri cron, la propria memoria. Il Gateway instrada i messaggi all'agente corretto in base al canale, all'account, o al peer.

2. **Collaborazione.** Come far lavorare due agenti sullo stesso progetto:
   - Condivisione di file via filesystem condiviso
   - Un agente può "parlare" a un altro via canale interno
   - Pattern "delega": l'agente PA assegna un task all'agente developer su Linear

3. **Conflitti.** Cosa succede se due agenti ricevono lo stesso messaggio? Regole di routing per evitare sovrapposizioni. Mention gating nei gruppi.

4. **Escalation.** Pattern: l'agente support non sa rispondere → chiede all'agente developer → risponde al canale con la risposta arricchita.

---

## PARTE V — Sicurezza e costi

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

[← Capitolo 11](./11-progettare-il-tuo-team-di-agenti.md)  ·  [Indice](../README.md)  ·  [Capitolo 13 →](../PARTE-V-Sicurezza-costi/13-sicurezza-la-guida-che-devi-leggere.md)
