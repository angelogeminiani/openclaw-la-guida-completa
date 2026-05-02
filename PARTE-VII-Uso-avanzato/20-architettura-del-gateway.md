# Capitolo 20 — L'architettura del Gateway [★★★]

## Cosa imparerai

- Il WebSocket control plane e il modello di sessione
- La media pipeline (immagini, audio, video)
- Il Pi agent runtime (RPC, streaming)
- Le companion app (macOS, iOS, Android)
- Live Canvas e A2UI

## Prerequisiti

Aver letto [Capitolo 2](../PARTE-I-Capire-OpenClaw/02-anatomia-di-un-agente-openclaw.md) e installato OpenClaw ([Capitolo 5](../PARTE-II-Installazione/05-installazione-step-by-step.md)). Conoscenza base di WebSocket e architetture client-server è utile ma non strettamente necessaria.

## Contenuto principale

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

**Prompt pronto:**
> "Spiegami l'architettura interna di te stesso, partendo dal Gateway. Voglio capire: (1) come funziona il control plane WebSocket su `127.0.0.1:18789`, (2) cosa succede quando arriva un messaggio Telegram (sequence diagram a parole), (3) come usi sessioni e queue mode quando ho più finestre aperte in parallelo, (4) la differenza tra il runtime RPC che esegui tu e una skill standard. Massimo un paragrafo per punto."

## Errori comuni e come risolverli

| Sintomo | Causa probabile | Fix |
|---------|-----------------|-----|
| Il WebSocket si disconnette ogni minuto | Timeout proxy/load balancer troppo basso | Aumentare timeout (es. nginx `proxy_read_timeout 3600s`) o keep-alive. |
| Companion app iOS/Android non si connette | Firewall del router blocca traffico in ingresso | Tailscale risolve senza port forwarding; alternativa: configurare port forwarding sul router. |
| Trascrizione audio fallisce | Media pipeline senza Whisper o senza provider remoto configurato | Installare Whisper localmente (`pip install openai-whisper`) o configurare un provider STT cloud. |
| Live Canvas/A2UI non renderizza | Versione gateway troppo vecchia o feature non abilitata | `openclaw update` + verificare il flag `experimental.a2ui` nella config. |

## Checklist di fine capitolo

- [ ] Capisco il ruolo del Gateway come control plane
- [ ] Verificato che il Gateway gira su `ws://127.0.0.1:18789` (default)
- [ ] Conosco i 5 input vector dell'autonomia
- [ ] So spiegare in due frasi cos'è una "session" e quali tipi esistono
- [ ] Conosco almeno una companion app (macOS/iOS/Android/Windows)

## Link e risorse utili

- [Documentazione ufficiale](https://docs.openclaw.ai) — reference del WebSocket control plane e del Pi agent runtime
- [Repository GitHub](https://github.com/openclaw/openclaw) — codice sorgente del Gateway
- [Architecting the Agentic Future](https://dev.to/mechcloud_academy/architecting-the-agentic-future-openclaw-vs-nanoclaw-vs-nvidias-nemoclaw-9f8) — inquadramento architetturale

Per l'elenco completo delle fonti del libro, vedi [Appendice E](../Appendici/E-risorse-e-link-utili.md).

---

[← Capitolo 19](./19-deploy-su-vps-e-infrastruttura-cloud.md)  ·  [Indice](../README.md)  ·  [Capitolo 21 →](../PARTE-VIII-Visione-futuro/21-ecosistema-openclaw.md)
