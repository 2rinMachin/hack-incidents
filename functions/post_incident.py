import base64
import os
import uuid
from datetime import datetime, timezone
from typing import Optional

import boto3
from pydantic import BaseModel

from common import parse_body, response
from schemas import (
    Incident,
    IncidentAuthor,
    IncidentKind,
    IncidentStatus,
    IncidentUrgency,
    User,
)

IMAGES_BUCKET = os.environ["AWS_INCIDENT_IMAGES_BUCKET"]

events = boto3.client("events")
dynamodb = boto3.resource("dynamodb")
s3 = boto3.resource("s3")

incidents = dynamodb.Table("hack-incidents")


class PostIncidentRequest(BaseModel):
    kind: IncidentKind
    description: str
    location: str
    urgency: IncidentUrgency
    image: Optional[str] = None


def handler(event, context):
    data, err = parse_body(PostIncidentRequest, event)
    if err != None:
        return err

    assert data != None

    author = User(**event["requestContext"]["authorizer"])

    new_incident = Incident(
        id=str(uuid.uuid4()),
        kind=data.kind,
        description=data.description,
        location=data.location,
        urgency=data.urgency,
        status=IncidentStatus.pending,
        author=IncidentAuthor(
            id=author.id, email=author.email, username=author.username, role=author.role
        ),
        created_at=datetime.now(timezone.utc).isoformat(),
    )

    if data.image != None:
        image_key = f"{new_incident.id}.png"
        s3.Object(IMAGES_BUCKET, image_key).put(Body=base64.b64decode(data.image))
        new_incident.image_url = f"https://{IMAGES_BUCKET}.s3.amazonaws.com/{image_key}"

    incidents.put_item(Item=new_incident.model_dump())

    events.put_events(
        Entries=[
            {
                "Source": "hack.incidents",
                "DetailType": "incident.created",
                "Detail": new_incident.model_dump_json(),
            }
        ]
    )

    return response(201, new_incident.model_dump_json())
