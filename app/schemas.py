from datetime import datetime
from typing import Optional

from pydantic import BaseModel
from pydantic import EmailStr


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


class OrderOut(BaseModel):
    order_id: int
    customer_id: int
    total_cost: int
    is_completed: bool
    order_date: datetime

    class Config:
        orm_mode = True
