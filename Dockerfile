FROM python:3.11-slim
WORKDIR /app

COPY requirements.txt .
RUN python -m pip install --upgrade pip setuptools wheel \
 && pip install --no-cache-dir -r requirements.txt

COPY . /app
ENV FLASK_APP=myapp FLASK_ENV=production

SHELL ["/bin/sh","-lc"]
CMD if [ ! -d migrations ]; then flask db init; fi; \
    flask db migrate -m autogen || true; \
    flask db upgrade; \
    exec gunicorn "myapp:create_app()" --bind 0.0.0.0:${PORT:-8080}
