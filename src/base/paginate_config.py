from typing import TypeVar

from fastapi import Query
from fastapi_pagination import Page, Params
from fastapi_pagination.customization import CustomizedPage, UseParams

T = TypeVar('T')


class PageParam(Params):
    """Pagination options."""
    page: int = Query(1, ge=1, description="Page number")
    size: int = Query(10, ge=1,  description="Page size")


PaginatePage = CustomizedPage[
    Page[T],
    UseParams(PageParam)
]
