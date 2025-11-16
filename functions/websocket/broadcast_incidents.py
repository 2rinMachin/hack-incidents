import os

import boto3
from pydantic import ValidationError

from schemas import Incident, IncidentSubscription

APIGW_DOMAIN = os.environ["APIGW_DOMAIN"]
APIGW_STAGE = os.environ["APIGW_STAGE"]
ENDPOINT_URL = f"https://{APIGW_DOMAIN}/{APIGW_STAGE}"

dynamodb = boto3.resource("dynamodb")
subscriptions = dynamodb.Table("hack-incident-subscriptions")
api_gw = boto3.client("apigatewaymanagementapi", endpoint_url=ENDPOINT_URL)


def handler(event, context):
    incident = Incident(**event["detail"])

    resp = subscriptions.scan()
    subs: list[dict] = resp.get("Items", [])
    print("incident: ", incident)
    print("subs: ", subs)

    for item in subs:
        sub: IncidentSubscription

        try:
            sub = IncidentSubscription(**item)
        except (KeyError, ValidationError):
            continue

        api_gw.post_to_connection(
            ConnectionId=sub.connection_id, Data=incident.model_dump_json()
        )
