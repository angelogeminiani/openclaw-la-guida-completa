#!/usr/bin/env python3
"""
HomeClaw LED Feedback.

Listens to Wyoming satellite events over the local TCP socket and maps
them to colored animations on the ReSpeaker USB 4-Mic Array's 12-LED
APA102 ring. Gives users instant visual feedback on the assistant state:

    IDLE        -> off
    LISTENING   -> blue pulse  (wake word detected, recording the command)
    THINKING    -> amber solid (STT done, agent is reasoning)
    SPEAKING    -> green solid (Piper is playing a response)
    ERROR       -> red solid for 2 seconds, then off

Quiet-hours support: between HOMECLAW_LED_QUIET_HOURS the brightness is
clamped to HOMECLAW_LED_QUIET_BRIGHTNESS to avoid lighting up the bedroom
at 2am.

Runs as a systemd service. See systemd/homeclaw-led-feedback.service.
"""

import asyncio
import datetime as dt
import json
import logging
import os
import signal
import sys
from dataclasses import dataclass
from typing import Optional

from apa102_pi.driver import apa102


_LOGGER = logging.getLogger("homeclaw-led-feedback")


# -----------------------------------------------------------------------------------------------------------------
#  c o n s t a n t s
# -----------------------------------------------------------------------------------------------------------------

# RGB color presets (R, G, B).
_COLOR_OFF = (0, 0, 0)
_COLOR_LISTENING = (0, 60, 255)
_COLOR_THINKING = (255, 150, 0)
_COLOR_SPEAKING = (0, 255, 60)
_COLOR_ERROR = (255, 0, 0)

# Pulse animation parameters.
_PULSE_PERIOD_SECONDS = 1.2
_PULSE_FRAMES_PER_SECOND = 30
_ERROR_HOLD_SECONDS = 2.0

# Wyoming event type names.
_EVENT_DETECTION = "detection"
_EVENT_TRANSCRIPT = "transcript"
_EVENT_SYNTHESIZE = "synthesize"
_EVENT_AUDIO_STOP = "audio-stop"
_EVENT_ERROR = "error"


# -----------------------------------------------------------------------------------------------------------------
#  c o n f i g
# -----------------------------------------------------------------------------------------------------------------

@dataclass
class FeedbackConfig:
    """Runtime config loaded from environment variables."""
    satellite_uri: str
    led_count: int
    brightness: float
    quiet_start: Optional[dt.time]
    quiet_end: Optional[dt.time]
    quiet_brightness: float

    @classmethod
    def from_env(cls) -> "FeedbackConfig":
        quiet_range = os.environ.get("HOMECLAW_LED_QUIET_HOURS", "").strip()
        quiet_start, quiet_end = cls._parse_quiet_range(quiet_range)
        return cls(
            satellite_uri=os.environ.get(
                "HOMECLAW_SATELLITE_URI", "tcp://127.0.0.1:10700"
            ),
            led_count=int(os.environ.get("HOMECLAW_LED_COUNT", "12")),
            brightness=float(os.environ.get("HOMECLAW_LED_BRIGHTNESS", "0.6")),
            quiet_start=quiet_start,
            quiet_end=quiet_end,
            quiet_brightness=float(
                os.environ.get("HOMECLAW_LED_QUIET_BRIGHTNESS", "0.1")
            ),
        )

    @staticmethod
    def _parse_quiet_range(raw: str) -> tuple[Optional[dt.time], Optional[dt.time]]:
        """Parse 'HH:MM-HH:MM' into two datetime.time objects (or None)."""
        if not raw or "-" not in raw:
            return None, None
        try:
            start_str, end_str = raw.split("-")
            return (
                dt.time.fromisoformat(start_str.strip()),
                dt.time.fromisoformat(end_str.strip()),
            )
        except ValueError:
            _LOGGER.warning("invalid quiet hours '%s', ignoring", raw)
            return None, None


# -----------------------------------------------------------------------------------------------------------------
#  r i n g
# -----------------------------------------------------------------------------------------------------------------

