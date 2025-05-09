# LLM Car Description Enhancer (Polish)

This repository contains a FastAPI application that utilizes a Hugging Face Transformers Large Language Model (specifically, `speakleash/Bielik-1.5B-v3.0-Instruct` or a similar model from the Bielik series) to generate enhanced marketing descriptions for cars, primarily in Polish.

The application is designed to be run locally for development or containerized using Docker for deployment. The LLM is baked into the Docker image for self-contained and efficient execution, which may require Hugging Face Hub authentication during the build process if the model is gated.

## Features

- Generate enhanced marketing descriptions for cars in Polish.
- Utilizes the `speakleash/Bielik-1.5B-v3.0-Instruct` model via the Hugging Face `transformers` library.
- Health check endpoint.
- Docker support for easy deployment, with the model included in the image.
- Includes a `start_container.sh` script for convenient container startup.

## Prerequisites

- Python 3.9 or higher
- `pip` (Python package installer)
- Docker (for containerized deployment, Docker BuildKit enabled recommended for secrets)
- Git (for cloning the repository)
- A Hugging Face Hub account and an access token (with `read` permissions) if the chosen model is gated (see Docker Usage section).
- For using `start_container.sh`: A bash-compatible shell (like those on Linux, macOS, or Git Bash on Windows).

## Project Structure

A typical layout for this project would be:

```text
.
├── app/
│   ├── __init__.py
│   ├── main.py                   # FastAPI application, endpoints
│   ├── models/
│   │   ├── __init__.py
│   │   └── huggingface_service.py  # Service for interacting with the LLM
│   └── schemas/
│       ├── __init__.py
│       └── schemas.py              # Pydantic schemas for request/response
├── .gitignore
├── Dockerfile
├── download_model.py             # Script to download model during Docker build
├── my_hf_token.txt               # (Example, should be in .gitignore) For storing HF token
├── requirements.txt
├── start_container.sh            # Helper script to run the Docker container
└── README.md

```

## Installation (Local Development)

1.  **Clone the repository:**
    ```bash
    git clone [https://github.com/studzin-sky/llm-description-enhancer.git](https://github.com/studzin-sky/llm-description-enhancer.git)
    cd llm-description-enhancer
    ```

2.  **Create and activate a virtual environment:**
    (Recommended to keep dependencies isolated)
    ```bash
    python -m venv venv
    ```
    * On macOS/Linux:
        ```bash
        source venv/bin/activate
        ```
    * On Windows (PowerShell):
        ```bash
        .\venv\Scripts\Activate.ps1
        ```
    * On Windows (Command Prompt):
        ```bash
        venv\Scripts\activate.bat
        ```

3.  **Install the required dependencies:**
    Ensure your `requirements.txt` includes `fastapi`, `uvicorn[standard]`, `transformers[torch]`, `torch`, `accelerate`, and `huggingface_hub`.
    ```bash
    pip install -r requirements.txt
    ```
    *Note: The first time you run the application locally (or if the model cache is empty), the Hugging Face model (~3.2GB) will be downloaded. This might take some time. **If the model (`speakleash/Bielik-1.5B-v3.0-Instruct` or the one configured) is gated or requires authentication, you may need to log in using `huggingface-cli login` in your terminal before running the application locally.** After logging in, your token will be cached by the `huggingface_hub` library.*

## Usage (Local Development)

1.  **Start the FastAPI server:**
    From the project root directory:
    ```bash
    uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
    ```
    * `--reload` enables auto-reloading for development.
    * `--host 0.0.0.0` makes the server accessible on your network.

