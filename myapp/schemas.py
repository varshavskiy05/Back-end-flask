from marshmallow import Schema, fields, validate, validates, ValidationError


# User Schemas
class UserSchema(Schema):
    """Схема для користувача"""
    id = fields.Int(dump_only=True)
    username = fields.Str(dump_only=True)
    name = fields.Str(required=True, validate=validate.Length(min=1, max=100))
    created_at = fields.DateTime(dump_only=True)


class UserCreateSchema(Schema):
    """Схема для створення користувача"""
    name = fields.Str(required=True, validate=validate.Length(min=1, max=100))


class UserUpdateSchema(Schema):
    """Схема для оновлення користувача"""
    name = fields.Str(validate=validate.Length(min=1, max=100))


# Category Schemas
class CategorySchema(Schema):
    """Схема для категорії"""
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True, validate=validate.Length(min=1, max=100))
    created_at = fields.DateTime(dump_only=True)


class CategoryCreateSchema(Schema):
    """Схема для створення категорії"""
    name = fields.Str(required=True, validate=validate.Length(min=1, max=100))

    @validates('name')
    def validate_name(self, value):
        if not value or not value.strip():
            raise ValidationError('Name cannot be empty')


class CategoryUpdateSchema(Schema):
    """Схема для оновлення категорії"""
    name = fields.Str(validate=validate.Length(min=1, max=100))


# Account Schemas
class AccountSchema(Schema):
    """Схема для рахунку"""
    id = fields.Int(dump_only=True)
    user_id = fields.Int(required=True)
    balance = fields.Decimal(as_string=True, places=2, dump_default='0.00')
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)

    @validates('balance')
    def validate_balance(self, value):
        if value < 0:
            raise ValidationError('Balance cannot be negative')


class AccountCreateSchema(Schema):
    """Схема для створення рахунку"""
    user_id = fields.Int(required=True)
    balance = fields.Decimal(as_string=True, places=2, dump_default='0.00')


class AccountUpdateSchema(Schema):
    """Схема для оновлення рахунку"""
    balance = fields.Decimal(as_string=True, places=2)


# Income Schemas
class IncomeSchema(Schema):
    """Схема для доходу"""
    id = fields.Int(dump_only=True)
    user_id = fields.Int(required=True)
    amount = fields.Decimal(required=True, as_string=True, places=2, validate=validate.Range(min=0.01))
    description = fields.Str(allow_none=True, validate=validate.Length(max=255))
    created_at = fields.DateTime(dump_only=True)

    @validates('amount')
    def validate_amount(self, value):
        if value <= 0:
            raise ValidationError('Amount must be positive')


class IncomeCreateSchema(Schema):
    """Схема для створення доходу"""
    user_id = fields.Int(required=True)
    amount = fields.Decimal(required=True, as_string=True, places=2)
    description = fields.Str(allow_none=True, validate=validate.Length(max=255))

    @validates('amount')
    def validate_amount(self, value):
        if value <= 0:
            raise ValidationError('Amount must be positive')


# Record (Expense) Schemas
class RecordSchema(Schema):
    """Схема для запису витрат"""
    id = fields.Int(dump_only=True)
    user_id = fields.Int(required=True)
    category_id = fields.Int(required=True)
    amount = fields.Decimal(required=True, as_string=True, places=2, validate=validate.Range(min=0.01))
    description = fields.Str(allow_none=True, validate=validate.Length(max=255))
    created_at = fields.DateTime(dump_only=True)

    @validates('amount')
    def validate_amount(self, value):
        if value <= 0:
            raise ValidationError('Amount must be positive')


class RecordCreateSchema(Schema):
    """Схема для створення запису витрат"""
    user_id = fields.Int(required=True)
    category_id = fields.Int(required=True)
    amount = fields.Decimal(required=True, as_string=True, places=2)
    description = fields.Str(allow_none=True, validate=validate.Length(max=255))

    @validates('amount')
    def validate_amount(self, value):
        if value <= 0:
            raise ValidationError('Amount must be positive')


class RecordUpdateSchema(Schema):
    """Схема для оновлення запису витрат"""
    category_id = fields.Int()
    amount = fields.Decimal(as_string=True, places=2)
    description = fields.Str(allow_none=True, validate=validate.Length(max=255))


# Query Schemas
class RecordQuerySchema(Schema):
    """Схема для фільтрації записів"""
    user_id = fields.Int()
    category_id = fields.Int()


# Auth Schemas
class AuthRegisterSchema(Schema):
    """Схема реєстрації"""
    username = fields.Str(required=True, validate=validate.Length(min=3, max=80))
    password = fields.Str(required=True, validate=validate.Length(min=6, max=128))
    name = fields.Str(required=False, validate=validate.Length(min=1, max=100))


class AuthLoginSchema(Schema):
    """Схема логіну"""
    username = fields.Str(required=True)
    password = fields.Str(required=True)

