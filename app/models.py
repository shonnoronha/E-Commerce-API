from sqlalchemy import Column, Integer, Numeric, String, TIMESTAMP, text

from app.database import Base


class Product(Base):
    __tablename__ = "products"

    product_id = Column(Integer, primary_key=True, nullable=False)
    name = Column(String, nullable=False)
    price = Column(Numeric, nullable=False)
    description = Column(String, nullable=True)
    created_at = Column(
        TIMESTAMP(timezone=True), nullable=False, server_default=text("now()")
    )
