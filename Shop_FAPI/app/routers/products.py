from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from .. import crud, schemas, database
from ..DefaultResponse import DefaultResponse
import logging
from typing import List

# Определение роутера
router = APIRouter(
    prefix="/products",
    tags=["products"],
    responses={404: {"description": "Not found"}},
)

logger = logging.getLogger(__name__)

# Определение методов роутера
@router.post("/", response_model=DefaultResponse)
def create_product(product: schemas.ProductCreate, db: Session = Depends(database.get_db)):
    try:
        created_product = crud.create_product(db=db, product=product)
        id = created_product.id
        name = created_product.name
        seller = created_product.seller
        price = created_product.price
        return DefaultResponse(error=False, message="Product created successfully", payload=[{"id": id, "name": name, "seller": seller, "price": price}])
    except Exception as e:
        logger.error(f"Error creating product: {e}")
        return DefaultResponse(error=True, message="Internal Server Error", payload=None)

@router.get("/", response_model=DefaultResponse)
def read_products(

    skip: int = 0,
    limit: int = 10,
    seller: str = Query(None, description="Filter by seller"),
    db: Session = Depends(database.get_db)
):
    try:
        products_list= []
        products = crud.get_products(db=db, skip=skip, limit=limit, seller=seller)
        for product in products:
            id = product.id
            name = product.name
            seller = product.seller
            price = product.price
            dict_product = {"id": id, "name": name, "seller": seller, "price": price}
            products_list.append(dict_product)
        return DefaultResponse(error=False, message="Products retrieved successfully", payload=products_list)

    except Exception as e:
        logger.error(f"Error reading products: {e}")
        return DefaultResponse(error=True, message="Internal Server Error", payload=None)

@router.get("/{product_id}", response_model=DefaultResponse)
def read_product(product_id: int, db: Session = Depends(database.get_db)):
    try:
        db_product = crud.get_product(db, product_id=product_id)
        id = db_product.id
        name = db_product.name
        seller = db_product.seller
        price = db_product.price
        return DefaultResponse(error=False, message="Product retrieved successfully", payload=[{"id": id, "name": name, "seller": seller, "price": price}])

    except Exception as e:
        logger.error(f"Error reading product: {e}")
        return DefaultResponse(error=True, message="Internal Server Error", payload=None)

@router.put("/{product_id}", response_model=DefaultResponse)
def update_product(product_id: int, product: schemas.ProductUpdate, db: Session = Depends(database.get_db)):
    try:
        db_product = crud.update_product(db, product_id=product_id, product=product)
        id = db_product.id
        name = db_product.name
        seller = db_product.seller
        price = db_product.price
        return DefaultResponse(error=False, message="Product updated successfully", payload=[{"id": id, "name": name, "seller": seller, "price": price}])
    except Exception as e:
        logger.error(f"Error updating product: {e}")
        return DefaultResponse(error=True, message="Internal Server Error", payload=None)

@router.delete("/{product_id}", response_model=DefaultResponse)
def delete_product(product_id: int, db: Session = Depends(database.get_db)):
    try:
        db_product = crud.delete_product(db, product_id=product_id)
        return DefaultResponse(error=False, message="User deleted successfully", payload=[{"id": product_id}])
    except Exception as e:
        logger.error(f"Error deleting user: {e}")
        return DefaultResponse(error=True, message="Internal Server Error", payload=None)
