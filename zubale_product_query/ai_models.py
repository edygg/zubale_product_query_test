
from zubale_product_query.rag.products import ProductQueryContext
from zubale_product_query.serializers.models import ProductQuerySerializer, AIModelResponseSerializer


def answer_product_query_operation(
        context: ProductQueryContext,
        product_query_operation: ProductQuerySerializer,
) -> AIModelResponseSerializer:
    # TODO Mock response
    return AIModelResponseSerializer(
        ai_model="gemini-2.0-flash",
        response="This is a response",
        product_query_operation_id=product_query_operation.operation_id,
    )