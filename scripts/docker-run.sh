#!/bin/sh -e

docker run -it \
  -p 8088:8088 \
  -e GALILEO_DATABASE_URL_WRITE="postgresql+psycopg2://galileo:dataquality@host.docker.internal:5432/galileo" \
  -e GALILEO_DATABASE_URL_READ="postgresql+psycopg2://galileo:dataquality@host.docker.internal:5432/galileo" \
  -e GALILEO_API_SECRET_KEY="pancakes" \
  -e GALILEO_MINIO_FQDN="host.docker.internal:9000" \
  -e GALILEO_MINIO_REGION="us-east-1" \
  -e GALILEO_MINIO_ENDPOINT_URL="http://host.docker.internal:9000" \
  -e GALILEO_MINIO_K8S_SVC_ADDR="http://minio.galileo:9000" \
  -e GALILEO_MINIO_ACCESS_KEY="minioadmin" \
  -e GALILEO_MINIO_SECRET_KEY="minioadmin" \
  -e GALILEO_CONSOLE_URL="http://host.docker.internal:3000" \
  -e PROMETHEUS_MULTIPROC_DIR="galileo-prometheus-metrics" \
  -e GALILEO_HEADLESS_API_SVC_DNS="localhost" \
  gcr.io/rungalileo-dev/api:latest
