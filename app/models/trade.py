from sqlalchemy import BigInteger, String
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base, TimestampMixin


class Trade(Base, TimestampMixin):
    __tablename__ = "trades"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    symbol: Mapped[str] = mapped_column(String(16), index=True)
    buy_order_id: Mapped[int] = mapped_column(BigInteger)
    sell_order_id: Mapped[int] = mapped_column(BigInteger)
    price: Mapped[int] = mapped_column(BigInteger)
    qty: Mapped[int] = mapped_column(BigInteger)
    ts_in_ns: Mapped[int] = mapped_column(BigInteger, default=0)
    ts_out_ns: Mapped[int] = mapped_column(BigInteger, default=0)
