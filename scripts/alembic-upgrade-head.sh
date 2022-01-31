#!/bin/sh -ex

echo "running alembic migrations"
alembic upgrade head
