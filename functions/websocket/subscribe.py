import boto3

from common import response
from schemas import IncidentSubscription

dynamodb = boto3.resource("dynamodb")
subscriptions = dynamodb.Table("hack-incident-subscriptions")


def handler(event, context):
    connection_id = event["requestContext"]["connectionId"]

    resp = subscriptions.get_item(Key={"connection_id": connection_id})
    if "Item" in resp:
        return response(
            200, {"kind": "subscription_failed", "data": "Already subscribed."}
        )

    new_subscription = IncidentSubscription(connection_id=connection_id)
    subscriptions.put_item(Item=new_subscription.model_dump())

    return response(
        200, {"kind": "subscription_success", "data": "Subscribed successfully."}
    )
