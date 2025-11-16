import uuid

import boto3
from pydantic import BaseModel

from common import parse_body, response
from schemas import Incident, IncidentKind, IncidentStatus, IncidentUrgency

dynamodb = boto3.resource("dynamodb")
incidents = dynamodb.Table("hack-incidents")


class PostIncidentRequest(BaseModel):
    kind: IncidentKind
    description: str
    location: str
    urgency: IncidentUrgency


def handler(event, context):
    data, err = parse_body(PostIncidentRequest, event)
    if err != None:
        return err

    assert data != None

    new_incident = Incident(
        id=str(uuid.uuid4()),
        kind=data.kind,
        description=data.description,
        location=data.location,
        urgency=data.urgency,
        status=IncidentStatus.pending,
    )

    new_incident_dict = new_incident.model_dump()

    incidents.put_item(Item=new_incident_dict)

    return response(201, new_incident_dict)
