FROM python:3.11.3-slim-bullseye

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . /app

CMD flask --app myapp run -h 0.0.0.0 -p $PORT

