import requests
from celery.utils.log import get_task_logger
from celery import Celery

import zubale_product_query.celery_config as celery_config
from zubale_product_query.ai_models import answer_product_query_operation
from zubale_product_query.notifications import get_product_query_notification_url
from zubale_product_query.rag.products import retrieve_product_query_context
from zubale_product_query.serializers.models import ProductQuerySerializer, AIModelResponseSerializer

logger = get_task_logger(__name__)


app = Celery()
app.config_from_object(celery_config)


@app.task()
def health_check(return_value):
    return f"Returning {return_value}"


@app.task()
def process_product_query(product_query: ProductQuerySerializer):
    logger.info(f"Processing query: {product_query.model_dump()}")
    context = retrieve_product_query_context(product_query)
    model_response = answer_product_query_operation(context, product_query)
    notify_ai_response.delay(model_response)


@app.task(
    acks_late=True,
    autoretry_for=(Exception,),
    retry_backoff=True,
    retry_kwargs={'max_retries': 3},
)
def notify_ai_response(model_response: AIModelResponseSerializer):
    url = get_product_query_notification_url()
    response = requests.post(
        url,
        json=model_response.model_dump(),
    )
    response.raise_for_status()
    logger.info(
        f"Notification sent to {url} "
        f"| payload: {model_response.model_dump()} "
        f"| status: {response.status_code} "
        f"| response: {response.text}"
    )