from flask import Blueprint

bp = Blueprint("categories", __name__)

from myapp.categories import routes
