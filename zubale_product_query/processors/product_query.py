import asyncio
import logging
from asyncio import Queue


from zubale_product_query.payloads.product_query import ProductQuery


class ProductQueryProcessor:
    def __init__(self, queue: Queue):
        self._queue = queue

    def _internal_queue(self):
        return self._queue

    async def process(self):
        while True:
            task: ProductQuery = await self._internal_queue().get()
            logging.info(f"Processing task: {task}")
            await asyncio.sleep(1)
            self._internal_queue().task_done()

    async def add_task(self, task: ProductQuery):
        self._internal_queue().put_nowait(task)

    async def start_processing(self):
        await asyncio.gather(
            self.process(),
            return_exceptions=True,
        )


__product_query_processor = ProductQueryProcessor(asyncio.Queue())


def get_product_query_processor():
    return __product_query_processor