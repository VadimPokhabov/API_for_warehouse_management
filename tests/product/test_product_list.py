from starlette import status

from tests.base.base_test import BaseTestCase
from tests.conftest import get_url_size


class TestCaseProductList(BaseTestCase):
    """Тест кейс на получение списка продуктов."""
    url = '/products/'

    async def test_get_product_list(self, product):
        """Тест на получение списка продуктов."""
        response = await self.make_get(self.url)
        assert len(response['items']) <= response['size']
        assert response['items'][0].get('id') is not None

    async def test_product_list_pagination(self, product):
        """Тест на получение списка продуктов с пагинацией."""
        size = 20
        url = get_url_size(self.url, size)
        response = await self.make_get(url)
        assert len(response['items']) <= size

        size, page = 2, 3
        url = get_url_size(self.url, size, page)
        response = await self.make_get(url)
        assert len(response['items']) <= size

    async def test_product_list_search(self, product, product2):
        """Тест на получение списка продуктов с поиском по полям."""
        url = f'{self.url}?search={product.name}'
        response = await self.make_get(url)
        assert response['items'][0].get('name') == f'{product.name}'

        url = f'{self.url}?id_search={product2.id}'
        response = await self.make_get(url)
        assert response['total'] == product2.id

    async def test_get_course_list_405(self):
        """Тест на получение списка продуктов с выбором ошибочного метода (ошибка 405)."""
        await self.make_delete(self.url, status_code=status.HTTP_405_METHOD_NOT_ALLOWED)

    async def test_get_course_list_422(self):
        """Тест на получение списка продуктов с логической ошибкой в запросе (ошибка 422)."""
        url = get_url_size(self.url, -20)
        await self.make_get(url, status_code=status.HTTP_422_UNPROCESSABLE_ENTITY)
