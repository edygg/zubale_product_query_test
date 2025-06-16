import os
from kombu.serialization import register
import zubale_product_query.serializers as app_serializers

register(
    "pydantic",
    app_serializers.pydantic_dumps,
    app_serializers.pydantic_loads,
    content_type="application/x-pydantic",
    content_encoding="utf-8",
)


redis_uri = f"redis://{os.getenv('REDIS_HOST')}:{os.getenv('REDIS_PORT')}/0"


broker_url = str(redis_uri)

imports = ('zubale_product_query.tasks',)

result_backend = str(redis_uri)

broker_connection_retry_on_startup = True

task_serializer = "pydantic"

result_serializer = "pydantic"

event_serializer = "pydantic"

accept_content = [
    "application/json",
    "application/x-pydantic",
]

result_accept_content = [
    "application/json",
    "application/x-pydantic",
]


