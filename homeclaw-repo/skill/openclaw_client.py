"""
Thin OpenClaw Gateway client used by the HomeClaw bridge.

The full OpenClaw Python SDK is heavy and includes tool registration,
skill management, etc. For the bridge we only need:
  - connect to the local gateway WebSocket
  - send a user message to a named agent on a given channel+peer
  - await the agent's reply

This tiny wrapper is intentionally narrow to keep the bridge small and
easy to audit. If you need more (file upload, multi-turn streaming, etc.)
use the full SDK instead.
"""

import asyncio
import json
import logging
import uuid
from dataclasses import dataclass
from typing import Optional

import websockets
from websockets.client import WebSocketClientProtocol


_LOGGER = logging.getLogger("homeclaw-bridge.openclaw")


# -----------------------------------------------------------------------------------------------------------------
#  t y p e s
# -----------------------------------------------------------------------------------------------------------------

@dataclass
class AgentReply:
    """The text returned by an OpenClaw agent for a single user message."""
    text: str
    model: Optional[str] = None
    session_id: Optional[str] = None


# -----------------------------------------------------------------------------------------------------------------
#  c l i e n t
# -----------------------------------------------------------------------------------------------------------------

class OpenClawAgent:
    """Minimal async client talking to the OpenClaw gateway WebSocket."""

    # -----------------------------------------------------------------------------------------------------------------
    #  c t r
    # -----------------------------------------------------------------------------------------------------------------

    def __init__(self, ws_url: str, agent_name: str) -> None:
        self._ws_url = ws_url
        self._agent_name = agent_name
        self._ws: Optional[WebSocketClientProtocol] = None
        self._lock = asyncio.Lock()

    # -----------------------------------------------------------------------------------------------------------------
    #  p u b l i c
    # -----------------------------------------------------------------------------------------------------------------

    async def connect(self) -> None:
        """Open the WebSocket connection to the OpenClaw gateway."""
        if self._ws is not None and not self._ws.closed:
            return
        _LOGGER.info("connecting to openclaw gateway at %s", self._ws_url)
        self._ws = await websockets.connect(
            self._ws_url,
            ping_interval=20,
            ping_timeout=20,
            close_timeout=5,
        )
        await self._send({
            "type": "handshake",
            "client": "homeclaw-bridge",
            "version": "1.0.0",
        })
        _LOGGER.info("openclaw gateway connection established")

    async def close(self) -> None:
        """Close the WebSocket connection gracefully."""
        if self._ws is not None and not self._ws.closed:
            await self._ws.close()
        self._ws = None

    async def send_message(
        self,
        text: str,
        channel: str,
        peer: str,
    ) -> AgentReply:
        """Send a user message to the agent and wait for a single reply.

        Raises:
            ConnectionError: if the gateway is not reachable
            RuntimeError: if the gateway returns a malformed response
        """
        if self._ws is None or self._ws.closed:
            await self.connect()

        correlation_id = str(uuid.uuid4())
        request = {
            "type": "agent.send_message",
            "correlation_id": correlation_id,
            "agent": self._agent_name,
            "channel": channel,
            "peer": peer,
            "content": {"text": text},
        }

        # The gateway is multiplexed: requests and responses can interleave.
        # For the bridge, serialize on a lock — we only have one voice input
        # at a time per satellite anyway, and this keeps the code dead-simple.
        async with self._lock:
            await self._send(request)
            return await self._await_reply(correlation_id)

    # -----------------------------------------------------------------------------------------------------------------
    #  p r i v a t e
    # -----------------------------------------------------------------------------------------------------------------

    async def _send(self, payload: dict) -> None:
        assert self._ws is not None
        await self._ws.send(json.dumps(payload))

    async def _await_reply(self, correlation_id: str) -> AgentReply:
        assert self._ws is not None
        while True:
            raw = await self._ws.recv()
            try:
                msg = json.loads(raw)
            except json.JSONDecodeError:
                _LOGGER.warning("gateway sent non-JSON frame; ignoring")
                continue

            # Skip messages that aren't for us.
            if msg.get("correlation_id") != correlation_id:
                continue

            msg_type = msg.get("type")
            if msg_type == "agent.reply":
                return self._parse_reply(msg)
            if msg_type == "agent.error":
                raise RuntimeError(msg.get("error", "unknown agent error"))
            # Intermediate progress events ('agent.typing', 'tool.call' etc.)
            # are harmless; we just keep reading until the final reply arrives.
            _LOGGER.debug("ignoring interim event type=%s", msg_type)

    @staticmethod
    def _parse_reply(msg: dict) -> AgentReply:
        content = msg.get("content") or {}
        text = content.get("text")
        if not isinstance(text, str):
            raise RuntimeError("gateway reply missing 'content.text'")
        return AgentReply(
            text=text,
            model=msg.get("model"),
            session_id=msg.get("session_id"),
        )
