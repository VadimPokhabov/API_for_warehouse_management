from typing import Annotated
from fastapi import APIRouter, Depends, Query, HTTPException
from fastapi_pagination.ext.sqlalchemy import paginate
from sqlalchemy import Select
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status
from src.base.paginate_config import PaginatePage
from src.base.responses import ResponseSchema
from src.config.session import get_async_session
from src.product.schemas import CreateProductSchema, ProductListSchema, ProductDetailSchema, ProductUpdateSchema
from src.product.session import ProductSession

product_router = APIRouter()
responses = ResponseSchema()


@product_router.post(
    "/",
    response_model=CreateProductSchema,
    responses=responses(CreateProductSchema, status.HTTP_201_CREATED, [status.HTTP_409_CONFLICT]),
    status_code=status.HTTP_201_CREATED,
    description="Product create",
)
async def create_product(
        product_data: CreateProductSchema,
        session: AsyncSession = Depends(get_async_session),
) -> CreateProductSchema:
    """
    Create product
    :param product_data:
    :param session:
    :return: product_data
    """
    return await ProductSession(session).create_product(product_data)


@product_router.get(
    "/",
    response_model=PaginatePage[ProductListSchema],
    responses=responses(PaginatePage[ProductListSchema]),
    description='Product list'
)
async def product_list(
        search: Annotated[str | None, Query(description="Search field")] = None,
        search_id: Annotated[int | None, Query(description="Search id field")] = None,
        session: AsyncSession = Depends(get_async_session)
) -> PaginatePage[ProductListSchema]:
    """
    Product list
    :param search_id:
    :param search:
    :param session:
    :return:
    """
    products: Select = await ProductSession(session).list_product(search, search_id)
    return await paginate(session, products)


@product_router.get(
    '/{product_id}/',
    response_model=ProductDetailSchema,
    responses=responses(ProductDetailSchema, statuses=[status.HTTP_404_NOT_FOUND]),
    description='Product detail',
)
async def product_detail(
        product_id: int,
        session: AsyncSession = Depends(get_async_session),
) -> ProductDetailSchema:
    """Product detail."""
    product = await ProductSession(session).get_product_by_id(product_id)
    if product:
        return product
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Product not found')


@product_router.put(
    '/{product_id}/',
    response_model=ProductUpdateSchema,
    responses=responses(ProductUpdateSchema, statuses=[status.HTTP_409_CONFLICT, status.HTTP_404_NOT_FOUND]),
    description='Product update'
)
async def product_update(
        product_id: int,
        product_data: ProductUpdateSchema,
        session: AsyncSession = Depends(get_async_session),
) -> ProductUpdateSchema:
    """Product update"""
    new_product = product_data.model_dump(exclude_unset=True)
    product = await ProductSession(session).update_product_by_id(product_id, **new_product)
    if product:
        return product
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Product not found')


@product_router.delete(
    '/{product_id}/',
    responses=responses(response_status=status.HTTP_204_NO_CONTENT, statuses=[status.HTTP_404_NOT_FOUND]),
    description='Product delete',
    status_code=status.HTTP_204_NO_CONTENT
)
async def product_delete(
        product_id: int,
        session: AsyncSession = Depends(get_async_session),
) -> None:
    """Product delete"""
    result = await ProductSession(session).delete_product_by_id(product_id)
    if result is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Product not found')
