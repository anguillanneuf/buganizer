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

1. Head over to [Cloud Console](http://console.cloud.google.com/functions/list) to check out the logs of your function. You should see something similar to:

    ```none
    2021-05-20 16:04:34.558 PDT demo djc01f1w7q5w Function triggered by 3:35 PM of messageId 2306546483605313 published to projects/tz-playground-bigdata/topics/your-incoming-topic-id at 2021-05-20T23:04:33.530Z
    2021-05-20 16:04:35.502 PDT demo djc01f1w7q5w Published message ID 2420032922414595
    2021-05-20 16:04:35.926 PDT demo djc01f1w7q5w Published message ID 2419982157525293
    ...
    2021-05-20 16:04:37.296 PDT demo djc01f1w7q5w Function execution took 2753 ms, finished with status: 'ok'
    ```