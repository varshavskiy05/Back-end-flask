# 📚 Довідник команд

## 🐳 Docker Commands

```bash
# Запустити тільки базу даних
docker-compose up db -d

# Запустити всі сервіси
docker-compose up --build

# Запустити в фоновому режимі
docker-compose up -d

# Зупинити всі контейнери
docker-compose down

# Зупинити і видалити volumes (видалить дані БД!)
docker-compose down -v

# Подивитися логи
docker-compose logs -f

# Логи тільки БД
docker-compose logs -f db

# Логи тільки app
docker-compose logs -f myapp

# Перезапустити контейнер
docker-compose restart db

# Статус контейнерів
docker-compose ps

# Підключитися до PostgreSQL
docker-compose exec db psql -U postgres -d expenses_db
```

## 🗄️ Database Commands

```bash
# Експортувати дані
docker-compose exec db pg_dump -U postgres expenses_db > backup.sql

# Імпортувати дані
docker-compose exec -T db psql -U postgres expenses_db < backup.sql

# Список таблиць (в psql)
\dt

# Описати таблицю (в psql)
\d users

# Вийти з psql
\q

# SQL запит через командний рядок
docker-compose exec db psql -U postgres -d expenses_db -c "SELECT * FROM users;"
```

## 🔄 Flask-Migrate Commands

```bash
# Встановити змінну середовища
export FLASK_APP=myapp

# Ініціалізувати міграції (тільки раз)
flask db init

# Створити нову міграцію
flask db migrate -m "Description of changes"

# Застосувати міграції
flask db upgrade

# Відкотити останню міграцію
flask db downgrade

# Історія міграцій
flask db history

# Поточна версія БД
flask db current

# Показати SQL для міграції (без виконання)
flask db upgrade --sql

# Створити порожню міграцію (для ручних змін)
flask db revision -m "Manual changes"
```

## 🐍 Flask Commands

```bash
# Запустити сервер
flask run

# Запустити на всіх інтерфейсах
flask run --host=0.0.0.0

# Запустити на конкретному порту
flask run --port=8080

# Debug режим
flask run --debug

# Запустити в production режимі
gunicorn "myapp:create_app()" --bind 0.0.0.0:8080

# Flask shell (інтерактивний Python з контекстом)
flask shell

# Виконати Python скрипт з Flask контекстом
flask run-script script.py
```

## 📦 Python/Pip Commands

```bash
# Встановити залежності
pip install -r requirements.txt

# Оновити requirements.txt
pip freeze > requirements.txt

# Встановити конкретний пакет
pip install flask-smorest

# Показати інформацію про пакет
pip show flask-smorest

# Список встановлених пакетів
pip list

# Перевірити залежності
pip check

# Оновити пакет
pip install --upgrade flask

# Видалити пакет
pip uninstall flask-smorest
```

## 🧪 Testing Commands

```bash
# Запустити тестовий скрипт
chmod +x test_api.sh
./test_api.sh

# Health check
curl http://localhost:8080/health

# Get запит
curl http://localhost:8080/api/account

# Post запит (додати дохід)
curl -X POST http://localhost:8080/api/income \
  -H "Content-Type: application/json" \
  -d '{"user_id":1,"amount":"500.00","description":"Bonus"}'

# Put/Patch запит (оновити баланс)
curl -X PATCH http://localhost:8080/api/account/1 \
  -H "Content-Type: application/json" \
  -d '{"balance":"2000.00"}'

# Delete запит
curl -X DELETE http://localhost:8080/api/income/1

# Запит з pretty JSON (потрібен jq)
curl -s http://localhost:8080/api/account/user/1 | jq

# Зберегти відповідь у файл
curl http://localhost:8080/api/record?user_id=1 > records.json
```

## 🔧 Git Commands

```bash
# Статус
git status

# Додати файли
git add .
git add myapp/

# Коміт
git commit -m "Message"

# Коміт з детальним описом
git commit -m "Title" -m "Description"

# Змінити останній коміт
git commit --amend

# Створити тег
git tag v2.0.0 -a -m "Lab 2"

# Список тегів
git tag -l

# Видалити тег (локально)
git tag -d v2.0.0

# Push коміти
git push origin main

# Push теги
git push --tags

# Push все разом
git push origin main --tags

# Pull зміни
git pull origin main

# Клонувати репозиторій
git clone <url>

# Подивитися історію
git log
git log --oneline
git log --graph --oneline --all

# Подивитися зміни
git diff
git diff --staged

# Відкотити зміни в файлі
git checkout -- filename

# Відкотити останній коміт (залишити зміни)
git reset --soft HEAD~1

# Відкотити останній коміт (видалити зміни)
git reset --hard HEAD~1

# Створити нову гілку
git branch feature-name
git checkout -b feature-name

# Переключитися на гілку
git checkout main

# Злити гілку
git merge feature-name
```

