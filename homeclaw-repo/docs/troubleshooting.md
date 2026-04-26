# Troubleshooting

If something doesn't work, run `./scripts/doctor.sh --verbose` first. It
will tell you which service is down, which port is silent, and which
file is missing. Then come back here for the specific fix.

---

## Setup and boot

### "`hailortcli fw-control identify` returns nothing"

- Make sure you've rebooted after installing the Hailo driver kernel module.
- Check `dmesg | grep -i hailo`. Expect lines like `hailo 0000:01:00.0:
  Probing on: 1e60:2864...`. If missing, the HAT isn't detected — re-seat
  the PCIe ribbon cable with the Pi powered off.
- Add `dtparam=pciex1_gen=3` to `/boot/firmware/config.txt` and reboot.

### "Driver Hailo crashes after `apt full-upgrade`"

The Hailo kernel module is built against the running kernel. A kernel
upgrade breaks it. Hold the kernel until Hailo releases a compatible
driver:

```bash
sudo apt-mark hold raspberrypi-kernel raspberrypi-kernel-headers
```

To release the hold later:

```bash
sudo apt-mark unhold raspberrypi-kernel raspberrypi-kernel-headers
```

### "Raspberry Pi throttles mid-conversation"

The 15W PSUs (often bundled with older Pi kits) can't feed the Pi 5 + HAT
+ USB microphone under load. Symptom: `vcgencmd get_throttled` returns
anything but `0x0`. Buy the official 27W USB-C supply.

---

## Audio

### Microphone doesn't appear in `arecord -L`

1. USB power: not enough current. Use the 27W PSU; avoid USB hubs
   without external power.
2. Try a different USB port on the Pi.
3. `dmesg | tail -20` immediately after plugging: look for kernel
   messages. A ReSpeaker USB 4-Mic announces as `ArrayUAC10` on the
   USB bus.

### "Recording is silent / all zeros"

Check `alsamixer`. Some ALSA devices start muted by default. Unmute
the capture side (`M` to toggle) and set capture level to ~70%. Save
with `sudo alsactl store`.

### "Audio is distorted or glitchy"

1. Power issue (see above).
2. Bluetooth speaker power-save. Disable in `/etc/bluetooth/main.conf`:
   ```
   [General]
   Disable=Handsfree,FakePlayer
   AutoConnect=true
   ```
   Restart bluetoothd: `sudo systemctl restart bluetooth`.
3. HDMI audio interfering. Add `dtparam=audio=off` to
   `/boot/firmware/config.txt` if you don't use HDMI audio.

### "Bluetooth speaker disconnects every 10 seconds"

BT modules in power-save. The fix above (`Disable=Handsfree,FakePlayer`)
usually solves it. If not, move to a USB speaker — more reliable for
always-on applications.

---

## Wake word

### False positives (it fires without me)

If it's more than ~2/hour:
1. Raise `--threshold` in the `wyoming-openwakeword` service (from 0.5 → 0.6).
2. Collect false-positive audio with `--debug-recording-dir` and
   fine-tune the model (see `wakeword-training.md`).
3. If TV is the culprit, consider a longer wake phrase — "Ehi HomeClaw"
   rather than "Ehi Claw".

### False negatives (it doesn't fire when I say it)

1. Lower `--threshold` (0.5 → 0.4).
2. Speak closer to the mic for the first week; the model learns less
   common conditions from real-world fine-tuning.
3. Check the wake phrase's phonetic clarity. Some accents slur "Claw"
   into "Claude" or "clo'" — fine-tune with your own voice specifically.

### LED pulses blue but nothing happens after

1. Microphone stopped recording: check `wyoming-satellite` logs
   (`journalctl -u wyoming-satellite -f` while triggering).
2. VAD too aggressive, cutting off the command immediately: adjust
   `--vad-threshold` (lower = more permissive, e.g. 0.3).

---

## STT (Whisper)

### "Whisper takes 4+ seconds per phrase"

On CPU with `small` model, that's expected. Three fixes:
1. Switch to `base-int8` (fast, lower accuracy).
2. Install Hailo-10H and switch to Hailo-accelerated small.
3. Ensure `small-int8` (quantized), not plain `small`.

### "Whisper transcribes English when I speak Italian"

Force the language flag in the service:
```
--language it
```
Whisper auto-detect fails on short utterances ("ciao" is valid in both
Italian and some Portuguese dialects).

### "Whisper mistranscribes proper nouns (names, places)"

1. Add an `--initial-prompt` to the service listing names/words common in
   your household:
   ```
   --initial-prompt "Conversazione italiana con HomeClaw. Nomi: Giacomo, Lucia, Pietro, Mia. Luoghi: Rimini, Riccione."
   ```
2. Switch to a larger model (`medium-int8`) for higher accuracy on
   uncommon words.

---

## TTS (Piper)

### "Voice sounds robotic"

You're probably on `riccardo-x_low`. Switch to `paola-medium`:
```
--voice it_IT-paola-medium
```
Download if not present:
```bash
python3 -m piper_tts.download_voices --data-dir /home/pi/piper-voices it_IT-paola-medium
```

