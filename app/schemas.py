from pydantic import BaseModel, EmailStr
from typing import Optional

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


class ProductField(BaseModel):
    product_id: int
    name: str
    price: float
    description: str
    created_at: datetime

    class Config:
        orm_mode = True


class CategoryIn(BaseModel):
    name: str
    parent_category_id: int


class CategoryOut(BaseModel):
    name: str
    category_id: int
    parent_category_id: Optional[int]

    class Config:
        orm_mode = True


class ProductCategoryIn(BaseModel):
    product_id: int
    category_id: int


class CategoryField(CategoryOut):
    class Config:
        fields = {"parent_category_id": {"exclude": True}}


class ProductOut(BaseModel):
    Product: ProductField
    Category: Optional[CategoryField]

    class Config:
        orm_mode = True


class TokenOut(BaseModel):
    access_token: str
    token_type: str
