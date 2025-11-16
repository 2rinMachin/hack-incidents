import boto3
from boto3.dynamodb.conditions import Key
from pydantic import ValidationError

from common import response
from schemas import IncidentSubscription

dynamodb = boto3.resource("dynamodb")
subscriptions = dynamodb.Table("hack-incidents-subscriptions")


def handler(event, context):
    connection_id = event["requestContext"]["connectionId"]

    resp = subscriptions.query(
        KeyConditionExpression=Key("connection_id").eq(connection_id),
        Limit=1,
    )

    items: list[dict] = resp.get("Items", [])

    for item in items:
        sub: IncidentSubscription

        try:
            sub = IncidentSubscription(**item)
        except (KeyError, ValidationError):
            continue

        subscriptions.delete_item(Key={"connection_id": sub.connection_id})

    return response(204, None)
