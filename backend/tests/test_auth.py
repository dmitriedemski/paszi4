"""
Тесты для функционала регистрации пользователей
"""
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.main import app
from app.database import Base, get_db
from app.security import hash_password, verify_password

# Тестовая база данных
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

# Создаем движок для тестовой базы
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

# Создаем фабрику сессий для тестов
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def override_get_db():
    """
    Переопределенная зависимость для тестов
    """
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


# Переопределяем зависимость
app.dependency_overrides[get_db] = override_get_db

# Создаем клиент для тестов
client = TestClient(app)


@pytest.fixture(scope="function", autouse=True)
def setup_database():
    """
    Фикстура для настройки тестовой базы данных
    """
    # Создаем таблицы
    Base.metadata.create_all(bind=engine)
    yield
    # Удаляем таблицы после тестов
    Base.metadata.drop_all(bind=engine)


class TestSecurity:
    """Тесты для модуля безопасности"""
    
    def test_hash_password(self):
        """Тест хэширования пароля"""
        password = "TestPassword123!"
        hashed = hash_password(password)
        
        assert hashed != password
        assert len(hashed) > 0
        assert isinstance(hashed, str)
    
    def test_verify_password_correct(self):
        """Тест проверки правильного пароля"""
        password = "TestPassword123!"
        hashed = hash_password(password)
        
        assert verify_password(password, hashed) == True
    
    def test_verify_password_incorrect(self):
        """Тест проверки неправильного пароля"""
        password = "TestPassword123!"
        wrong_password = "WrongPassword123!"
        hashed = hash_password(password)
        
        assert verify_password(wrong_password, hashed) == False


class TestUserRegistration:
    """Тесты регистрации пользователей"""
    
    def test_successful_registration(self):
        """
        Тест 1: Успешная регистрация пользователя
        
        Этот тест проверяет, что пользователь с корректными данными
        может успешно зарегистрироваться в системе.
        """
        user_data = {
            "login": "testuser",
            "password": "TestPassword123!"
        }
        
        response = client.post("/api/register", json=user_data)
        
        assert response.status_code == 200
        assert response.json()["message"] == "Пользователь успешно создан"
        assert response.json()["login"] == "testuser"
    
    def test_duplicate_login(self):
        """
        Тест 2: Регистрация с дублирующим логином
        
        Этот тест проверяет, что система корректно обрабатывает
        попытку регистрации пользователя с уже существующим логином.
        """
        user_data = {
            "login": "duplicateuser",
            "password": "TestPassword123!"
        }
        
        # Первая регистрация - должна быть успешной
        response1 = client.post("/api/register", json=user_data)
        assert response1.status_code == 200
        
        # Вторая регистрация с тем же логином - должна вернуть ошибку 409
        response2 = client.post("/api/register", json=user_data)
        assert response2.status_code == 409
        assert "уже существует" in response2.json()["detail"]
    
    def test_weak_password(self):
        """
        Тест 3: Регистрация со слабым паролем
        
        Этот тест проверяет, что система корректно валидирует
        сложность пароля и отклоняет слабые пароли.
        """
        # Тестируем различные слабые пароли
        weak_passwords = [
            "short",          # слишком короткий
            "nouppercase1!",  # нет заглавных букв
            "NOLOWERCASE1!",  # нет строчных букв
            "NoSpecialChar1", # нет специальных символов
            "NoNumbers!",     # нет цифр
        ]
        
        for password in weak_passwords:
            user_data = {
                "login": f"testuser{weak_passwords.index(password)}",
                "password": password
            }
            
            response = client.post("/api/register", json=user_data)
            
            # Должна вернуться ошибка валидации (422)
            assert response.status_code == 422
            assert "Пароль должен" in response.json()["detail"]
    
    def test_invalid_login(self):
        """Тест регистрации с невалидным логином"""
        invalid_logins = [
            "ab",               # слишком короткий
            "a" * 33,          # слишком длинный
            "тест",             # кириллица
            "user@name",        # неразрешенный символ @
            "user name",        # пробел
        ]
        
        for login in invalid_logins:
            user_data = {
                "login": login,
                "password": "TestPassword123!"
            }
            
            response = client.post("/api/register", json=user_data)
            
            # Должна вернуться ошибка валидации (422)
            assert response.status_code == 422
    
    def test_missing_fields(self):
        """Тест регистрации с отсутствующими полями"""
        # Отсутствует логин
        response1 = client.post("/api/register", json={"password": "TestPassword123!"})
        assert response1.status_code == 422
        
        # Отсутствует пароль
        response2 = client.post("/api/register", json={"login": "testuser"})
        assert response2.status_code == 422
        
        # Пустой JSON
        response3 = client.post("/api/register", json={})
        assert response3.status_code == 422


class TestAPIEndpoints:
    """Тесты API эндпоинтов"""
    
    def test_root_endpoint(self):
        """Тест корневого эндпоинта"""
        response = client.get("/")
        
        assert response.status_code == 200
        assert response.json()["message"] == "User Registration API"
    
    def test_health_endpoint(self):
        """Тест эндпоинта проверки здоровья"""
        response = client.get("/health")
        
        assert response.status_code == 200
        assert response.json()["status"] == "healthy"
    
    def test_api_info_endpoint(self):
        """Тест эндпоинта информации об API"""
        response = client.get("/api/info")
        
        assert response.status_code == 200
        assert "app_env" in response.json()
        assert "hash_scheme" in response.json()


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
