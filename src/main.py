import uvicorn
from fastapi import FastAPI
from fastapi_pagination import add_pagination

from src.config.settings import config
from src.order.routers import order_router
from src.product.routers import product_router

app = FastAPI(title='Products Type', debug=config.app.DEBUG, docs_url='/api/docs/', redoc_url='/api/redoc')

app.include_router(product_router, prefix='/api/products', tags=['Products'])
app.include_router(order_router, prefix='/api/order', tags=['Order'])

add_pagination(app)


if __name__ == '__main__':
    uvicorn.run('main:app', host='127.0.0.1', port=8000, reload=True)
