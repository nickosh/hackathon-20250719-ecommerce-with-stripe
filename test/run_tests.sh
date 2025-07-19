#!/bin/bash
set -e

# Function to load .env file
load_env() {
    if [ -f .env ]; then
        set -a
        source .env
        set +a
    fi
}

# Load .env file
load_env

# Configuration
IMAGE_NAME=${PLAYWRIGHT_IMAGE_NAME:-playwright-pytest}
CONTAINER_NAME=${PLAYWRIGHT_CONTAINER_NAME:-playwright-pytest-runner}
PLAYWRIGHT_VERSION=${PLAYWRIGHT_CONTAINER_VERSION:-v1.45.0-jammy}


# Build the Docker image
docker build --build-arg PLAYWRIGHT_CONTAINER_VERSION=$PLAYWRIGHT_VERSION -t $IMAGE_NAME .

# Run the tests
docker run --rm \
    --name $CONTAINER_NAME \
    -v "$(pwd):/tests" \
    -w /tests \
    $IMAGE_NAME \
    -v tests
