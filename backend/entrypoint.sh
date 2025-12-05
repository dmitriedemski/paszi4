#!/bin/bash

# Простая пауза вместо ожидания netcat
echo "Waiting 5 seconds for database..."
sleep 5

# Применяем миграции
echo "Applying database migrations..."
alembic upgrade head

# Запускаем приложение
echo "Starting application..."
exec uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload