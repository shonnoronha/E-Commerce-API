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
from app import utils

router = APIRouter(prefix="/products", tags=["Products"])


@router.get("", response_model=List[schemas.ProductOut])
def get_all_products(
    db: Session = Depends(database.get_db),
    customer: schemas.CustomerOut = Depends(oauth2.get_current_customer),
):
    products = (
        db.query(
            models.Product.product_id,
            models.Product.name.label("product_name"),
            models.Product.description,
            models.Product.quantity,
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


@router.get("/{product_id}", response_model=schemas.ProductOut)
def get_single_product(
    product_id: int,
    db: Session = Depends(database.get_db),
    customer: schemas.CustomerOut = Depends(oauth2.get_current_customer),
):
    product = (
        db.query(
            models.Product.product_id,
            models.Product.name.label("product_name"),
            models.Product.description,
            models.Product.quantity,
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
        .filter(models.Product.product_id == product_id)
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
    if product.category_id:
        category = (
            db.query(models.Category)
            .filter(models.Category.category_id == product.category_id)
            .first()
        )
        if not category:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"category with id {product.category_id} not found",
            )

    new_product = models.Product(
        **product.dict(exclude={"category_id"}), customer_id=customer.customer_id
    )
    db.add(new_product)
    db.commit()
    db.refresh(new_product)

    res = utils.convert_to_dict(new_product)

    if product.category_id:
        db.add(
            models.productCategory(
                product_id=new_product.product_id, category_id=category.category_id
            )
        )
        db.commit()

        res.update(
            {"category_id": category.category_id, "category_name": category.name}
        )

    return res


@router.delete("/{product_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_product(
    product_id: int,
    db: Session = Depends(database.get_db),
    customer: schemas.CustomerOut = Depends(oauth2.get_current_customer),
):
    product_query = db.query(models.Product).filter(
        models.Product.product_id == product_id
    )

    if not product_query.first():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Product with id {product_id} does not exist",
        )

    if product_query.first().customer_id != customer.customer_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"You are forbidden from deleting post with id {product_id}",
        )

    product_query.delete(synchronize_session=False)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put("/{product_id}", response_model=schemas.ProductOut)
def update_product(
    product_id: int,
    product_in: schemas.ProductIn,
    db: Session = Depends(database.get_db),
    customer: schemas.CustomerOut = Depends(oauth2.get_current_customer),
):
    product_query = db.query(models.Product).filter(
        models.Product.product_id == product_id
    )

    product = product_query.first()

    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"product with id {product_id} not found",
        )

    if product.customer_id != customer.customer_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"customer {customer.customer_id} cannot update product {product_id}",
        )

    product_query.update(
        product_in.dict(exclude={"category_id"}),
        synchronize_session=False,
    )
    db.commit()
    db.refresh(product)

    res = utils.convert_to_dict(product)

    if product_in.category_id:
        category = (
            db.query(models.Category)
            .filter(models.Category.category_id == product_in.category_id)
            .first()
        )
        if not category:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"category with id {product_in.category_id} not found",
            )

        prod_cat = (
            db.query(models.productCategory)
            .filter(models.productCategory.product_id == product_id)
            .first()
        )

        if prod_cat:
            prod_cat.category_id = product_in.category_id
        else:
            db.add(
                models.productCategory(
                    product_id=product_id, category_id=category.category_id
                )
            )
        res.update(
            {"category_id": category.category_id, "category_name": category.name}
        )
        db.commit()

    return res
