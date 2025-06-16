from typing import Annotated
from fastapi import FastAPI, Body

from zubale_product_query.payloads.product_query import ProductQuery
from zubale_product_query.serializers.models import ProductQuerySerializer, get_new_operation_id
from zubale_product_query.tasks import process_product_query
from zubale_product_query.rag.products import initialize_product_query_context


def startup_event():
    """Initialize the product query context on app startup"""
    initialize_product_query_context()


app = FastAPI(
    title="Zubale Product Query API Test by Edilson Gonzalez",
    on_startup=[startup_event],
)


@app.get("/health-check")
async def health_check():
    return {"status": "ok"}


@app.post("/")
async def product_query(product_query: Annotated[ProductQuery, Body]):
    message: ProductQuerySerializer = ProductQuerySerializer(
        user_id=product_query.user_id,
        query=product_query.query,
        operation_id=get_new_operation_id(),
    )

    process_product_query.delay(message)

    return {
        "status": "enqueue",
        "operation_id": message.operation_id,
    }
