# HomeClaw Tools

Skills and integrations available to HomeClaw. Listed in priority order —
when multiple skills could answer, prefer the one highest in this list.

## `home-assistant`

REST-based bridge to the Home Assistant instance at `http://homeassistant.local:8123`.
- Scope: lights, switches, scenes, media players, climate, scripts, scenes.
- Auth: long-lived access token stored in `~/.openclaw/.env` as `HA_TOKEN`.
- Preferred for: all physical-device commands.
- Usage example:
  - Intent: "accendi la luce del salotto" → `light.turn_on(area_id='salotto')`
  - Intent: "temperatura a 20" → `climate.set_temperature(temperature=20)`
- On failure (device not found, HA unreachable): reply literally
  *"non ho trovato NOME"* or *"Home Assistant non risponde"*.

## `weather`

Wraps Open-Meteo for short-range forecasts.
- No API key needed (free tier).
- Default location: user's home coordinates in `~/.openclaw/homeclaw-workspace/USER.md`.
- Always answer in one sentence: condition + high temperature.

## `timer`

Local in-memory timer. Runs inside the agent, no external service needed.
- Multiple concurrent timers supported.
- Timer names are optional ("timer 5 minuti" vs "timer pasta 8 minuti").
- When a timer fires, synthesize a SHORT announcement through the bridge
  and flash the LEDs red-to-green gradient.

## `telegram-notify`

For messages that are too long for voice.
- Send to the user's personal Telegram (chat ID in `.env` as `TG_OWNER_CHAT`).
- ALWAYS use this for: URLs, lists of 3+ items, email full-text, any text >30 words.
- Never use for: short confirmations, smart-home feedback.

## `gog` (Gmail, Calendar, Drive)

Read-only access to Google Workspace.
- Use for: "che email ho", "che ho domani", "cerca il file X".
- NEVER send emails from here — that requires the dedicated `gmail-send`
  skill with explicit confirmation (see SOUL.md rule 7).
- Summarize aggressively: "hai tre email importanti, te le mando su Telegram".

## `search-web`

Brave Search API for queries that need current web info.
- Only invoke when the local model admits it doesn't know.
- Never read raw search results aloud. Summarize to 2 sentences.

## Routing hints

These mappings help the agent pick a skill fast:

| Intent keyword | Primary skill |
|----|----|
| accendi, spegni, alza, abbassa, chiudi, apri | `home-assistant` |
| che tempo, pioverà, temperatura | `weather` |
| timer, pastafrolla, sveglia, ricordami | `timer` |
| email, mail, messaggio, inbox | `gog` |
| oggi, domani, calendario, riunione | `gog` |
| cerca, cosa è, chi è, quando è | `search-web` (if local model doesn't know) |

## Never do

- Do NOT call `search-web` for sensitive keywords (see SOUL.md rule 6.1).
- Do NOT modify calendar events without `confermo HomeClaw`.
- Do NOT send Telegram messages that include passwords or secrets.
