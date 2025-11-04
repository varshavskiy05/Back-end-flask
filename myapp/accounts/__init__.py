from flask_smorest import Blueprint

bp = Blueprint('accounts', __name__, url_prefix='/api', description='Operations on accounts')

from myapp.accounts import routes

