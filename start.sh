#!/bin/sh
set -e

echo "==> Starting migration process..."

# Сброс alembic_version, если есть конфликт версий
psql "$DATABASE_URL" -c "DROP TABLE IF EXISTS alembic_version;" || true

# Инициализация migrations (если нет)
if [ ! -d migrations ]; then
  echo "==> Initializing migrations..."
  flask db init
fi

# Генерация миграции
echo "==> Generating migration..."
flask db migrate -m "autogen" || true

# Применение миграций
echo "==> Applying migrations..."
flask db upgrade

echo "==> Starting gunicorn..."
exec gunicorn "myapp:create_app()" --bind 0.0.0.0:${PORT:-8080}

