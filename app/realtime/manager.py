import asyncio
import json

import asyncpg
from fastapi import WebSocket

from app.core.config import settings
from app.realtime.notify import CHANNEL


class ConnectionManager:
    def __init__(self) -> None:
        self.subs: dict[str, set[tuple[WebSocket, int, str]]] = {}

    async def connect(self, topic: str, ws: WebSocket, user) -> None:
        await ws.accept()
        self.subs.setdefault(topic, set()).add((ws, user.id, user.role))

    def disconnect(self, topic: str, ws: WebSocket, user) -> None:
        self.subs.get(topic, set()).discard((ws, user.id, user.role))

    async def broadcast(self, msg: dict) -> None:
        topic, data = msg["topic"], msg["data"]
        for ws, uid, role in list(self.subs.get(topic, ())):
            # Orders are private: owner or admin only. Trades are public.
            if topic == "orders" and role != "admin" and data.get("user_id") != uid:
                continue
            try:
                await ws.send_json(msg)
            except Exception:
                self.subs[topic].discard((ws, uid, role))


manager = ConnectionManager()


async def pg_listener() -> None:
    """One LISTEN connection per API worker -> fan out to that worker's websockets.
    Because it uses Postgres NOTIFY, it works with many workers/servers (no Redis needed at first)."""
    loop = asyncio.get_running_loop()

    def on_event(_conn, _pid, _channel, payload: str) -> None:
        loop.create_task(manager.broadcast(json.loads(payload)))

    while True:
        try:
            conn = await asyncpg.connect(settings.asyncpg_dsn)
            await conn.add_listener(CHANNEL, on_event)
            while not conn.is_closed():
                await asyncio.sleep(1)
        except asyncio.CancelledError:
            raise
        except Exception:
            await asyncio.sleep(2)  # reconnect
