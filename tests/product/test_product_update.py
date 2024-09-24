from starlette import status

from tests.base.base_test import BaseTestCase
from tests.conftest import get_random_value


class TestCaseProductUpdate(BaseTestCase):
    """Тест кейс на обновление продукта."""
    url = '/products'
    new_product_data = {
        "id": 1,
        'name': 'product',
        'description': 'description',
        'price': 120.0,
        'quantity': 50
    }

    async def test_update_product(self, product):
        """Тест на обновление продукта."""
        url = f'{self.url}/{product.id}/'
        response = await self.make_put(url, self.new_product_data, status_code=status.HTTP_200_OK)
        assert response.get('name') == self.new_product_data.get('name')

    async def test_update_product_404(self):
        """Тест на обновление продукта с несуществующим id (ошибка 404)."""
        product_id = get_random_value()
        url = f'{self.url}/{product_id}/'
        await self.make_put(url, self.new_product_data, status_code=status.HTTP_404_NOT_FOUND)

    async def test_update_product_405(self, product):
        """Тест на обновление продукта с выбором ошибочного метода (ошибка 405)."""
        url = f'{self.url}/{product.id}/'
        await self.make_post(url, self.new_product_data, status_code=status.HTTP_405_METHOD_NOT_ALLOWED)

    async def test_update_product_422(self, product):
        """Тест на обновление продукта с логической ошибкой в запросе (ошибка 422)."""
        url = f'{self.url}/{product.id}/'
        await self.make_put(url, {}, status_code=status.HTTP_422_UNPROCESSABLE_ENTITY)
