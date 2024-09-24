import json
from typing import Any

from httpx import AsyncClient, ASGITransport
from starlette import status

from src.main import app


class BaseTestCase:
    """
    Базовый класс для тестирования всего проекта
    """
    base_url = 'http://test/api'
    transport = ASGITransport(app=app)

    async def _make_request(
            self,
            method: str,
            url: str,
            data: object = None,
            status_code: int = status.HTTP_200_OK,
    ) -> dict | None:
        """
        Метод для генерации запроса.
        """
        async with AsyncClient(transport=self.transport, base_url=self.base_url, follow_redirects=True) as client:
            url = f'{self.base_url}{url}'

            request_data = None
            if data and method.lower() != 'get':
                request_data = json.dumps(data)

            response = await client.request(method, url, content=request_data, follow_redirects=True)
            assert response is not None
            assert response.status_code == status_code

            if method != 'DELETE' and response.status_code != status.HTTP_204_NO_CONTENT:
                return response.json()

    async def make_post(
            self,
            url: str,
            data: Any,
            status_code: int,
    ) -> dict:
        """
        Метод для создания post-запроса.
        """
        return await self._make_request('POST', url, data, status_code)

    async def make_get(
            self,
            url: str,
            params: dict = None,
            status_code: int = status.HTTP_200_OK,
    ) -> dict:
        """
        Метод для создания get-запроса.
        """
        return await self._make_request('GET', url, params, status_code)

    async def make_patch(
            self,
            url: str,
            data: dict,
            status_code: int = status.HTTP_200_OK,
    ) -> dict:
        """
        Метод для создания patch-запроса.
        """
        return await self._make_request('PATCH', url, data, status_code)

    async def make_put(
            self,
            url: str,
            data: dict,
            status_code: int = status.HTTP_200_OK,
    ) -> dict:
        """
        Метод для создания put-запроса.
        """
        return await self._make_request('PUT', url, data, status_code)

    async def make_delete(
            self,
            url: str,
            data: dict = None,
            status_code: int = status.HTTP_204_NO_CONTENT,
    ) -> None:
        """
        Метод для создания delete-запроса.
        """
        return await self._make_request('DELETE', url, data, status_code)

