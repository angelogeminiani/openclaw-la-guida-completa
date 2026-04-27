# Capitolo 20 — L'architettura del Gateway [★★★]

**Cosa imparerai:**
- Il WebSocket control plane e il modello di sessione
- La media pipeline (immagini, audio, video)
- Il Pi agent runtime (RPC, streaming)
- Le companion app (macOS, iOS, Android)
- Live Canvas e A2UI

**Contenuto principale:**

1. **Il Gateway.** È il "cervello" di OpenClaw: un control plane WebSocket (`ws://127.0.0.1:18789`) che gestisce sessioni, canali, tool ed eventi. Tutto passa dal Gateway.

2. **Sessioni.** Tipi: main (chat 1:1), group isolation, activation modes, queue modes, reply-back. Il modello di sessione determina come l'agente processa i messaggi in arrivo.

3. **Media pipeline.** Come l'agente gestisce immagini, audio e video: trascrizione automatica, size caps, lifecycle dei file temporanei.

4. **Pi agent runtime.** L'agente gira in modalità RPC con tool streaming e block streaming. Architettura per integrazioni avanzate.

5. **Companion app.** 
   - macOS: menu bar con Voice Wake, push-to-talk, WebChat, debug tools
   - iOS/Android: nodes che si connettono al Gateway via WebSocket
   - Windows: System Tray app, shared library, PowerToys Command Palette extension

6. **Live Canvas e A2UI.** L'Agent-to-UI: l'agente può creare interfacce visive dinamiche in tempo reale.

7. **Lobster.** Il workflow shell OpenClaw-native: pipeline composabili tipizzate, local-first, per trasformare skill/tool in automazioni sicure.

---

## PARTE VIII — Visione e futuro

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

[← Capitolo 19](./19-deploy-su-vps-e-infrastruttura-cloud.md)  ·  [Indice](../README.md)  ·  [Capitolo 21 →](../PARTE-VIII-Visione-futuro/21-ecosistema-openclaw.md)
