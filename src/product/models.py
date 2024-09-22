from typing import TYPE_CHECKING, List
from sqlalchemy.orm import Mapped, relationship
from src.base.models import BaseDBModel, mc
if TYPE_CHECKING:
    from src import OrderItem


class ProductDB(BaseDBModel):
    __tablename__ = "product"
    name: Mapped[str] = mc(nullable=False)
    description: Mapped[str] = mc(nullable=False)
    price: Mapped[float] = mc(nullable=False)
    quantity: Mapped[int] = mc(nullable=False)
    order: Mapped['OrderItem'] = relationship(back_populates="product")
