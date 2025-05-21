#!/bin/bash

IMAGE_NAME="bielik-fastapi-service"
CONTAINER_NAME="bielik_app_instance"
TOKEN_FILE="my_hf_token.txt"

# Build the Docker image with Hugging Face token as a secret
echo "Building Docker image..."
DOCKER_BUILDKIT=1 docker build --secret id=huggingface_token,src=$TOKEN_FILE -t $IMAGE_NAME .

echo "Attempting to stop and remove existing container named $CONTAINER_NAME (if any)..."
docker stop $CONTAINER_NAME > /dev/null 2>&1 || true # Stop if running, ignore error if not
docker rm $CONTAINER_NAME > /dev/null 2>&1 || true   # Remove if exists, ignore error if not

echo "Starting new $IMAGE_NAME container as $CONTAINER_NAME..."
docker run -d --name $CONTAINER_NAME -p 8000:8000 $IMAGE_NAME
# -d : Runs the container in detached mode (in the background)
# --name : Assigns a specific name to your running container instance
# -p 8000:8000 : Maps port 8000 on your host to port 8000 in the container

echo ""
echo "$CONTAINER_NAME should be starting up."
echo "You can view logs with: docker logs $CONTAINER_NAME -f"
echo "To stop the container, run: docker stop $CONTAINER_NAME"
echo "The service will be available at http://127.0.0.1:8000"