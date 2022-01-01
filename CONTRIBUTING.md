# How to contribute!

#### **Did you find a bug?**

- **Ensure the bug was not already reported** by searching on GitHub under [Issues](https://github.com/anthonycorletti/cloudrun-fastapi/issues).

- If you're unable to find an open issue addressing the problem, [open a new one](https://github.com/anthonycorletti/cloudrun-fastapi/issues/new). Be sure to include a **title and clear description**, as much relevant information as possible, and a **code sample** or an **executable test case** demonstrating the expected behavior that is not occurring.

#### **Did you write a patch that fixes a bug?**

- Open a new GitHub pull request with the patch.

- Ensure the PR description clearly describes the problem and solution. Include the relevant issue number if applicable.

#### **Did you fix whitespace, format code, or make a purely cosmetic patch?**

Changes that are cosmetic in nature and do not add anything substantial to the stability, functionality, or testability of this codebase and will generally not be accepted.

Thanks! Read on for technical details below to get your environment ready to build.

# Technical Guide

Assuming you have cloned this repository to your local machine, you can follow these guidelines to make contributions.

**First, please install pyenv https://github.com/pyenv/pyenv to manage your python environment.**

Install the version of python as mentioned in this repo.

```sh
pyenv install $(cat .python-version)
```

## Use a virtual environment

```sh
python -m venv .venv
```

This will create a directory `.venv` with python binaries and then you will be able to install packages for that isolated environment.

Next, activate the environment.

```sh
source .venv/bin/activate
```

To check that it worked correctly;

```sh
which python pip
```

You should see paths that use the .venv/bin in your current working directory.

## Installing with Flit

This project uses `flit` to manage our project's dependencies.

Install dependencies, including flit.

```sh
./scripts/install.sh
pyenv rehash
```

## Formatting

```sh
./scripts/format.sh
```

## Tests

```sh
./scripts/test.sh
```

## Running local dependencies (postgres), you will need to install psql

```sh
./scripts/run-dependencies.sh
```

## Working with Postgres

We are using alembic to facilitate migrations with PostgreSQL. As this template stands, we are using the default user `postgres` and database `postgres`. We suggest you use your own user, password, and database for production.

To create your migrations locally (from a virtualenv!):

```sh
# create the migration
alembic revision --autogenerate -m "initial setup"
# apply the migration
alembic upgrade head
# view history
alembic current -vvv
alembic history -vvv
```

To create your migrations on a cloudsql instance:

```sh
cloud_sql_proxy -instances=${PROJECT_ID}:${REGION}:${DB_INSTANCE_NAME}=tcp:5432 -dir=/tmp/cloudsql
# then simply upgrade to head
./scripts/run-alembic-upgrade-head.sh
```

If you want to directly connect to the remote database, while the proxy is running in one session, run the following command in another shell session:

```sh
psql "sslmode=disable host=localhost user=postgres dbname=postgres"
```
