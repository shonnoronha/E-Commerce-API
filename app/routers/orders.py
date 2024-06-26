from typing import List

from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException
from fastapi import Query
from fastapi import Response
from fastapi import status
from sqlalchemy.orm import Session

from app import database
from app import models
from app import oauth2
from app import schemas

router = APIRouter(tags=["Orders"], prefix="/orders")


@router.get("/my", response_model=List[schemas.OrderOut])
def get_all_orders(
    completed: bool = Query(default=None),
    db: Session = Depends(database.get_db),
    customer: schemas.CustomerOut = Depends(oauth2.get_current_customer),
):
    orders_query = db.query(models.Orders).filter(
        models.Orders.customer_id == customer.customer_id,
    )
    if completed is not None:
        orders = orders_query.filter(models.Orders.is_completed == completed).all()
    else:
        orders = orders_query.all()
    return orders


@router.get("/details/{order_id}")
def show_order_details(
    order_id: int,
    db: Session = Depends(database.get_db),
    customer: schemas.CustomerOut = Depends(oauth2.get_current_customer),
):
    order = db.query(models.Orders).filter(models.Orders.order_id == order_id).first()
    if not order:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"order {order_id} not found!"
        )

    if order.customer_id != customer.customer_id:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"customer {customer.customer_id} not authorized!",
        )

    order_items = (
        db.query(
            models.OrderItems.order_id,
            models.Product.product_id,
            models.Product.name.label("product_name"),
            models.OrderItems.quantity,
            models.OrderItems.order_item_id,
            models.Product.price,
            models.Product.description,
            models.Category.category_id,
            models.Category.name.label("category_name"),
        )
        .join(
            models.Product,
            models.Product.product_id == models.OrderItems.product_id,
            isouter=True,
        )
        .join(
            models.productCategory,
            models.productCategory.product_id == models.Product.product_id,
            isouter=True,
        )
        .join(
            models.Category,
            models.Category.category_id == models.productCategory.category_id,
            isouter=True,
        )
        .filter(models.OrderItems.order_id == order_id)
        .all()
    )

    return order_items


@router.post("/items/add/{product_id}", response_model=schemas.OrderItemOut)
def add_items_to_order(
    product_id: int,
    quantity: int = Query(default=1),
    customer: schemas.CustomerOut = Depends(oauth2.get_current_customer),
    db: Session = Depends(database.get_db),
):
    product_query = (
        db.query(models.Product).filter(models.Product.product_id == product_id).first()
    )

    if not product_query:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"product {product_id} not found",
        )

    if product_query.customer_id == customer.customer_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"customer {customer.customer_id} cannot buy their own product",
        )

    customer_order = (
        db.query(models.Orders)
        .filter(
            models.Orders.customer_id == customer.customer_id,
            models.Orders.is_completed == False,
        )
        .first()
    )
    if not customer_order:
        new_order = models.Orders(customer_id=customer.customer_id)
        db.add(new_order)
        db.commit()
        db.refresh(new_order)
        customer_order = new_order

    if product_query.quantity - quantity < 0:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"product {product_id} has only {product_query.quantity} unit(s) left!",
        )
    else:
        product_query.quantity -= quantity

    customer_order.total_cost += int(product_query.price * quantity)

    if product_id in [
        order_item.product_id for order_item in db.query(models.OrderItems).all()
    ]:
        order_item = (
            db.query(models.OrderItems)
            .filter(models.OrderItems.product_id == product_id)
            .first()
        )
        order_item.quantity += quantity
    else:
        order_item = models.OrderItems(
            order_id=customer_order.order_id, product_id=product_id, quantity=quantity
        )
        db.add(order_item)

    db.commit()

    return order_item


@router.post("/{order_id}/complete", response_model=schemas.OrderOut)
def mark_order_as_complete(
    order_id: int,
    customer: schemas.CustomerOut = Depends(oauth2.get_current_customer),
    db: Session = Depends(database.get_db),
):
    order = (
        db.query(models.Orders)
        .filter(models.Orders.order_id == order_id, models.Orders.is_completed == False)
        .first()
    )
    if not order:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No Incomplete order {order_id} found!",
        )
    if order.customer_id != customer.customer_id:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"customer {customer.customer_id} is not authorized to update order {order_id}",
        )
    order.is_completed = True
    db.commit()
    db.refresh(order)
    return order


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_an_order(
    id: int,
    db: Session = Depends(database.get_db),
    customer: schemas.CustomerOut = Depends(oauth2.get_current_customer),
):
    order_query = db.query(models.Orders).filter(models.Orders.order_id == id)
    if not order_query.first():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"order with id {id} does not exists!",
        )
    if order_query.first().customer_id != customer.customer_id:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"customer {customer.customer_id} is not authorized to delete order {id}",
        )
    order_query.delete(synchronize_session=False)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)