class LedRing:
    """Thin wrapper around apa102_pi to paint the ReSpeaker's 12-LED ring."""

    # -----------------------------------------------------------------------------------------------------------------
    #  c t r
    # -----------------------------------------------------------------------------------------------------------------

    def __init__(self, count: int, brightness: float) -> None:
        self._count = count
        self._brightness = brightness
        # global_brightness ranges 1..31 on APA102 hardware.
        hw_brightness = max(1, min(31, int(round(brightness * 31))))
        self._strip = apa102.APA102(
            num_led=count,
            global_brightness=hw_brightness,
            mosi=10,
            sclk=11,
            order="rgb",
        )
        self._strip.clear_strip()
        self._strip.show()

    # -----------------------------------------------------------------------------------------------------------------
    #  p u b l i c
    # -----------------------------------------------------------------------------------------------------------------

    def set_brightness(self, brightness: float) -> None:
        self._brightness = brightness
        hw_brightness = max(1, min(31, int(round(brightness * 31))))
        self._strip.global_brightness = hw_brightness

    def fill(self, rgb: tuple[int, int, int]) -> None:
        r, g, b = rgb
        for i in range(self._count):
            self._strip.set_pixel(i, r, g, b)
        self._strip.show()

    def off(self) -> None:
        self._strip.clear_strip()
        self._strip.show()

    def cleanup(self) -> None:
        self.off()
        self._strip.cleanup()


# -----------------------------------------------------------------------------------------------------------------
#  f e e d b a c k   c o n t r o l l e r
# -----------------------------------------------------------------------------------------------------------------

