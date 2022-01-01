#!/bin/sh -e

REGISTRY_NAME="ghcr.io"
IMAGE_NAME="cloudrunfastapi/cloudrunfastapi"
IMAGE_VERSION=${IMAGE_VERSION:=latest}

docker push "${REGISTRY_NAME}/${IMAGE_NAME}:${IMAGE_VERSION}"
