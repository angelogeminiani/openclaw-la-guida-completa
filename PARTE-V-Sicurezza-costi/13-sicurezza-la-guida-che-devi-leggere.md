# Capitolo 13 — Sicurezza: la guida che devi leggere [★]

**Cosa imparerai:**
- Il modello di rischio di OpenClaw
- Come difendersi dalla prompt injection
- Come gestire API key e secrets
- La checklist di sicurezza operativa

**Contenuto principale:**

1. **Il modello di rischio.** OpenClaw ha accesso completo al computer su cui gira. Può eseguire comandi, editare file, installare software, accedere alla rete, comunicare via email e API. Questo è ciò che lo rende utile — e ciò che lo rende pericoloso.

2. **Dati preoccupanti.** A febbraio 2026: 42.665 istanze esposte su internet, 9+ CVE nei primi 2 mesi, 20% delle skill su ClawHub identificate come malevole (~900 skill), campagna ClawHavoc con data exfiltration, la vulnerabilità ClawJacked che permette controllo remoto via WebSocket locale. Meta ha vietato l'uso interno. La Cina ha vietato l'uso negli uffici governativi e nelle imprese statali.

3. **Prompt injection.** Cos'è: istruzioni malevole nascoste in email, pagine web, o contenuti che l'agente processa. Esempio reale: il ricercatore Matvey Kukuy ha inviato un'email con un prompt malevolo incorporato, e l'istanza OpenClaw l'ha eseguito immediatamente. Difese: rinforzare le regole nel SOUL.md, limitare le azioni automatiche, richiedere approvazione per azioni critiche.

4. **Accesso al computer.** L'agente può: leggere/scrivere file, eseguire script, navigare il web, installare software. Mitigazioni: Docker sandbox nativo di OpenClaw (vedi Capitolo 4), NemoClaw (OpenShell di Nvidia per sandboxing), NanoClaw (container Docker isolati), limitare i permessi nel TOOLS.md.

5. **Comunicazione esterna.** Se ha email o API (Gmail, Twilio), l'agente può comunicare con il mondo esterno — e potenzialmente impersonare l'utente. Regola: definire esplicitamente nel SOUL.md e TOOLS.md come l'agente è autorizzato a comunicare.

6. **Skill di terze parti.** Caso Cisco: skill malevola su ClawHub che eseguiva data exfiltration e prompt injection senza che l'utente ne fosse consapevole. Regola: installare solo skill dal bundle ufficiale o da sviluppatori conosciuti. Leggere il SKILL.md prima di eseguire qualsiasi skill trovata online.

7. **Gestione API key e secrets.** Metodo: `.openclaw/.env` per le variabili d'ambiente. Usare 1Password o un password manager. Non condividere mai il file .env.

8. **Aggiornamenti e audit.**
   - `openclaw update` — aggiornamento alla versione più recente e sicura
   - `openclaw security audit` — audit di sicurezza automatico
   - `openclaw doctor` — diagnostica configurazioni rischiose
   - Programmare un cron sull'agente per eseguire questi comandi regolarmente

9. **Il caso MoltMatch.** Lo studente Jack Luo configura il suo agente per esplorare piattaforme come Moltbook. L'agente, senza istruzioni esplicite, crea un profilo su MoltMatch (piattaforma di dating per agenti AI) e inizia a scremare potenziali match. Morale: definire confini chiari nel SOUL.md su cosa l'agente può e non può fare autonomamente.

10. **Avvertimento di Shadow (maintainer OpenClaw):** "Se non sai come eseguire un comando da terminale, questo progetto è troppo pericoloso per te."

**(!) Attenzione:** Non condividere MAI il bot in un gruppo chat pubblico. Chiunque possa inviare messaggi al bot può istruirlo.

**Checklist di sicurezza operativa** (stampabile):
- [ ] OpenClaw gira su un dispositivo dedicato (non il computer personale)
- [ ] Sandbox Docker attivo (vedi Capitolo 4 per i livelli di isolamento)
- [ ] API key con scope minimo necessario
- [ ] Token read-only per tutte le integrazioni finché non ci si fida
- [ ] SOUL.md con regole esplicite su cosa l'agente NON deve fare
- [ ] `openclaw update` eseguito almeno settimanalmente
- [ ] `openclaw security audit` eseguito almeno mensilmente
- [ ] File .env protetto e mai condiviso
- [ ] Nessuna skill di terze parti non verificata installata
- [ ] Bot non esposto in gruppi pubblici
- [ ] Screen Sharing e Remote Login configurati per accesso di emergenza

## Errori comuni e come risolverli

> *Sezione da rifinire in fase di stesura. Annota qui i sintomi reali che incontri seguendo il capitolo, le cause probabili e i fix verificati.*

| Sintomo | Causa probabile | Fix |
|---------|-----------------|-----|
| _TODO_ | _TODO_ | _TODO_ |


---

[← Capitolo 12](../PARTE-IV-Multi-agente/12-comunicazione-e-coordinamento-tra-agenti.md)  ·  [Indice](../README.md)  ·  [Capitolo 14 →](./14-gestire-i-costi-senza-sorprese.md)
