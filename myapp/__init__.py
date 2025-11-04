from flask import Flask
from flask_smorest import Api
from flask_migrate import Migrate
from myapp.models import db


def create_app():
    app = Flask(__name__)
    
    # Завантажуємо конфігурацію
    app.config.from_pyfile('config.py', silent=True)

    # Ініціалізуємо розширення
    db.init_app(app)
    migrate = Migrate(app, db)
    api = Api(app)

    # Імпортуємо та реєструємо blueprints
    from myapp.users import bp as users_bp
    from myapp.categories import bp as categories_bp
    from myapp.records import bp as records_bp
    from myapp.healthcheck import bp as healthcheck_bp
    # Новий blueprint для рахунків
    from myapp.accounts import bp as accounts_bp
    # Новий blueprint для доходів
    from myapp.incomes import bp as incomes_bp

    api.register_blueprint(users_bp)
    api.register_blueprint(categories_bp)
    api.register_blueprint(records_bp)
    api.register_blueprint(accounts_bp)
    api.register_blueprint(incomes_bp)
    app.register_blueprint(healthcheck_bp)

    return app
