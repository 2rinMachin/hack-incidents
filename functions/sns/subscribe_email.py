import os

import boto3
from pydantic import BaseModel

from common import parse_body, response

sns = boto3.client("sns")

TOPIC_ARN = os.environ["AWS_INCIDENTS_TOPIC_ARN"]


class SubscribeEmailRequest(BaseModel):
    email: str


def handler(event, context):
    data, err = parse_body(SubscribeEmailRequest, event)
    if err != None:
        return err

    assert data != None

    sns.subscribe(
        TopicArn=TOPIC_ARN,
        Protocol="email",
        Endpoint=data.email,
    )

    return response(200, {"message": "Subscription successful."})
