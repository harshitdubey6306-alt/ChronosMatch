from app.crud.base import CRUDBase
from app.models.order import Order

order_crud = CRUDBase(Order, topic="orders")
