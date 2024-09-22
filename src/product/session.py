from sqlalchemy import insert, Select, select, update, delete
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from src import ProductDB
from src.base.utils import handle_error
from src.product.schemas import CreateProductSchema, ProductDetailSchema, ProductUpdateSchema


class ProductSession:

    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def create_product(self, data: CreateProductSchema):
        """Create product in the database."""
        async with self.session.begin():
            product = data.model_dump()
            try:
                query = insert(ProductDB).values(**product).returning(ProductDB)
                return await self.session.scalar(query)
            except IntegrityError as err:
                return handle_error(err)

    async def list_product(self, value: str | None, values: int | None) -> Select:
        """Returns list product"""
        async with self.session.begin():
            query = select(ProductDB)
            if value:
                query = query.filter(
                    ProductDB.name.ilike(f"%{value}%"),
                ).distinct()
            if values:
                query = query.filter(
                    ProductDB.id == values
                ).distinct()
            return query

    async def get_product_by_id(self, product_id: int) -> ProductDetailSchema:
        """Returns product by id."""
        async with self.session.begin():
            query = select(ProductDB).filter_by(id=product_id)
            result = await self.session.execute(query)
            product = result.first()
            result, = product or (None,)
            return result

    async def update_product_by_id(self, product_id: int, **data) -> ProductUpdateSchema:
        """Update product by id."""
        async with self.session.begin():
            query = update(ProductDB).where(ProductDB.id == product_id).values(**data).returning(ProductDB)
            try:
                result = await self.session.execute(query)
                product, = result.first() or (None,)
                return product
            except IntegrityError as err:
                return handle_error(err)

    async def delete_product_by_id(self, product_id: int) -> int | None:
        """Delete product by id."""
        async with self.session.begin():
            query = delete(ProductDB).where(ProductDB.id == product_id).returning(ProductDB)
            result = await self.session.execute(query)
            id_product, = result.first() or (None,)
            return id_product
