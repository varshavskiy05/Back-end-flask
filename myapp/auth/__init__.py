from flask_smorest import Blueprint

bp = Blueprint('auth', __name__, url_prefix='/api', description='Authentication endpoints')

from myapp.auth import routes


