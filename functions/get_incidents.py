import boto3
from boto3.dynamodb.conditions import Attr
import json
from common import response

dynamodb = boto3.resource("dynamodb")


def handler(event, context):
    incidents = dynamodb.Table("hack-incidents")
    query = event.get("queryStringParameters") or {}

    kind = query.get("kind")
    status = query.get("status")
    urgency = query.get("urgency")
    location = query.get("location")

    limit = int(query.get("limit", 20))
    next_token = query.get("next_token")

    filter_expression = None

    if kind:
        expr = Attr("kind").eq(kind)
        filter_expression = expr if filter_expression is None else filter_expression & expr

    if status:
        expr = Attr("status").eq(status)
        filter_expression = expr if filter_expression is None else filter_expression & expr

    if urgency:
        expr = Attr("urgency").eq(urgency)
        filter_expression = expr if filter_expression is None else filter_expression & expr

    if location:
        expr = Attr("location").contains(location)
        filter_expression = expr if filter_expression is None else filter_expression & expr

    scan_kwargs = {"Limit": limit}

    if filter_expression:
        scan_kwargs["FilterExpression"] = filter_expression

    if next_token:
        scan_kwargs["ExclusiveStartKey"] = json.loads(next_token)

    resp = incidents.scan(**scan_kwargs)

    items = resp.get("Items", [])
    sorted_items = sorted(items, key=lambda x: x.get("created_at", ""), reverse=True)

    return response(200, {
        "items": sorted_items,
        "next_token": json.dumps(resp["LastEvaluatedKey"]) if "LastEvaluatedKey" in resp else None
    })
