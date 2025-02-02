# LLM Description Enhancer

This repository contains a FastAPI application that utilizes the GPT4All model to generate enhanced descriptions based on car data.

## Features

- Generate enhanced descriptions for cars
- Health check endpoint

## Installation

1. Clone the repository:
    ```bash
    git clone https://github.com/studzin-sky/llm-description-enhancer.git
    cd llm-description-enhancer
    ```

2. Install the required dependencies:
    ```bash
    pip install -r requirements.txt
    ```

## Usage

1. Start the FastAPI server:
    ```bash
    uvicorn main:app --reload
    ```

2. Access the application:
    - Health Check: [http://127.0.0.1:8000/health](http://127.0.0.1:8000/health)
    - Enhance Description: [http://127.0.0.1:8000/enhance-description](http://127.0.0.1:8000/enhance-description)

## API Endpoints

### Health Check

- **Endpoint:** `/health`
- **Method:** `GET`
- **Description:** Returns the status of the application.

### Enhance Description

- **Endpoint:** `/enhance-description`
- **Method:** `POST`
- **Request Body:**
    ```json
    {
      "make": "string",
      "model": "string",
      "year": 2021,
      "mileage": 10000,
      "features": ["feature1", "feature2"],
      "condition": "string"
    }
    ```
- **Response:**
    ```json
    {
      "description": "string"
    }
    ```

## Models

### GPT4AllService

- **Methods:**
  - `generate_description(prompt: str) -> str`: Generates a description based on the provided prompt.
  - `initialize()`: Asynchronous initialization method.

## Schemas

### CarData

- **Fields:**
  - `make`: `str`
  - `model`: `str`
  - `year`: `int`
  - `mileage`: `int`
  - `features`: `list[str]`
  - `condition`: `str`

### EnhancedDescriptionResponse

- **Fields:**
  - `description`: `str`

## Contributing

Contributions are welcome! Please open an issue or submit a pull request for any changes.

## License

This project is licensed under the MIT License.
