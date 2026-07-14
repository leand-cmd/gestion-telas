FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN mkdir -p uploads/productos

ENV PORT=5000
EXPOSE 5000

CMD flask db upgrade && gunicorn --bind 0.0.0.0:${PORT} --workers 4 --timeout 120 wsgi:app
