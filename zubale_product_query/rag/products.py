from typing import List
from pydantic import BaseModel

from zubale_product_query.serializers.models import ProductQuerySerializer


class ProductQueryContextDocument(BaseModel):
    document_content: str


class ProductQueryContext(BaseModel):
    context: List[ProductQueryContextDocument]



def retrieve_product_query_context(product_query_operation: ProductQuerySerializer) -> ProductQueryContext:
    # TODO Mock response
    return ProductQueryContext(
        context=[
            ProductQueryContextDocument(document_content="This is a context"),
            ProductQueryContextDocument(document_content="This is another context"),
        ]
    )