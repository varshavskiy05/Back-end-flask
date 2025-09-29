from flask import Flask


def create_app():
    app = Flask(__name__)

    # импортируем и регистрируем blueprints
    from myapp.users import bp as users_bp
    from myapp.categories import bp as categories_bp
    from myapp.records import bp as records_bp
    from myapp.healthcheck import bp as healthcheck_bp


    app.register_blueprint(users_bp)
    app.register_blueprint(categories_bp)
    app.register_blueprint(records_bp)
    app.register_blueprint(healthcheck_bp)

    return app
