"""
Конфигурация приложения
"""
from pydantic_settings import BaseSettings
from typing import List
import secrets
import json


class Settings(BaseSettings):
    """Настройки приложения"""
    
    # Настройки приложения
    app_env: str = "development"
    secret_key: str = secrets.token_urlsafe(32)
    debug: bool = False
    
    # Настройки базы данных
    database_url: str
    database_url_local: str
    
    # Настройки сервера
    host: str = "0.0.0.0"
    port: int = 8000
    cors_origins: List[str] = ["http://localhost:3000"]
    
    # Настройки хэширования паролей
    hash_scheme: str = "argon2"
    argon2_time_cost: int = 2
    argon2_memory_cost: int = 65536
    argon2_parallelism: int = 4
    argon2_hash_length: int = 32
    argon2_salt_length: int = 16
    
    # Настройки валидации
    min_login_length: int = 3
    max_login_length: int = 32
    min_password_length: int = 8
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        
        @classmethod
        def parse_env_var(cls, field_name: str, raw_val: str):
            if field_name == "cors_origins":
                # Если строка начинается с [ и заканчивается ], это JSON
                if raw_val.startswith("[") and raw_val.endswith("]"):
                    try:
                        return json.loads(raw_val)
                    except json.JSONDecodeError:
                        # Если не получилось распарсить JSON, разбиваем по запятой
                        pass
                # Разбиваем по запятой
                return [origin.strip() for origin in raw_val.split(",")]
            return raw_val


settings = Settings()
