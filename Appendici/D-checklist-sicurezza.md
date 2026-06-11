# Appendice D — Checklist di sicurezza

> Liste di controllo stampabili per audit periodici. Adattate dai **Cap. 4** e **Cap. 13**.

## 1. Checklist operativa di sicurezza (mensile)

- [ ] OpenClaw gira su un dispositivo dedicato (non il computer personale)
- [ ] Sandbox Docker attivo (vedi Cap. 4 per i livelli di isolamento)
- [ ] API key con scope minimo necessario
- [ ] Token read-only per tutte le integrazioni finché non ci si fida
- [ ] SOUL.md con regole esplicite su cosa l'agente NON deve fare
- [ ] `openclaw update` eseguito almeno settimanalmente
- [ ] `openclaw security audit` eseguito almeno mensilmente
- [ ] Nessun segreto in chiaro in file `.env`: le credenziali
      vivono cifrate in `~/.openclaw/credentials/`
- [ ] Porta 18789 non raggiungibile da internet
      (`lsof -i :18789` → bind su `127.0.0.1`)
- [ ] Nessuna skill di terze parti non verificata installata
- [ ] Bot non esposto in gruppi pubblici
- [ ] Accesso remoto d'emergenza configurato in modo sicuro
      (SSH/Tailscale, mai esposto su internet — Cap. 15)

## 2. Checklist hardening Docker (al setup e dopo ogni modifica)

- [ ] Container eseguito come utente non-root (uid 1000)
- [ ] `--cap-drop=ALL` per rimuovere tutte le Linux capability
- [ ] Egress filtering: allowlist esplicita per i domini raggiungibili
- [ ] mDNS disabilitato dentro la rete Docker (no lateral movement)
- [ ] Profilo seccomp personalizzato per limitare le syscall
- [ ] `read_only: true` sul filesystem del container dove possibile
- [ ] Livello di isolamento adatto al caso d'uso (Cap. 4)
- [ ] Docker Desktop/Engine in esecuzione e aggiornato
- [ ] Immagine sandbox costruita (`openclaw-sandbox:bookworm-slim`)
- [ ] `workspaceAccess` configurato al livello minimo necessario (`none` → `ro` → `rw`)

## 3. Checklist pre-integrazione (prima di collegare un nuovo tool)

- [ ] Token con scope minimo e `read-only` di default
- [ ] Documentato in `TOOLS.md` come l'agente deve usare il tool
- [ ] Documentato in `SOUL.md` cosa il tool NON può fare
- [ ] Credenziali cifrate in `~/.openclaw/credentials/`
      (mai in `.env`, inline nel codice o nei prompt)
- [ ] Backup recente dell'intera cartella `~/.openclaw/`

## 4. Checklist post-incident

- [ ] Identificato il vettore (skill terza parte? prompt injection? config?)
- [ ] Rotazione di tutte le credenziali potenzialmente esposte
- [ ] `openclaw security audit` eseguito
- [ ] Log e cron rivisti per attività anomale
- [ ] Aggiornato `SOUL.md` per prevenire ricorrenza
- [ ] Comunicato alla community se è un problema OpenClaw upstream

## 5. Dieci red flag da non ignorare

- [ ] Comportamento dell'agente improvvisamente diverso senza modifiche da parte tua
- [ ] Email o messaggi inviati che non hai approvato
- [ ] Cron creati che non riconosci
- [ ] Connessioni di rete verso domini non in allowlist
- [ ] Picco anomalo di consumo token / costi LLM
- [ ] File modificati fuori dai workspace dell'agente
- [ ] Skill installate che non ricordi di aver autorizzato
- [ ] Account di terze parti che mostrano accessi da IP sconosciuti
- [ ] File in `~/.openclaw/` (config o credenziali) modificati
      senza tua azione
- [ ] L'agente che chiede credenziali aggiuntive in modo inusuale

---

[← Appendice C](./C-template-soul-identity.md)  ·  [Indice](../README.md)  ·  [Appendice E →](./E-risorse-e-link-utili.md)
