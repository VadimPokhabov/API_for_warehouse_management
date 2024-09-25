from datetime import date
from pydantic import BaseModel, Field
from src.product.schemas import ProductQuantityScheme


class BaseOrderSchema(BaseModel):
    create_date: date
    status: str


class CreateOrderSchema(BaseModel):
    """
    Create Order
    """
    product_id: int
    quantity_in_order: int = Field(ge=1)
    product: str


class OrderListSchema(BaseOrderSchema):
    """
    List Order
    """


class OrderDetailSchema(BaseOrderSchema):
    """
    Order detail scheme
    """
    id: int
    product: ProductQuantityScheme | None = None


class OrderUpdateSchema(BaseModel):
    """
    Order update schema
    """
    create_date: date | None = None
    status: str | None = None
