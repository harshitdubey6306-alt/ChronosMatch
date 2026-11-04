from app.crud.base import CRUDBase
from app.models.trade import Trade

trade_crud = CRUDBase(Trade, topic="trades")
