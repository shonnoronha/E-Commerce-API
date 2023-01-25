from pydantic import BaseModel

from datetime import datetime


class ProductOut(BaseModel):
    product_id: int
    name: str
    price: float
    description: str
    created_at: datetime

    class Config:
        orm_mode = True


class ProductIn(BaseModel):
    name: str
    price: float
    description: str
