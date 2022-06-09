#!/bin/sh -e

pip install --upgrade pip
pip install flit

flit install --deps=all --extras=all --symlink
pre-commit install
