from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.security import hash_password, verify_password
from app.crud.base import CRUDBase
from app.models.user import User


class CRUDUser(CRUDBase[User]):
    async def get_by_email(self, db: AsyncSession, email: str) -> User | None:
        return await db.scalar(select(User).where(User.email == email.lower()))

    async def register(self, db: AsyncSession, email: str, password: str) -> User:
        return await self.create(db, {"email": email.lower(), "hashed_password": hash_password(password)})

    async def authenticate(self, db: AsyncSession, email: str, password: str) -> User | None:
        user = await self.get_by_email(db, email)
        return user if user and verify_password(password, user.hashed_password) else None


user_crud = CRUDUser(User)  # no topic: user rows are never broadcast
