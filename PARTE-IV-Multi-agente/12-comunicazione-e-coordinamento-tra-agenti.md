# Capitolo 12 — Comunicazione e coordinamento tra agenti [★★★]

## Cosa imparerai

- L'architettura multi-agente: workspace, binding, routing
- Pattern di collaborazione su progetti condivisi
- Gestire conflitti e sovrapposizioni di competenza
- Pattern di escalation: quando un agente chiede aiuto a un altro

## Prerequisiti

Avere almeno due agenti definiti (vedi [Capitolo 11](./11-progettare-il-tuo-team-di-agenti.md)). Familiarità con i concetti di sessione e canale ([Capitolo 2](../PARTE-I-Capire-OpenClaw/02-anatomia-di-un-agente-openclaw.md)).

## Contenuto principale

1. **Architettura.** Ogni agente ha il proprio workspace (cartella `.openclaw/[nome]-workspace`), le proprie skill, i propri cron, la propria memoria. Il Gateway instrada i messaggi all'agente corretto in base al canale, all'account, o al peer.

2. **Collaborazione.** Come far lavorare due agenti sullo stesso progetto:
   - Condivisione di file via filesystem condiviso
   - Un agente può "parlare" a un altro via canale interno
   - Pattern "delega": l'agente PA assegna un task all'agente developer su Linear

3. **Conflitti.** Cosa succede se due agenti ricevono lo stesso messaggio? Regole di routing per evitare sovrapposizioni. Mention gating nei gruppi.

4. **Escalation.** Pattern: l'agente support non sa rispondere → chiede all'agente developer → risponde al canale con la risposta arricchita.

**Prompt pronto:**
> "Voglio impostare un pattern coordinatore tra [Agente A, ruolo PA] e [Agente B, ruolo developer]. Quando arriva un task complesso, A lo scompone, delega la parte tecnica a B con `sessions_send`, attende il risultato e mi risponde. Aiutami a: (1) configurare il binding A↔B nei rispettivi TOOLS.md, (2) impostare un budget massimo di 5 iterazioni per evitare loop, (3) scrivere il prompt di delega che A userà verso B, (4) testare il flusso end-to-end su un task reale."

## Errori comuni e come risolverli

| Sintomo | Causa probabile | Fix |
|---------|-----------------|-----|
| Loop infinito tra due agenti che si rispondono | Nessun budget di iterazioni configurato | Impostare `max-turns` nel cron o nel pattern coordinatore. |
| Agente A non riesce a parlare con B | Routing/binding non configurato in TOOLS.md | Aggiungere `peer:B` nel TOOLS.md di A e verificare con `openclaw agents list`. |
| Messaggio duplicato in un gruppo (due agenti rispondono) | Mention gating assente o due agenti "owner" sovrapposti | Mention gating attivo + un solo agente designato come owner del gruppo. |
| Pattern coordinatore non scala | Il coordinatore diventa collo di bottiglia | Trasformare task indipendenti in `sessions_spawn` paralleli invece di sequenziali. |

## Checklist di fine capitolo

- [ ] Configurato almeno un pattern coordinatore/esecutore tra due agenti
- [ ] Budget di iterazioni impostato per evitare loop infiniti
- [ ] Mention gating attivo nei gruppi multi-agente
- [ ] Testato un pattern di escalation (support → developer) su un task reale

## Link e risorse utili

- [Documentazione ufficiale](https://docs.openclaw.ai) — reference su `sessions_send`, `sessions_spawn`, binding e routing
- [Architecting the Agentic Future](https://dev.to/mechcloud_academy/architecting-the-agentic-future-openclaw-vs-nanoclaw-vs-nvidias-nemoclaw-9f8) — pattern multi-agente a confronto

Per l'elenco completo delle fonti del libro, vedi [Appendice E](../Appendici/E-risorse-e-link-utili.md).

---

[← Capitolo 11](./11-progettare-il-tuo-team-di-agenti.md)  ·  [Indice](../README.md)  ·  [Capitolo 13 →](../PARTE-V-Sicurezza-costi/13-sicurezza-la-guida-che-devi-leggere.md)
