# Capitolo 18 — Cron job e automazioni avanzate [★★★]

## Cosa imparerai

- L'anatomia di un cron job in OpenClaw
- Pattern temporali e trigger
- Cron ricorsivi: cron che creano altri cron
- Debugging dei cron

## Prerequisiti

Aver già attivato almeno un workflow ricorrente ([Capitolo 8](../PARTE-III-Primo-mese/08-dieci-workflow-pronti-all-uso.md)). Familiarità con la sintassi cron è utile ma non obbligatoria: OpenClaw accetta anche linguaggio naturale.

## Contenuto principale

1. **Anatomia.** Un cron job è un'istruzione programmata che si ripete: orario, giornaliero, settimanale, su evento.

2. **Pattern.** Mattina (digest, check), sera (wrap-up, review), settimanale (report, audit), su evento (nuovo messaggio, nuova iscrizione).

3. **Cron ricorsivi.** L'agente può crearsi nuovi cron autonomamente. Esempio: "Ogni lunedì, verifica se ci sono nuovi competitor e, se sì, crea un cron giornaliero per monitorarli."

4. **Debugging.** `openclaw crons list` per verificare i cron attivi. Chiedere all'agente: "Ispeziona i tuoi cron e dimmi cosa è rotto."

**Prompt pronto:**
> "Voglio creare un cron che [descrivi: es. "ogni mattina alle 7:00 (Europe/Rome) mi mandi su Telegram un riassunto delle email importanti del giorno e dei meeting"]. Aiutami a: (1) scrivere l'espressione cron con timezone esplicito, (2) decidere se è un cron singolo o un pipeline di task dipendenti, (3) impostare un budget massimo di esecuzione per evitare costi a sorpresa, (4) testarlo con un primo run forzato e verificare il log."

## Errori comuni e come risolverli

| Sintomo | Causa probabile | Fix |
|---------|-----------------|-----|
| Il cron non scatta | Timezone non specificato (default UTC) o cron syntax errato | Aggiungere timezone esplicito (es. `Europe/Rome`); validare l'espressione cron con un parser online. |
| Il cron scatta due volte di seguito | Due cron sovrapposti per errore o cron + heartbeat che si pestano i piedi | `openclaw crons list` per verificare; eliminare il duplicato. |
| Meta-cron crea cron infiniti | Nessun budget o stop-condition | Aggiungere `max-iterations` o una stop-condition (data, contatore, file flag). |
| Il cron ha un costo mensile inaspettato | Frequenza troppo alta o modello costoso usato per ogni esecuzione | Ridurre frequenza, usare modelli più economici per task ripetitivi. |

## Checklist di fine capitolo

- [ ] Almeno un cron mattutino funzionante e verificato per 3 giorni
- [ ] Timezone esplicito su tutti i cron
- [ ] Budget di iterazioni e stop-condition impostati per i meta-cron
- [ ] Log dei cron riveduti almeno una volta a settimana
- [ ] Ho un cron "audit" che mi avvisa se la spesa supera la soglia

## Link e risorse utili

- [Documentazione ufficiale](https://docs.openclaw.ai) — reference della sintassi cron e dei comandi `openclaw crons`
- [Use OpenClaw to Build a Business That Runs Itself](https://creatoreconomy.so/p/use-openclaw-to-build-a-business-that-runs-itself-nat-eliason) — esempi di automazioni ricorrenti per un business reale

Per l'elenco completo delle fonti del libro, vedi [Appendice E](../Appendici/E-risorse-e-link-utili.md).

---

[← Capitolo 17](./17-creare-skill-personalizzate.md)  ·  [Indice](../README.md)  ·  [Capitolo 19 →](./19-deploy-su-vps-e-infrastruttura-cloud.md)
