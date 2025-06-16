from pydantic import BaseModel
from uuid import uuid4


class ProductQuerySerializer(BaseModel):
    user_id: str
    query: str
    operation_id: str


def get_new_operation_id():
    return str(uuid4())


class AIModelResponseSerializer(BaseModel):
    ai_model: str  # e.g. gemini-2.0-flash
    response: str
    product_query_operation_id: str