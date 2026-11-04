# Import every model here so Base.metadata (and Alembic) sees all tables.
from app.models.base import Base  # noqa: F401
from app.models.order import Order  # noqa: F401
from app.models.trade import Trade  # noqa: F401
from app.models.user import User  # noqa: F401
