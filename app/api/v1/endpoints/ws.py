from fastapi import APIRouter, Query, WebSocket, WebSocketDisconnect

from app.api.deps import user_from_token
from app.db.session import AsyncSessionLocal
from app.realtime.manager import manager

router = APIRouter(tags=["realtime"])
TOPICS = {"orders", "trades"}


@router.websocket("/ws/{topic}")
async def stream(websocket: WebSocket, topic: str, token: str = Query(...)):
    """Connect: ws://host/api/v1/ws/trades?token=<JWT>"""
    if topic not in TOPICS:
        await websocket.close(code=4404)
        return
    async with AsyncSessionLocal() as db:
        user = await user_from_token(db, token)
    if not user:
        await websocket.close(code=4401)
        return
    await manager.connect(topic, websocket, user)
    try:
        while True:
            await websocket.receive_text()  # keep-alive; clients may send pings
    except WebSocketDisconnect:
        manager.disconnect(topic, websocket, user)
