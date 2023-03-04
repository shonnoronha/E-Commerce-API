from typing import List

from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException
from fastapi import Response
from fastapi import status
from sqlalchemy import text
from sqlalchemy.orm import Session

from app import database
from app import models
from app import oauth2
from app import schemas

router = APIRouter(prefix="/products", tags=["Products"])


@router.get("/test")
def test(
    db: Session = Depends(database.get_db),
    customer: schemas.CustomerOut = Depends(oauth2.get_current_customer),
):
    products = (
        db.query(
            models.Product.product_id,
            models.Product.name.label("product_name"),
            models.Product.description,
            models.Product.price,
            models.Category.name.label("category_name"),
            models.Category.category_id,
            models.Product.created_at,
        )
        .join(
            models.productCategory,
            models.Product.product_id == models.productCategory.product_id,
            isouter=True,
        )
        .join(
            models.Category,
            models.Category.category_id == models.productCategory.category_id,
            isouter=True,
        )
        .order_by(text("products.product_id"))
        .all()
    )
    return products


@router.get("", response_model=List[schemas.ProductOut])
def get_all_products(
    db: Session = Depends(database.get_db),
    customer: schemas.CustomerOut = Depends(oauth2.get_current_customer),
):
    products = (
        db.query(models.Product, models.Category)
        .join(
            models.productCategory,
            models.Product.product_id == models.productCategory.product_id,
            isouter=True,
        )
        .join(
            models.Category,
            models.Category.category_id == models.productCategory.category_id,
            isouter=True,
        )
        .all()
    )
    return products


@router.get("/{id}", response_model=schemas.ProductOut)
def get_single_product(
    id: int,
    db: Session = Depends(database.get_db),
    customer: schemas.CustomerOut = Depends(oauth2.get_current_customer),
):
    product = (
        db.query(models.Product, models.Category)
        .join(
            models.productCategory,
            models.Product.product_id == models.productCategory.product_id,
            isouter=True,
        )
        .join(
            models.Category,
            models.Category.category_id == models.productCategory.category_id,
            isouter=True,
        )
        .filter(models.Product.product_id == id)
        .first()
    )
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
