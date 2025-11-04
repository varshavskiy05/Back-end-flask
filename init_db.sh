#!/bin/bash

# Скрипт для ініціалізації бази даних та міграцій

echo "🚀 Initializing database..."

# Встановлюємо змінні середовища для Flask
export FLASK_APP=myapp

# Перевіряємо чи існує папка migrations
if [ ! -d "migrations" ]; then
    echo "📁 Creating migrations folder..."
    flask db init
else
    echo "📁 Migrations folder already exists"
fi

# Створюємо міграції
echo "📝 Creating migration..."
flask db migrate -m "Initial migration with all models"

# Застосовуємо міграції
echo "⬆️ Applying migrations..."
flask db upgrade

# Заповнюємо базу початковими даними
echo "🌱 Seeding database..."
python seed_data.py

echo "✅ Database initialization completed!"

