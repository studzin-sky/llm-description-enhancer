# LLM Car Description Enhancer (Polish)

This repository contains a FastAPI application that utilizes a Hugging Face Transformers Large Language Model (specifically, `speakleash/Bielik-1.5B-v3.0-Instruct` or a similar model from the Bielik series) to generate enhanced marketing descriptions for cars, primarily in Polish.

The application is designed to be run locally for development or containerized using Docker for deployment. The LLM is baked into the Docker image for self-contained and efficient execution.

## Features

- Generate enhanced marketing descriptions for cars in Polish.
- Utilizes the `speakleash/Bielik-1.5B-v3.0-Instruct` model via the Hugging Face `transformers` library.
- Health check endpoint.
- Docker support for easy deployment, with the model included in the image.

## Prerequisites

- Python 3.9 or higher
- `pip` (Python package installer)
- Docker (for containerized deployment)
- Git (for cloning the repository)

## Project Structure

.
├── app/
│   ├── main.py                   # FastAPI application, endpoints
│   ├── models/
│   │   └── huggingface_service.py  # Service for interacting with the LLM
│   └── schemas/
│       └── schemas.py              # Pydantic schemas for request/response
├── Dockerfile
├── requirements.txt
└── README.md


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
    *Note: The first time you run the application locally (or if the model cache is empty), the Hugging Face model (~3.2GB) will be downloaded. This might take some time.*

## Usage (Local Development)

1.  **Start the FastAPI server:**
    From the project root directory (where `Dockerfile` and the `app` folder are):
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

The included `Dockerfile` builds an image with the application and the pre-downloaded Hugging Face model, making it self-contained.

1.  **Build the Docker image:**
    From the project root directory:
    ```bash
    docker build -t llm-description-enhancer .
    ```
    *(This step will take a while, especially the first time, as it downloads the LLM).*

2.  **Run the Docker container:**
    ```bash
    docker run --rm -p 8000:8000 llm-description-enhancer
    ```
    * `--rm`: Automatically removes the container when it stops.
    * `-p 8000:8000`: Maps port 8000 on your host to port 8000 in the container.

3.  **Test the containerized application:**
    Once the container is running, you can send requests to `http://127.0.0.1:8000` as you would for the local setup (e.g., using cURL or an API client).

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
-   **Example cURL request:**
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

-   **Model Used:** `speakleash/Bielik-1.5B-v3.0-Instruct` (or as configured in `app/main.py` for local runs, and baked into `/app/pretrain_model` in the Docker image).
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