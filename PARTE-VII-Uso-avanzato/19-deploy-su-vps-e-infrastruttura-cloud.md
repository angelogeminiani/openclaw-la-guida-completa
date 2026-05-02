# Capitolo 19 — Deploy su VPS e infrastruttura cloud [★★★]

## Cosa imparerai

- Deploy su Railway, DigitalOcean, Google Cloud, Render
- Hardening dell'infrastruttura
- Accesso remoto sicuro con Tailscale
- NanoClaw come alternativa con container isolati

## Prerequisiti

Avere un'installazione locale funzionante ([Capitolo 5](../PARTE-II-Installazione/05-installazione-step-by-step.md)). Conoscenza base di Linux e SSH. Aver letto [Capitolo 4](../PARTE-II-Installazione/04-preparare-un-ambiente-sicuro-docker-sandbox.md) sul sandboxing e [Capitolo 13](../PARTE-V-Sicurezza-costi/13-sicurezza-la-guida-che-devi-leggere.md) sulla sicurezza.

## Contenuto principale

1. **Railway.** 1-Click deploy: il modo più veloce per avere OpenClaw in cloud.

2. **DigitalOcean.** Hardened security image: immagine pre-configurata con sicurezza rafforzata ($24/mese).

3. **Google Cloud.** Deploy container con GKE o Cloud Run. Guida ufficiale: docs.openclaw.ai/install/gcp.

4. **Render.** Deploy serverless-like: docs.openclaw.ai/install/render.

5. **Tailscale.** Per accesso remoto sicuro al Gateway senza esporre porte pubbliche. Serve/Funnel per il dashboard + WebSocket.

6. **NanoClaw.** Alternativa minimalista (~700 righe TypeScript) con container Docker isolati per ogni chat. Ideale per chi prioritizza sicurezza e semplicità. Limite: supporto solo Claude, ecosistema ridotto.

**Prompt pronto:**
> "Voglio spostarti dal Mac Mini di casa a un VPS [DigitalOcean / Railway / Hetzner]. Aiutami nella migrazione: (1) checklist pre-migrazione (cosa fare sul Mac prima di spegnerlo), (2) scelta della region più vicina al mio provider LLM, (3) hardening base del VPS (SSH key-only, firewall, fail2ban), (4) configurazione di Tailscale per accesso senza esporre la porta del Gateway su internet, (5) `openclaw doctor` post-migrazione per confermare che tutto funzioni."

## Errori comuni e come risolverli

| Sintomo | Causa probabile | Fix |
|---------|-----------------|-----|
| Deploy Railway funziona ma timeout sui task lunghi | Limite di esecuzione del piano free/hobby | Passare a piano superiore o a VPS dedicato (DigitalOcean, Hetzner). |
| SSH lentissimo, comandi che bloccano | VPS in regione lontana dal modello LLM | Scegliere region vicina al provider LLM (USA East per Anthropic/OpenAI). |
| Docker non parte sul VPS | Kernel troppo vecchio o swap insufficiente | Verificare `uname -r`, aggiungere swap (`fallocate -l 2G /swapfile`). |
| Espongo accidentalmente il Gateway su internet | Porta 18789 aperta sul firewall pubblico | MAI esporre la porta del Gateway. Usare Tailscale Serve/Funnel per accesso remoto sicuro. |

## Checklist di fine capitolo

- [ ] Provider scelto e VPS provisionato
- [ ] Hardening base completato: SSH key-only, firewall attivo, fail2ban
- [ ] Tailscale (o equivalente) per accesso senza esporre porte pubbliche
- [ ] Backup periodico della cartella `.openclaw/` su storage esterno
- [ ] `openclaw doctor` non segnala warning

## Link e risorse utili

- [Railway 1-Click Deploy](https://railway.com/deploy/openclaw) — la via più rapida per spostare OpenClaw in cloud
- [How to Run OpenClaw with DigitalOcean](https://www.digitalocean.com/community/tutorials/how-to-run-openclaw) — guida ufficiale DigitalOcean (Marketplace dal 24 gennaio 2026)
- [Hostinger VPS per OpenClaw](https://www.hostinger.com/vps/docker/openclaw) — opzione low-cost con Docker preconfigurato
- [OpenClaw Docker: Hardening for Production 2026](https://advenboost.com/openclaw-docker-hardening-your-ai-sandbox-for-production-2026/) — hardening per VPS pubblici

Per l'elenco completo delle fonti del libro, vedi [Appendice E](../Appendici/E-risorse-e-link-utili.md).

---

[← Capitolo 18](./18-cron-job-e-automazioni-avanzate.md)  ·  [Indice](../README.md)  ·  [Capitolo 20 →](./20-architettura-del-gateway.md)
