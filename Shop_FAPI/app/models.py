from sqlalchemy import Column, Integer, String, ForeignKey, Float, Table
from sqlalchemy.orm import relationship, backref
from .database import Base

#Определение модели для работы с пользователями
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, index=True)
    phone = Column(String)
    address = Column(String)
    email = Column(String, unique=True, index=True)

    orders = relationship("Order", back_populates="user", cascade="all, delete-orphan")

#Определение модели для работы с товарами
class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    seller = Column(String)
    price = Column(Float)

    orders = relationship("Order", back_populates="product", cascade="all, delete-orphan")

#Определение модели для работы с заказами
class Order(Base):
    __tablename__ = "orders"

    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), primary_key=True)
    product_id = Column(Integer, ForeignKey("products.id", ondelete="CASCADE"), primary_key=True)
    count = Column(Integer)

    user = relationship("User", back_populates="orders")
    product = relationship("Product", back_populates="orders")
