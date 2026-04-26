# HomeClaw LED Feedback

Maps Wyoming satellite events to animations on the 12-LED APA102 ring
that sits on the ReSpeaker USB 4-Mic Array.

## Event → color mapping

| Wyoming event   | Meaning                             | LED animation               |
|-----------------|-------------------------------------|-----------------------------|
| `detection`     | Wake word recognized                | Blue pulse (1.2 s period)   |
| `transcript`    | STT finished, agent reasoning       | Amber solid                 |
| `synthesize`    | Piper is playing the reply          | Green solid                 |
| `audio-stop`    | Playback finished, back to idle     | Off                         |
| `error`         | Anything blew up                    | Red solid for 2 s, then off |

## Hardware pinout

The ReSpeaker USB 4-Mic Array exposes the APA102 ring on the Pi's hardware
SPI bus. The default SPI0 pins are:

- MOSI → GPIO 10 (pin 19)
- SCLK → GPIO 11 (pin 23)

These are the defaults used by `apa102-pi`. No changes needed unless you
rewire.

Enable SPI on the Pi:

```bash
sudo raspi-config nonint do_spi 0
sudo reboot
```

## Install

```bash
cd led-feedback/
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## Run manually (for testing)

```bash
source venv/bin/activate
HOMECLAW_LED_BRIGHTNESS=0.6 python homeclaw_led_feedback.py
```

Then trigger the wake word on your satellite and watch the ring light up.

## Run as service

```bash
sudo cp ../systemd/homeclaw-led-feedback.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable --now homeclaw-led-feedback
sudo journalctl -u homeclaw-led-feedback -f
```

## Quiet hours

The service respects `HOMECLAW_LED_QUIET_HOURS` (default `22:00-07:00`).
During those hours, brightness drops to `HOMECLAW_LED_QUIET_BRIGHTNESS`
(default `0.1`, i.e. 10%). Useful if HomeClaw sits in a bedroom.

Disable with `HOMECLAW_LED_QUIET_HOURS=` (empty).
