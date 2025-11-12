from flask import Flask, jsonify
from flask_smorest import Api
from flask_migrate import Migrate
from myapp.models import db
from flask_jwt_extended import JWTManager
import os


def create_app():
    app = Flask(__name__)
    
    # Завантажуємо конфігурацію
    app.config.from_pyfile('config.py', silent=True)

    # Ініціалізуємо розширення
    db.init_app(app)
    migrate = Migrate(app, db)
    api = Api(app)
    app.config["JWT_SECRET_KEY"] = os.getenv("JWT_SECRET_KEY")
    jwt = JWTManager(app)

    # Імпортуємо та реєструємо blueprints
    from myapp.users import bp as users_bp
    from myapp.categories import bp as categories_bp
    from myapp.records import bp as records_bp
    from myapp.healthcheck import bp as healthcheck_bp
    # Новий blueprint для рахунків
    from myapp.accounts import bp as accounts_bp
    # Новий blueprint для доходів
    from myapp.incomes import bp as incomes_bp
    # Новий blueprint для аутентифікації
    from myapp.auth import bp as auth_bp

    api.register_blueprint(users_bp)
    api.register_blueprint(categories_bp)
    api.register_blueprint(records_bp)
    api.register_blueprint(accounts_bp)
    api.register_blueprint(incomes_bp)
    api.register_blueprint(auth_bp)
    app.register_blueprint(healthcheck_bp)

    # JWT error handlers
    @jwt.expired_token_loader
    def expired_token_callback(jwt_header, jwt_payload):
        return jsonify({"message": "The token has expired.", "error": "token_expired"}), 401

    @jwt.invalid_token_loader
    def invalid_token_callback(error):
        return jsonify({"message": "Signature verification failed.", "error": "invalid_token"}), 401

    @jwt.unauthorized_loader
    def missing_token_callback(error):
        return jsonify({"description": "Request does not contain an access token.", "error": "authorization_required"}), 401

    return app
