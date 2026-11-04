import json

from fastapi.encoders import jsonable_encoder
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

CHANNEL = "events"


def row_to_dict(obj) -> dict:
    data = {c.name: getattr(obj, c.name) for c in obj.__table__.columns if c.name != "hashed_password"}
    return jsonable_encoder(data)


async def notify(db: AsyncSession, topic: str, event: str, data: dict) -> None:
    """pg_notify runs inside the caller's transaction: it is delivered only if the commit succeeds."""
    payload = json.dumps({"topic": topic, "event": event, "data": data})  # Postgres limit: 8000 bytes
    await db.execute(text("SELECT pg_notify(:ch, :p)"), {"ch": CHANNEL, "p": payload})
