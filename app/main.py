import asyncio
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.v1.router import api_router
from app.db.base import Base
from app.db.session import engine
from app.realtime.manager import pg_listener


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Dev convenience. In production, manage the schema with Alembic migrations instead.
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    listener = asyncio.create_task(pg_listener())
    yield
    listener.cancel()
    await engine.dispose()


app = FastAPI(title="ChronosMatch API", version="1.0.0", lifespan=lifespan)
app.add_middleware(CORSMiddleware, allow_origins=["http://localhost:3000"],
                   allow_methods=["*"], allow_headers=["*"], allow_credentials=True)
app.include_router(api_router, prefix="/api/v1")


@app.get("/health", tags=["meta"])
async def health():
    return {"status": "ok"}
