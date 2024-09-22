from datetime import date
from pydantic import BaseModel


class BaseOrderSchema(BaseModel):
    order_id: int
    product_id: int
    product_in_order: int
    create_date: date
    status: str


class CreateOrderSchema(BaseOrderSchema):
    """
    Create Order
    """


class OrderListSchema(BaseOrderSchema):
    """
    List Order
    """


class OrderDetailSchema(BaseOrderSchema):
    """
    Order detail scheme
    """
    id: int


class OrderUpdateSchema(BaseModel):
    """
    Order update schema
    """
    create_date: date | None = None
    status: str | None = None