## 🌱 Seed Data Commands

```bash
# Запустити seed скрипт
python seed_data.py

# Очистити БД і запустити seed заново (в Flask shell)
flask shell
>>> from myapp import db
>>> from myapp.models import *
>>> db.drop_all()
>>> db.create_all()
>>> exit()
python seed_data.py
```

## 🛠️ Utility Commands

```bash
# Знайти процес на порту
lsof -i :8080
netstat -ano | findstr :8080  # Windows

# Вбити процес
kill -9 <PID>

# Перевірити версію Python
python --version

# Перевірити версію pip
pip --version

# Створити віртуальне середовище
python -m venv venv

# Активувати venv (Linux/Mac)
source venv/bin/activate

# Активувати venv (Windows)
venv\Scripts\activate

# Деактивувати venv
deactivate

# Зробити файл виконуваним
chmod +x script.sh

# Запустити скрипт
./script.sh

# Подивитися змінні середовища
printenv
echo $FLASK_APP

# Встановити змінну середовища
export FLASK_APP=myapp

# Очистити термінал
clear

# Історія команд
history

# Знайти файл
find . -name "*.py"

# Знайти в файлах
grep -r "search_text" .

# Подивитися розмір папки
du -sh myapp/

# Подивитися вільне місце
df -h
```

## 📊 Database Query Examples (в Flask shell)

```bash
# Запустити Flask shell
flask shell

# Імпорти
>>> from myapp import db
>>> from myapp.models import *

# Отримати всі записи
>>> User.query.all()
>>> Category.query.all()
>>> Account.query.all()

# Отримати за ID
>>> user = User.query.get(1)
>>> user.name

# Фільтрація
>>> Income.query.filter_by(user_id=1).all()
>>> Record.query.filter(Record.amount > 100).all()

# Створити запис
>>> user = User(name="Demo")
>>> db.session.add(user)
>>> db.session.commit()

# Оновити запис
>>> account = Account.query.filter_by(user_id=user.id).first()
>>> account.balance = 500
>>> db.session.commit()

# Видалити запис
>>> record = Record.query.first()
>>> db.session.delete(record)
>>> db.session.commit()

# Rollback
>>> db.session.rollback()

# Кількість записів
>>> Income.query.count()

# Join
>>> Record.query.join(Category).filter(Category.name == "Food").all()

# Order by
>>> Income.query.order_by(Income.created_at.desc()).all()

# Limit
>>> Record.query.limit(10).all()

# Вийти
>>> exit()
```

## 🔍 Debugging Commands

```bash
# Переглянути логи Flask
tail -f flask.log

# Переглянути активні з'єднання до БД
docker-compose exec db psql -U postgres -d expenses_db -c "SELECT * FROM pg_stat_activity;"

# Перевірити розмір таблиць
docker-compose exec db psql -U postgres -d expenses_db -c "\dt+"

# Python debugger
python -m pdb myapp.py

# Тестувати імпорти
python -c "from myapp import create_app; print('OK')"

# Перевірити синтаксис Python
python -m py_compile myapp/models.py

# Запустити з verbose режимом
flask run --debug

# Профілювання
python -m cProfile -o output.prof script.py
```

## 💡 Quick Commands Combos

```bash
# Повний рестарт з очисткою БД
docker-compose down -v && docker-compose up db -d && sleep 5 && ./init_db.sh && flask run

# Швидкий тест після змін
git add . && git commit -m "Update" && ./test_api.sh

# Бекап і рестарт БД
docker-compose exec db pg_dump -U postgres expenses_db > backup_$(date +%Y%m%d).sql && docker-compose restart db

# Створити міграцію і застосувати
flask db migrate -m "Changes" && flask db upgrade

# Переглянути всі API endpoints
curl -s http://localhost:8080/swagger-ui
```

## 📖 Help Commands

```bash
# Flask help
flask --help

# Docker Compose help
docker-compose --help

# Git help
git --help
git commit --help

# Pip help
pip --help

# Python help
python --help
```

---

**💡 Порада**: додайте часто використовувані команди до alias у `.bashrc` або `.zshrc`:

```bash
alias frun="flask run --host=0.0.0.0 --port=8080"
alias dcup="docker-compose up -d"
alias dcdown="docker-compose down"
alias fshell="flask shell"
alias dbmigrate="flask db migrate -m"
alias dbupgrade="flask db upgrade"
```

