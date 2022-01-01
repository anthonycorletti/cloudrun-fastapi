#!/bin/sh -e

docker run -it \
  -p 8080:8080 \
  -e DATABASE_URL="postgresql+psycopg2://cloud:run@host.docker.internal:5432/cloudrunfastapi" \
  -e API_SECRET_KEY="cloudrunfastapi" \
  anthonycorletti/cloudrunfastapi:latest
