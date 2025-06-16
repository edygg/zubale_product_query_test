# Zubale Product Query API

A FastAPI application that processes product queries using Retrieval Augmented Generation (RAG) and AI models.

## Project Overview

This project provides an API for processing product queries. It uses a RAG (Retrieval Augmented Generation) approach to retrieve relevant product information from a vector database and then uses an AI model to generate responses to user queries.

### Key Modules

- **FastAPI Application (`main.py`)**: The main entry point for the API, handling HTTP requests.
- **Celery Tasks (`zubale_product_query/tasks.py`)**: Asynchronous task processing for product queries.
- **RAG System (`zubale_product_query/rag/`)**: Handles retrieval of relevant product information from a vector database.
- **AI Models (`zubale_product_query/ai_models.py`)**: Integration with AI models for generating responses.
- **Serializers (`zubale_product_query/serializers/`)**: Data serialization and deserialization.
- **Payloads (`zubale_product_query/payloads/`)**: Request and response payload definitions.
- **Notifications (`zubale_product_query/notifications.py`)**: Handles sending notifications with query results.

## Getting Started

### Prerequisites

- Docker and Docker Compose

### Starting the Project

To start the project, run:

```bash
docker compose up
```

This will start the following services:
- FastAPI application on port 8000
- Celery worker for processing tasks
- Redis for message brokering

### Environment Configuration

The project uses environment variables for configuration, which are stored in the `.docker-compose/.envs` directory:

- `.docker-compose/.envs/.config-envs`: Contains application configuration variables
  - `CALLBACK_URL`: URL where notifications are sent (default: "https://httpbin.org/post")
  - `TOP_K`: Number of top results to return from queries (default: 3)

- `.docker-compose/.envs/.redis-envs`: Contains Redis configuration variables
  - `REDIS_HOST`: Redis server hostname (default: redis)
  - `REDIS_PORT`: Redis server port (default: 6379)

To modify these configurations, edit the corresponding files before starting the services.

### API Endpoints

- `GET /health-check`: Check if the API is running
- `POST /`: Submit a product query

## Running Tests

To run the test suite, use:

```bash
docker compose run --rm product_query pytest
```

This will run all the tests in the `tests/` directory.

## Project Structure

- `main.py`: FastAPI application entry point
- `docker-compose.yml`: Docker Compose configuration
- `requirements.txt`: Python dependencies
- `product_docs/`: Markdown files containing product information
- `tests/`: Test files
- `zubale_product_query/`: Main package
  - `ai_models.py`: AI model integration
  - `celery_config.py`: Celery configuration
  - `notifications.py`: Notification handling
  - `tasks.py`: Celery task definitions
  - `payloads/`: Request/response payload definitions
  - `rag/`: Retrieval Augmented Generation functionality
  - `serializers/`: Data serialization/deserialization
