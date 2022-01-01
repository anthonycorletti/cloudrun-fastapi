#!/bin/sh -e

. ./scripts/set-local-env.sh

gunicorn cloudrunfastapi.main:api -c cloudrunfastapi/gunicorn_config.py