2.  **Access the application:**
    * Health Check: [http://127.0.0.1:8000/health](http://127.0.0.1:8000/health)
    * API Documentation (Swagger UI): [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
    * Enhance Description: `POST` requests to [http://127.0.0.1:8000/enhance-description](http://127.0.0.1:8000/enhance-description)

## Docker Usage

The included `Dockerfile` builds an image with the application and the pre-downloaded Hugging Face model, making it self-contained. Downloading gated models during the build process requires a Hugging Face Hub token.

1.  **Prepare Hugging Face Hub Token (for Gated Models):**
    The `speakleash/Bielik-1.5B-v3.0-Instruct` model may require authentication to download.
    * **Get a Token:**
        1.  Go to your Hugging Face account settings: [https://huggingface.co/settings/tokens](https://huggingface.co/settings/tokens)
        2.  Create a new token (e.g., named "docker-bielik-access") with `read` permissions.
        3.  Copy the generated token (it will start with `hf_`).
    * **Create Token File:**
        1.  In your project's root directory (next to your `Dockerfile`), create a file named `my_hf_token.txt`.
        2.  Paste **only the token string** (e.g., `hf_YourActualTokenValueHere`) into this file. Do not add any other text or variable names.
        3.  **Important:** Add `my_hf_token.txt` to your `.gitignore` file to prevent accidentally committing your token to version control:
            ```bash
            echo "my_hf_token.txt" >> .gitignore
            ```

2.  **Build the Docker image:**
    From the project root directory, run:
    ```bash
    DOCKER_BUILDKIT=1 docker build --secret id=huggingface_token,src=my_hf_token.txt -t llm-description-enhancer .
    ```
    * `DOCKER_BUILDKIT=1`: Enables BuildKit, which is required for using `--secret`.
    * `--secret id=huggingface_token,src=my_hf_token.txt`: Securely provides the content of `my_hf_token.txt` to the build process. The `id=huggingface_token` must match the ID used in the `RUN --mount` directive in your `Dockerfile`.
    * *(This step will take a while, especially the first time, as it downloads the LLM using your token).*

3.  **Run the Docker container using the Helper Script (`start_container.sh`):**
    A helper script `start_container.sh` is included in the repository to simplify starting the Docker container. This script typically handles stopping/removing any pre-existing container with the same configured name and then starts a new one.

    * **Ensure the script is executable:**
        After cloning the repository, or if the execute permission isn't set, you might need to make the script executable (on Linux, macOS, or Git Bash on Windows):
        ```bash
        chmod +x start_container.sh
        ```

    * **Run the script:**
        From the project root directory:
        ```bash
        ./start_container.sh
        ```

    * **Expected Outcome (depends on your script's content):**
        The script will likely:
        * Output messages indicating it's managing the container.
        * Start the container (possibly in detached mode).
        * Inform you that the service is available at `http://127.0.0.1:8000`.
        * Provide commands to view logs or stop the container if it's running in detached mode (e.g., `docker logs <container_name> -f` and `docker stop <container_name>`).

    *(Alternatively, you can run the container manually: `docker run --rm -p 8000:8000 llm-description-enhancer`)*

4.  **Test the containerized application:**
    Once the container is running (via the script or manually), send requests to `http://127.0.0.1:8000` as described in the API Endpoints section.

## API Endpoints

### Health Check

-   **Endpoint:** `/health`
-   **Method:** `GET`
-   **Description:** Returns the status of the application and model initialization.
-   **Example Response:**
    ```json
    {
      "status": "ok",
      "model_initialized": true,
      "model_path": "/app/pretrain_model" 
    }
    ```

### Enhance Description

-   **Endpoint:** `/enhance-description`
-   **Method:** `POST`
-   **Description:** Generates an enhanced marketing description for a car in Polish.
-   **Request Body (`application/json`):**
    ```json
    {
      "make": "Volkswagen",
      "model": "Golf",
      "year": 2022,
      "mileage": 15000,
      "features": ["Klimatyzacja automatyczna", "System nawigacji", "Czujniki parkowania"],
      "condition": "Bardzo dobry"
    }
    ```
-   **Response (`application/json`):**
    ```json
    {
      "description": "Wygenerowany przez AI opis samochodu..."
    }
    ```
-   **Example cURL request (for Git Bash / bash-like shells):**
    ```bash
    curl -X POST "[http://127.0.0.1:8000/enhance-description](http://127.0.0.1:8000/enhance-description)" \
    -H "Content-Type: application/json" \
    -d '{
        "make": "Volkswagen",
        "model": "Golf",
        "year": 2022,
        "mileage": 15000,
        "features": ["Klimatyzacja automatyczna", "System nawigacji", "Czujniki parkowania", "Podgrzewane fotele"],
        "condition": "Bardzo dobry"
    }'
    ```

## Core Service (`app/models/huggingface_service.py`)

The `HuggingFaceTextGenerationService` class handles the interaction with the Large Language Model.

-   **Key Methods:**
    -   `async initialize()`: Loads the pre-trained model and tokenizer from the path specified during service instantiation (e.g., `/app/pretrain_model` in Docker, or from Hugging Face cache locally).
    -   `async generate_text(chat_template_messages: list, max_new_tokens: int, ...)`: Generates text based on a structured chat prompt, applying appropriate chat templates and parsing the model's output to return only the assistant's response.

## Configuration

-   **Model Used:** `speakleash/Bielik-1.5B-v3.0-Instruct`. This is baked into `/app/pretrain_model` in the Docker image. For local development, it's downloaded to the Hugging Face cache.
-   **Language:** The primary focus is on generating descriptions in **Polish**.
-   **Prompt Engineering:** The system and user prompts in `app/main.py` are crafted to guide the model towards generating concise and relevant marketing descriptions.

## Schemas (`app/schemas/schemas.py`)

Pydantic models are used for request and response validation.

### `CarData`

-   **Fields:**
    -   `make`: `str`
    -   `model`: `str`
    -   `year`: `int`
    -   `mileage`: `int`
    -   `features`: `list[str]`
    -   `condition`: `str`

### `EnhancedDescriptionResponse`

-   **Fields:**
    -   `description`: `str`

## Contributing

Contributions are welcome! Please open an issue or submit a pull request for any changes.

## License

This project is licensed under the MIT License.
