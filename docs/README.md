# cloudrun-fastapi Docs

Future Features:

- Testing with Pytest
- PostgreSQL connection and migrations with Alembic
- Secrets Management with Google Cloud Secrets Manager
- Deployment with CloudBuild, Triggers, and GitHub
- DNS Setup with Managed Domain Mappings
- Oauth & JWT Authentication and Authorization
- Google Cloud PubSub Integration
- Google Cloud Scheduler Integration

#### Local Development

```sh
pip3 install -r requirements.txt
# running with uvicorn, not recommended in production, better for development
uvicorn main:api --reload
# running with gunicorn, recommended for production
gunicorn main:api -c gunicorn_config.py
```

#### Secrets manager

It's suggested that you reauth with the following to use secrets manager locally `gcloud auth application-default login`.

Remotely, you will have to configure Cloud Run and Cloud Build service accounts to have Secret Manager Secret Accessor permissions. In this example we are using the default Compute (GCE) service account for Cloud Run services.

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

#### CloudBuild, Deployment, running a live Cloud Run service

To deploy this API to Cloud Run, you will need to have the following

- enable GCP's GitHub Integration for your repo
- have a PostgreSQL instance created in GCP that you will use for the service
- two cloud build triggers that refer the right cloudsql db instance name
