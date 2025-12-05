"""
Безопасность: хэширование паролей
"""
from passlib.context import CryptContext
from app.config import settings
import logging

logger = logging.getLogger(__name__)

# Создаем контекст для хэширования паролей
pwd_context = CryptContext(
    schemes=[settings.hash_scheme],
    argon2__time_cost=settings.argon2_time_cost,
    argon2__memory_cost=settings.argon2_memory_cost,
    argon2__parallelism=settings.argon2_parallelism,
    argon2__hash_len=settings.argon2_hash_length,
    argon2__salt_len=settings.argon2_salt_length,
    deprecated="auto"
)


def hash_password(password: str) -> str:
    """
    Хэширование пароля с использованием Argon2id
    
    Args:
        password: Пароль в открытом виде
    
    Returns:
        Хэшированный пароль
    
    Raises:
        ValueError: Если пароль пустой
    """
    if not password:
        raise ValueError("Пароль не может быть пустым")
    
    # Логируем факт хэширования (без самого пароля)
    logger.info("Хэширование пароля с использованием Argon2id")
    
    # Хэшируем пароль
    hashed_password = pwd_context.hash(password)
    
    logger.info(f"Пароль успешно хэширован. Длина хэша: {len(hashed_password)}")
    return hashed_password


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Проверка пароля
    
    Args:
        plain_password: Пароль в открытом виде
        hashed_password: Хэшированный пароль
    
    Returns:
        True если пароль верный, иначе False
    """
    try:
        result = pwd_context.verify(plain_password, hashed_password)
        logger.info(f"Проверка пароля: {'успешно' if result else 'неудачно'}")
        return result
    except Exception as e:
        logger.error(f"Ошибка при проверке пароля: {str(e)}")
        return False
