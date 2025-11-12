from flask.views import MethodView
from flask_smorest import abort
from sqlalchemy import func

from myapp.categories import bp
from myapp.models import db, Category
from myapp.schemas import CategorySchema, CategoryCreateSchema, CategoryUpdateSchema
from flask_jwt_extended import jwt_required


@bp.route('/category')
class CategoryList(MethodView):
    """Робота зі списком категорій"""

    @bp.response(200, CategorySchema(many=True))
    @jwt_required()
    def get(self):
        """Отримати всі категорії"""
        categories = Category.query.order_by(Category.name.asc()).all()
        return categories

    @bp.arguments(CategoryCreateSchema)
    @bp.response(201, CategorySchema)
    @jwt_required()
    def post(self, category_data):
        """Створити нову категорію"""
        existing = Category.query.filter(func.lower(Category.name) == category_data['name'].lower()).first()
        if existing:
            abort(400, message='Category with this name already exists')

        category = Category(**category_data)
        db.session.add(category)
        
        try:
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            abort(500, message=f'Error creating category: {str(e)}')
        
        return category


@bp.route('/category/<int:category_id>')
class CategoryDetail(MethodView):
    """Робота з окремою категорією"""

    @bp.response(200, CategorySchema)
    @jwt_required()
    def get(self, category_id):
        """Отримати категорію за ID"""
        category = Category.query.get_or_404(category_id, description='Category not found')
        return category

    @bp.arguments(CategoryUpdateSchema)
    @bp.response(200, CategorySchema)
    @jwt_required()
    def patch(self, update_data, category_id):
        """Оновити категорію"""
        category = Category.query.get_or_404(category_id, description='Category not found')
        
        # Оновлюємо поля
        for key, value in update_data.items():
            setattr(category, key, value)
        
        try:
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            abort(500, message=f'Error updating category: {str(e)}')
        
        return category

    @bp.response(204)
    @jwt_required()
    def delete(self, category_id):
        """Видалити категорію"""
        category = Category.query.get_or_404(category_id, description='Category not found')
        
        # Перевіряємо чи не використовується категорія
        if category.records:
            abort(400, message='Cannot delete category that has records')
        
        try:
            db.session.delete(category)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            abort(500, message=f'Error deleting category: {str(e)}')
