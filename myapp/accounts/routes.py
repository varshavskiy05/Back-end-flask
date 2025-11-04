from decimal import Decimal

from flask.views import MethodView
from flask_smorest import abort

from myapp.accounts import bp
from myapp.models import db, Account, User
from myapp.schemas import AccountSchema, AccountCreateSchema, AccountUpdateSchema


@bp.route('/account')
class AccountList(MethodView):
    """Робота зі списком рахунків"""

    @bp.response(200, AccountSchema(many=True))
    def get(self):
        """Отримати всі рахунки"""
        accounts = Account.query.all()
        return accounts

    @bp.arguments(AccountCreateSchema)
    @bp.response(201, AccountSchema)
    def post(self, account_data):
        """Створити новий рахунок"""
        # Перевіряємо чи існує користувач
        user = User.query.get(account_data['user_id'])
        if not user:
            abort(404, message='User not found')
        
        # Перевіряємо чи у користувача вже є рахунок
        if Account.query.filter_by(user_id=account_data['user_id']).first():
            abort(400, message='User already has an account')
        
        balance_value = Decimal(str(account_data.get('balance', '0.00')))
        account = Account(user_id=account_data['user_id'], balance=balance_value)
        db.session.add(account)
        
        try:
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            abort(500, message=f'Error creating account: {str(e)}')
        
        return account


@bp.route('/account/<int:account_id>')
class AccountDetail(MethodView):
    """Робота з окремим рахунком"""

    @bp.response(200, AccountSchema)
    def get(self, account_id):
        """Отримати рахунок за ID"""
        account = Account.query.get_or_404(account_id, description='Account not found')
        return account

    @bp.arguments(AccountUpdateSchema)
    @bp.response(200, AccountSchema)
    def patch(self, update_data, account_id):
        """Оновити рахунок"""
        account = Account.query.get_or_404(account_id, description='Account not found')
        
        # Перевіряємо баланс (не дозволяємо негативний)
        if 'balance' in update_data:
            balance_value = Decimal(str(update_data['balance']))
            if balance_value < 0:
                abort(400, message='Balance cannot be negative')
            account.balance = balance_value
        
        try:
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            abort(500, message=f'Error updating account: {str(e)}')
        
        return account

    @bp.response(204)
    def delete(self, account_id):
        """Видалити рахунок"""
        account = Account.query.get_or_404(account_id, description='Account not found')
        
        try:
            db.session.delete(account)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            abort(500, message=f'Error deleting account: {str(e)}')


@bp.route('/account/user/<int:user_id>')
class AccountByUser(MethodView):
    """Отримати рахунок користувача"""

    @bp.response(200, AccountSchema)
    def get(self, user_id):
        """Отримати рахунок користувача за user_id"""
        account = Account.query.filter_by(user_id=user_id).first()
        if not account:
            abort(404, message='Account not found for this user')
        return account

