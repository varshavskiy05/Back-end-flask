
# Expenses Tracker API (Коротко)

- Вариант: 0 (облік доходів). Доходи поповнюють баланс рахунку, витрати списують, «мінус» заборонений.
- Стек: Flask 3, Flask‑SQLAlchemy, Flask‑Migrate, Flask‑Smorest (Swagger), Marshmallow, PostgreSQL.
- Живі точки: `/health`, `/swagger-ui`.

## Швидкий старт (локально)
1) Залежності
```bash
python3 -m venv venv && source venv/bin/activate
python3 -m pip install --upgrade pip
python3 -m pip install -r requirements.txt
```
2) База даних
```bash
docker-compose up db -d
```
3) Міграції та початкові дані
```bash
chmod +x init_db.sh
./init_db.sh
```
4) Запуск
```bash
flask run --host=0.0.0.0 --port=8080
```
Перевір: http://localhost:8080/health та http://localhost:8080/swagger-ui

## Деплой (Render)
- ENV: `DATABASE_URL`, `SECRET_KEY`, `FLASK_APP=myapp`, `FLASK_ENV=production`
- Start Command (без Dockerfile):
```bash
bash -lc "flask db upgrade && gunicorn 'myapp:create_app()' --bind 0.0.0.0:$PORT"
```
- Якщо Dockerfile — додай аналогічний `flask db upgrade` у CMD.

## API (огляд)
- Users: CRUD `/api/user`
- Categories: CRUD `/api/category`
- Accounts: `/api/account`, `/api/account/user/<user_id>`
- Incomes: `/api/income` (поповнює баланс)
- Records: `/api/record` (списує баланс)

## Деталі та посилання
- Установка/налаштування: `SETUP_GUIDE.md`, `QUICKSTART.md`
- Сценарії тестування: `TESTING_SCENARIOS.md`, скрипт `test_api.sh`
- Підсумок і критерії: `PROJECT_SUMMARY.md`, `LAB_CHECKLIST.md`
- Git/команди: `GIT_WORKFLOW.md`, `COMMANDS_REFERENCE.md`
- Postman: `Expenses_API.postman_collection.json`, `Expenses_API.postman_environment.json`

## Що додати в звіт
- Лінк на репозиторій і тег `v2.0.0`
- Лінк на деплой (Render) + скріни `/health`, `/swagger-ui`
- 2–3 успішні запити (user/account/income/record) і 1 помилка (валідація або insufficient funds)

