# Контрольний список для Лабораторної №2 (Варіант 0)

## ✅ Готово

### Базова конфігурація
- [x] PostgreSQL в `docker-compose.yaml`
- [x] Конфігурація в `myapp/config.py`
- [x] Оновлений `requirements.txt`
- [x] Актуальний `.gitignore`

### SQLAlchemy моделі
- [x] `User`
- [x] `Category`
- [x] `Account`
- [x] `Income`
- [x] `Record`

### Marshmallow схеми
- [x] Схеми для читання/створення/оновлення всіх сутностей
- [x] Валідація назв, сум та зв'язків

### API (Flask-Smorest)
- [x] `/api/user` — CRUD користувачів
- [x] `/api/category` — CRUD категорій
- [x] `/api/account` — робота з рахунками
- [x] `/api/income` — доходи з автоматичним поповненням балансу
- [x] `/api/record` — витрати зі списанням балансу
- [x] `/health` — перевірка стану

### Облік доходів (варіант 0)
- [x] Автоматичне поповнення балансу при доході
- [x] Автоматичне списання при витраті
- [x] Заборона від’ємного балансу
- [x] Перерахунок балансу при оновленні/видаленні запису

### Документація та підтримка
- [x] `README.md` з описом варіанту 0
- [x] `SETUP_GUIDE.md` + `QUICKSTART.md`
- [x] `TESTING_SCENARIOS.md`
- [x] `PROJECT_SUMMARY.md`
- [x] Postman колекція + environment
- [x] Скрипти `init_db.sh`, `seed_data.py`, `test_api.sh`

### Swagger/OpenAPI
- [x] Автоматична документація через Flask-Smorest
- [x] Доступна за `/swagger-ui`

## 📝 Що зробити вручну

1. Створити `.env` (див. README).
2. `pip install -r requirements.txt`
3. `docker-compose up db -d`
4. `./init_db.sh`
5. `flask run --host=0.0.0.0 --port=8080`
6. Протестувати через Swagger/Postman/`test_api.sh`
7. `git add . && git commit -m "Lab 2: Variant 0 income tracking"`
8. `git tag v2.0.0 -a -m "Lab 2" && git push origin main --tags`

## 🎯 Критерії оцінювання

| Критерій | Статус |
|----------|--------|
| Валідація та обробка помилок | ✅ |
| ORM + PostgreSQL + міграції | ✅ |
| Варіант 0 (рахунок + доходи + витрати) | ✅ |
| Postman колекція + environment | ✅ |
| Git workflow (коміти + тег) | ✅ |

## 🧪 Мінімальний тест (cURL)
```bash
# Створити користувача
curl -X POST http://localhost:8080/api/user \
  -H "Content-Type: application/json" \
  -d '{"name":"Demo"}'

# Додати категорію
curl -X POST http://localhost:8080/api/category \
  -H "Content-Type: application/json" \
  -d '{"name":"Food"}'

# Створити рахунок
curl -X POST http://localhost:8080/api/account \
  -H "Content-Type: application/json" \
  -d '{"user_id":1,"balance":"0.00"}'

# Додати дохід
curl -X POST http://localhost:8080/api/income \
  -H "Content-Type: application/json" \
  -d '{"user_id":1,"amount":"1500.00","description":"Salary"}'

# Створити витрату
curl -X POST http://localhost:8080/api/record \
  -H "Content-Type: application/json" \
  -d '{"user_id":1,"category_id":1,"amount":"200.00","description":"Groceries"}'

# Перевірити баланс
curl http://localhost:8080/api/account/user/1 | jq
```

Успіхів на захисті! 🚀

