from fastapi import APIRouter, Depends, HTTPException, status

from app.api.deps import get_current_user
from app.crud.order import order_crud
from app.db.session import get_db
from app.models.order import Order
from app.models.user import User
from app.schemas.order import OrderCreate, OrderRead, OrderUpdate

router = APIRouter(prefix="/orders", tags=["orders"])


async def _owned_order(order_id: int, db, user: User) -> Order:
    order = await order_crud.get(db, order_id)
    # 404 (not 403) so users can't probe for other people's order ids
    if not order or (order.user_id != user.id and user.role != "admin"):
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Order not found")
    return order


@router.post("/", response_model=OrderRead, status_code=201)
async def create_order(body: OrderCreate, db=Depends(get_db), user: User = Depends(get_current_user)):
    return await order_crud.create(db, {**body.model_dump(), "user_id": user.id})


@router.get("/", response_model=list[OrderRead])
async def list_orders(skip: int = 0, limit: int = 100, symbol: str | None = None, db=Depends(get_db),
                      user: User = Depends(get_current_user)):
    filters = {"symbol": symbol} if symbol else {}
    if user.role != "admin":
        filters["user_id"] = user.id
    return await order_crud.list(db, skip, limit, **filters)


@router.get("/{order_id}", response_model=OrderRead)
async def get_order(order_id: int, db=Depends(get_db), user: User = Depends(get_current_user)):
    return await _owned_order(order_id, db, user)


@router.patch("/{order_id}", response_model=OrderRead)
async def update_order(order_id: int, body: OrderUpdate, db=Depends(get_db),
                       user: User = Depends(get_current_user)):
    order = await _owned_order(order_id, db, user)
    if order.status != "OPEN":
        raise HTTPException(status.HTTP_409_CONFLICT, "Only OPEN orders can be modified")
    return await order_crud.update(db, order, body.model_dump(exclude_unset=True))


@router.delete("/{order_id}", status_code=204)
async def delete_order(order_id: int, db=Depends(get_db), user: User = Depends(get_current_user)):
    await order_crud.delete(db, await _owned_order(order_id, db, user))
