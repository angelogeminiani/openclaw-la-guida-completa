# Capitolo 17 — Creare skill personalizzate [★★★]

## Cosa imparerai

- L'anatomia di una skill: directory + SKILL.md
- Come scrivere una skill da zero
- Come pubblicare su ClawHub
- Sicurezza delle skill: code review e sandboxing

## Prerequisiti

Aver già installato e usato qualche skill esistente ([Capitolo 9](../PARTE-III-Primo-mese/09-aggiungere-strumenti-e-integrazioni.md)). Conoscenza di base di Markdown e YAML. Per le skill con script, dimestichezza con un linguaggio di scripting (Python, Node, bash).

## Contenuto principale

1. **Anatomia.** Una skill è una directory contenente un file SKILL.md con metadati e istruzioni per l'uso dello strumento. Le skill possono essere: bundled (incluse con OpenClaw), globali (installate dall'utente), o di workspace (specifiche per un agente — priorità massima).

2. **ClawHub.** Il registry ufficiale delle skill: clawhub.com. 700+ skill della community, ma attenzione alla sicurezza (il 20% è stato identificato come malevolo).

3. **Scrivere una skill.** Guida passo-passo: creare la directory, scrivere il SKILL.md con schema, testare localmente, iterare.

4. **Pubblicare.** Come sottomettere una skill a ClawHub. Processo di review.

5. **Sicurezza.** Code review obbligatorio. Sandboxing con NemoClaw/OpenShell. Non installare mai skill non verificate in produzione.

**Prompt pronto:**
> "Voglio creare una skill custom che [descrivi cosa deve fare, es. "estrae i prezzi dei voli da Skyscanner per una rotta e date date"]. Aiutami a: (1) scrivere il SKILL.md con frontmatter completo (`name`, `description` con keyword chiare, `allowed-tools`), (2) scegliere se serve uno script in `scripts/` e in quale linguaggio, (3) testare la skill in sandbox prima di abilitarla, (4) decidere se pubblicarla su ClawHub o tenerla privata."

## Errori comuni e come risolverli

| Sintomo | Causa probabile | Fix |
|---------|-----------------|-----|
| La skill custom non viene "scoperta" dall'agente | Description nel SKILL.md poco specifico (parole chiave assenti) | Riscrivere description con parole chiave concrete legate ai casi d'uso. |
| Skill funziona localmente, fallisce in container | Dipendenze non installate nel sandbox | Aggiungere requirements.txt o package.json in `scripts/`, ricostruire l'immagine sandbox. |
| Skill da ClawHub non si installa: "signature verification failed" | Skill non firmata o checksum non corrisponde | NON forzare l'installazione; segnalare al maintainer o cercare alternativa firmata. |
| Skill troppo "chiacchierona" nelle risposte | Body di SKILL.md verboso, molti esempi caricati a ogni chiamata | Compattare il body, mettere gli esempi lunghi in `references/` (caricati on-demand). |

## Checklist di fine capitolo

- [ ] Almeno una skill custom funzionante in locale
- [ ] SKILL.md con frontmatter completo (name + description con keyword)
- [ ] Code review fatta sull'eventuale codice in `scripts/`
- [ ] Skill testata in sandbox prima di abilitarla in produzione
- [ ] Ho deciso se pubblicarla su ClawHub o tenerla privata

## Link e risorse utili

- [Documentazione ufficiale](https://docs.openclaw.ai) — reference completo del formato SKILL.md
- [ClawHub (skill registry)](https://clawhub.com) — registry ufficiale per cercare e pubblicare skill
- [OpenClaw vs NemoClaw vs NanoClaw Security](https://dev.to/_46ea277e677b888e0cd13/openclaw-vs-nemoclaw-vs-nanoclaw-ai-agent-platform-security-comparison-i3k) — rischi delle skill di terze parti e come mitigarli

Per l'elenco completo delle fonti del libro, vedi [Appendice E](../Appendici/E-risorse-e-link-utili.md).

---

[← Capitolo 16](../PARTE-VI-Manutenzione/16-ottimizzare-la-qualita-delle-risposte.md)  ·  [Indice](../README.md)  ·  [Capitolo 18 →](./18-cron-job-e-automazioni-avanzate.md)
