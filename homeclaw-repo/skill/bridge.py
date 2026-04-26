#!/usr/bin/env python3
"""
HomeClaw Bridge — Wyoming Protocol <-> OpenClaw Gateway.

This process connects as a TCP client to a running wyoming-satellite,
receives ASR transcript events, forwards them to an OpenClaw agent on the
'voice' channel, and sends back synthesize events so Piper speaks the
agent's reply on the satellite's speaker.

It is designed to be run as a systemd service on the same host as the
wyoming stack (the HomeClaw hub). See systemd/homeclaw-bridge.service.

Implementation notes:
 - Wyoming is a tiny TCP/JSON newline-delimited protocol. We use the
   official 'wyoming' Python package for event parsing/serialization.
 - We maintain a single long-lived connection. If the connection drops
   (satellite restart, network blip), we reconnect with exponential
   backoff capped at 30 seconds.
 - OpenClaw SDK is called via its local WebSocket at ws://127.0.0.1:18789.
   We expose only what we need here to keep the bridge dependency-light.
"""

import argparse
import asyncio
import logging
import os
import re
import signal
import sys
from dataclasses import dataclass
from typing import Optional

from wyoming.asr import Transcript
from wyoming.client import AsyncTcpClient
from wyoming.error import Error as WyomingError
from wyoming.event import Event
from wyoming.info import Describe, Info
from wyoming.tts import Synthesize, SynthesizeVoice

from openclaw_client import OpenClawAgent   # local thin wrapper, see below


_LOGGER = logging.getLogger("homeclaw-bridge")


# -----------------------------------------------------------------------------------------------------------------
#  c o n s t a n t s
# -----------------------------------------------------------------------------------------------------------------

# Regex patterns to scrub Markdown artifacts from agent replies before TTS.
# Order matters: remove container patterns before their contents would be touched.
_MARKDOWN_PATTERNS = [
    (re.compile(r"```[\s\S]*?```"), ""),                        # fenced code blocks
    (re.compile(r"`([^`]+)`"), r"\1"),                          # inline code
    (re.compile(r"\[([^\]]+)\]\([^)]+\)"), r"\1"),              # [text](url) -> text
    (re.compile(r"!\[[^\]]*\]\([^)]+\)"), ""),                  # images
    (re.compile(r"\*\*([^*]+)\*\*"), r"\1"),                    # **bold**
    (re.compile(r"\*([^*]+)\*"), r"\1"),                        # *italic*
    (re.compile(r"__([^_]+)__"), r"\1"),                        # __bold__
    (re.compile(r"_([^_]+)_"), r"\1"),                          # _italic_
    (re.compile(r"^#{1,6}\s+", re.MULTILINE), ""),              # headings
    (re.compile(r"^[\s]*[-*+]\s+", re.MULTILINE), ""),          # bullet list markers
    (re.compile(r"^\s*>\s+", re.MULTILINE), ""),                # blockquotes
    (re.compile(r"\s+"), " "),                                  # collapse whitespace (last)
]

# Reconnect backoff in seconds.
_RECONNECT_INITIAL = 1.0
_RECONNECT_MAX = 30.0
_RECONNECT_FACTOR = 2.0

# Wyoming event type names we care about. Spelled out for grep-ability.
_EVENT_TRANSCRIPT = "transcript"


# -----------------------------------------------------------------------------------------------------------------
#  c o n f i g
# -----------------------------------------------------------------------------------------------------------------

@dataclass
class BridgeConfig:
    """Runtime config for the bridge, populated from CLI args + env."""

    satellite_uri: str
    agent_name: str
    tts_voice: str
    response_timeout: float
    silent_ok_marker: str
    openclaw_ws: str
    log_level: str

    @classmethod
    def from_args(cls, args: argparse.Namespace) -> "BridgeConfig":
        return cls(
            satellite_uri=args.satellite_uri,
            agent_name=args.agent,
            tts_voice=args.tts_voice,
            response_timeout=args.response_timeout,
            silent_ok_marker=args.silent_ok_marker,
            openclaw_ws=args.openclaw_ws,
            log_level=args.log_level,
        )


# -----------------------------------------------------------------------------------------------------------------
#  b r i d g e
# -----------------------------------------------------------------------------------------------------------------

