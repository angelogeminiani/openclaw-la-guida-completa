# Capitolo 6 — Configurare Telegram (e altri canali) [★]

**Cosa imparerai:**
- Come creare un bot Telegram con @BotFather (step-by-step)
- Come configurare WhatsApp via Baileys
- Come collegare Slack e Discord per uso lavorativo
- Come scegliere il canale giusto per ogni caso d'uso

**Contenuto principale:**

1. **Telegram (consigliato per iniziare).** Guida passo-passo completa:
   - Scaricare Telegram sul telefono
   - Aprire una chat con @BotFather
   - Creare un nuovo bot (/newbot), scegliere nome e username
   - Copiare il token API
   - Collegare il token a OpenClaw: `openclaw channels login --channel telegram`
   - Test: inviare il primo messaggio al bot

2. **WhatsApp (via Baileys).** Il canale più "naturale" per l'uso personale, ma più complesso:
   - Setup del bridge Baileys
   - Scansione QR code
   - Limiti: no gruppi business, rischio ban se si invia troppo spam

3. **Slack e Discord.** Per team di lavoro:
   - Creazione app Slack con Bolt
   - Creazione bot Discord con discord.js
   - Routing dei canali verso agenti specifici

4. **Canali avanzati.**
   - Signal (signal-cli) — massima privacy, setup complesso
   - iMessage (BlueBubbles consigliato, legacy imsg disponibile) — solo con hardware Apple
   - Microsoft Teams — per ambienti corporate
   - Matrix — per utenti open-source / privacy-first
   - WeChat — plugin ufficiale Tencent (WeChat > Impostazioni > Plugin > ClawBot)
   - Google Chat, Feishu, LINE, IRC e altri

5. **Come scegliere.** Tabella decisionale per caso d'uso:
   - Uso personale → Telegram o WhatsApp
   - Famiglia → WhatsApp (gruppo familiare)
   - Team di lavoro → Slack o Discord
   - Privacy massima → Signal o Matrix
   - Ecosistema Apple → iMessage via BlueBubbles
   - Mercato cinese → WeChat

---

## PARTE III — Il primo mese con OpenClaw

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

[← Capitolo 5](./05-installazione-step-by-step.md)  ·  [Indice](../README.md)  ·  [Capitolo 7 →](../PARTE-III-Primo-mese/07-prima-conversazione-onboarding-agente.md)
