from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException
from fastapi import status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app import database
from app import models
from app import oauth2
from app import schemas


router = APIRouter(prefix="/product_category", tags=["Product-Category"])


@router.post("", status_code=status.HTTP_201_CREATED)
def add_product_category(
    product_category: schemas.ProductCategoryIn,
    db: Session = Depends(database.get_db),
    customer: schemas.CustomerOut = Depends(oauth2.get_current_customer),
):
    product = (
        db.query(models.Product)
        .filter(models.Product.product_id == product_category.product_id)
        .first()
    )
    if not product:
        raise HTTPException(
            detail=f"product with id {product_category.product_id} not found!",
            status_code=status.HTTP_404_NOT_FOUND,
        )

    category = (
        db.query(models.Category)
        .filter(models.Category.category_id == product_category.category_id)
        .first()
    )

    if not category:
        raise HTTPException(
            detail=f"category with id {product_category.category_id} not found!",
            status_code=status.HTTP_404_NOT_FOUND,
        )

    if product.customer_id != customer.customer_id:
        raise HTTPException(
            detail=f"user with id {customer.customer_id} cannot add category to product with id {product_category.product_id}",
            status_code=status.HTTP_409_CONFLICT,
        )

    try:
        db.add(
            models.productCategory(
                product_id=product_category.product_id,
                category_id=product_category.category_id,
            )
        )
        db.commit()
        return {"message": "category successfully added to product"}
    except IntegrityError:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"product {product_category.product_id} with category {product_category.category_id} already exists",  # FIXME: changed constraint from composite primary key to unique
        )
