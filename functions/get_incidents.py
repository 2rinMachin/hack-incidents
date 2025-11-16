import boto3

from common import response

dynamodb = boto3.resource("dynamodb")


def handler(event, context):
    incidents = dynamodb.Table("hack-incidents")

    resp = incidents.scan()
    incidents = resp.get("Items")

    return response(200, incidents)
