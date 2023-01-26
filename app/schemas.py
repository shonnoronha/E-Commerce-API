from pydantic import BaseModel, EmailStr

from datetime import datetime


class ProductIn(BaseModel):
    name: str
    price: float
    description: str


class ProductOut(ProductIn):
    product_id: int
    created_at: datetime

    class Config:
        orm_mode = True


class CustomerIn(BaseModel):
    name: str
    email: EmailStr
    password: str
    address: str


class CustomerOut(CustomerIn):
    customer_id: int
    created_at: datetime

    class Config:
        orm_mode = True
