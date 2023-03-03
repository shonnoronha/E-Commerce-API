from typing import List

from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException
from fastapi import Response
from fastapi import status
from sqlalchemy.orm import Session

from app import database
from app import models
from app import oauth2
from app import schemas

router = APIRouter(tags=["Orders"], prefix="/orders")


@router.get("/", response_model=List[schemas.OrderOut])
def get_all_orders(
    db: Session = Depends(database.get_db),
    customer: schemas.CustomerOut = Depends(oauth2.get_current_customer),
):
    orders = db.query(models.Orders).all()
    return orders


@router.post("/", response_model=schemas.OrderOut)
def create_new_order(
    db: Session = Depends(database.get_db),
    customer: schemas.CustomerOut = Depends(oauth2.get_current_customer),
):
    check_order = (
        db.query(models.Orders)
        .filter(models.Orders.customer_id == customer.customer_id)
        .first()
    )
    if check_order and (check_order.is_completed == False):
        raise HTTPException(
            detail=f"incomplete order exists for customer {customer.customer_id}",
            status_code=status.HTTP_409_CONFLICT,
        )
    new_order = models.Orders(customer_id=customer.customer_id)
    db.add(new_order)
    db.commit()
    db.refresh(new_order)
    return new_order


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
