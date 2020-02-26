# cloudrun-fastapi Docs

## Contents

- [Usage](#Usage)

Future Features:

- Testing with Pytest
- PostgreSQL connection and migrations with Alembic
- Secrets Management with Google Cloud Secrets Manager
- Deployment with CloudBuild, Triggers, and GitHub
- DNS Setup with Managed Domain Mappings
- Oauth & JWT Authentication and Authorization
- Google Cloud PubSub Integration
- Google Cloud Scheduler Integration

## Usage

#### Local Development

```sh
pip3 install -r requirements.txt
# running with uvicorn, not recommended in production, better for development
uvicorn main:api --reload
# running with gunicorn, recommended for production
gunicorn main:api -c gunicorn_config.py
```

#### Testing Locally

```sh
TESTING=True PYTHONPATH=. pytest tests -s --cov=. --cov-report html:./htmlcov --cov-fail-under 100 --log-cli-level DEBUG
# view coverage output
open htmlcov/index.html
```

#### Working with Postgres

We are using alembic to facilitate migrations with PostgreSQL. As this template stands, we are using the default user `postgres` and database `postgres`. We suggest you use your own user, password, and database for production.

To create your migrations locally:

```sh
# create the migration
PYTHONPATH=. alembic revision --autogenerate -m "initial setup"
# apply the migration
PYTHONPATH=. alembic upgrade head
# view history
PYTHONPATH=. alembic current -vvv
PYTHONPATH=. alembic history -vvv
```

To create your migrations on a cloudsql instance:

```sh
cloud_sql_proxy -instances=PROJECT_ID:REGION:INSTANCE_NAME -dir=/tmp/cloudsql
# then run the commands as listed above
```

If you want to directly connect to the remote database, while the proxy is running on one process;

```sh
psql "sslmode=disable host=/tmp/cloudsql/PROJECT_ID:REGION:INSTANCE_NAME user=postgres dbname=postgres"
```

#### Docker and Google Container Registry

```sh
docker build -t us.gcr.io/$PROJECT_ID/cloud_run_fastapi .
docker run -p 8000:8000 -it us.gcr.io/$PROJECT_ID/cloud_run_fastapi:latest
docker push us.gcr.io/$PROJECT_ID/cloud_run_fastapi
```
