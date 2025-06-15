from typing import Annotated
from fastapi import FastAPI, Body

from zubale_product_query.payloads.product_query import ProductQuery
from zubale_product_query.processors.product_query import get_product_query_processor


product_query_processor = get_product_query_processor()


async def on_server_start():
    product_query_processor.start_processing()

app = FastAPI(
    on_startup=[on_server_start],
)


@app.get("/health-check")
async def health_check():
    return {"status": "ok"}


@app.post("/")
async def product_query(product_query: Annotated[ProductQuery, Body]):
    await product_query_processor.add_task(product_query)
    return {"status": "ok"}