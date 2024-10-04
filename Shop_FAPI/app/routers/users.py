from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from .. import crud, schemas, database
from ..DefaultResponse import DefaultResponse
import logging
from typing import List



# Определение роутера
router = APIRouter(
    prefix="/users",
    tags=["users"],
    responses={404: {"description": "Not found"}},
)

logger = logging.getLogger(__name__)

# Определение методов роутера
@router.post("/", response_model=DefaultResponse)
def create_user(user: schemas.UserCreate, db: Session = Depends(database.get_db)):
    try:
        created_user = crud.create_user(db=db, user=user)
        id = created_user.id
        name = created_user.username
        phone = created_user.phone
        address = created_user.address
        email = created_user.email
        return DefaultResponse(error=False, message="User created successfully", payload=[{"id": id, "name": name, "phone": phone, "address": address, "email": email}])
    except Exception as e:
        logger.error(f"Error creating user: {e}")
        return DefaultResponse(error=True, message="Internal Server Error", payload=None)

@router.get("/", response_model=DefaultResponse)
def read_users(
    skip: int = 0,
    limit: int = 10,
    city: str = Query(None, description="Filter by city"),
    db: Session = Depends(database.get_db)
):
    try:
        users_list = []
        users = crud.get_users(db=db, skip=skip, limit=limit, city=city)
        for user in users:
            id = user.id
            name = user.username
            phone = user.phone
            address = user.address
            email = user.email
            dict_user = {"id": id, "name": name, "phone": phone, "address": address, "email": email}
            users_list.append(dict_user)
        return DefaultResponse(error=False, message="Users retrieved successfully", payload=users_list)
    except Exception as e:
        logger.error(f"Error reading users: {e}")
        return DefaultResponse(error=True, message="Internal Server Error", payload=None)

@router.get("/{user_id}", response_model=DefaultResponse)
def read_user(user_id: int, db: Session = Depends(database.get_db)):
    try:
        db_user = crud.get_user(db, user_id=user_id)
        id = db_user.id
        name = db_user.username
        phone = db_user.phone
        address = db_user.address
        email = db_user.email
        return DefaultResponse(error=False, message="User retrieved successfully", payload=[{"id": id, "name": name, "phone": phone, "address": address, "email": email}])
        
    except Exception as e:
        logger.error(f"Error reading user: {e}")
        return DefaultResponse(error=True, message="Wrong user id", payload=None)

@router.put("/{user_id}", response_model=DefaultResponse)
def update_user(user_id: int, user: schemas.UserUpdate, db: Session = Depends(database.get_db)):
    try:
        db_user = crud.update_user(db, user_id=user_id, user=user)
        id = db_user.id
        name = db_user.username
        phone = db_user.phone
        address = db_user.address
        email = db_user.email
        return DefaultResponse(error=False, message="User updated successfully", payload=[{"id": id, "name": name, "phone": phone, "address": address, "email": email}])
    except Exception as e:
        logger.error(f"Error updating user: {e}")
        return DefaultResponse(error=True, message="Internal Server Error", payload=None)

@router.delete("/{user_id}", response_model=DefaultResponse)
def delete_user(user_id: int, db: Session = Depends(database.get_db)):
    try:
        db_user = crud.delete_user(db, user_id=user_id)
        return DefaultResponse(error=False, message="User deleted successfully", payload=[{"id": user_id}])
    except Exception as e:
        logger.error(f"Error deleting user: {e}")
        return DefaultResponse(error=True, message="Internal Server Error", payload=None)
