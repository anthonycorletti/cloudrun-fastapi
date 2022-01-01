#!/bin/sh -e

REGISTRY_NAME="gcr.io"
GCP_PROJECT="${GCP_PROJECT:=rungalileo-dev}"

IMAGE_NAME="${GCP_PROJECT}/api"
IMAGE_VERSION=${IMAGE_VERSION:=latest}

docker push "${REGISTRY_NAME}/${IMAGE_NAME}:${IMAGE_VERSION}"
