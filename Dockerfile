
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

# Copy the download script into the image
COPY download_model.py /app/download_model.py

# Download the model using the script and the secret
RUN --mount=type=secret,id=huggingface_token \
    echo "--- Docker RUN: Starting model download script /app/download_model.py..." && \
    python /app/download_model.py && \
    echo "--- Docker RUN: Model download script finished." && \
    rm /app/download_model.py # Optional: clean up the script after use

# Copy the rest of your application code AFTER model download
COPY . .

# Expose the port the app runs on
EXPOSE 8000

# Run the application
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]