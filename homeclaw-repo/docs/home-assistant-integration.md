# Home Assistant integration

HomeClaw speaks the language; Home Assistant speaks to the devices.
Together they turn "Ehi Claw, accendi la luce" into a real photon
hitting a real wall.

This doc describes **Modalità 1** from the chapter: HomeClaw is the LLM
conversational agent, Home Assistant is the IoT backplane. HomeClaw calls
HA's REST API; HA stays in charge of all device state and automations.

---

## Prerequisites

- A working Home Assistant installation (HAOS, Docker, or Supervised).
  Tested with HA 2026.4.
- Network connectivity from the HomeClaw hub to HA on port 8123.
- An admin user on HA (to create the long-lived access token).

---

## Step 1 — Create a HomeClaw user + token

1. On HA, go to **Settings → People → Users → Add user**.
2. Name: `homeclaw`. Admin: **yes** (or restrict via per-area access
   control if you prefer).
3. Log in as `homeclaw`, go to the profile icon (bottom left) →
   **Security → Long-Lived Access Tokens → Create Token**.
4. Name: `HomeClaw Bridge`. Copy the token — it's shown only once.
5. On the hub:
   ```bash
   echo 'HA_BASE_URL=http://homeassistant.local:8123' | sudo tee -a ~/.openclaw/.env
   echo 'HA_TOKEN=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.xxxxx...' | sudo tee -a ~/.openclaw/.env
   sudo chmod 0600 ~/.openclaw/.env
   ```

---

## Step 2 — Install the `home-assistant` OpenClaw skill

```bash
openclaw skills install homeclaw-home-assistant    # from official skill registry
```

(If it's not yet in the registry, install from source: the skill is in
`skill-home-assistant/` in this repo's companion repository
`homeclaw-skill-home-assistant`.)

---

## Step 3 — Teach HomeClaw about your rooms

The skill auto-discovers HA areas, but a one-time teaching helps the
LLM understand which room nicknames map to which area. In HomeClaw's
workspace, create `rooms.yaml`:

```yaml
rooms:
  salotto:
    area_id: salotto
    aliases: [sala, soggiorno, living room]
  cucina:
    area_id: cucina
    aliases: [kitchen]
  camera:
    area_id: camera_padronale
    aliases: [camera da letto, bedroom, stanza matrimoniale]
  bagno:
    area_id: bagno_piano_terra
    aliases: [toilette]
  studio:
    area_id: studio
    aliases: [ufficio, office, stanza lavoro]
```

HomeClaw's SOUL.md already knows to consult this file when interpreting
location references.

---

## Step 4 — Wire the skill to the agent

In HomeClaw's `TOOLS.md` (already configured in the template shipped with
this repo), the `home-assistant` skill is listed with these entry points:

| Intent | Skill function |
|---|---|
| "accendi X" | `light.turn_on(area_id=X)` |
| "spegni X" | `light.turn_off(area_id=X)` |
| "luce X al N per cento" | `light.turn_on(area_id=X, brightness_pct=N)` |
| "imposta temperatura a N" | `climate.set_temperature(entity=area, temperature=N)` |
| "metti musica X" | `media_player.play_media(entity=..., media_id=X)` |
| "pausa" / "riprendi" | `media_player.media_pause/play` |

---

## Step 5 — Test with a single device

Before wiring up the whole house, verify one device end-to-end:

```bash
# On the hub:
openclaw agents send HomeClaw "Accendi la luce del salotto" \
    --channel voice --peer test
```

You should see in the logs:
1. Agent decides to call `home-assistant.light_turn_on(area_id='salotto')`
2. Skill calls `POST http://homeassistant.local:8123/api/services/light/turn_on`
3. HA returns 200
4. Agent replies `[SILENT_OK]`

And the light in your living room should actually turn on. If it doesn't,
check `journalctl -u homeclaw-bridge -n 50` and the HA logbook (**Settings
→ System → Logs**).

---

## Advanced: routing to HA Assist instead

If you'd rather have HA handle voice input directly (using HA's built-in
Assist pipeline) and only fall back to OpenClaw for complex queries, see
**Modalità 2** in the chapter. That requires a `custom_components/openclaw_conversation/`
in HA — not provided in this repo yet. Contributions welcome.

---

## Security notes

- The HA token grants whatever access the `homeclaw` user has. If you
  gave it admin, HomeClaw can do anything: delete devices, edit
  automations, etc. Consider restricting to non-admin + explicit per-area
  access.
- The token is stored in `~/.openclaw/.env` with mode 0600 on the hub.
  Anyone with shell access to the `pi` user can read it.
- If you're running HA on HAOS with a dedicated appliance, make sure
  only the hub's IP can reach port 8123 (use the HA Network config or
  a firewall rule).
- Never put your HA URL + token into a cloud-hosted LLM query. The
  SOUL.md already instructs HomeClaw to redact credentials.
