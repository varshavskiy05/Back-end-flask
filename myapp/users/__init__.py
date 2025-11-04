from flask_smorest import Blueprint

bp = Blueprint('users', __name__, url_prefix='/api', description='Operations on users')

from myapp.users import routes