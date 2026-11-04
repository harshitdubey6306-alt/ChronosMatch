from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class TradeCreate(BaseModel):
    symbol: str
    buy_order_id: int
    sell_order_id: int
    price: int = Field(gt=0)
    qty: int = Field(gt=0)
    ts_in_ns: int = 0
    ts_out_ns: int = 0


class TradeUpdate(BaseModel):
    price: int | None = Field(default=None, gt=0)
    qty: int | None = Field(default=None, gt=0)


class TradeRead(TradeCreate):
    model_config = ConfigDict(from_attributes=True)
    id: int
    created_at: datetime
