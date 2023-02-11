from pydantic import BaseModel, EmailStr

from datetime import datetime


class CustomerIn(BaseModel):
    name: str
    email: EmailStr
    password: str
    address: str


class CustomerOut(BaseModel):
    customer_id: int
    name: str
    email: EmailStr
    address: str
    # created_at: datetime

    class Config:
        orm_mode = True


class ProductIn(BaseModel):
    name: str
    price: float
    description: str


class ProductOut(ProductIn):
    product_id: int
    created_at: datetime
    # customer: CustomerOut

    class Config:
        orm_mode = True


class TokenOut(BaseModel):
    access_token: str
    token_type: str
