from flask.views import MethodView
from flask_smorest import abort
from flask import request
from myapp.records import bp
from myapp.models import db, Record, User, Category, Account
from myapp.schemas import RecordSchema, RecordCreateSchema, RecordUpdateSchema, RecordQuerySchema
from decimal import Decimal


@bp.route('/record')
class RecordList(MethodView):
    """Робота зі списком записів витрат"""

    @bp.arguments(RecordQuerySchema, location='query')
    @bp.response(200, RecordSchema(many=True))
    def get(self, query_args):
        """Отримати записи витрат (можна фільтрувати по user_id та/або category_id)"""
        user_id = query_args.get('user_id')
        category_id = query_args.get('category_id')

        query = Record.query

        if user_id:
            query = query.filter_by(user_id=user_id)
        if category_id:
            query = query.filter_by(category_id=category_id)

        records = query.order_by(Record.created_at.desc()).all()
        return records

    @bp.arguments(RecordCreateSchema)
    @bp.response(201, RecordSchema)
    def post(self, record_data):
        """Створити новий запис витрат і списати суму з рахунку"""
        # Перевіряємо чи існує користувач
        user = User.query.get(record_data['user_id'])
        if not user:
            abort(404, message='User not found')
        
        # Перевіряємо чи існує категорія
        category = Category.query.get(record_data['category_id'])
        if not category:
            abort(404, message='Category not found')
        
        # Знаходимо рахунок користувача
        account = Account.query.filter_by(user_id=record_data['user_id']).first()
        if not account:
            abort(400, message='User does not have an account. Create an account first.')
        
        # Перевіряємо чи достатньо коштів
        expense_amount = Decimal(str(record_data['amount']))
        if account.balance < expense_amount:
            abort(400, message='Insufficient funds in account')
        
        # Створюємо запис витрат
        record = Record(**record_data)
        db.session.add(record)
        
        # Списуємо суму з рахунку
        account.balance = Decimal(str(account.balance)) - expense_amount
        
        try:
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            abort(500, message=f'Error creating record: {str(e)}')
        
        return record


@bp.route('/record/<int:record_id>')
class RecordDetail(MethodView):
    """Робота з окремим записом витрат"""

    @bp.response(200, RecordSchema)
    def get(self, record_id):
        """Отримати запис витрат за ID"""
        record = Record.query.get_or_404(record_id, description='Record not found')
        return record

    @bp.arguments(RecordUpdateSchema)
    @bp.response(200, RecordSchema)
    def patch(self, update_data, record_id):
        """Оновити запис витрат"""
        record = Record.query.get_or_404(record_id, description='Record not found')
        
        # Перевіряємо категорію якщо вона оновлюється
        if 'category_id' in update_data:
            category = Category.query.get(update_data['category_id'])
            if not category:
                abort(404, message='Category not found')
        
        # Якщо оновлюється сума, коригуємо баланс рахунку
        if 'amount' in update_data:
            account = Account.query.filter_by(user_id=record.user_id).first()
            if account:
                # Повертаємо стару суму
                account.balance = Decimal(str(account.balance)) + Decimal(str(record.amount))
                # Списуємо нову суму
                new_amount = Decimal(str(update_data['amount']))
                if account.balance < new_amount:
                    db.session.rollback()
                    abort(400, message='Insufficient funds for the new amount')
                account.balance = Decimal(str(account.balance)) - new_amount
        
        # Оновлюємо поля
        for key, value in update_data.items():
            setattr(record, key, value)
        
        try:
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            abort(500, message=f'Error updating record: {str(e)}')
        
        return record

    @bp.response(204)
    def delete(self, record_id):
        """Видалити запис витрат (і повернути суму на рахунок)"""
        record = Record.query.get_or_404(record_id, description='Record not found')
        
        # Знаходимо рахунок користувача
        account = Account.query.filter_by(user_id=record.user_id).first()
        if account:
            # Повертаємо суму на рахунок
            account.balance = Decimal(str(account.balance)) + Decimal(str(record.amount))
        
        try:
            db.session.delete(record)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            abort(500, message=f'Error deleting record: {str(e)}')
