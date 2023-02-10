from fastapi import FastAPI

from app.routers import products, customers, auth

app = FastAPI()

app.include_router(products.router)
app.include_router(customers.router)
app.include_router(auth.router)


@app.get("/")
def root():
    return "/"
