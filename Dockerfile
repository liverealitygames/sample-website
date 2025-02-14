FROM python:3.13-slim

WORKDIR /app

COPY src/lrg/requirements.txt .
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

COPY src/lrg .

CMD ["gunicorn", "lrg.wsgi:application", "--bind", "0.0.0.0:8080"]