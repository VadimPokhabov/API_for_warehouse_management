from starlette import status

from tests.base.base_test import BaseTestCase


class TestCaseProductCreate(BaseTestCase):
    """
    Тест кейс на создание продукта
    """
    url = '/products'
    product_data = {
        'name': 'some product',
        'description': 'some description',
        'price': 120.0,
        'quantity': 50
    }

    async def test_create_product(self):
        """Тест на создание продукта."""
        response = await self.make_post(self.url, self.product_data, status_code=status.HTTP_201_CREATED)
        assert response.get('name') == self.product_data.get('name')

    async def test_create_product_405(self):
        """Тест на создание продукта с выбором ошибочного метода (ошибка 405)."""
        await self.make_put(self.url, self.product_data, status_code=status.HTTP_405_METHOD_NOT_ALLOWED)

    async def test_create_product_422(self):
        """Тест на создание продукта с логической ошибкой в запросе (ошибка 422)."""
        await self.make_post(self.url, {}, status_code=status.HTTP_422_UNPROCESSABLE_ENTITY)
