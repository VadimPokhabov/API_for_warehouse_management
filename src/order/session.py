from sqlalchemy import insert, Select, select, update
from sqlalchemy.ext.asyncio import AsyncSession
from src.base.utils import handle_error
from src import Order, OrderItem
from src.order.schemas import CreateOrderSchema, OrderDetailSchema, OrderUpdateSchema
from sqlalchemy.exc import IntegrityError


class OrderSession:

    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def create_order(self, data: CreateOrderSchema):
        """Create order in the database."""
        async with self.session.begin():
            order = data.model_dump()
            try:
                query = insert(Order).values(**order).returning(Order)
                return await self.session.scalar(query)
            except IntegrityError as err:
                return handle_error(err)

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
