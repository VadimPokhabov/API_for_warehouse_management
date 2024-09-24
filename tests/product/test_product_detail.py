from starlette import status

from tests.base.base_test import BaseTestCase
from tests.conftest import get_random_value


class TestCaseProductGet(BaseTestCase):
    """Тест кейс на получение продукта."""
    url = '/products'

    async def test_get_product(self, product):
        """Тест на получение продукта."""
        url = f'{self.url}/{product.id}/'
        response = await self.make_get(url)
        assert response.get('id') == product.id

    async def test_get_product_404(self):
        """Тест на получение продукта с несуществующим id (ошибка 404)."""
        course_id = get_random_value()
        url = f'{self.url}/{course_id}/'
        await self.make_get(url, status_code=status.HTTP_404_NOT_FOUND)

    async def test_get_product_405(self, product):
        """Тест на получение продукта с выбором ошибочного метода (ошибка 405)."""
        url = f'{self.url}/{product.id}/'
        await self.make_post(url, None, status_code=status.HTTP_405_METHOD_NOT_ALLOWED)

    async def test_get_product_422(self, product):
        """Тест на получение продукта с логической ошибкой в запросе (ошибка 422)."""
        url = f'{self.url}/{product}/'
        await self.make_get(url, status_code=status.HTTP_422_UNPROCESSABLE_ENTITY)
