# Используем официальный образ Python
FROM python:3.12-slim

# Устанавливаем системные зависимости для работы с Postgres (psycopg2)
RUN apt-get update && apt-get install -y \
    libpq-dev \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Устанавливаем рабочую директорию
WORKDIR /app

# Копируем и устанавливаем зависимости
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Копируем весь проект
COPY . .

# Отключаем буферизацию логов Python (чтобы видеть их в терминале докера)
ENV PYTHONUNBUFFERED=1
