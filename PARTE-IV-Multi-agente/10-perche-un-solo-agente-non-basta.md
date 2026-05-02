# Capitolo 10 — Perché un solo agente non basta [★★]

## Cosa imparerai

- Il principio della specializzazione applicato agli agenti AI
- Come aggiungere un nuovo agente con un comando
- Come i workspace separati garantiscono isolamento
- Come trasferire conoscenza tra agenti

## Prerequisiti

Avere già un agente attivo ([Capitolo 7](../PARTE-III-Primo-mese/07-prima-conversazione-onboarding-agente.md)) e averlo usato per almeno una settimana, così da capire dove serve davvero specializzare.

## Contenuto principale

1. **Il principio della specializzazione.** Come dice Claire Vo: "Ho scoperto che non dovresti cercare di far fare tutto a un solo agente." Un agente con identità stretta fa un lavoro migliore ed è più divertente da usare. La metafora del team: ogni agente ha un ruolo, come ogni dipendente ha una mansione.

2. **Aggiungere un agente.** Un singolo comando:
   ```
   openclaw agents add <nome_agente>
   ```
   Si ripete l'onboarding per il nuovo agente. Il nuovo agente ha workspace separato: identità, tool, cron, memoria — tutto isolato.

3. **Routing e binding.** Come instradare i canali verso agenti specifici: ogni canale (o account/peer) può essere "bindato" a un agente. Esempio: Telegram personale → Polly, Slack aziendale → Max.

4. **Trasferire conoscenza.** Far "migrare" competenze tra agenti:
   
   > "Hey Bob, ho appena creato Annie la Marketing Intern. Trasferisci tutto ciò che c'è nel tuo SOUL, nelle tue memorie e nei tuoi cron riguardo al marketing nel suo workspace, e cancellalo dal tuo."

**Prompt pronto:**
> "Voglio creare un secondo agente specializzato accanto a te. Si chiamerà [nome], si occuperà di [area, es. "gestione famiglia"]. Aiutami a: (1) lanciare `openclaw agents add` con i parametri giusti, (2) impostare il suo workspace, IDENTITY.md e una prima bozza di SOUL.md, (3) decidere quali tool gli servono e quali esplicitamente NON deve avere, (4) instradare verso di lui i messaggi del canale [Telegram / Slack / WhatsApp]."

**(i) Pro tip:** Il multi-agente è stato il vero unlock per Claire Vo. Invece di un bot che fa tutto, un team di bot specializzati produce risultati migliori, più velocemente, con meno errori.

## Errori comuni e come risolverli

| Sintomo | Causa probabile | Fix |
|---------|-----------------|-----|
| L'agente unico diventa "schizofrenico" nelle risposte | SOUL.md sovraccarico di responsabilità diverse | Dividere in 2-3 agenti specializzati (es. uno PA, uno developer). |
| Confusione su quale agente sta rispondendo | Nomi e canali poco distintivi | Nome + emoji distintivi + un canale dedicato per ogni agente quando possibile. |
| Conoscenza non condivisa tra agenti | Memorie completamente isolate | Filesystem condiviso per artefatti comuni, oppure `sessions_send` per trasferire contesto puntualmente. |

## Checklist di fine capitolo

- [ ] Ho identificato almeno un'area dove serve un secondo agente
- [ ] Ho creato un secondo agente con `openclaw agents add <nome>`
- [ ] I due agenti hanno workspace, identità, tool e cron separati
- [ ] So come instradare i messaggi al giusto agente (binding/routing)

## Link e risorse utili

- [The Complete Guide to Building Your Personal AI Agent](https://www.lennysnewsletter.com/p/openclaw-the-complete-guide-to-building) — come Claire Vo ha diviso il suo team in 9 agenti

Per l'elenco completo delle fonti del libro, vedi [Appendice E](../Appendici/E-risorse-e-link-utili.md).

---

[← Capitolo 9](../PARTE-III-Primo-mese/09-aggiungere-strumenti-e-integrazioni.md)  ·  [Indice](../README.md)  ·  [Capitolo 11 →](./11-progettare-il-tuo-team-di-agenti.md)