class LedFeedback:
    """Main controller: parses Wyoming events and drives the LED ring."""

    # -----------------------------------------------------------------------------------------------------------------
    #  c t r
    # -----------------------------------------------------------------------------------------------------------------

    def __init__(self, config: FeedbackConfig) -> None:
        self._config = config
        self._ring = LedRing(config.led_count, config.brightness)
        self._animation_task: Optional[asyncio.Task] = None
        self._stop_event = asyncio.Event()

    # -----------------------------------------------------------------------------------------------------------------
    #  p u b l i c
    # -----------------------------------------------------------------------------------------------------------------

    async def run(self) -> None:
        """Main loop: connect to satellite, process events, reconnect on drop."""
        host, port = self._parse_uri(self._config.satellite_uri)
        while not self._stop_event.is_set():
            try:
                await self._apply_quiet_hours()
                reader, _ = await asyncio.open_connection(host, port)
                _LOGGER.info("connected to satellite at %s:%d", host, port)
                await self._read_loop(reader)
            except (ConnectionError, OSError) as exc:
                _LOGGER.warning("satellite connection error: %s; retrying in 3s", exc)
                self._ring.off()
                try:
                    await asyncio.wait_for(self._stop_event.wait(), timeout=3.0)
                    break
                except asyncio.TimeoutError:
                    pass

        await self._stop_animation()
        self._ring.cleanup()

    def stop(self) -> None:
        self._stop_event.set()

    # -----------------------------------------------------------------------------------------------------------------
    #  p r i v a t e   —   p r o t o c o l
    # -----------------------------------------------------------------------------------------------------------------

    async def _read_loop(self, reader: asyncio.StreamReader) -> None:
        while not self._stop_event.is_set():
            line = await reader.readline()
            if not line:
                break
            try:
                event = json.loads(line.decode("utf-8"))
            except json.JSONDecodeError:
                continue
            await self._on_event(event)

    async def _on_event(self, event: dict) -> None:
        event_type = event.get("type")
        if event_type == _EVENT_DETECTION:
            await self._enter_listening()
        elif event_type == _EVENT_TRANSCRIPT:
            await self._enter_thinking()
        elif event_type == _EVENT_SYNTHESIZE:
            await self._enter_speaking()
        elif event_type == _EVENT_AUDIO_STOP:
            await self._enter_idle()
        elif event_type == _EVENT_ERROR:
            await self._flash_error()
        else:
            _LOGGER.debug("ignoring event type=%s", event_type)

    @staticmethod
    def _parse_uri(uri: str) -> tuple[str, int]:
        assert uri.startswith("tcp://"), f"unsupported URI: {uri}"
        host, port = uri[len("tcp://"):].rsplit(":", 1)
        return host, int(port)

    # -----------------------------------------------------------------------------------------------------------------
    #  p r i v a t e   —   s t a t e   t r a n s i t i o n s
    # -----------------------------------------------------------------------------------------------------------------

    async def _enter_listening(self) -> None:
        await self._stop_animation()
        self._animation_task = asyncio.create_task(self._pulse(_COLOR_LISTENING))

    async def _enter_thinking(self) -> None:
        await self._stop_animation()
        self._ring.fill(_COLOR_THINKING)

    async def _enter_speaking(self) -> None:
        await self._stop_animation()
        self._ring.fill(_COLOR_SPEAKING)

    async def _enter_idle(self) -> None:
        await self._stop_animation()
        self._ring.off()

    async def _flash_error(self) -> None:
        await self._stop_animation()
        self._ring.fill(_COLOR_ERROR)
        await asyncio.sleep(_ERROR_HOLD_SECONDS)
        self._ring.off()

    async def _stop_animation(self) -> None:
        task = self._animation_task
        if task is not None and not task.done():
            task.cancel()
            try:
                await task
            except asyncio.CancelledError:
                pass
        self._animation_task = None

    # -----------------------------------------------------------------------------------------------------------------
    #  p r i v a t e   —   a n i m a t i o n s
    # -----------------------------------------------------------------------------------------------------------------

    async def _pulse(self, rgb: tuple[int, int, int]) -> None:
        """Pulse the whole ring between 10% and 100% of `rgb`."""
        frame_interval = 1.0 / _PULSE_FRAMES_PER_SECOND
        half_period = _PULSE_PERIOD_SECONDS / 2.0
        frames_per_half = int(half_period * _PULSE_FRAMES_PER_SECOND)
        try:
            while True:
                # fade in
                for i in range(frames_per_half):
                    factor = 0.1 + (0.9 * i / frames_per_half)
                    self._ring.fill(self._scale(rgb, factor))
                    await asyncio.sleep(frame_interval)
                # fade out
                for i in range(frames_per_half):
                    factor = 1.0 - (0.9 * i / frames_per_half)
                    self._ring.fill(self._scale(rgb, factor))
                    await asyncio.sleep(frame_interval)
        except asyncio.CancelledError:
            raise

    @staticmethod
    def _scale(rgb: tuple[int, int, int], factor: float) -> tuple[int, int, int]:
        r, g, b = rgb
        return (int(r * factor), int(g * factor), int(b * factor))

    # -----------------------------------------------------------------------------------------------------------------
    #  p r i v a t e   —   q u i e t   h o u r s
    # -----------------------------------------------------------------------------------------------------------------

    async def _apply_quiet_hours(self) -> None:
        """Clamp brightness when inside the configured quiet hours window."""
        if self._config.quiet_start is None or self._config.quiet_end is None:
            return
        now = dt.datetime.now().time()
        in_quiet = self._is_in_range(now, self._config.quiet_start, self._config.quiet_end)
        brightness = (
            self._config.quiet_brightness if in_quiet else self._config.brightness
        )
        self._ring.set_brightness(brightness)

    @staticmethod
    def _is_in_range(now: dt.time, start: dt.time, end: dt.time) -> bool:
        # Ranges that cross midnight are supported: start=22:00, end=07:00.
        if start <= end:
            return start <= now < end
        return now >= start or now < end


# -----------------------------------------------------------------------------------------------------------------
#  m a i n
# -----------------------------------------------------------------------------------------------------------------

async def _async_main() -> int:
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    )
    config = FeedbackConfig.from_env()
    feedback = LedFeedback(config)

    loop = asyncio.get_running_loop()
    for sig in (signal.SIGINT, signal.SIGTERM):
        loop.add_signal_handler(sig, feedback.stop)

    await feedback.run()
    return 0


def main() -> int:
    try:
        return asyncio.run(_async_main())
    except KeyboardInterrupt:
        return 130


if __name__ == "__main__":
    sys.exit(main())
