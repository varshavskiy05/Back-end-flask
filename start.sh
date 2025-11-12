#!/bin/sh
set -e

echo "==> Starting migration process..."

# Сброс alembic_version через Python (если конфликт)
python3 << 'PYTHON_SCRIPT'
import os
from sqlalchemy import create_engine, text

db_url = os.environ.get("DATABASE_URL")
if db_url:
    engine = create_engine(db_url)
    with engine.connect() as conn:
        conn.execute(text("DROP TABLE IF EXISTS alembic_version CASCADE;"))
        conn.commit()
    print("==> Dropped alembic_version table")
PYTHON_SCRIPT

# Инициализация migrations (если нет)
if [ ! -d migrations ]; then
  echo "==> Initializing migrations..."
  flask db init
fi

# Создать папку versions, если её нет
mkdir -p migrations/versions

# Генерация миграции
echo "==> Generating migration..."
flask db migrate -m "autogen" || true

# Применение миграций
echo "==> Applying migrations..."
flask db upgrade

echo "==> Starting gunicorn..."
exec gunicorn "myapp:create_app()" --bind 0.0.0.0:${PORT:-8080}

