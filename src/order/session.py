from fastapi import HTTPException
from sqlalchemy import Select, select, update
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from src.base.utils import handle_error
from src import Order, ProductDB
from src.order.schemas import CreateOrderSchema, OrderDetailSchema, OrderUpdateSchema
from sqlalchemy.exc import IntegrityError


class OrderSession:

    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def create_order(self, data: CreateOrderSchema):
        """Create order in the database."""
        async with self.session.begin():
            query = select(ProductDB).where(ProductDB.id == data.product_id)
            product_row = await self.session.scalar(query)
            product_quantity = product_row.quantity
            if product_quantity > data.quantity_in_order:
                try:
                    result = product_quantity - data.quantity_in_order
                    qua = update(ProductDB).where(ProductDB.id == data.product_id).values(quantity=result).returning(
                        ProductDB)
                    res = await self.session.execute(qua)
                    order, = res.first() or (None,)
                    return order
                except IntegrityError as error:
                    handle_error(error)
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail="Недостаточное количество товара на складе")

    async def order_list(self, values: int | None) -> Select:
        """Returns list order"""
        async with self.session.begin():
            query = select(Order)
            if values:
                query = query.filter(
                    Order.id == values
                ).distinct()
            return query

    async def get_order_by_id(self, order_id: int) -> OrderDetailSchema:
        """Returns order by id."""
        async with self.session.begin():
            query = select(Order).filter_by(id=order_id)
            result = await self.session.execute(query)
            product = result.first()
            result, = product or (None,)
            return result

    async def update_order_by_id(self, order_id: int, **data) -> OrderUpdateSchema:
        """Update order by id."""
        async with self.session.begin():
            query = update(Order).where(Order.id == order_id).values(**data).returning(Order)
            try:
                result = await self.session.execute(query)
                product, = result.first() or (None,)
                return product
            except IntegrityError as err:
                return handle_error(err)
