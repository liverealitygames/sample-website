FROM python:3.13-slim

WORKDIR /app

RUN apt-get update && apt-get install -y postgresql-client dos2unix && rm -rf /var/lib/apt/lists/*

COPY src/lrg .
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt
RUN dos2unix scripts/full_reset.sh

CMD ["gunicorn", "lrg.wsgi:application", "--bind", "0.0.0.0:8080"]
