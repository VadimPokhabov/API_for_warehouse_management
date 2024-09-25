import pytest
from src.order_item.models import OrderItem

ORDER_DATA = {
    'quantity_in_order': 10,
}


async def create_orders(override_get_async_session, product, count: int = 0):
    """Функция для создания заказов."""
    for _ in range(count):
        await create_order(override_get_async_session, product)


async def create_order(override_get_async_session, product):
    """Функция для создания заказа"""
    order_copy = ORDER_DATA.copy() | {'product_id': product.id} | {'product': product.name}
    order = OrderItem(**order_copy)
    override_get_async_session.add(order)
    await override_get_async_session.commit()
    return order


@pytest.fixture(scope='function')
async def order(override_get_async_session, product):
    """Фикстура для создания заказа"""
    order = await create_order(override_get_async_session, product)
    await create_orders(override_get_async_session, product, 10)
    return order


@pytest.fixture(scope='function')
async def type2(override_get_async_session, product):
    """Фикстура для создания заказа"""
    return await create_order(override_get_async_session, product)



# async def create_lessons(override_get_async_session, order, count: int = 0):
#     """Функция для создания заказов."""
#     for _ in range(count):
#         await create_order(override_get_async_session, order)
#
#
# async def create_order(override_get_async_session, product):
#     """Функция для создания заказа."""
#     order_data = ORDER_DATA.copy() | {'product_id': product.id} | {'product': product.name}
#     order = Order(**order_data)
#     override_get_async_session.add(order)
#     await override_get_async_session.commit()
#     return order
#
#
# @pytest.fixture(scope='function')
# async def order(override_get_async_session, product):
#     """Фиктсура для создания заказа."""
#     order = await create_order(override_get_async_session, product)
#     await create_order(override_get_async_session, product, 10)
#     return order
#
#
# @pytest.fixture(scope='function')
# async def lesson2(override_get_async_session, product):
#     """Фиктсура для создания заказа 2."""
#     return await create_order(override_get_async_session, product)
