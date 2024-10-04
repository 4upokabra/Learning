from sqlalchemy.orm import Session
from . import models, schemas

#Определение функций для работы с пользователями
def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()

def get_users(db: Session, skip: int = 0, limit: int = 10, city: str = None):
    query = db.query(models.User).offset(skip).limit(limit)
    if city:
        query = query.filter(models.User.address.like(f"%{city}%"))
    return query.all()

def create_user(db: Session, user: schemas.UserCreate):
    db_user = models.User(**user.dict())
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def update_user(db: Session, user_id: int, user: schemas.UserUpdate):
    db_user = db.query(models.User).filter(models.User.id == user_id).first()
    if db_user:
        for key, value in user.dict(exclude_unset=True).items():
            setattr(db_user, key, value)
        db.commit()
        db.refresh(db_user)
    return db_user

def delete_user(db: Session, user_id: int):
    db_user = db.query(models.User).filter(models.User.id == user_id).first()
    if db_user:
        db.delete(db_user)
        db.commit()
    return db_user

#Определение функций для работы с товарами
def get_product(db: Session, product_id: int):
    return db.query(models.Product).filter(models.Product.id == product_id).first()

def get_products(db: Session, skip: int = 0, limit: int = 10, seller: str = None):
    query = db.query(models.Product).offset(skip).limit(limit)
    if seller:
        query = query.filter(models.Product.seller == seller)
    return query.all()

def create_product(db: Session, product: schemas.ProductCreate):
    db_product = models.Product(**product.dict())
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product

def update_product(db: Session, product_id: int, product: schemas.ProductUpdate):
    db_product = db.query(models.Product).filter(models.Product.id == product_id).first()
    if db_product:
        for key, value in product.dict(exclude_unset=True).items():
            setattr(db_product, key, value)
        db.commit()
        db.refresh(db_product)
    return db_product

def delete_product(db: Session, product_id: int):
    db_product = db.query(models.Product).filter(models.Product.id == product_id).first()
    if db_product:
        db.delete(db_product)
        db.commit()
    return db_product

#Определение функций для работы с заказами
def get_order(db: Session, user_id: int, product_id: int):
    return db.query(models.Order).filter(models.Order.user_id == user_id, models.Order.product_id == product_id).first()

def get_orders(db: Session, skip: int = 0, limit: int = 10, user_id: int = None):
    query = db.query(models.Order).offset(skip).limit(limit)
    if user_id:
        query = query.filter(models.Order.user_id == user_id)
    return query.all()

def create_order(db: Session, order: schemas.OrderCreate):
    db_order = models.Order(**order.dict())
    db.add(db_order)
    db.commit()
    db.refresh(db_order)
    return db_order

def update_order(db: Session, user_id: int, product_id: int, order: schemas.OrderUpdate):
    db_order = db.query(models.Order).filter(models.Order.user_id == user_id, models.Order.product_id == product_id).first()
    if db_order:
        for key, value in order.dict(exclude_unset=True).items():
            setattr(db_order, key, value)
        db.commit()
        db.refresh(db_order)
    return db_order

def delete_order(db: Session, user_id: int, product_id: int):
    db_order = db.query(models.Order).filter(models.Order.user_id == user_id, models.Order.product_id == product_id).first()
    if db_order:
        db.delete(db_order)
        db.commit()
    return db_order
