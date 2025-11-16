from collections import Counter

import boto3

from common import response
from schemas import Incident, IncidentKind, IncidentStatus, IncidentUrgency

dynamodb = boto3.resource("dynamodb")


def handler(event, context):
    incidents = dynamodb.Table("hack-incidents")

    resp = incidents.scan()
    items: list[dict] = resp.get("Items", [])

    incidents = [Incident(**item) for item in items]

    total_incidents = len(incidents)
    kind_count = Counter(incident.kind for incident in incidents)
    urgency_count = Counter(incident.urgency for incident in incidents)
    status_count = Counter(incident.status for incident in incidents)

    kind_count = {kind.value: kind_count.get(kind, 0) for kind in IncidentKind}
    urgency_count = {
        urgency.value: urgency_count.get(urgency, 0) for urgency in IncidentUrgency
    }
    status_count = {
        status.value: status_count.get(status, 0) for status in IncidentStatus
    }

    return response(
        200,
        {
            "total_incidents": total_incidents,
            "kind_count": kind_count,
            "urgency_count": urgency_count,
            "status_count": status_count,
        },
    )
