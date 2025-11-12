from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class User(db.Model):
    """Модель користувача"""
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Зв'язки
    records = db.relationship('Record', back_populates='user', cascade='all, delete-orphan')
    account = db.relationship('Account', back_populates='user', uselist=False, cascade='all, delete-orphan')
    incomes = db.relationship('Income', back_populates='user', cascade='all, delete-orphan')

    def __repr__(self):
        return f'<User {self.name}>'


class Category(db.Model):
    """Модель категорії витрат"""
    __tablename__ = 'categories'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Зв'язки
    records = db.relationship('Record', back_populates='category', cascade='all, delete-orphan')

    def __repr__(self):
        return f'<Category {self.name}>'


class Account(db.Model):
    """Модель рахунку для обліку доходів (Варіант 0)"""
    __tablename__ = 'accounts'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), unique=True, nullable=False)
    balance = db.Column(db.Numeric(precision=12, scale=2), default=0.0, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Зв'язки
    user = db.relationship('User', back_populates='account')

    def __repr__(self):
        return f'<Account user_id={self.user_id} balance={self.balance}>'


class Income(db.Model):
    """Модель доходу (Варіант 0)"""
    __tablename__ = 'incomes'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    amount = db.Column(db.Numeric(precision=12, scale=2), nullable=False)
    description = db.Column(db.String(255), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Зв'язки
    user = db.relationship('User', back_populates='incomes')

    def __repr__(self):
        return f'<Income {self.amount} user_id={self.user_id}>'


class Record(db.Model):
    """Модель запису витрат"""
    __tablename__ = 'records'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'), nullable=False)
    amount = db.Column(db.Numeric(precision=12, scale=2), nullable=False)
    description = db.Column(db.String(255), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Зв'язки
    user = db.relationship('User', back_populates='records')
    category = db.relationship('Category', back_populates='records')

    def __repr__(self):
        return f'<Record {self.amount} user_id={self.user_id} category_id={self.category_id}>'
