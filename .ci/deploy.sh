#!/bin/bash
set -e

echo "$DOCKER_PASSWORD" | docker login -u "$DOCKER_USERNAME" --password-stdin

if [ ! -z "${TRAVIS_TAG}" ]; then
    export IMAGE_VERSION=${TRAVIS_TAG}
fi

make push-image

if [ "$(uname -m)" != "x86_64" ]; then
	echo "Running on $(uname -m), skip pushing manifest"
	exit 0
fi

make push-manifest

