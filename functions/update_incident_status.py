from datetime import datetime, timezone

import boto3
from pydantic import BaseModel

from common import parse_body, response
from schemas import Incident, IncidentAuthor, IncidentHistoryEntry, IncidentStatus, User

events = boto3.client("events")
dynamodb = boto3.resource("dynamodb")
incidents = dynamodb.Table("hack-incidents")


class UpdateIncidentStatusRequest(BaseModel):
    status: IncidentStatus


def handler(event, context):

    data, err = parse_body(UpdateIncidentStatusRequest, event)
    if err != None:
        return err

    assert data != None

    incident_id = event["pathParameters"]["incident_id"]
    actor = User(**event["requestContext"]["authorizer"])

    new_entry = IncidentHistoryEntry(
        status=data.status,
        actor=IncidentAuthor(
            id=actor.id,
            email=actor.email,
            username=actor.username,
            role=actor.role,
        ),
        date=datetime.now(timezone.utc).isoformat(),
    )

    resp = incidents.update_item(
        Key={"id": incident_id},
        UpdateExpression="""
            SET #sts = :status,
                history = list_append(:entry, history)
        """,
        ExpressionAttributeNames={"#sts": "status"},
        ExpressionAttributeValues={
            ":status": data.status,
            ":entry": [new_entry.model_dump()],
        },
        ReturnValues="ALL_NEW",
    )

    attrs: dict = resp["Attributes"]
    new_incident = Incident(**attrs)

    events.put_events(
        Entries=[
            {
                "Source": "hack.incidents",
                "DetailType": "incident.status_updated",
                "Detail": new_incident.model_dump_json(),
            }
        ]
    )

    return response(200, new_incident.model_dump_json())
