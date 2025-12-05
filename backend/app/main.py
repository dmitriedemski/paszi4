"""
Основной файл приложения FastAPI
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import logging
from loguru import logger
import sys
from app.config import settings
from app.routers import auth
from app.database import Base, engine

# Настраиваем логирование
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.StreamHandler(sys.stdout)
    ]
)

# Настраиваем loguru
logger.remove()
logger.add(
    sys.stdout,
    format="{time:YYYY-MM-DD HH:mm:ss} - {level} - {message}",
    level="INFO" if settings.app_env == "production" else "DEBUG"
)

# Создаем таблицы в базе данных (в продакшене используем миграции)
if settings.app_env == "development":
    Base.metadata.create_all(bind=engine)

# Создаем приложение FastAPI
app = FastAPI(
    title="User Registration API",
    description="API для регистрации пользователей с валидацией и хэшированием паролей",
    version="1.0.0",
    docs_url="/docs" if settings.debug else None,
    redoc_url="/redoc" if settings.debug else None
)

# Настраиваем CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Подключаем маршруты
app.include_router(auth.router)


@app.get("/")
async def root():
    """
    Корневой эндпоинт для проверки работоспособности API
    """
    return {
        "message": "User Registration API",
        "version": "1.0.0",
        "status": "running",
        "docs": "/docs" if settings.debug else None
    }


@app.get("/health")
async def health_check():
    """
    Эндпоинт для проверки здоровья приложения
    """
    return {
        "status": "healthy",
        "database": "connected" if engine else "disconnected"
    }


@app.get("/api/info")
async def api_info():
    """
    Информация о конфигурации API (безопасная версия)
    """
    return {
        "app_env": settings.app_env,
        "hash_scheme": settings.hash_scheme,
        "min_login_length": settings.min_login_length,
        "max_login_length": settings.max_login_length,
        "min_password_length": settings.min_password_length
    }


# Логирование при запуске приложения
@app.on_event("startup")
async def startup_event():
    logger.info("=" * 50)
    logger.info("Запуск приложения регистрации пользователей")
    logger.info(f"Режим: {settings.app_env}")
    logger.info(f"Хост: {settings.host}")
    logger.info(f"Порт: {settings.port}")
    logger.info(f"База данных: {settings.database_url[:30]}...")
    logger.info("=" * 50)


@app.on_event("shutdown")
async def shutdown_event():
    logger.info("Остановка приложения регистрации пользователей")
