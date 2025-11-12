# Посібник з налаштування та запуску проєкту

## Передумови

- Python 3.11+
- Docker та Docker Compose
- Git

## Крок 1: Клонування репозиторію

```bash
git clone <your-repository-url>
cd Back-end-flask
```

## Крок 2: Створення .env файлу

Створіть файл `.env` в корені проєкту:

```bash
cat > .env << EOF
# Database configuration
DB_USER=postgres
DB_PASSWORD=postgres
DB_NAME=expenses_db
DB_HOST=localhost

# Flask configuration
FLASK_APP=myapp
FLASK_ENV=development
SECRET_KEY=your-secret-key-change-this
EOF
```

## Крок 3: Запуск бази даних

```bash
# Запустити тільки базу даних
docker-compose up db -d

# Перевірити що база працює
docker-compose ps
```

## Крок 4: Встановлення Python залежностей

```bash
# Створити віртуальне середовище (рекомендується)
python -m venv venv

# Активувати віртуальне середовище
# На macOS/Linux:
source venv/bin/activate
# На Windows:
# venv\Scripts\activate

# Встановити залежності
pip install -r requirements.txt
```

## Крок 5: Ініціалізація бази даних

### Варіант A: Використання скрипта (рекомендується)

```bash
# Зробити скрипт виконуваним
chmod +x init_db.sh

# Запустити скрипт
./init_db.sh
```

### Варіант B: Ручна ініціалізація

```bash
# Встановити змінну середовища
export FLASK_APP=myapp

# Ініціалізувати міграції (тільки перший раз)
flask db init

# Створити міграцію
flask db migrate -m "Initial migration"

# Застосувати міграції
flask db upgrade

# Заповнити базу початковими даними
python seed_data.py
```

## Крок 6: Запуск застосунку

### Локальний запуск

```bash
# Переконайтеся що база даних запущена
docker-compose up db -d

# Запустіть Flask застосунок
flask run --host=0.0.0.0 --port=8080
```

Застосунок буде доступний на `http://localhost:8080`

### Запуск через Docker Compose

```bash
# Запустити всі сервіси
docker-compose up --build

# Або в фоновому режимі
docker-compose up -d --build
```

## Крок 7: Перевірка роботи

### Використання cURL

```bash
# Health check
curl http://localhost:8080/health

# Отримати всіх користувачів
curl http://localhost:8080/api/user

# Отримати всі рахунки
curl http://localhost:8080/api/account

# Створити дохід
curl -X POST http://localhost:8080/api/income \
  -H "Content-Type: application/json" \
  -d '{"user_id":1,"amount":"1000.00","description":"Salary"}'

# Отримати витрати користувача
curl http://localhost:8080/api/record?user_id=1
```

### Використання Swagger UI

Відкрийте в браузері:
```
http://localhost:8080/swagger-ui
```

### Використання Postman

1. Імпортуйте колекцію: `Expenses_API.postman_collection.json`
2. Імпортуйте environment: `Expenses_API.postman_environment.json`
3. Виберіть environment "Expenses API Environment"
4. Почніть тестувати API!

## Корисні команди

### Міграції бази даних

```bash
# Створити нову міграцію після зміни моделей
flask db migrate -m "Description of changes"

# Застосувати міграції
flask db upgrade

# Відкотити останню міграцію
flask db downgrade

# Показати історію міграцій
flask db history
```

### Docker

```bash
# Зупинити всі контейнери
docker-compose down

# Зупинити і видалити volumes (видалить дані БД)
docker-compose down -v

# Переглянути логи
docker-compose logs -f

# Переглянути логи тільки застосунку
docker-compose logs -f myapp

# Переглянути логи тільки бази даних
docker-compose logs -f db
```

### База даних

```bash
# Підключитися до PostgreSQL через Docker
docker-compose exec db psql -U postgres -d expenses_db

# Експортувати дані
docker-compose exec db pg_dump -U postgres expenses_db > backup.sql

# Імпортувати дані
docker-compose exec -T db psql -U postgres expenses_db < backup.sql
```

## Структура проєкту

```
Back-end-flask/
├── myapp/                          # Основний пакет застосунку
│   ├── __init__.py                 # Application factory
│   ├── config.py                   # Конфігурація
│   ├── models.py                   # ORM моделі
│   ├── schemas.py                  # Marshmallow схеми
│   ├── accounts/                   # Blueprint рахунків
│   ├── categories/                 # Blueprint категорій
│   ├── healthcheck/                # Health check
│   ├── incomes/                    # Blueprint доходів
│   ├── records/                    # Blueprint витрат
│   └── users/                      # Blueprint користувачів
├── migrations/                     # Міграції БД (після flask db init)
├── .env                            # Змінні середовища (НЕ КОММІТИТИ!)
├── .gitignore                      # Git ignore файл
├── docker-compose.yaml             # Docker Compose конфігурація
├── Dockerfile                      # Docker образ
├── init_db.sh                      # Скрипт ініціалізації БД
├── requirements.txt                # Python залежності
├── seed_data.py                    # Скрипт для початкових даних
├── README.md                       # Основна документація
├── SETUP_GUIDE.md                  # Цей файл
├── Expenses_API.postman_collection.json      # Postman колекція
└── Expenses_API.postman_environment.json     # Postman environment
```

## Troubleshooting

### Проблема: База даних не запускається

```bash
# Перевірте статус контейнерів
docker-compose ps

# Перегляньте логи
docker-compose logs db

# Спробуйте перезапустити
docker-compose restart db
```

### Проблема: Помилка підключення до бази даних

- Переконайтеся що контейнер БД запущений
- Перевірте змінні середовища в `.env`
- Для локального запуску використовуйте `DB_HOST=localhost`
- Для Docker використовується `DB_HOST=db`

### Проблема: Помилки міграції

```bash
# Видаліть папку migrations і почніть заново
rm -rf migrations
flask db init
flask db migrate -m "Initial migration"
flask db upgrade
```

### Проблема: Порт вже зайнятий

```bash
# Знайдіть процес що використовує порт 8080
lsof -i :8080

# Або змініть порт в docker-compose.yaml
ports:
  - "8081:8080"  # Використовувати 8081 замість 8080
```

## Git workflow для лабораторної

```bash
# Після завершення всіх змін
git add .
git commit -m "Lab 2: Add validation, error handling, ORM, and new features"

# Створити тег версії
git tag v2.0.0 -a -m "Lab 2"

# Запушити все
git push origin main
git push --tags
```

## Наступні кроки

1. Протестуйте всі endpoints через Postman або Swagger
2. Спробуйте створити користувача, рахунок, додати дохід та витрату
3. Перевірте що баланс рахунку коректно оновлюється
4. Спробуйте створити приватні категорії
5. Протестуйте валідацію (спробуйте ввести некоректні дані)

## Додаткові ресурси

- [Flask Documentation](https://flask.palletsprojects.com/)
- [Flask-SQLAlchemy](https://flask-sqlalchemy.palletsprojects.com/)
- [Flask-Migrate](https://flask-migrate.readthedocs.io/)
- [Flask-Smorest](https://flask-smorest.readthedocs.io/)
- [Marshmallow](https://marshmallow.readthedocs.io/)

