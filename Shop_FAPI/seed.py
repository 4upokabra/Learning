from sqlalchemy.orm import Session
from app import models, database

#Функция для добавления пользователей, продуктов и зависимостей в базу данных
#Для добавления orders нужно использовать уже сущесвующих юзеров и продукты либо знать с каким id будут новый юзер и продукт
def seed_data(db: Session):
    # Users
    db.add_all([
        models.User(username="user10", phone="1234567890", address="Address 10", email="user10@example.com"),
        models.User(username="user11", phone="0987654321", address="Address 11", email="user11@example.com"),
    ])

    # Products
    db.add_all([
        models.Product(name="Product 10", seller="Seller 10", price=10.0),
        models.Product(name="Product 11", seller="Seller 11", price=11.0),
    ])

    # Orders
    db.add_all([

        models.Order(user_id=5, product_id=1, count=100),
    ])

    db.commit()

if __name__ == "__main__":
    db = database.SessionLocal()
    seed_data(db)
    db.close()