class HomeClawBridge:
    """Orchestrates Wyoming satellite <-> OpenClaw agent.

    Lifecycle:
      - run()                   main loop, reconnects forever
      - _connect_and_serve()    open TCP to satellite, serve until disconnect
      - _on_event(event)        dispatch incoming Wyoming events
      - _on_transcript(t)       main path: STT text -> agent -> TTS
    """

    # -----------------------------------------------------------------------------------------------------------------
    #  c t r
    # -----------------------------------------------------------------------------------------------------------------

    def __init__(self, config: BridgeConfig) -> None:
        self._config = config
        self._agent = OpenClawAgent(
            ws_url=config.openclaw_ws,
            agent_name=config.agent_name,
        )
        self._client: Optional[AsyncTcpClient] = None
        self._current_peer: str = "default"
        self._stop_event = asyncio.Event()

    # -----------------------------------------------------------------------------------------------------------------
    #  p u b l i c
    # -----------------------------------------------------------------------------------------------------------------

    async def run(self) -> None:
        """Main loop: connect, serve, reconnect on failure, until stopped."""
        await self._agent.connect()
        _LOGGER.info(
            "bridge ready (satellite=%s, agent=%s, voice=%s)",
            self._config.satellite_uri,
            self._config.agent_name,
            self._config.tts_voice,
        )
        backoff = _RECONNECT_INITIAL
        while not self._stop_event.is_set():
            try:
                await self._connect_and_serve()
                backoff = _RECONNECT_INITIAL          # successful session resets backoff
            except asyncio.CancelledError:
                raise
            except Exception as exc:
                _LOGGER.warning(
                    "satellite connection error (%s); reconnecting in %.1fs",
                    exc, backoff,
                )
                try:
                    await asyncio.wait_for(self._stop_event.wait(), timeout=backoff)
                    break                              # stop requested during sleep
                except asyncio.TimeoutError:
                    pass
                backoff = min(backoff * _RECONNECT_FACTOR, _RECONNECT_MAX)

        await self._agent.close()
        _LOGGER.info("bridge stopped")

    def stop(self) -> None:
        """Signal graceful shutdown. Safe to call from a signal handler."""
        self._stop_event.set()

    # -----------------------------------------------------------------------------------------------------------------
    #  p r i v a t e   —   c o n n e c t i o n
    # -----------------------------------------------------------------------------------------------------------------

    async def _connect_and_serve(self) -> None:
        """Open one TCP session to the satellite and serve events until EOF."""
        host, port = self._parse_tcp_uri(self._config.satellite_uri)
        async with AsyncTcpClient(host, port) as client:
            self._client = client
            _LOGGER.info("connected to wyoming-satellite at %s:%d", host, port)

            # Handshake: ask the satellite to describe itself. This also
            # lets us learn the peer name (Tier C multi-room scenario).
            await client.write_event(Describe().event())

            while not self._stop_event.is_set():
                event = await client.read_event()
                if event is None:
                    _LOGGER.info("satellite closed the connection")
                    break
                await self._on_event(event)

        self._client = None

    @staticmethod
    def _parse_tcp_uri(uri: str) -> tuple[str, int]:
        """Split 'tcp://host:port' into (host, port)."""
        if not uri.startswith("tcp://"):
            raise ValueError(f"unsupported URI scheme: {uri}")
        host_port = uri[len("tcp://"):]
        host, port_str = host_port.rsplit(":", 1)
        return host, int(port_str)

    # -----------------------------------------------------------------------------------------------------------------
    #  p r i v a t e   —   e v e n t   d i s p a t c h
    # -----------------------------------------------------------------------------------------------------------------

    async def _on_event(self, event: Event) -> None:
        """Route an incoming Wyoming event to its handler."""
        if Transcript.is_type(event.type):
            await self._on_transcript(Transcript.from_event(event))
        elif Info.is_type(event.type):
            info = Info.from_event(event)
            self._current_peer = self._extract_peer_name(info)
            _LOGGER.info("satellite identifies as peer=%s", self._current_peer)
        elif WyomingError.is_type(event.type):
            err = WyomingError.from_event(event)
            _LOGGER.error("satellite reported error: %s", err.text)
        else:
            _LOGGER.debug("ignoring event type=%s", event.type)

    @staticmethod
    def _extract_peer_name(info: Info) -> str:
        """Pull a satellite's symbolic name out of its Info event."""
        # Prefer 'satellite' section when present, fall back to first name found.
        try:
            if info.satellite and info.satellite.name:
                return info.satellite.name
        except AttributeError:
            pass
        return "default"

    # -----------------------------------------------------------------------------------------------------------------
    #  p r i v a t e   —   m a i n   p a t h :   t r a n s c r i p t  ->  a g e n t  ->  T T S
    # -----------------------------------------------------------------------------------------------------------------

    async def _on_transcript(self, transcript: Transcript) -> None:
        """Handle a finalized speech-to-text transcript from the satellite."""
        text = (transcript.text or "").strip()
        if not text:
            return
        _LOGGER.info("peer=%s said: %s", self._current_peer, text)

        try:
            reply = await asyncio.wait_for(
                self._agent.send_message(
                    text=text,
                    channel="voice",
                    peer=self._current_peer,
                ),
                timeout=self._config.response_timeout,
            )
        except asyncio.TimeoutError:
            _LOGGER.error("agent did not respond within %.1fs", self._config.response_timeout)
            await self._speak(
                "Non riesco a raggiungere il mio cervello. Riprova tra un momento."
            )
            return
        except Exception as exc:
            _LOGGER.exception("agent call failed: %s", exc)
            await self._speak("Qualcosa è andato storto. Controlla i log del bridge.")
            return

        clean = self._clean_for_tts(reply.text)
        if not clean:
            _LOGGER.warning("agent returned empty response, nothing to speak")
            return

        if clean == self._config.silent_ok_marker:
            _LOGGER.info("silent-ok marker received; suppressing TTS")
            return

        await self._speak(clean)

    async def _speak(self, text: str) -> None:
        """Send a Wyoming synthesize event so Piper generates and plays audio."""
        if self._client is None:
            _LOGGER.warning("cannot speak: no active satellite connection")
            return
        synth = Synthesize(
            text=text,
            voice=SynthesizeVoice(name=self._config.tts_voice),
        )
        await self._client.write_event(synth.event())
        _LOGGER.info("synthesize dispatched (len=%d)", len(text))

    # -----------------------------------------------------------------------------------------------------------------
    #  p r i v a t e   —   t e x t   s a n i t i z a t i o n
    # -----------------------------------------------------------------------------------------------------------------

    @staticmethod
    def _clean_for_tts(text: Optional[str]) -> str:
        """Strip Markdown so the TTS engine does not read symbols literally.

        The agent's SOUL.md instructs it to avoid Markdown, but LLMs drift.
        This belt-and-suspenders pass ensures the user never hears asterisks
        or backticks spoken out loud.
        """
        if not text:
            return ""
        out = text
        for pattern, replacement in _MARKDOWN_PATTERNS:
            out = pattern.sub(replacement, out)
        return out.strip()


