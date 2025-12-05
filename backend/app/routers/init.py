"""
Пакет маршрутизаторов API

Этот модуль содержит все маршруты API для приложения регистрации пользователей.
Каждый роутер отвечает за определенную группу эндпоинтов.
"""

from .auth import router as auth_router

__all__ = [
    'auth_router'
]

__version__ = "1.0.0"
__author__ = "API Team"
__description__ = "Маршруты API для системы регистрации пользователей"

# Логирование при импорте пакета маршрутизаторов
import logging
logger = logging.getLogger(__name__)
logger.info("Инициализация пакета маршрутизаторов API")
