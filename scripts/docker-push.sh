#!/bin/sh -e

IMAGE_VERSION=${IMAGE_VERSION:=latest}
docker push "anthonycorletti/cloudrunfastapi:${IMAGE_VERSION}"
