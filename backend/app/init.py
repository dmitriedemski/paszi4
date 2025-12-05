"""
Пакет приложения регистрации пользователей

Этот модуль инициализирует основное приложение FastAPI и настраивает все компоненты.
"""

from .main import app
from .config import settings
from .database import Base, engine, SessionLocal
from . import models, schemas, crud, security, dependencies

__version__ = "1.0.0"
__author__ = "Registration System Team"
__description__ = "Система регистрации пользователей с использованием FastAPI, React и PostgreSQL"

__all__ = [
    'app',
    'settings',
    'Base',
    'engine',
    'SessionLocal',
    'models',
    'schemas',
    'crud',
    'security',
    'dependencies'
]

# Логирование при инициализации пакета
import logging
logger = logging.getLogger(__name__)
logger.info(f"Инициализация пакета регистрации пользователей версии {__version__}")
logger.info(f"Режим работы: {settings.app_env}")
logger.info(f"Используемая схема хэширования: {settings.hash_scheme}")

# Проверка конфигурации безопасности
if settings.app_env == "production":
    if settings.secret_key == "your-secret-key-change-in-production":
        logger.warning("ВНИМАНИЕ: Используется стандартный SECRET_KEY! Замените его в production!")
    if settings.debug:
        logger.warning("ВНИМАНИЕ: DEBUG режим включен в production окружении!")
