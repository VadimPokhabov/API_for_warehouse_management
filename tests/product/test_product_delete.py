from sqlalchemy import select
from starlette import status

from src.product.models import ProductDB
from tests.base.base_test import BaseTestCase
from tests.conftest import get_random_value


class TestCaseCourseDelete(BaseTestCase):
    """Тест кейс на удаление продукта."""
    url = '/products'

    async def test_delete_product(self, product, override_get_async_session):
        """Тест на удаление продукта."""
        url = f'{self.url}/{product.id}/'
        await self.make_delete(url)
        await self.make_get(f'{url}/{product.id}/', status_code=status.HTTP_404_NOT_FOUND)
        assert_query = select(ProductDB).filter_by(id=product.id)
        result = await override_get_async_session.scalar(assert_query)
        assert result is None

    async def test_delete_product_404(self):
        """Тест на удаление продукта с несуществующим id (ошибка 404)."""
        course_id = get_random_value()
        url = f'{self.url}/{course_id}/'
        await self.make_delete(url, status_code=status.HTTP_404_NOT_FOUND)

    async def test_delete_product_405(self, product):
        """Тест на удаление продукта с выбором ошибочного метода (ошибка 405)."""
        url = f'{self.url}/{product.id}/'
        await self.make_post(url, None, status_code=status.HTTP_405_METHOD_NOT_ALLOWED)

    async def test_delete_product_422(self, product):
        """Тест на удаление продукта с логической ошибкой в запросе (ошибка 422)."""
        url = f'{self.url}/{product.name}/'
        await self.make_delete(url, status_code=status.HTTP_422_UNPROCESSABLE_ENTITY)
