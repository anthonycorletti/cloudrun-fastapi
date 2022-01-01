#!/bin/sh -ex

echo "exporting local environment variables"

export DATABASE_URL="postgresql+psycopg2://cloud:run@127.0.0.1:5432/cloudrunfastapi"
export API_SECRET_KEY="cloudrunfastapi"
