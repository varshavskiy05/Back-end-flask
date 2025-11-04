import os
from dotenv import load_dotenv

# Завантажуємо змінні середовища з .env файлу
load_dotenv()

# Database configuration
SQLALCHEMY_DATABASE_URI = os.getenv(
    'DATABASE_URL',
    f"postgresql://{os.getenv('DB_USER', 'postgres')}:"
    f"{os.getenv('DB_PASSWORD', 'postgres')}@"
    f"{os.getenv('DB_HOST', 'localhost')}:5432/"
    f"{os.getenv('DB_NAME', 'expenses_db')}"
)
SQLALCHEMY_TRACK_MODIFICATIONS = False

# Flask-Smorest configuration
API_TITLE = "Expenses API"
API_VERSION = "v2.0.0"
OPENAPI_VERSION = "3.0.2"
OPENAPI_URL_PREFIX = "/"
OPENAPI_SWAGGER_UI_PATH = "/swagger-ui"
OPENAPI_SWAGGER_UI_URL = "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"

# Secret key for sessions
SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')

