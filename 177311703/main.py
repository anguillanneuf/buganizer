import base64
import os

from google import api_core
from google.cloud import pubsub_v1

# Instantiate a Pub/Sub client
publisher = pubsub_v1.PublisherClient()

# See more details about setting runtime environment variables in Cloud Functions
# https://cloud.google.com/functions/docs/env-var#using_runtime_environment_variables
PROJECT_ID = os.getenv("GOOGLE_CLOUD_PROJECT")
FORWARDING_TOPIC_ID = os.getenv("FORWARDING_TOPIC_ID")

"""
This function is triggered by a message published to a Pub/Sub topic. When
triggered, it will then publish 10 messages to a different Pub/Sub topic
with retry settings.
"""


def demo(event, context):
    # print(f"event: {event}")
    # print(f"context: {context}")

    message_id = context.event_id
    incoming_topic_id = context.resource.name
    publish_timestamp = context.timestamp

    message_data = "an empty message"
    if "data" in event:
        message_data = base64.b64decode(event["data"]).decode("utf-8")

    print(
        """Function triggered by {} of messageId {} published to {} at {}
    """.format(
            message_data, message_id, incoming_topic_id, publish_timestamp
        )
    )

    # The code for publishing with retry settings below is copied from
    # https://cloud.google.com/pubsub/docs/publisher#retry

    # Configure the retry settings. Defaults shown in comments are values applied
    # by the library by default, instead of default values in the Retry object.
    custom_retry = api_core.retry.Retry(
        initial=0.250,  # seconds (default: 0.1)
        maximum=90.0,  # seconds (default: 60.0)
        multiplier=1.45,  # default: 1.3
        deadline=300.0,  # seconds (default: 60.0)
        predicate=api_core.retry.if_exception_type(
            api_core.exceptions.Aborted,
            api_core.exceptions.DeadlineExceeded,
            api_core.exceptions.InternalServerError,
            api_core.exceptions.ResourceExhausted,
            api_core.exceptions.ServiceUnavailable,
            api_core.exceptions.Unknown,
            api_core.exceptions.Cancelled,
        ),
    )

    topic_path = publisher.topic_path(PROJECT_ID, FORWARDING_TOPIC_ID)

    try:
        for n in range(1, 10):
            data = f"Message number {n}"
            future = publisher.publish(
                topic=topic_path, data=data.encode("utf-8"), retry=custom_retry
            )
            print(f"Published message ID {future.result()}")

        return f"Published messages with retry settings to {topic_path}."
    except api_core.exceptions.NotFound:
        return ("Pub/Sub topic not found", 404)
