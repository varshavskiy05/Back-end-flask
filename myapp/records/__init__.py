from flask_smorest import Blueprint

bp = Blueprint('records', __name__, url_prefix='/api', description='Operations on expense records')
from myapp.records import routes