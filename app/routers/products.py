from fastapi import APIRouter, Depends, HTTPException, status, Response
from sqlalchemy.orm import Session
from typing import List

from app import schemas, models, database, oauth2

router = APIRouter(prefix="/products", tags=["Products"])


@router.get("", response_model=List[schemas.ProductOut])
def get_all_products(
    db: Session = Depends(database.get_db),
    customer: schemas.CustomerOut = Depends(oauth2.get_current_customer),
):
    products = db.query(models.Product).all()
    return products


@router.get("/{id}", response_model=schemas.ProductOut)
def get_single_product(
    id: int,
    db: Session = Depends(database.get_db),
    customer: schemas.CustomerOut = Depends(oauth2.get_current_customer),
):
    product = db.query(models.Product).filter(models.Product.product_id == id).first()
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"product with id {id} not found",
        )
    return product


@router.post("", response_model=schemas.ProductOut)
def create_product(
    product: schemas.ProductIn,
    db: Session = Depends(database.get_db),
    customer: schemas.CustomerOut = Depends(oauth2.get_current_customer),
):
    new_product = models.Product(**product.dict(), customer_id=customer.customer_id)
    db.add(new_product)
    db.commit()
    db.refresh(new_product)
    return new_product


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_product(
    id: int,
    db: Session = Depends(database.get_db),
    customer: schemas.CustomerOut = Depends(oauth2.get_current_customer),
):
    product_query = db.query(models.Product).filter(models.Product.product_id == id)

    if not product_query.first():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Product with id {id} does not exist",
        )

    if product_query.first().customer_id != customer.customer_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"You are forbidden from deleting post with id {id}",
        )

    product_query.delete(synchronize_session=False)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put("/{id}", response_model=schemas.ProductOut)
def update_product(
    id: int,
    product: schemas.ProductIn,
    db: Session = Depends(database.get_db),
    customer: schemas.CustomerOut = Depends(oauth2.get_current_customer),
):
    product_query = db.query(models.Product).filter(models.Product.product_id == id)

    if not product_query.first():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Product with id {id} does not exist",
        )

    if product_query.first().customer_id != customer.customer_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"You are forbidden from updating post with id {id}",
        )

    product_query.update(product.dict(), synchronize_session=False)
    db.commit()
    db.refresh(product_query.first())
    return product_query.first()
