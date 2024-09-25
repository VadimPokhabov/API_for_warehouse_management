from starlette import status

from tests.base.base_test import BaseTestCase


class TestCaseProductTypeCreate(BaseTestCase):
    url = '/order'
    order_data = {
        "quantity_in_order": 1
    }

    async def test_create_order(self, product):
        """Create order"""
        data = self.order_data.copy() | {'product_id': product.id} | {'product': product.name}
        response = await self.make_post(url=self.url, data=data, status_code=status.HTTP_201_CREATED)
        assert response.get('id') == self.order_data.get('product_id')

    async def test_create_order_405(self):
        """order creation test with wrong method selection (Error 405)"""
        await self.make_put(self.url, self.order_data, status_code=status.HTTP_405_METHOD_NOT_ALLOWED)

    async def test_create_order_422(self):
        """order creation test with missing field (Error 422)"""
        await self.make_post(self.url, {}, status_code=status.HTTP_422_UNPROCESSABLE_ENTITY)
