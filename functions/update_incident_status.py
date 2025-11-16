import boto3
from pydantic import BaseModel

from common import parse_body, response
from schemas import Incident, IncidentStatus

events = boto3.client("events")
dynamodb = boto3.resource("dynamodb")
incidents = dynamodb.Table("hack-incidents")


class UpdateIncidentStatusRequest(BaseModel):
    id: str
    status: IncidentStatus


def handler(event, context):
    data, err = parse_body(UpdateIncidentStatusRequest, event)
    if err != None:
        return err

    assert data != None

    resp = incidents.update_item(
        Key={"id": data.id},
        UpdateExpression="SET #sts = :status",
        ExpressionAttributeNames={"#sts": "status"},
        ExpressionAttributeValues={":status": data.status},
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
