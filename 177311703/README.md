# Deploy a Cloud Functions function triggered by Pub/Sub and publishes to Pub/Sub

This example deploys a function named `demo` in Pyhton, it gets invoked whenever a message is published to a Pub/Sub topic, and when invoked, it publishes ten messages to a different Pub/Sub topic. 

## How to deploy the function

1. Create an incoming and forwarding Pub/Sub topic. Also attach a subscription to your forwarding Pub/Sub topic.

    ```sh
    PROJECT_ID=$(gcloud config get-value project)
    INCOMING_TOPIC_ID=your-incoming-topic-id
    FORWARDING_TOPIC_ID=your-forwarding-topic-id
    FORWARDING_SUBSCRIPTION_ID=your-forwarding-subscription-id

    gcloud pubsub topics create $INCOMING_TOPIC_ID
    gcloud pubsub topics create $FORWARDING_TOPIC_ID
    gcloud pubsub subscriptions create $FORWARDING_SUBSCRIPTION_ID --topic=$FORWARDING_TOPIC_ID
    ```

1. Deploy your function. Set `--trigger-topic` to your incoming topic ID. Set runtime environment variables for your function.

    ```sh
    gcloud functions deploy demo \
        --trigger-topic=$INCOMING_TOPIC_ID \
        --runtime=python39 \
        --set-env-vars GOOGLE_CLOUD_PROJECT=$PROJECT_ID,FORWARDING_TOPIC_ID=$FORWARDING_TOPIC_ID
    ```

1. Publish a message to your incoming Pub/Sub topic.

    ```sh
    gcloud pubsub topics publish $INCOMING_TOPIC_ID --message="3:35 PM"
    ```

1. Head over to [Cloud Console]() to check out the logs of your function. You should see something similar to:

    ```none
    2021-05-20 14:56:29.440 PDT demo iofjzwgy90q0 Function triggered by 3:35 PM of messageId 2306343060931168 published to projects/tz-playground-bigdata/topics/april at 2021-05-20T21:56:28.301Z
    2021-05-20 14:56:30.118 PDT demo iofjzwgy90q0 Published message ID 2419832115448835
    2021-05-20 14:56:30.319 PDT demo iofjzwgy90q0 Published message ID 2419844337901231
    ...
    ```