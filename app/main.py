from fastapi import FastAPI

from app.routers import products, customers, auth, categories, product_category

app = FastAPI()

app.include_router(products.router)
app.include_router(customers.router)
app.include_router(auth.router)
app.include_router(categories.router)
app.include_router(product_category.router)


@app.get("/")
def root():
    return "/"
