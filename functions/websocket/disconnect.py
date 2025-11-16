import boto3

from common import response

dynamodb = boto3.resource("dynamodb")
subscriptions = dynamodb.Table("hack-incidents-subscriptions")


def handler(event, context):
    connection_id = event["requestContext"]["connectionId"]

    try:
        subscriptions.delete_item(
            Key={"connection_id": connection_id},
        )
    except KeyError:
        pass

    return response(204, None)
