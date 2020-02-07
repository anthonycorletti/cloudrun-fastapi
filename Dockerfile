FROM python:3.7-slim

RUN apt-get update -y \
    && apt-get install -y gcc libpq-dev

WORKDIR /app
COPY . /app

RUN pip3 install -r requirements.txt

CMD gunicorn main:api -c gunicorn_config.py
