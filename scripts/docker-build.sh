#!/bin/sh -e

IMAGE_VERSION=${IMAGE_VERSION:=latest}
docker build -t "anthonycorletti/cloudrunfastapi:${IMAGE_VERSION}" .
