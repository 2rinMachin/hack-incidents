import boto3
from pydantic import BaseModel

from common import parse_body, response
from schemas import IncidentStatus

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

    return response(200, resp["Attributes"])
