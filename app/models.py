from sqlalchemy import Column, Integer, Numeric, String, TIMESTAMP, text, ForeignKey
from sqlalchemy.orm import relationship

from app.database import Base


class Product(Base):
    __tablename__ = "products"

    product_id = Column(Integer, primary_key=True, nullable=False)
    name = Column(String, nullable=False)
    price = Column(Numeric, nullable=False)
    description = Column(String, nullable=True)
    customer_id = Column(
        Integer,
        ForeignKey(
            "customers.customer_id", ondelete="CASCADE", name="fk_product_customer"
        ),
        nullable=False,
    )
    created_at = Column(
        TIMESTAMP(timezone=True), nullable=False, server_default=text("now()")
    )
    customer = relationship("Customer")


class Customer(Base):
    __tablename__ = "customers"

    customer_id = Column(Integer, primary_key=True, nullable=False)
    name = Column(String, nullable=False)
    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    address = Column(String, nullable=False)
    created_at = Column(
        TIMESTAMP(timezone=True), nullable=False, server_default=text("now()")
    )
