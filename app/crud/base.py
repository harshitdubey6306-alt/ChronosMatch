from typing import Generic, TypeVar

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.realtime.notify import notify, row_to_dict

ModelT = TypeVar("ModelT")


class CRUDBase(Generic[ModelT]):
    """Generic async CRUD. Set `topic` to push every change to websocket subscribers."""

    def __init__(self, model: type[ModelT], topic: str | None = None):
        self.model, self.topic = model, topic

    async def get(self, db: AsyncSession, id: int) -> ModelT | None:
        return await db.get(self.model, id)

    async def list(self, db: AsyncSession, skip: int = 0, limit: int = 100, **filters) -> list[ModelT]:
        stmt = (select(self.model).filter_by(**filters)
                .order_by(self.model.id.desc()).offset(skip).limit(min(limit, 500)))
        return list((await db.scalars(stmt)).all())

    async def create(self, db: AsyncSession, data: dict) -> ModelT:
        obj = self.model(**data)
        db.add(obj)
        await db.flush()                      # get id + defaults
        if self.topic:
            await notify(db, self.topic, "created", row_to_dict(obj))
        await db.commit()
        return obj

    async def update(self, db: AsyncSession, obj: ModelT, changes: dict) -> ModelT:
        for k, v in changes.items():
            setattr(obj, k, v)
        await db.flush()
        if self.topic:
            await notify(db, self.topic, "updated", row_to_dict(obj))
        await db.commit()
        return obj

    async def delete(self, db: AsyncSession, obj: ModelT) -> None:
        snapshot = row_to_dict(obj)
        await db.delete(obj)
        await db.flush()
        if self.topic:
            await notify(db, self.topic, "deleted", snapshot)
        await db.commit()
