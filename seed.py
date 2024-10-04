# seed.py
from database import SessionLocal, engine, Base
from models import User, Product, Order

# Создание таблиц
Base.metadata.create_all(bind=engine)

# Создание сессии
db = SessionLocal()

# Добавление тестовых данных
users = [
    User(username="Anton Skorinin", phone="765-83873-3738", address="123 Main St", email="anton@example.com"),
    User(username="jane_smith", phone="987-654-3210", address="456 Elm St", email="jane@example.com")
]

products = [
    Product(name="Laptop", seller="TechStore", price=1000),
    Product(name="Smartphone", seller="PhoneShop", price=500)
]

orders = [
    Order(user_id=1, product_id=1, count=2),
    Order(user_id=2, product_id=2, count=1)
]

# Добавление данных в базу данных
db.add_all(users)
db.add_all(products)
db.add_all(orders)
db.commit()

# Закрытие сессии
db.close()
