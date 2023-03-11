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
    quantity: Optional[int] = 1
    category_id: Optional[int] = None


class ProductOut(BaseModel):
    product_id: int
    product_name: str
    description: str
    quantity: int
    price: float
    category_id: Optional[int] = None
    category_name: Optional[str] = None
    created_at: datetime

    class Config:
        orm_mode = True


class CategoryIn(BaseModel):
    name: str
    parent_category_id: Optional[int] = None


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


class OrderItemOut(BaseModel):
    order_item_id: int
    order_id: int
    product_id: int
    quantity: int

    class Config:
        orm_mode = True
