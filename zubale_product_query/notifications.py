import os


def get_product_query_notification_url():
    notification_url = os.getenv("CALLBACK_URL")

    if notification_url is None:
        raise Exception("There is no CALLBACK_URL configured yey")

    return notification_url