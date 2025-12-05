"""
Модели базы данных
"""
from sqlalchemy import Column, Integer, String, DateTime, Index
from sqlalchemy.sql import func
from app.database import Base


class User(Base):
    """
    Модель пользователя
    """
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    login = Column(String(64), unique=True, index=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Создаем уникальный индекс для логина
    __table_args__ = (
        Index('ix_users_login_unique', 'login', unique=True),
    )
    
    def __repr__(self):
        return f"<User(id={self.id}, login='{self.login}')>"
