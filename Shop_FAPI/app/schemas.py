from pydantic import BaseModel
from typing import List, Optional



#Определение базового класса для пользователей
class UserBase(BaseModel):
    username: str
    phone: str
    address: str
    email: str

#Определение класса для создания пользователя
class UserCreate(UserBase):
    pass

#Определение класса для обновления пользователя
class UserUpdate(BaseModel):
    email: Optional[str] = None
    phone: Optional[str] = None
    address: Optional[str] = None

#Определение класса для пользователя
class User(UserBase):
    id: int

    class Config:
        from_attributes = True

#Определение базового класса для товара
class ProductBase(BaseModel):
    name: str
    seller: str
    price: float

#Определение класса для создания товара
class ProductCreate(ProductBase):
    pass

#Определение класса для обновления товара
class ProductUpdate(BaseModel):
    price: Optional[float] = None

#Определение класса для товара
class Product(ProductBase):
    id: int

    class Config:
        from_attributes = True

#Определение базового класса для заказа
class OrderBase(BaseModel):
    user_id: int
    product_id: int
    count: int

#Определение класса для создания заказа
class OrderCreate(OrderBase):
    pass

#Определение класса для обновления заказа
class OrderUpdate(BaseModel):
    count: Optional[int] = None

# Определение класса для заказа
class Order(OrderBase):
    class Config:
        from_attributes = True
