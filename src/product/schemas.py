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
    id: int


class ProductDetailSchema(BaseProductSchema):
    """
    Product detail schema
    """
    id: int


class ProductUpdateSchema(BaseProductSchema):
    """
    Product update schema
    """


class ProductQuantityScheme(BaseProductSchema):
    """
    Product quantity schema
    """
    id: int
    quantity: int

