FROM python:3.9.6-slim

WORKDIR /api
COPY . /api

RUN apt-get update -y \
    && apt-get install build-essential -y \
    && rm -rf /var/lib/apt/lists/* \
    && pip install flit \
    && FLIT_ROOT_INSTALL=1 flit install --deps production \
    && rm -rf $(pip cache dir)

CMD uvicorn cloudrunfastapi.main:api --host 0.0.0.0 --port 80
