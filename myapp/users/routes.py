from flask.views import MethodView
from flask_smorest import abort
from flask_jwt_extended import jwt_required
from myapp.users import bp
from myapp.models import db, User
from myapp.schemas import UserSchema, UserCreateSchema, UserUpdateSchema


@bp.route('/user')
class UserList(MethodView):
    """Робота зі списком користувачів"""

    @bp.response(200, UserSchema(many=True))
    @jwt_required()
    def get(self):
        """Отримати всіх користувачів"""
        users = User.query.all()
        return users

    @bp.arguments(UserCreateSchema)
    @bp.response(201, UserSchema)
    @jwt_required()
    def post(self, user_data):
        """Створити нового користувача"""
        user = User(**user_data)
        db.session.add(user)
        
        try:
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            abort(500, message=f'Error creating user: {str(e)}')
        
        return user


@bp.route('/user/<int:user_id>')
class UserDetail(MethodView):
    """Робота з окремим користувачем"""

    @bp.response(200, UserSchema)
    @jwt_required()
    def get(self, user_id):
        """Отримати користувача за ID"""
        user = User.query.get_or_404(user_id, description='User not found')
        return user

    @bp.arguments(UserUpdateSchema)
    @bp.response(200, UserSchema)
    @jwt_required()
    def patch(self, update_data, user_id):
        """Оновити користувача"""
        user = User.query.get_or_404(user_id, description='User not found')
        
        # Оновлюємо поля
        for key, value in update_data.items():
            setattr(user, key, value)
        
        try:
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            abort(500, message=f'Error updating user: {str(e)}')
        
        return user

    @bp.response(204)
    @jwt_required()
    def delete(self, user_id):
        """Видалити користувача"""
        user = User.query.get_or_404(user_id, description='User not found')
        
        try:
            db.session.delete(user)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            abort(500, message=f'Error deleting user: {str(e)}')
