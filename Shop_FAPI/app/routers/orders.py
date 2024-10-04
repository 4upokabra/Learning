from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from .. import crud, schemas, database
from ..DefaultResponse import DefaultResponse
import logging
from typing import List

# Определение роутера
router = APIRouter(
    prefix="/orders",
    tags=["orders"],
    responses={404: {"description": "Not found"}},
)

logger = logging.getLogger(__name__)

# Определение методов роутера
@router.post("/", response_model=DefaultResponse)
def create_order(order: schemas.OrderCreate, db: Session = Depends(database.get_db)):
    try:
        created_order = crud.create_order(db=db, order=order)
        user_id = created_order.user_id
        product_id = created_order.product_id
        quantity = created_order.count
        return DefaultResponse(error=False, message="Order created successfully", payload=[{"user_id": user_id, "product_id": product_id, "quantity": quantity}])
    except Exception as e:
        logger.error(f"Error creating order: {e}")
        return DefaultResponse(error=True, message="Internal Server Error", payload=None)

@router.get("/", response_model=DefaultResponse)
def read_orders(
    skip: int = 0,
    limit: int = 10,
    user_id: int = Query(None, description="Filter by user ID"),
    db: Session = Depends(database.get_db)
):
    try:
        orders_list = []
        orders = crud.get_orders(db=db, skip=skip, limit=limit, user_id=user_id)
        for order in orders:
            user_id = order.user_id
            product_id = order.product_id
            quantity = order.count
            dict_order = {"user_id": user_id, "product_id": product_id, "quantity": quantity}
            orders_list.append(dict_order)
        return DefaultResponse(error=False, message="Orders retrieved successfully", payload=orders_list)
    except Exception as e:
        logger.error(f"Error reading orders: {e}")
        return DefaultResponse(error=True, message="Internal Server Error", payload=None)

@router.get("/{user_id}/{product_id}", response_model=DefaultResponse)
def read_order(user_id: int, product_id: int, db: Session = Depends(database.get_db)):
    try:
        db_order = crud.get_order(db, user_id=user_id, product_id=product_id)
        
        user_id = db_order.user_id
        product_id = db_order.product_id
        quantity = db_order.count
        return DefaultResponse(error=False, message="Order retrieved successfully", payload=[{"user_id": user_id, "product_id": product_id, "quantity": quantity}])
    except Exception as e:
        logger.error(f"Error reading order: {e}")
        return DefaultResponse(error=True, message="Internal Server Error", payload=None)

@router.put("/{user_id}/{product_id}", response_model=DefaultResponse)
def update_order(user_id: int, product_id: int, order: schemas.OrderUpdate, db: Session = Depends(database.get_db)):
    try:
        db_order = crud.update_order(db, user_id=user_id, product_id=product_id, order=order)
        user_id = db_order.user_id
        product_id = db_order.product_id
        quantity = db_order.count
        return DefaultResponse(error=False, message="Order updated successfully", payload=[{"user_id": user_id, "product_id": product_id, "quantity": quantity}])

    except Exception as e:
        logger.error(f"Error updating order: {e}")
        return DefaultResponse(error=True, message="Internal Server Error", payload=None)

@router.delete("/{user_id}/{product_id}", response_model=DefaultResponse)
def delete_order(user_id: int, product_id: int, db: Session = Depends(database.get_db)):
    try:
        db_order = crud.delete_order(db, user_id=user_id, product_id=product_id)
        return DefaultResponse(error=False, message="Order deleted successfully", payload=[{"product_id": product_id}, {"user_id": user_id}])
    except Exception as e:
        logger.error(f"Error deleting order: {e}")
        return DefaultResponse(error=True, message="Internal Server Error", payload=None)
