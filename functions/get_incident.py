import boto3

from common import response

sfn = boto3.client("stepfunctions")
dynamodb = boto3.resource("dynamodb")

incidents = dynamodb.Table("hack-incidents")


def handler(event, context):
    incident_id = event["pathParameters"]["incident_id"]

    resp = incidents.get_item(Key={"id": incident_id})
    item: dict | None = resp.get("Item")

    if item == None:
        return response(404, {"message": "Incident not found."})

    return response(200, item)
