from fastapi import FastAPI

from app.routers import auth
from app.routers import categories
from app.routers import customers
from app.routers import orders
from app.routers import product_category
from app.routers import products

app = FastAPI()

app.include_router(products.router)
app.include_router(customers.router)
app.include_router(auth.router)
app.include_router(categories.router)
app.include_router(product_category.router)
app.include_router(orders.router)


@app.get("/")
def root():
    return "/"
