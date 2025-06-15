from pydantic import BaseModel, Field


class ProductQuery(BaseModel):
    user_id: str = Field(description="User unique identifier", min_length=1)
    query: str = Field(description="User query about a product", max_length=500)