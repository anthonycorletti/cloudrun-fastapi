#!/bin/sh -e

. ./scripts/set-local-env.sh

uvicorn cloudrunfastapi.main:api --reload
