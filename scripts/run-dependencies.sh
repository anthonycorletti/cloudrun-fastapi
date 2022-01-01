#!/bin/sh -ex

echo "running cloudrunfastapi-postgres"
docker run --rm --name=cloudrunfastapi-postgres -d -p 5432:5432 \
-e POSTGRES_USER=cloud \
-e POSTGRES_PASSWORD=run \
-e POSTGRES_HOST_AUTH_METHOD=password \
-e POSTGRES_DB=cloudrunfastapi \
postgres:10.5
