#!/bin/sh -ex

mypy cloudrunfastapi
flake8 cloudrunfastapi tests
black cloudrunfastapi tests --check
isort cloudrunfastapi tests scripts --check-only
