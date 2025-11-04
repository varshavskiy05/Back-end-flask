FROM python:3.11-slim

WORKDIR /app

# 1) системные либы для psycopg2
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential libpq-dev \
 && rm -rf /var/lib/apt/lists/*

# 2) свежий pip/setuptools/wheel
RUN python -m pip install --upgrade pip setuptools wheel

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . /app

# 3) нормальный старт для продакшена
CMD gunicorn "myapp:create_app()" --bind 0.0.0.0:${PORT:-8080}
