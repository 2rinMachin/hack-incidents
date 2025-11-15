import boto3

from common import response

dynamodb = boto3.resource("dynamodb")


def handler(event, context):
    orders = dynamodb.Table("hack-incidents")

    resp = orders.scan()
    orders = resp["Items"]

    return response(200, orders)
