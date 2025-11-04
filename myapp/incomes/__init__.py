from flask_smorest import Blueprint

bp = Blueprint('incomes', __name__, url_prefix='/api', description='Operations on incomes')

from myapp.incomes import routes

