# MVP: Регистрация пользователей (Frontend — Backend — PostgreSQL)

Проект — минимально работоспособный продукт (MVP) для регистрации пользователей:
- Frontend: React + Vite (TypeScript)
- Backend: Python + FastAPI
- База данных: PostgreSQL (migrations — Alembic)
- Контейнеризация: Docker (отдельные Dockerfile для frontend и backend) и `docker-compose`

Цель: форма регистрации (login + password) → создание пользователя в БД → хэш пароля (Argon2) → логирование события → ответ UI. Всё запускается через `docker compose up`.

-------------------------

Содержание
- Коротко о структуре проекта
- Требования (локально)
- Переменные окружения (.env)
- Быстрый запуск (Docker)
- Локальная разработка (опционально)
- Тесты
- API: примеры запросов
- Миграции
- Отладка и часто встречаемые ошибки
- Безопасность: что сделано
- Список действий участников / скриншоты веток (инструкция)

-------------------------

Структура репозитория (важные директории/файлы)

- `backend/` — FastAPI-приложение, Dockerfile, миграции Alembic, тесты (`backend/tests`)
- `frontend/` — React + Vite приложение, Dockerfile, сборка в `dist/`
- `docker-compose.yml` — описывает сервисы `db`, `backend`, `frontend`
- `backend/requirements.txt` — python зависимости
- `frontend/package.json` — зависимости frontend
- `.env.example` — пример переменных окружения (должен быть в корне/в frontend/backend)

Требования (локально)
- Docker (Engine) и Docker-Compose (плагин `docker-compose`) — рекомендуется последняя стабильная версия.

Переменные окружения
Файл `.env` (в папке `backend`, смотрите `app.config`) должен содержать, как минимум:

```env
DATABASE_URL=postgresql://postgres:password@db:5432/registration_db
SECRET_KEY=your_secret_key_here
APP_ENV=development
PORT=8000
# Параметры Argon2 (пример)
ARGON2_TIME_COST=2
ARGON2_MEMORY_COST=65536
ARGON2_PARALLELISM=4
# CORS
CORS_ORIGINS=["http://localhost:3000","http://127.0.0.1:3000"]
```

См. `.env.example` для подробностей. Не добавляйте реальные секреты в VCS.

Быстрый запуск (Docker)
1. В корне проекта:
```bash
cd "/home/dmitri/Рабочий стол/mvp_proj"
docker compose up --build
```
2. Приложения станут доступны:
- Frontend: http://127.0.0.1:3000
- Backend (API): http://127.0.0.1:8000

Фоновый режим:
```bash
docker compose up -d --build
```
Остановить и удалить контейнеры и сеть:
```bash
docker compose down
# + удалить том с данными postgres:
docker compose down -v
```

Тесты
- В контейнере backend:
```bash
docker compose exec backend pytest -q
```

- В проекте есть минимум 3 покрытия тестов:
  1. Успешная регистрация
  2. Попытка регистрации с дублирующим логином → 409
  3. Регистрация со слабым паролем → 422

API (основные endpoint'ы)
- POST /api/register
  - Описание: регистрация пользователя
  - Request JSON:
    ```json
    {
      "login": "имя",
      "password": "СильныйПароль1!"
    }
    ```
  - Успех: HTTP 200 (пример ответа):
    ```json
    {
      "login": "имя",
      "message": "Пользователь успешно создан"
    }
    ```
  - Ошибки:
    - 422 — валидация (недопустимый логин/пароль)
    - 409 — логин уже существует

Примеры curl
```bash
curl -X POST http://127.0.0.1:8000/api/register \
  -H "Content-Type: application/json" \
  -d '{"login":"testuser","password":"TestPassword123!"}'
```

Миграции (Alembic)
- Выполнить миграции вручную:
```bash
docker compose run --rm backend alembic upgrade head
```

Отладка и типичные проблемы
- Порт 5432 занят на хосте: Docker не сможет пробросить порт — остановите локальный Postgres или измените проброс в `docker-compose.yml` (например `5433:5432`).
- CORS: если фронтенд и бэкенд на разных хостах/портax, проверьте `CORS_ORIGINS` (в `.env`) и убедитесь, что origin фронтенда (`http://127.0.0.1:3000` или `http://localhost:3000`) указан.
- Preflight OPTIONS возвращает 400: убедитесь, что приложение использует `CORSMiddleware` и нет конфликтного кастомного обработчика OPTIONS.
- Если тесты в контейнере падают из‑за соединения к `db`: при импорте приложения код не должен пытаться подключаться к внешней БД (в проекте это учтено — создание таблиц защищено try/except).



Безопасность: что сделано

- Пароли никогда не хранятся в открытом виде — используется Argon2id через `passlib`/`argon2-cffi`.

- Параметры Argon2 (time/memory/parallelism) конфигурируются через переменные окружения, чтобы их можно было адаптировать под окружение Docker.

- В БД установлен уникальный индекс/constraint на поле `login`, предотвращающий дублирование логинов.

- В логах не записывается сырой пароль; логируются только события (успешная регистрация, ошибки).

- Валидация входных данных на backend (длина логина, допустимые символы; сложность пароля — минимум 1 заглавная, 1 строчная, 1 цифра, 1 спецсимвол).

