from fastapi import FastAPI

from app.routers import products, customers

app = FastAPI()

app.include_router(products.router)
app.include_router(customers.router)


@app.get("/")
def root():
    return "/"
