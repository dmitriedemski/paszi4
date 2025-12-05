"""
Тестовый пакет для приложения регистрации пользователей

Этот модуль содержит все тесты для проверки функциональности приложения,
включая тесты регистрации, безопасности и валидации данных.
"""

import sys
import os

# Добавляем путь к корневой директории проекта
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Импортируем основные модули для использования в тестах
from app.main import app
from app.database import Base, engine, SessionLocal
from app.models import User
from app.schemas import UserCreate, UserResponse
from app.crud import create_user, get_user_by_login
from app.security import hash_password, verify_password

# Конфигурация тестового окружения
TEST_DATABASE_URL = "sqlite:///./test.db"

__version__ = "1.0.0"
__author__ = "Test Team"
__description__ = "Тесты для системы регистрации пользователей"

__all__ = [
    'app',
    'Base',
    'engine',
    'SessionLocal',
    'User',
    'UserCreate',
    'UserResponse',
    'create_user',
    'get_user_by_login',
    'hash_password',
    'verify_password',
    'TEST_DATABASE_URL'
]

# Логирование при импорте тестового пакета
import logging
logger = logging.getLogger(__name__)
logger.info(f"Инициализация тестового пакета версии {__version__}")
logger.info(f"Описание: {__description__}")
