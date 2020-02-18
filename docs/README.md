# cloudrun-fastapi Docs

## Contents

- [Usage](#Usage)

Future Features:

- Testing with Pytest
- Deployment with CloudBuild, Triggers, and GitHub
- DNS Setup with Managed Domain Mappings
- PostgreSQL connection and migrations with Alembic
- Secrets Management with Google Cloud Secrets Manager
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
TESTING=True PYTHONPATH=. pytest tests -s --cov=. --cov-report html:./htmlcov --cov-fail-under 80 --log-cli-level DEBUG
# view coverage output
open htmlcov/index.html
```
