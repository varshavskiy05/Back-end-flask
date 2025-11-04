"""Скрипт для заповнення бази даних початковими даними (варіант 0)"""

from decimal import Decimal

from sqlalchemy import func

from myapp import create_app
from myapp.models import db, User, Category, Account, Income, Record


def seed_database():
    """Заповнюємо базу початковими даними"""
    app = create_app()

    with app.app_context():
        print("Starting database seeding...")

        # Базові категорії
        print("Creating categories...")
        categories_data = [
            "Food",
            "Transport",
            "Entertainment",
            "Utilities",
            "Healthcare",
            "Education",
            "Savings",
            "Other",
        ]

        for name in categories_data:
            if not Category.query.filter(func.lower(Category.name) == name.lower()).first():
                db.session.add(Category(name=name))
                print(f"  Added category: {name}")

        # Тестовий користувач та рахунок
        print("\nCreating test user and account...")
        user = User.query.filter_by(name="Test User").first()
        if not user:
            user = User(name="Test User")
            db.session.add(user)
            db.session.flush()
            print(f"  Created user with ID: {user.id}")
        else:
            print(f"  User already exists with ID: {user.id}")

        account = Account.query.filter_by(user_id=user.id).first()
        if not account:
            account = Account(user_id=user.id, balance=Decimal("1000.00"))
            db.session.add(account)
            print("  Created account with balance 1000.00")
        else:
            print("  Account already exists")

        # Базовий дохід та витрати для демонстрації
        print("\nCreating sample income and expense...")
        income_exists = Income.query.filter_by(user_id=user.id, description="Initial deposit").first()
        if not income_exists:
            income = Income(user_id=user.id, amount=Decimal("1500.00"), description="Initial deposit")
            db.session.add(income)
            account.balance = (Decimal(str(account.balance)) + Decimal("1500.00"))
            print("  Added income: 1500.00")

        food_category = Category.query.filter_by(name="Food").first()
        if food_category and not Record.query.filter_by(user_id=user.id, description="Groceries").first():
            expense = Record(
                user_id=user.id,
                category_id=food_category.id,
                amount=Decimal("250.00"),
                description="Groceries",
            )
            db.session.add(expense)
            account.balance = (Decimal(str(account.balance)) - Decimal("250.00"))
            print("  Added expense: 250.00")

        db.session.commit()
        print("\n✅ Database seeding completed successfully!")


if __name__ == "__main__":
    seed_database()

