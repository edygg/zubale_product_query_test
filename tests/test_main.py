import pytest
from unittest.mock import patch
from fastapi.testclient import TestClient

from main import app

client = TestClient(app)


def test_health_check():
    """Test that the health check endpoint returns a 200 status code and expected data."""
    response = client.get("/health-check")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_product_query_endpoint_works_correctly():
    """Test that the product query endpoint works correctly."""
    # Create a valid payload
    payload = {
        "user_id": "test_user_123",
        "query": "What is the price of the product?"
    }

    # Mock the process_product_query.delay function to avoid actual processing
    with patch("main.process_product_query.delay") as mock_process:
        # Send a POST request with the valid payload
        response = client.post("/query", json=payload)

        # Verify the response status code is 200
        assert response.status_code == 200

        # Verify the response contains the expected status
        assert response.json()["status"] == "enqueue"

        # Verify the response contains an operation_id
        assert "operation_id" in response.json()

        # Verify that process_product_query.delay was called once with the correct arguments
        mock_process.assert_called_once()

        # Get the argument that was passed to process_product_query.delay
        args, _ = mock_process.call_args
        message = args[0]

        # Verify the message has the correct properties
        assert message.user_id == payload["user_id"]
        assert message.query == payload["query"]
        assert message.operation_id == response.json()["operation_id"]


@pytest.mark.parametrize(
    "payload,expected_status_code,expected_error_type",
    [
        # Missing user_id
        (
            {"query": "What is the price of the product?"},
            422,
            "missing",
        ),
        # Empty user_id (violates min_length=1)
        (
            {"user_id": "", "query": "What is the price of the product?"},
            422,
            "string_too_short",
        ),
        # Missing query
        (
            {"user_id": "test_user_123"},
            422,
            "missing",
        ),
        # Query that exceeds max_length=500
        (
            {"user_id": "test_user_123", "query": "x" * 501},
            422,
            "string_too_long",
        ),
    ],
)
def test_product_query_endpoint_handles_malformed_input(payload, expected_status_code, expected_error_type):
    """Test that the product query endpoint correctly handles malformed input."""
    response = client.post("/query", json=payload)

    # Verify the response status code matches the expected status code
    assert response.status_code == expected_status_code

    # Verify the response contains validation errors
    assert "detail" in response.json()

    # Verify at least one error has the expected error type
    errors = response.json()["detail"]
    assert any(error["type"] == expected_error_type for error in errors)
