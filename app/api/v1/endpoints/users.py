from fastapi import APIRouter, Depends

from app.api.deps import get_current_user, require_admin
from app.crud.user import user_crud
from app.db.session import get_db
from app.models.user import User
from app.schemas.user import UserRead

router = APIRouter(prefix="/users", tags=["users"])


@router.get("/me", response_model=UserRead)
async def me(user: User = Depends(get_current_user)):
    return user


@router.get("/", response_model=list[UserRead])
async def list_users(skip: int = 0, limit: int = 100, db=Depends(get_db), _: User = Depends(require_admin)):
    return await user_crud.list(db, skip, limit)