### "TTS takes >1 second to start"

1. First-use cold start is slow (model loading). Warm up with:
   ```bash
   echo 'test' | piper --model it_IT-paola-medium.onnx --output_file /tmp/warmup.wav
   ```
   and keep the service running.
2. Check CPU: if the Pi is thermal-throttling, TTS generation stalls.
   See "Raspberry Pi throttles" above.

### "HomeClaw reads 'asterisk asterisk' or says 'hash'"

The Markdown stripper in the bridge handles most cases, but an obscure
pattern may slip through. Check `journalctl -u homeclaw-bridge | grep
"synthesize dispatched"` to see exactly what text was sent to Piper.
If it still contains Markdown, open an issue with the example.

The ultimate fix is in `SOUL.md`: add a concrete negative example like
*"Non dire '* testo *' ma 'testo'"* — LLMs learn examples faster than
rules.

---

## Bridge and OpenClaw

### "Bridge shows 'agent did not respond within 8s'"

1. OpenClaw gateway down. Check `systemctl status openclaw-gateway`.
2. Cloud LLM unreachable (internet down, rate limit). Check OpenClaw's
   own logs: `openclaw logs --agent HomeClaw`.
3. LLM taking too long on a complex query. Increase timeout:
   `HOMECLAW_RESPONSE_TIMEOUT=15.0` in the bridge env.

### "Bridge connects, says 'peer=default' forever"

The satellite's `Info` event isn't being parsed. Either the wyoming
version is older than expected, or the satellite's `--name` flag is
missing. Check:
```bash
sudo systemctl cat wyoming-satellite | grep name
```
Should show `--name homeclaw-studio` (or whatever).

### "Agent replies are always in English even though I speak Italian"

The STT is transcribing correctly (you can check in logs), so this is
the LLM drifting. Three fixes:
1. SOUL.md rule 9 (language) must be present. Verify with
   `cat ~/.openclaw/homeclaw-workspace/SOUL.md | grep -i language`.
2. If using Claude Sonnet, the system prompt should lead with the
   language choice: "You are HomeClaw. Always reply in Italian."
3. First few reminders may be needed: the LLM sometimes needs 2–3
   turns to lock into a language.

---

## LED feedback

### "LEDs don't light up at all"

1. SPI not enabled: `sudo raspi-config nonint do_spi 0 && sudo reboot`.
2. Wrong pins: the ReSpeaker USB uses MOSI=GPIO10, SCLK=GPIO11 (default
   SPI0). If you rewired, edit `homeclaw_led_feedback.py` accordingly.
3. Service not running: `systemctl status homeclaw-led-feedback`.
4. User not in `spi` group: `sudo usermod -a -G spi pi` then logout/login.

### "LEDs stick on one color and never go off"

The Wyoming `audio-stop` event isn't being received. Could be a wyoming
version mismatch. Upgrade:
```bash
cd ~/wyoming-satellite
git pull
source venv/bin/activate
pip install -U -r requirements.txt
sudo systemctl restart wyoming-satellite
```

---

## Multi-room (Tier C)

### "Satellite in kitchen doesn't respond"

1. Ping check: from hub, `ping homeclaw-cucina.local`.
2. ESPHome device online in HA? **Settings → Devices & Services → ESPHome**.
3. Wi-Fi signal on the satellite: ESPHome exposes a sensor; check it.
4. microWakeWord can be lazy: if it hasn't heard its phrase in a long time,
   the first "Ehi Claw" is sometimes missed. Say it twice initially.

### "All rooms respond when I speak in one room"

Acoustic bleed. Two fixes:
1. microWakeWord threshold per-satellite: bump it up on satellites closer
   to the source.
2. Put them physically further apart (walls, doors, different floors).

### "HomeClaw responds from the wrong room's speaker"

The `peer` tag is being set incorrectly. Check the ESPHome yaml's
`substitutions.room:` matches the intended name, and that the satellite's
unique name (e.g. `homeclaw-cucina`) is what HA knows it as.

---

## Privacy and safety

### "I want to verify nothing leaves my network"

Install `tcpdump` on the hub:
```bash
sudo tcpdump -i eth0 -n -c 100 'host not 192.168.0.0/16 and host not 10.0.0.0/8'
```
During an air-gapped test, this should capture zero packets (after the
initial DNS / NTP). Any unexpected outbound traffic = misconfigured
skill, investigate.

### "I don't trust the Bluetooth mic to be off when I hit mute"

The ReSpeaker USB 4-Mic Array's physical mute button cuts the mic signal
at the chip level — software can't override it. If you want even more
paranoia, physically unplug the USB cable. There's no substitute for
airgap.

### "Can I see what was said today?"

Yes, if you enabled `--debug-recording-dir`. Files are WAV, dated. For
text transcripts:
```bash
journalctl -u wyoming-faster-whisper --since today | grep transcript
```

---

## Getting more help

1. `./scripts/doctor.sh --verbose` — structured diagnosis
2. OpenClaw Discord, `#homeclaw` channel
3. GitHub Issues on this repo, with output from `doctor.sh --verbose`
4. Community wake-word training data: the `#dataset-sharing` channel
