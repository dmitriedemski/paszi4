"""
Схемы Pydantic для валидации данных
"""
from pydantic import BaseModel, field_validator
import re
from typing import Optional
from app.config import settings


class UserBase(BaseModel):
    """Базовая схема пользователя"""
    login: str
    password: str


class UserCreate(UserBase):
    """Схема для создания пользователя"""
    
    @field_validator('login')
    def validate_login(cls, v):
        """Валидация логина"""
        if not v:
            raise ValueError('Логин не может быть пустым')
        
        if len(v) < settings.min_login_length:
            raise ValueError(f'Логин должен быть не короче {settings.min_login_length} символов')
        
        if len(v) > settings.max_login_length:
            raise ValueError(f'Логин должен быть не длиннее {settings.max_login_length} символов')
        
        # Проверка разрешенных символов
        if not re.match(r'^[a-zA-Z0-9._-]+$', v):
            raise ValueError('Логин может содержать только латинские буквы, цифры и символы . _ -')
        
        return v
    
    @field_validator('password')
    def validate_password(cls, v):
        """Валидация пароля"""
        if not v:
            raise ValueError('Пароль не может быть пустым')
        
        if len(v) < settings.min_password_length:
            raise ValueError(f'Пароль должен быть не короче {settings.min_password_length} символов')
        
        # Проверка сложности пароля
        has_upper = any(c.isupper() for c in v)
        has_lower = any(c.islower() for c in v)
        has_digit = any(c.isdigit() for c in v)
        has_special = any(c in '!@#$%^&*(),.?":{}|<>' for c in v)
        
        errors = []
        if not has_upper:
            errors.append('заглавную букву')
        if not has_lower:
            errors.append('строчную букву')
        if not has_digit:
            errors.append('цифру')
        if not has_special:
            errors.append('специальный символ')
        
        if errors:
            raise ValueError(f'Пароль должен содержать хотя бы: {", ".join(errors)}')
        
        return v


class UserResponse(BaseModel):
    """Схема ответа при успешной регистрации"""
    message: str = "Пользователь успешно создан"
    login: str
    
    class Config:
        from_attributes = True


class ErrorResponse(BaseModel):
    """Схема ответа при ошибке"""
    message: str
    detail: Optional[str] = None
