from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy import Select
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status
from typing import Annotated
from fastapi_pagination.ext.sqlalchemy import paginate
from src.base.paginate_config import PaginatePage
from src.base.responses import ResponseSchema
from src.base.utils import DatabaseError, EnoughProductOrder
from src.config.session import get_async_session
from src.order.schemas import CreateOrderSchema, OrderListSchema, OrderDetailSchema, OrderUpdateSchema
from src.order.session import OrderSession

order_router = APIRouter()
responses = ResponseSchema()


@order_router.post(
    "/",
    # response_model=CreateOrderSchema,
    # responses=responses(CreateOrderSchema, status.HTTP_201_CREATED, [status.HTTP_409_CONFLICT]),
    status_code=status.HTTP_201_CREATED,
    description="Order create",
)
async def create_order(
        order_data: CreateOrderSchema,
        session: AsyncSession = Depends(get_async_session),
):
    """
    Create order
    :param order_data:
    :param session:
    :return: order_data
    """
    try:
        a = await OrderSession(session).create_order(order_data)
        return {'message': a}

    except DatabaseError as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail='Ошибка базы данных')
    except EnoughProductOrder as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=e.message)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail='SERVER_ERROR')
    # Здесь полная хрень надо переделать

    # полный топор


@order_router.get(
    "/",
    response_model=PaginatePage[OrderListSchema],
    responses=responses(PaginatePage[OrderListSchema]),
    description='Order list'
)
async def order_list(
        search_id: Annotated[int | None, Query(description="Search id field")] = None,
        session: AsyncSession = Depends(get_async_session)
) -> PaginatePage[OrderListSchema]:
    """
    Order list
    :param search_id:
    :param session:
    :return:
    """
    order: Select = await OrderSession(session).order_list(search_id)
    return await paginate(session, order)


@order_router.get(
    '/{order_id}/',
    response_model=OrderDetailSchema,
    responses=responses(OrderDetailSchema, statuses=[status.HTTP_404_NOT_FOUND]),
    description='Order detail',
)
async def order_detail(
        order_id: int,
        session: AsyncSession = Depends(get_async_session),
) -> OrderDetailSchema:
    """Order detail"""
    order = await OrderSession(session).get_order_by_id(order_id)
    if order:
        return order
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Order not found')


@order_router.patch(
    '/{order_id}/',
    response_model=OrderUpdateSchema,
    responses=responses(OrderUpdateSchema, statuses=[status.HTTP_409_CONFLICT,
                                                     status.HTTP_404_NOT_FOUND]),
    description='Order update'
)
async def order_update(
        order_id: int,
        order_data: OrderUpdateSchema,
        session: AsyncSession = Depends(get_async_session),
) -> OrderUpdateSchema:
    """Order update"""
    new_order = order_data.model_dump(exclude_unset=True)
    order = await OrderSession(session).update_order_by_id(order_id, **new_order)
    if order:
        return order
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Order not found')
