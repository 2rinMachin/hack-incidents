import boto3
from boto3.dynamodb.conditions import Key

from common import response
from schemas import IncidentSubscription

dynamodb = boto3.resource("dynamodb")
subscriptions = dynamodb.Table("hack-incident-subscriptions")


def handler(event, context):
    connection_id = event["requestContext"]["connectionId"]

    try:
        subscriptions.get_item(Key={"connection_id": connection_id})
        return response(200, {"message": "Already subscribed."})
    except KeyError:
        pass

    new_subscription = IncidentSubscription(connection_id=connection_id)
    subscriptions.put_item(Item=new_subscription.model_dump())

    return response(200, {"message": "Subscribed."})
