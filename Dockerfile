# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set the working directory
WORKDIR /app

# Define where the model will be stored in the image
ENV MODEL_DIR=/app/pretrain_model
ENV HF_HUB_DISABLE_SYMLINKS_WARNING=1

# Copy the requirements file
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Download the model using the secret
RUN --mount=type=secret,id=huggingface_token \
    echo "Downloading Hugging Face model to ${MODEL_DIR}..." && \
    python -c "from huggingface_hub import snapshot_download; token = open('/run/secrets/huggingface_token').read().strip(); snapshot_download(repo_id='speakleash/Bielik-1.5B-v3.0-Instruct', local_dir='${MODEL_DIR}', token=token, local_dir_use_symlinks=False, resume_download=True, ignore_patterns=['*.fp16.safetensors', '*.gguf'])" && \
    echo "Model download complete."

# Copy the rest of your application code AFTER model download
COPY . .

# Expose the port the app runs on
EXPOSE 8000

# Run the application
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]