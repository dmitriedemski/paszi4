"""
Операции с базой данных (CRUD)
"""
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from app import models, schemas, security
import logging

logger = logging.getLogger(__name__)


def create_user(db: Session, user: schemas.UserCreate) -> models.User:
    """
    Создание нового пользователя
    
    Args:
        db: Сессия базы данных
        user: Данные пользователя
    
    Returns:
        Созданный пользователь
    
    Raises:
        IntegrityError: Если пользователь с таким логином уже существует
    """
    # Хэшируем пароль
    hashed_password = security.hash_password(user.password)
    
    # Создаем объект пользователя
    db_user = models.User(
        login=user.login,
        password_hash=hashed_password
    )
    
    try:
        # Добавляем в базу данных
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        
        # Логируем успешную регистрацию (без пароля)
        logger.info(f"Пользователь успешно создан: {user.login}")
        
        return db_user
        
    except IntegrityError as e:
        # Откатываем транзакцию
        db.rollback()
        
        # Логируем ошибку дублирования
        logger.error(f"Ошибка при создании пользователя {user.login}: {str(e)}")
        
        # Проверяем, является ли ошибка дублированием логина
        if "unique constraint" in str(e).lower() or "duplicate key" in str(e).lower():
            raise ValueError(f"Пользователь с логином '{user.login}' уже существует")
        
        raise e
    
    except Exception as e:
        # Откатываем транзакцию при любой другой ошибке
        db.rollback()
        logger.error(f"Неизвестная ошибка при создании пользователя: {str(e)}")
        raise e


def get_user_by_login(db: Session, login: str) -> models.User | None:
    """
    Поиск пользователя по логину
    
    Args:
        db: Сессия базы данных (Session, а не generator)
        login: Логин пользователя
    
    Returns:
        Пользователь или None если не найден
    """
    # Убедитесь, что db - это Session, а не generator
    from sqlalchemy.orm import Session as SessionType
    if not isinstance(db, SessionType):
        raise TypeError(f"Expected Session, got {type(db)}")
    
    return db.query(models.User).filter(models.User.login == login).first()