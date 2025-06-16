import pytest
from unittest.mock import patch, MagicMock

from zubale_product_query.tasks import health_check, process_product_query, notify_ai_response
from zubale_product_query.serializers.models import ProductQuerySerializer, AIModelResponseSerializer
from zubale_product_query.rag.products import ProductQueryContext, ProductQueryContextDocument


def test_health_check():
    """Test that the health_check task returns the expected string."""
    # Call the task with a test value
    result = health_check("test_value")
    
    # Verify the result is as expected
    assert result == "Returning test_value"


@patch("zubale_product_query.tasks.retrieve_product_query_context")
@patch("zubale_product_query.tasks.answer_product_query_operation")
@patch("zubale_product_query.tasks.notify_ai_response.delay")
def test_process_product_query(mock_notify, mock_answer, mock_retrieve):
    """Test that the process_product_query task processes a query correctly."""
    # Create test data
    product_query = ProductQuerySerializer(
        user_id="test_user_123",
        query="What is the price of the product?",
        operation_id="test_operation_id"
    )
    
    # Set up mock returns
    mock_context = ProductQueryContext(
        context=[
            ProductQueryContextDocument(document_content="This is a context"),
            ProductQueryContextDocument(document_content="This is another context"),
        ]
    )
    mock_retrieve.return_value = mock_context
    
    mock_response = AIModelResponseSerializer(
        ai_model="gemini-2.0-flash",
        response="This is a response",
        product_query_operation_id=product_query.operation_id
    )
    mock_answer.return_value = mock_response
    
    # Call the task
    process_product_query(product_query)
    
    # Verify the mocks were called with the expected arguments
    mock_retrieve.assert_called_once_with(product_query)
    mock_answer.assert_called_once_with(mock_context, product_query)
    mock_notify.assert_called_once_with(mock_response)


@patch("zubale_product_query.tasks.get_product_query_notification_url")
@patch("zubale_product_query.tasks.requests.post")
@patch("zubale_product_query.tasks.logger")
def test_notify_ai_response_success(mock_logger, mock_post, mock_get_url):
    """Test that the notify_ai_response task sends a notification successfully."""
    # Create test data
    model_response = AIModelResponseSerializer(
        ai_model="gemini-2.0-flash",
        response="This is a response",
        product_query_operation_id="test_operation_id"
    )
    
    # Set up mock returns
    mock_url = "https://example.com/callback"
    mock_get_url.return_value = mock_url
    
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.text = "Success"
    mock_post.return_value = mock_response
    
    # Call the task
    notify_ai_response(model_response)
    
    # Verify the mocks were called with the expected arguments
    mock_get_url.assert_called_once()
    mock_post.assert_called_once_with(
        mock_url,
        json=model_response.model_dump()
    )
    mock_response.raise_for_status.assert_called_once()
    mock_logger.info.assert_called_once()


@patch("zubale_product_query.tasks.get_product_query_notification_url")
@patch("zubale_product_query.tasks.requests.post")
def test_notify_ai_response_error(mock_post, mock_get_url):
    """Test that the notify_ai_response task handles errors correctly."""
    # Create test data
    model_response = AIModelResponseSerializer(
        ai_model="gemini-2.0-flash",
        response="This is a response",
        product_query_operation_id="test_operation_id"
    )
    
    # Set up mock returns
    mock_url = "https://example.com/callback"
    mock_get_url.return_value = mock_url
    
    # Set up mock to raise an exception
    mock_response = MagicMock()
    mock_response.raise_for_status.side_effect = Exception("HTTP Error")
    mock_post.return_value = mock_response
    
    # Call the task and expect an exception
    with pytest.raises(Exception):
        notify_ai_response(model_response)
    
    # Verify the mocks were called with the expected arguments
    mock_get_url.assert_called_once()
    mock_post.assert_called_once_with(
        mock_url,
        json=model_response.model_dump()
    )
    mock_response.raise_for_status.assert_called_once()


@patch("os.getenv")
def test_get_product_query_notification_url_missing(mock_getenv):
    """Test that get_product_query_notification_url raises an exception when CALLBACK_URL is not set."""
    # Import here to avoid circular import
    from zubale_product_query.notifications import get_product_query_notification_url
    
    # Set up mock to return None
    mock_getenv.return_value = None
    
    # Call the function and expect an exception
    with pytest.raises(Exception) as excinfo:
        get_product_query_notification_url()
    
    # Verify the exception message
    assert "There is no CALLBACK_URL configured yey" in str(excinfo.value)
    
    # Verify the mock was called with the expected argument
    mock_getenv.assert_called_once_with("CALLBACK_URL")


@patch("os.getenv")
def test_get_product_query_notification_url_success(mock_getenv):
    """Test that get_product_query_notification_url returns the correct URL when CALLBACK_URL is set."""
    # Import here to avoid circular import
    from zubale_product_query.notifications import get_product_query_notification_url
    
    # Set up mock to return a URL
    mock_url = "https://example.com/callback"
    mock_getenv.return_value = mock_url
    
    # Call the function
    result = get_product_query_notification_url()
    
    # Verify the result is as expected
    assert result == mock_url
    
    # Verify the mock was called with the expected argument
    mock_getenv.assert_called_once_with("CALLBACK_URL")