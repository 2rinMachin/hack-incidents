from collections import Counter

import boto3
from boto3.dynamodb.conditions import Attr

from common import response
from schemas import Incident, IncidentKind, IncidentStatus, IncidentUrgency

dynamodb = boto3.resource("dynamodb")


def handler(event, context):
    incidents = dynamodb.Table("hack-incidents")
    query = event.get("queryStringParameters") or {}

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
        resp = incidents.scan(FilterExpression=filter_expression)
    else:
        resp = incidents.scan()

    items: list[dict] = resp.get("Items", [])
    incidents = [Incident(**item) for item in items]

    kind_count = Counter({kind.value: 0 for kind in IncidentKind})
    urgency_count = Counter({urgency.value: 0 for urgency in IncidentUrgency})
    status_count = Counter({status.value: 0 for status in IncidentStatus})

    total_incidents = len(incidents)
    kind_count.update(incident.kind for incident in incidents)
    urgency_count.update(incident.urgency for incident in incidents)
    status_count.update(incident.status for incident in incidents)

    return response(
        200,
        {
            "total_incidents": total_incidents,
            "kind_count": dict(kind_count),
            "urgency_count": dict(urgency_count),
            "status_count": dict(status_count),
        },
    )
