FROM python:3.8.2-slim

WORKDIR /app
COPY . /app

RUN apt-get update -y \
    && apt-get install -y gcc libpq-dev \
    && pip3 install -r requirements.txt --no-cache-dir \
    && pytest tests -s --cov=. --cov-fail-under 100 --log-cli-level info 
