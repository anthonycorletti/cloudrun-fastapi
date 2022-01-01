#!/bin/sh -ex

# Sort imports one per line, so autoflake can remove unused imports
isort --force-single-line-imports cloudrunfastapi tests scripts

autoflake --remove-all-unused-imports --recursive --remove-unused-variables --in-place cloudrunfastapi tests scripts --exclude=__init__.py
black cloudrunfastapi tests scripts
isort cloudrunfastapi tests scripts
