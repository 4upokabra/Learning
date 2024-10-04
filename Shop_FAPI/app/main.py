#Импорт нужных библеотек и зависимостей
import logging
import uvicorn
from fastapi import FastAPI
from .database import engine, Base
from .routers import users, products, orders

# Настройка логгера для записи в файл
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("app.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

Base.metadata.create_all(bind=engine)

app = FastAPI()

#Включение роутеров
app.include_router(users.router)
app.include_router(products.router)
app.include_router(orders.router)


#Определение корневого сервиса
@app.get("/")
def read_root():
    logger.info("Root endpoint accessed")
    return {"message": "Welcome to the Internet Shop API"}

