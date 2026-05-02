# Capitolo 6 — Configurare Telegram (e altri canali) [★]

## Cosa imparerai

- Come creare un bot Telegram con @BotFather (step-by-step)
- Come configurare WhatsApp via Baileys
- Come collegare Slack e Discord per uso lavorativo
- Come scegliere il canale giusto per ogni caso d'uso

## Prerequisiti

Aver completato l'installazione del [Capitolo 5](./05-installazione-step-by-step.md). Smartphone con Telegram (per il setup iniziale del bot via @BotFather).

## Contenuto principale

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

**Prompt pronto:**
> "Guidami nella creazione di un bot Telegram da collegare a te. Spiegami in ordine: (1) cosa fare in @BotFather per ottenere il token, (2) come passarlo a `openclaw channels login --channel telegram`, (3) come testare che ci siamo davvero parlando, (4) come abilitare il mention gating se ti aggiungerò a un gruppo. Vai diretto, niente preamboli."

## Errori comuni e come risolverli

| Sintomo | Causa probabile | Fix |
|---------|-----------------|-----|
| Bot Telegram non risponde | Token incollato in modo incompleto o bot non attivato in @BotFather | Rigenerare il token in @BotFather e rifare `openclaw channels login --channel telegram`. |
| WhatsApp QR scade prima della scansione | Tempo limite stretto, smartphone lontano dalla scrivania | Avere lo smartphone in mano prima di lanciare il comando, ripetere se serve. |
| Account WhatsApp bannato | Troppo traffico automatizzato su numero personale | Usare un numero secondario dedicato all'agente; limitare il volume di messaggi automatici. |
| Nei gruppi l'agente risponde a ogni messaggio | Mention gating non attivo | Configurare il bot per rispondere solo se menzionato (`@nomebot`) o solo a comandi (`/`). |

## Checklist di fine capitolo

- [ ] Almeno un canale collegato (`openclaw channels status` lo conferma)
- [ ] Test di andata e ritorno: ho mandato un messaggio e ho ricevuto risposta
- [ ] Mention gating configurato per i gruppi (l'agente non risponde a tutto)
- [ ] Token e secrets salvati nel password manager, mai in chiaro

## Link e risorse utili

- [Documentazione ufficiale](https://docs.openclaw.ai) — reference dei canali supportati e dei comandi `openclaw channels`
- [OpenClaw Setup Guide 2026](https://popularaitools.ai/blog/openclaw-setup-guide-2026) — walkthrough con screenshot per Telegram e WhatsApp

Per l'elenco completo delle fonti del libro, vedi [Appendice E](../Appendici/E-risorse-e-link-utili.md).

---

[← Capitolo 5](./05-installazione-step-by-step.md)  ·  [Indice](../README.md)  ·  [Capitolo 7 →](../PARTE-III-Primo-mese/07-prima-conversazione-onboarding-agente.md)
