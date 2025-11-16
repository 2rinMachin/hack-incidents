import os

import boto3

from schemas import Incident

sns = boto3.client("sns")

TOPIC_ARN = os.environ["AWS_INCIDENTS_TOPIC_ARN"]


def handler(event, context):
    incident = Incident(**event["detail"])

    sns.publish(
        TopicArn=TOPIC_ARN,
        Subject="Incidente reportado",
        Message=f"""
            Hola, se ha registrado un nuevo incidente:

            "{incident.description}"
        """,
        MessageAttributes={
            "urgency": {
                "DataType": "String",
                "StringValue": incident.urgency.value,
            },
        },
    )
