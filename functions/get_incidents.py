import boto3
from boto3.dynamodb.conditions import Attr

from common import response

dynamodb = boto3.resource("dynamodb")


def handler(event, context):
    incidents = dynamodb.Table("hack-incidents")
    query = event.get("queryStringParameters") or {}

    kind = query.get("kind")
    status = query.get("status")
    urgency = query.get("urgency")
    location = query.get("location")

    page = int(query.get("page", 1))
    limit = int(query.get("limit", 5))
    start_index = (page - 1) * limit

    filter_expression = None

    if kind:
        expr = Attr("kind").eq(kind)
        filter_expression = (
            expr if filter_expression is None else filter_expression & expr
        )

    if status:
        expr = Attr("status").eq(status)
        filter_expression = (
            expr if filter_expression is None else filter_expression & expr
        )

    if urgency:
        expr = Attr("urgency").eq(urgency)
        filter_expression = (
            expr if filter_expression is None else filter_expression & expr
        )

    if location:
        expr = Attr("location").contains(location)
        filter_expression = (
            expr if filter_expression is None else filter_expression & expr
        )

    scan_params: dict = {"Limit": limit}

    if filter_expression:
        scan_params["FilterExpression"] = filter_expression

    current_index = 0
    while current_index < start_index:
        resp = incidents.scan(**scan_params)
        last_evaluated_key = resp.get("LastEvaluatedKey")

        if not last_evaluated_key:
            break

        scan_params["ExclusiveStartKey"] = last_evaluated_key
        current_index += len(resp.get("Items", []))

    resp = incidents.scan(**scan_params)
    items: list[dict] = resp.get("Items", [])
    sorted_items = sorted(items, key=lambda x: x.get("created_at", ""), reverse=True)

    last_evaluated_key = resp.get("LastEvaluatedKey")

    response_data = {
        "current_page": page,
        "items": sorted_items,
    }

    if last_evaluated_key:
        response_data["next_page"] = page + 1

    return response(200, response_data)
