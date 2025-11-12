# 🚀 Швидкий старт

Мінімальний набір команд для запуску проєкту за 5 хвилин.

## Крок 1: Створити .env файл

```bash
cat > .env << 'EOF'
DB_USER=postgres
DB_PASSWORD=postgres
DB_NAME=expenses_db
DB_HOST=localhost
FLASK_APP=myapp
FLASK_ENV=development
SECRET_KEY=dev-secret-key-change-in-production
EOF
```

## Крок 2: Встановити залежності

```bash
pip install -r requirements.txt
```

## Крок 3: Запустити базу даних

```bash
docker-compose up db -d
```

Почекайте 5-10 секунд, поки база даних повністю запуститься.

## Крок 4: Ініціалізувати базу даних

```bash
chmod +x init_db.sh
./init_db.sh
```

Або вручну:
```bash
export FLASK_APP=myapp
flask db init
flask db migrate -m "Initial migration"
flask db upgrade
python seed_data.py
```

## Крок 5: Запустити застосунок

```bash
flask run --host=0.0.0.0 --port=8080
```

## Крок 6: Перевірити що все працює

```bash
# Health check
curl http://localhost:8080/health

# Отримати користувачів
curl http://localhost:8080/api/user

# Отримати рахунок тестового користувача
curl http://localhost:8080/api/account/user/1 | jq

# Додати витрату (швидкий тест)
curl -X POST http://localhost:8080/api/record \
  -H "Content-Type: application/json" \
  -d '{"user_id":1,"category_id":1,"amount":"100.00","description":"Groceries"}'
```

## Крок 7: Відкрити Swagger UI

Відкрийте в браузері:
```
http://localhost:8080/swagger-ui
```

## 🎉 Готово!

Тепер ви можете:
- Тестувати API через Swagger UI
- Імпортувати Postman колекцію: `Expenses_API.postman_collection.json`
- Читати детальну документацію в `SETUP_GUIDE.md`
- Дивитися тестові сценарії в `TESTING_SCENARIOS.md`

## Альтернативний метод: Docker Compose

Якщо ви хочете запустити все через Docker:

```bash
# Створити .env файл (змінити DB_HOST на db)
cat > .env << 'EOF'
DB_USER=postgres
DB_PASSWORD=postgres
DB_NAME=expenses_db
DB_HOST=db
FLASK_APP=myapp
FLASK_ENV=development
SECRET_KEY=dev-secret-key-change-in-production
EOF

# Запустити все разом
docker-compose up --build
```

## Швидкий smoke-test (bash)

```bash
BASE_URL="http://localhost:8080"

echo "=== Users ==="
curl -s $BASE_URL/api/user | jq

echo "\n=== Accounts ==="
curl -s "$BASE_URL/api/account" | jq

echo "\n=== Balance (user=1) ==="
curl -s "$BASE_URL/api/account/user/1" | jq

echo "\n=== Incomes (user=1) ==="
curl -s "$BASE_URL/api/income?user_id=1" | jq

echo "\n=== Records (user=1) ==="
curl -s "$BASE_URL/api/record?user_id=1" | jq
```

## Troubleshooting

### База даних не запускається
```bash
docker-compose down -v
docker-compose up db -d
```

### Помилка міграції
```bash
rm -rf migrations
flask db init
flask db migrate -m "Initial migration"
flask db upgrade
```

### Порт зайнятий
Змініть порт в команді запуску:
```bash
flask run --host=0.0.0.0 --port=8081
```

---

**Час виконання**: ~5 хвилин  
**Складність**: Легко  
**Результат**: Повністю робочий API з базою даних

