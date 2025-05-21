# PowerShell script to build and run the Docker container for your FastAPI service

# Set variables
$imageName = "bielik-fastapi-service"
$containerName = "bielik_app_instance"
$tokenFile = "my_hf_token.txt"

Write-Host "Building Docker image..."
docker build --secret id=huggingface_token,src=$tokenFile -t $imageName .

Write-Host "Stopping and removing any existing container named $containerName..."
docker stop $containerName | Out-Null 2>&1

docker rm $containerName | Out-Null 2>&1

Write-Host "Running new container..."
docker run -d --name $containerName -p 8000:8000 $imageName

Write-Host ""
Write-Host "$containerName should be starting up."
Write-Host "You can view logs with: docker logs $containerName -f"
Write-Host "To stop the container, run: docker stop $containerName"
Write-Host "The service will be available at http://127.0.0.1:8000"
