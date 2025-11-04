# Expenses Tracker API

Backend застосунок для обліку витрат та доходів, побудований на Flask з використанням PostgreSQL.

## Лабораторна робота №2 - v2.0.0

### Визначення варіанту

**Формула**: `36 % 3 | остача 0`

> **Варіант 0 — облік доходів**

### Основна ідея

Проєкт реалізує фінансовий облік для користувача:
- дохід зараховується на особистий рахунок;
- витрати автоматично списуються з рахунку;
- заборонено йти «в мінус» (баланс не може бути від’ємним).

## Сутності

1. **User** — користувачі системи.
2. **Category** — глобальні категорії витрат (Food, Transport тощо).
3. **Account** — рахунок користувача з актуальним балансом.
4. **Income** — запис доходу з описом та сумою.
5. **Record** — запис витрати, що зменшує баланс рахунку.

## API Endpoints

### Users
- `GET /api/user` — список користувачів
- `POST /api/user` — створення користувача
- `GET /api/user/<id>` — перегляд користувача
- `PATCH /api/user/<id>` — оновлення користувача
- `DELETE /api/user/<id>` — видалення користувача

### Categories
- `GET /api/category` — список категорій
- `POST /api/category` — створення категорії
- `GET /api/category/<id>` — перегляд категорії
- `PATCH /api/category/<id>` — оновлення категорії
- `DELETE /api/category/<id>` — видалення категорії (якщо не використовується)

### Accounts
- `GET /api/account` — список рахунків
- `POST /api/account` — створення рахунку для користувача
- `GET /api/account/<id>` — перегляд рахунку
- `GET /api/account/user/<user_id>` — перегляд рахунку користувача
- `PATCH /api/account/<id>` — оновлення балансу
- `DELETE /api/account/<id>` — видалення рахунку

### Incomes
- `GET /api/income` — список доходів (можна фільтрувати `user_id`)
- `POST /api/income` — додати дохід (баланс збільшується автоматично)
- `GET /api/income/<id>` — перегляд доходу
- `DELETE /api/income/<id>` — видалення доходу (баланс зменшується)

### Records (витрати)
- `GET /api/record` — список витрат (можна фільтрувати `user_id`, `category_id`)
- `POST /api/record` — створення витрати (баланс зменшується)
- `GET /api/record/<id>` — перегляд витрати
- `PATCH /api/record/<id>` — оновлення витрати (баланс перераховується)
- `DELETE /api/record/<id>` — видалення витрати (баланс повертається)

### Health Check
- `GET /health` — перевірка стану застосунку

## Валідація та обробка помилок

- Перевірка обов’язкових полів і типів (Marshmallow).
- Позитивні значення для сум доходів/витрат.
- Перевірка існування користувача, категорії та рахунку.
- Неможливість списати суму, якщо недостатньо коштів.
- Стандартизована обробка помилок (400, 404, 422, 500).

## Технології

- **Flask 3** — веб-фреймворк.
- **Flask-SQLAlchemy** — ORM.
- **Flask-Migrate** — міграції бази даних.
- **Flask-Smorest** — побудова REST API та Swagger.
- **Marshmallow** — валідація та серіалізація даних.
- **PostgreSQL** — база даних.
- **Docker / Docker Compose** — контейнеризація.

## Установка та запуск

### 1. Клонування
```bash
git clone <repository-url>
cd Back-end-flask
```

### 2. Створіть `.env`
```bash
DB_USER=postgres
DB_PASSWORD=postgres
DB_NAME=expenses_db
DB_HOST=localhost
FLASK_APP=myapp
FLASK_ENV=development
SECRET_KEY=your-secret-key
```

### 3. Залежності
```bash
pip install -r requirements.txt
```

### 4. Запустіть базу даних
```bash
docker-compose up db -d
```

### 5. Міграції + початкові дані
```bash
chmod +x init_db.sh
./init_db.sh
```
> Скрипт створить структуру БД, заповнить базові категорії, тестового користувача та транзакції.

### 6. Запуск застосунку
```bash
flask run --host=0.0.0.0 --port=8080
```

### 7. Swagger UI
```
http://localhost:8080/swagger-ui
```

## Структура проєкту

```
Back-end-flask/
├── myapp/
│   ├── __init__.py          # Application factory
│   ├── config.py            # Конфігурація
│   ├── models.py            # ORM-моделі (User, Category, Account, Income, Record)
│   ├── schemas.py           # Marshmallow схеми
│   ├── users/               # Blueprint користувачів
│   ├── categories/          # Blueprint категорій
│   ├── accounts/            # Blueprint рахунків
│   ├── incomes/             # Blueprint доходів
│   ├── records/             # Blueprint витрат
│   └── healthcheck/         # Health check
├── migrations/              # Міграції бази даних
├── docker-compose.yaml      # Docker конфігурація
├── Dockerfile               # Docker образ
├── requirements.txt         # Залежності Python
├── seed_data.py             # Початкові дані
└── README.md                # Документація
```

## Тестування

- Swagger UI (автоматична документація).
- Postman колекція та environment:
  - `Expenses_API.postman_collection.json`
  - `Expenses_API.postman_environment.json`
- Скрипт швидкої перевірки: `./test_api.sh`
- Файл `TESTING_SCENARIOS.md` містить розгорнуті сценарії.

## Git workflow

```bash
git add .
git commit -m "Lab 2: Variant 0 implementation"
git tag v2.0.0 -a -m "Lab 2"
git push origin main --tags
```

## Ліцензія

MIT

