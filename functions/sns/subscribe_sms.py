import json
import os

import boto3
from pydantic import BaseModel

from common import parse_body, response
from schemas import IncidentUrgency

sns = boto3.client("sns")

TOPIC_ARN = os.environ["AWS_INCIDENTS_TOPIC_ARN"]


class SubscribeSmsRequest(BaseModel):
    sms: str


def handler(event, context):
    data, err = parse_body(SubscribeSmsRequest, event)
    if err != None:
        return err

    assert data != None

    sns.subscribe(
        TopicArn=TOPIC_ARN,
        Protocol="sms",
        Endpoint=data.sms,
        Attributes={
            "FilterPolicy": json.dumps(
                {
                    "urgency": [IncidentUrgency.high.value],
                }
            )
        },
    )

    return response(200, {"message": "Subscription successful."})
