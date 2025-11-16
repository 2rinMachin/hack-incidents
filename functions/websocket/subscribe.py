import boto3
from boto3.dynamodb.conditions import Key
from pydantic import BaseModel

from common import parse_body, response
from schemas import IncidentSubscription

dynamodb = boto3.resource("dynamodb")
subscriptions = dynamodb.Table("hack-incidents-subscriptions")


class SubscribeRequest(BaseModel):
    connection_id: str


def handler(event, context):
    data, err = parse_body(SubscribeRequest, event)
    if err != None:
        return err

    assert data != None

    connection_id = event["requestContext"]["connectionId"]

    resp = subscriptions.query(
        KeyConditionExpression=Key("connection_id").eq(connection_id),
        Limit=1,
    )

    if resp.get("Count") > 0:
        return response(200, {"message": "Already subscribed."})

    new_subscription = IncidentSubscription(connection_id=connection_id)
    subscriptions.put_item(Item=new_subscription.model_dump())

    return response(200, {"message": "Subscribed."})