# -----------------------------------------------------------------------------------------------------------------
#  m a i n
# -----------------------------------------------------------------------------------------------------------------

def _build_arg_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="homeclaw-bridge",
        description="Wyoming <-> OpenClaw bridge for HomeClaw voice agent.",
    )
    parser.add_argument(
        "--satellite-uri",
        default=os.environ.get("HOMECLAW_SATELLITE_URI", "tcp://127.0.0.1:10700"),
        help="Wyoming satellite TCP URI",
    )
    parser.add_argument(
        "--agent",
        default=os.environ.get("HOMECLAW_AGENT", "HomeClaw"),
        help="OpenClaw agent name to route messages to",
    )
    parser.add_argument(
        "--tts-voice",
        default=os.environ.get("HOMECLAW_TTS_VOICE", "it_IT-paola-medium"),
        help="Piper voice model name",
    )
    parser.add_argument(
        "--response-timeout",
        type=float,
        default=float(os.environ.get("HOMECLAW_RESPONSE_TIMEOUT", "8.0")),
        help="Max wait (seconds) for agent response",
    )
    parser.add_argument(
        "--silent-ok-marker",
        default=os.environ.get("HOMECLAW_SILENT_OK", "[SILENT_OK]"),
        help="Agent reply exactly matching this is NOT spoken aloud",
    )
    parser.add_argument(
        "--openclaw-ws",
        default=os.environ.get("HOMECLAW_OPENCLAW_WS", "ws://127.0.0.1:18789"),
        help="OpenClaw gateway WebSocket URL",
    )
    parser.add_argument(
        "--log-level",
        default=os.environ.get("HOMECLAW_LOG_LEVEL", "INFO"),
        choices=["DEBUG", "INFO", "WARNING", "ERROR"],
    )
    return parser


async def _async_main(config: BridgeConfig) -> int:
    bridge = HomeClawBridge(config)

    loop = asyncio.get_running_loop()
    for sig in (signal.SIGINT, signal.SIGTERM):
        loop.add_signal_handler(sig, bridge.stop)

    await bridge.run()
    return 0


def main() -> int:
    parser = _build_arg_parser()
    args = parser.parse_args()
    config = BridgeConfig.from_args(args)

    logging.basicConfig(
        level=getattr(logging, config.log_level),
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    )

    try:
        return asyncio.run(_async_main(config))
    except KeyboardInterrupt:
        return 130


if __name__ == "__main__":
    sys.exit(main())
