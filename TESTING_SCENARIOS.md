# Сценарії тестування API (Варіант 0)

## 1. Базовий сценарій: Створення користувача і повний цикл

```bash
# 1. Створити користувача
curl -X POST http://localhost:8080/api/user \
  -H "Content-Type: application/json" \
  -d '{"name":"Іван"}'

# 2. Створити категорію
curl -X POST http://localhost:8080/api/category \
  -H "Content-Type: application/json" \
  -d '{"name":"Їжа"}'

# 3. Створити рахунок
curl -X POST http://localhost:8080/api/account \
  -H "Content-Type: application/json" \
  -d '{"user_id":1,"balance":"0.00"}'

# 4. Додати дохід
curl -X POST http://localhost:8080/api/income \
  -H "Content-Type: application/json" \
  -d '{"user_id":1,"amount":"12000.00","description":"Зарплата"}'

# 5. Перевірити рахунок (баланс 12000)
curl http://localhost:8080/api/account/user/1 | jq

# 6. Додати витрату
curl -X POST http://localhost:8080/api/record \
  -H "Content-Type: application/json" \
  -d '{"user_id":1,"category_id":1,"amount":"750.00","description":"Продукти"}'

# 7. Перевірити баланс (12000 - 750)
curl http://localhost:8080/api/account/user/1 | jq
```

## 2. Сценарії валідації

### 2.1 Негативна сума
```bash
curl -X POST http://localhost:8080/api/income \
  -H "Content-Type: application/json" \
  -d '{"user_id":1,"amount":"-50.00"}'
# Очікувано: 422 + помилка валідації
```

### 2.2 Нестача коштів
```bash
curl -X POST http://localhost:8080/api/record \
  -H "Content-Type: application/json" \
  -d '{"user_id":1,"category_id":1,"amount":"999999.00"}'
# Очікувано: 400 + "Insufficient funds"
```

### 2.3 Категорія не знайдена
```bash
curl -X POST http://localhost:8080/api/record \
  -H "Content-Type: application/json" \
  -d '{"user_id":1,"category_id":999,"amount":"10.00"}'
# Очікувано: 404 "Category not found"
```

## 3. Робота з доходами

```bash
# Додати кілька доходів
curl -X POST http://localhost:8080/api/income \
  -H "Content-Type: application/json" \
  -d '{"user_id":1,"amount":"3000.00","description":"Фріланс"}'

curl -X POST http://localhost:8080/api/income \
  -H "Content-Type: application/json" \
  -d '{"user_id":1,"amount":"500.00","description":"Подарунок"}'

# Отримати всі доходи користувача
curl http://localhost:8080/api/income?user_id=1 | jq

# Видалити дохід і перевірити баланс
curl -X DELETE http://localhost:8080/api/income/1
curl http://localhost:8080/api/account/user/1 | jq
```

## 4. Робота з витратами

```bash
# Створити кілька категорій
curl -X POST http://localhost:8080/api/category \
  -H "Content-Type: application/json" \
  -d '{"name":"Транспорт"}'

curl -X POST http://localhost:8080/api/category \
  -H "Content-Type: application/json" \
  -d '{"name":"Розваги"}'

# Додати витрати по різних категоріях
curl -X POST http://localhost:8080/api/record \
  -H "Content-Type: application/json" \
  -d '{"user_id":1,"category_id":2,"amount":"150.00","description":"Метро"}'

curl -X POST http://localhost:8080/api/record \
  -H "Content-Type: application/json" \
  -d '{"user_id":1,"category_id":3,"amount":"400.00","description":"Кіно"}'

# Отримати витрати по категорії "Транспорт"
curl http://localhost:8080/api/record?category_id=2 | jq

# Оновити витрату (зміна суми)
curl -X PATCH http://localhost:8080/api/record/2 \
  -H "Content-Type: application/json" \
  -d '{"amount":"320.00","description":"Кіно + попкорн"}'

# Видалити витрату й перевірити баланс
curl -X DELETE http://localhost:8080/api/record/2
curl http://localhost:8080/api/account/user/1 | jq
```

## 5. Сторонні сценарії

### 5.1 Повний життєвий цикл (bash)
```bash
#!/bin/bash
BASE_URL="http://localhost:8080"

# Користувач
USER=$(curl -s -X POST $BASE_URL/api/user -H "Content-Type: application/json" -d '{"name":"Demo"}')
USER_ID=$(echo $USER | jq -r '.id')

# Категорія
CATEGORY=$(curl -s -X POST $BASE_URL/api/category -H "Content-Type: application/json" -d '{"name":"Харчування"}')
CATEGORY_ID=$(echo $CATEGORY | jq -r '.id')

# Рахунок
curl -s -X POST $BASE_URL/api/account -H "Content-Type: application/json" -d '{"user_id":'$USER_ID',"balance":"0.00"}'

# Дохід
curl -s -X POST $BASE_URL/api/income -H "Content-Type: application/json" \
  -d '{"user_id":'$USER_ID',"amount":"8000.00","description":"Аванс"}'

# Витрата
curl -s -X POST $BASE_URL/api/record -H "Content-Type: application/json" \
  -d '{"user_id":'$USER_ID',"category_id":'$CATEGORY_ID',"amount":"600.00","description":"Кафе"}'

# Баланс
curl -s $BASE_URL/api/account/user/$USER_ID | jq
```

### 5.2 Swagger UI
1. Перейти на `http://localhost:8080/swagger-ui`
2. Виконати запити (можна почати з `/api/user`, `/api/account`)

### 5.3 Postman
1. Імпортувати колекцію `Expenses_API.postman_collection.json`
2. Імпортувати environment `Expenses_API.postman_environment.json`
3. Вибрати environment "Expenses API Environment"
4. Виконувати запити в групах `Users → Accounts → Incomes → Records`

## 6. Очікувані результати

- Створення доходу збільшує баланс рахунку.
- Створення витрати зменшує баланс (і неможливе без достатніх коштів).
- Оновлення/видалення витрати коректно перераховує баланс.
- Неможливо створити категорію з дублюючою назвою.
- API повертає зрозумілі повідомлення про помилки.

## 7. Негативні кейси для перевірки

| Сценарій | Очікувана відповідь |
|----------|---------------------|
| Витрата без рахунку | 400 `User does not have an account` |
| Дохід без користувача | 404 `User not found` |
| Категорія, що має витрати, при видаленні | 400 `Cannot delete category that has records` |
| Порожнє ім’я категорії | 422 `Name cannot be empty` |

---

Сценарії покривають увесь функціонал варіанту 0 і можуть бути використані для демонстрації на захисті.

