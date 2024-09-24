import pytest

from src.product.models import ProductDB

PRODUCT_DATA = {
    'name': 'some product',
    'description': 'some description',
    'price': 120.0,
    'quantity': 50
}


async def create_products(override_get_async_session, count: int = 0):
    """Функция для создания продуктов."""
    for _ in range(count):
        await create_product(override_get_async_session)


async def create_product(override_get_async_session):
    """Функция для создания продукта."""
    product = ProductDB(**PRODUCT_DATA)
    override_get_async_session.add(product)
    await override_get_async_session.commit()
    return product


@pytest.fixture(scope='function')
async def product(override_get_async_session):
    """Фикстура для создания продукта."""
    product = await create_product(override_get_async_session)
    await create_products(override_get_async_session, 10)
    return product


@pytest.fixture(scope='function')
async def product2(override_get_async_session):
    """Фикстура для создания продукта."""
    return await create_product(override_get_async_session)
