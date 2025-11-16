import boto3
from pydantic import BaseModel

from common import parse_body, response
from schemas import IncidentStatus

dynamodb = boto3.resource("dynamodb")
incidents = dynamodb.Table("hack-incidents")


class CloseIncidentRequest(BaseModel):
    id: str


def handler(event, context):
    data, err = parse_body(CloseIncidentRequest, event)
    if err != None:
        return err

    assert data != None

    incidents.update_item(
        Key={"id": data.id},
        UpdateExpression="SET #sts = :status",
        ExpressionAttributeNames={"#sts": "status"},
        ExpressionAttributeValues={":status": IncidentStatus.done},
    )

    return response(200, {"message": "Incident closed successfully."})
