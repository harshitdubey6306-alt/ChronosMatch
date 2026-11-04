from fastapi import APIRouter, Depends, HTTPException, status

from app.api.deps import get_current_user, require_admin
from app.crud.trade import trade_crud
from app.db.session import get_db
from app.schemas.trade import TradeCreate, TradeRead, TradeUpdate

router = APIRouter(prefix="/trades", tags=["trades"])


@router.get("/", response_model=list[TradeRead], dependencies=[Depends(get_current_user)])
async def list_trades(skip: int = 0, limit: int = 100, symbol: str | None = None, db=Depends(get_db)):
    return await trade_crud.list(db, skip, limit, **({"symbol": symbol} if symbol else {}))


@router.get("/{trade_id}", response_model=TradeRead, dependencies=[Depends(get_current_user)])
async def get_trade(trade_id: int, db=Depends(get_db)):
    trade = await trade_crud.get(db, trade_id)
    if not trade:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Trade not found")
    return trade


# Writes are admin/service-only: the matching engine's flusher is the real producer of trades.
@router.post("/", response_model=TradeRead, status_code=201, dependencies=[Depends(require_admin)])
async def create_trade(body: TradeCreate, db=Depends(get_db)):
    return await trade_crud.create(db, body.model_dump())


@router.patch("/{trade_id}", response_model=TradeRead, dependencies=[Depends(require_admin)])
async def update_trade(trade_id: int, body: TradeUpdate, db=Depends(get_db)):
    trade = await trade_crud.get(db, trade_id)
    if not trade:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Trade not found")
    return await trade_crud.update(db, trade, body.model_dump(exclude_unset=True))


@router.delete("/{trade_id}", status_code=204, dependencies=[Depends(require_admin)])
async def delete_trade(trade_id: int, db=Depends(get_db)):
    trade = await trade_crud.get(db, trade_id)
    if not trade:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Trade not found")
    await trade_crud.delete(db, trade)
