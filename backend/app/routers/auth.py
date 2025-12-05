"""
Маршруты для аутентификации
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app import schemas, crud
from app.dependencies import get_database
from app.database import get_db
import logging

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api", tags=["authentication"])


@router.post(
    "/register",
    response_model=schemas.UserResponse,
    status_code=status.HTTP_200_OK,
    summary="Регистрация нового пользователя",
    description="""
    Регистрирует нового пользователя с указанным логином и паролем.
    
    Требования:
    - Логин: 3-32 символа, латинские буквы, цифры и символы ._-
    - Пароль: минимум 8 символов, должен содержать заглавную букву, строчную букву, цифру и специальный символ
    """
)
async def register_user(
    user: schemas.UserCreate,
    db: Session = Depends(get_db)
):
    """
    Регистрация пользователя
    
    Args:
        user: Данные пользователя для регистрации
        db: Сессия базы данных
    
    Returns:
        Успешный ответ или ошибка
    
    Raises:
        HTTPException: 409 - пользователь уже существует
        HTTPException: 422 - ошибка валидации
        HTTPException: 500 - внутренняя ошибка сервера
    """
    try:
        # Проверяем, существует ли уже пользователь с таким логином
        existing_user = crud.get_user_by_login(db, user.login)
        if existing_user:
            logger.warning(f"Попытка регистрации с существующим логином: {user.login}")
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Пользователь с таким логином уже существует"
            )
        
        # Создаем пользователя
        db_user = crud.create_user(db, user)
        
        # Логируем успешную регистрацию
        logger.info(f"Успешная регистрация пользователя: {user.login}")
        
        return schemas.UserResponse(login=db_user.login)
        
    except ValueError as e:
        # Логируем ошибку валидации
        logger.error(f"Ошибка валидации при регистрации: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=str(e)
        )
        
    except HTTPException:
        # Перебрасываем HTTP исключения
        raise
        
    except Exception as e:
        # Логируем внутреннюю ошибку
        logger.error(f"Внутренняя ошибка при регистрации: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Внутренняя ошибка сервера"
        )
