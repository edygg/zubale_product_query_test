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
- FastAPI application on port 8000 (accessible at http://localhost:8000)
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

Once the application is running, you can access the API at http://localhost:8000 with the following endpoints:

- `GET /health-check`: Check if the API is running
- `POST /`: Submit a product query

### Langflow Integration

The project includes [Langflow](https://github.com/langflow-ai/langflow), a UI for LangChain, which provides a visual way to build and interact with agent workflows.

#### Accessing Langflow

When you run `docker compose up`, Langflow will be available at:
```
http://localhost:7860
```

#### Using the Workflow

The project includes a pre-configured workflow with two agents:

1. **Product Information Agent**: Specializes in retrieving and providing detailed information about products.
2. **Customer Support Agent**: Handles customer inquiries and provides appropriate responses based on product information.

To use the workflow:

1. Open Langflow at http://localhost:7860
2. Click on "Import" in the top right corner
3. Select the file `langflow/Zubale Agents Test.json`
4. Once imported, click on the workflow to open it
5. Click the "Run" button to activate the workflow
6. Use the chat interface to interact with the agents

The workflow demonstrates how multiple agents can work together to provide comprehensive responses to product queries. The first agent retrieves product information, and the second agent uses that information to provide customer support.

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
