from datetime import datetime
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field


class OrderCreate(BaseModel):
    symbol: str = Field(min_length=1, max_length=16)
    side: Literal["BUY", "SELL"]
    price: int = Field(gt=0, description="integer ticks")
    qty: int = Field(gt=0)


class OrderUpdate(BaseModel):
    price: int | None = Field(default=None, gt=0)
    qty: int | None = Field(default=None, gt=0)
    status: Literal["OPEN", "FILLED", "CANCELLED"] | None = None


class OrderRead(OrderCreate):
    model_config = ConfigDict(from_attributes=True)
    id: int
    user_id: int
    status: str
    created_at: datetime
