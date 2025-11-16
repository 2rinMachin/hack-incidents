import boto3
from boto3.dynamodb.conditions import Attr

from common import response

dynamodb = boto3.resource("dynamodb")


def handler(event, context):
    incidents_table = dynamodb.Table("hack-incidents")
    query = event.get("queryStringParameters", {})

    kind = query.get("kind")
    status = query.get("status")
    urgency = query.get("urgency")
    location = query.get("location")

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
        # For partial matches, use contains
        expr = Attr("location").contains(location)
        filter_expression = (
            expr if filter_expression is None else filter_expression & expr
        )

    if filter_expression:
        resp = incidents_table.scan(FilterExpression=filter_expression)
    else:
        resp = incidents_table.scan()

    incidents = resp.get("Items", [])

    return response(200, incidents)
