from fastapi import APIRouter

from app.api.v1.endpoints import auth, orders, trades, users, ws

api_router = APIRouter()
for module in (auth, users, orders, trades, ws):
    api_router.include_router(module.router)
