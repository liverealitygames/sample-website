FROM python:3.13-slim

WORKDIR /app

# Install PostgreSQL client (psql)
RUN apt-get update && apt-get install -y postgresql-client && rm -rf /var/lib/apt/lists/*

COPY src/lrg/requirements.txt .
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

COPY src/lrg .

CMD ["gunicorn", "lrg.wsgi:application", "--bind", "0.0.0.0:8080"]