from flask import Blueprint

bp = Blueprint('records', __name__)
from myapp.records import routes