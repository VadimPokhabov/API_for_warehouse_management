from pydantic import BaseModel


class BaseProductSchema(BaseModel):
    name: str
    description: str
    price: float
    quantity: int


class CreateProductSchema(BaseProductSchema):
    """
    Create Product
    """


class ProductListSchema(BaseProductSchema):
    """
    List Product
    """


class ProductDetailSchema(BaseProductSchema):
    """
    Product detail schema
    """
    id: int


class ProductUpdateSchema(BaseProductSchema):
    """
    Product update schema
    """


    # class ProductUpdateSchema(BaseModel):  FROM PATH NEED NONE
    # """ Product update scheme """
    # name: str | None = None
    # description: str | None = None
    # price: float | None = None
    # quantity: int | None = None
