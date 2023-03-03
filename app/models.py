from sqlalchemy import (
    Column,
    Integer,
    Numeric,
    String,
    TIMESTAMP,
    text,
    ForeignKey,
    Boolean,
)
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


class Category(Base):
    __tablename__ = "categories"

    category_id = Column(Integer, primary_key=True, nullable=False)
    name = Column(String, nullable=False)
    parent_category_id = Column(
        Integer,
        ForeignKey(
            "categories.category_id", ondelete="CASCADE", name="fk_category_category"
        ),
    )


class productCategory(Base):
    __tablename__ = "product_category"

    product_id = Column(
        Integer,
        ForeignKey(
            "products.product_id", ondelete="CASCADE", name="fk_product_category"
        ),
        primary_key=True,
    )
    category_id = Column(
        Integer,
        ForeignKey(
            "categories.category_id", name="fk_category_product", ondelete="CASCADE"
        ),
        primary_key=True,
    )


class Orders(Base):
    __tablename__ = "orders"

    order_id = Column(Integer, primary_key=True, nullable=False)
    customer_id = Column(
        Integer,
        ForeignKey(
            "customers.customer_id", name="fk_orders_customer", ondelete="CASCADE"
        ),
    )
    total_cost = Column(Integer, nullable=False, server_default=text("0"))
    is_completed = Column(Boolean, default=False, nullable=False)
    order_date = Column(
        TIMESTAMP(timezone=True), nullable=False, server_default=text("now()")
    )


# class OrderItems(Base):
#     __tablename__ = "order_items"

#     order_item_id = Column(Integer, primary_key=True, nullable=False)
#     order_id = Column(
#         Integer,
#         ForeignKey("orders.order_id", name="fk_order_items_order", ondelete="CASCADE"),
#     )
#     product_id = Column(
#         Integer,
#         ForeignKey(
#             "products.product_id", name="fk_order_items_product", ondelete="CASCADE"
#         ),
#     )
#     quantity = Column(Integer, default=text("1"))
