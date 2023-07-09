import boto3
import os
from boto3.dynamodb.conditions import Key
import json

def lambda_handler(event, context):
    print(event)

    tenant_id = event['path']['tenant_id']
    route_id = event['path']['route_id']

    # Obtener ubicaciones de la ruta
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table(os.environ["TABLE_LOCATIONS"])

    response = table.query(
        KeyConditionExpression=(
            Key('tenant_id').eq(tenant_id) & Key('route_id').eq(route_id)
        )
    )
    items = response['Items']
    items = list(map((lambda o: json.loads(o['location'])), response['Items']))

    return {
        'statusCode': 200,
        'data': items
    }
