from flask.views import MethodView
from flask_smorest import abort
from flask import request
from flask_jwt_extended import jwt_required
from myapp.incomes import bp
from myapp.models import db, Income, User, Account
from myapp.schemas import IncomeSchema, IncomeCreateSchema
from decimal import Decimal


@bp.route('/income')
class IncomeList(MethodView):
    """Робота зі списком доходів"""

    @bp.response(200, IncomeSchema(many=True))
    @jwt_required()
    def get(self):
        """Отримати всі доходи (з фільтрацією по user_id)"""
        user_id = request.args.get('user_id', type=int)
        
        query = Income.query
        if user_id:
            query = query.filter_by(user_id=user_id)
        
        incomes = query.order_by(Income.created_at.desc()).all()
        return incomes

    @bp.arguments(IncomeCreateSchema)
    @bp.response(201, IncomeSchema)
    @jwt_required()
    def post(self, income_data):
        """Створити новий дохід і автоматично додати його до рахунку користувача"""
        # Перевіряємо чи існує користувач
        user = User.query.get(income_data['user_id'])
        if not user:
            abort(404, message='User not found')
        
        # Перевіряємо чи є рахунок у користувача
        account = Account.query.filter_by(user_id=income_data['user_id']).first()
        if not account:
            abort(400, message='User does not have an account. Create an account first.')
        
        # Створюємо дохід
        income = Income(**income_data)
        db.session.add(income)
        
        # Додаємо суму до балансу рахунку
        account.balance = Decimal(str(account.balance)) + Decimal(str(income_data['amount']))
        
        try:
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            abort(500, message=f'Error creating income: {str(e)}')
        
        return income


@bp.route('/income/<int:income_id>')
class IncomeDetail(MethodView):
    """Робота з окремим доходом"""

    @bp.response(200, IncomeSchema)
    @jwt_required()
    def get(self, income_id):
        """Отримати дохід за ID"""
        income = Income.query.get_or_404(income_id, description='Income not found')
        return income

    @bp.response(204)
    @jwt_required()
    def delete(self, income_id):
        """Видалити дохід (і відняти суму з рахунку)"""
        income = Income.query.get_or_404(income_id, description='Income not found')
        
        # Знаходимо рахунок користувача
        account = Account.query.filter_by(user_id=income.user_id).first()
        if account:
            # Віднімаємо суму з балансу
            account.balance = Decimal(str(account.balance)) - Decimal(str(income.amount))
            
            # Перевіряємо чи баланс не став негативним
            if account.balance < 0:
                db.session.rollback()
                abort(400, message='Cannot delete income: account balance would become negative')
        
        try:
            db.session.delete(income)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            abort(500, message=f'Error deleting income: {str(e)}')

