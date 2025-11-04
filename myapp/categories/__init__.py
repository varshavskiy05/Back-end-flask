from flask_smorest import Blueprint

bp = Blueprint('categories', __name__, url_prefix='/api', description='Operations on categories')

from myapp.categories import routes
