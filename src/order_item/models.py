from typing import TYPE_CHECKING
from sqlalchemy.orm import Mapped, relationship
from src.base.models import BaseDBModel, mc, FK
if TYPE_CHECKING:
    from src import ProductDB


class OrderItem(BaseDBModel):
    __tablename__ = "order_item"
    order_id: Mapped[int] = mc(FK("order.id", ondelete="CASCADE"))
    product_id: Mapped[int] = mc(FK("product.id", ondelete="CASCADE"))
    quantity_in_order: Mapped[int] = mc(nullable=False)
    product: Mapped["ProductDB"] = relationship(back_populates="order")
