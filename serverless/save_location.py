import boto3
import json
import os

def lambda_handler(event, context):
    body = json.loads(event['Records'][0]['body'])
    Message = json.loads(body['Message'])

    # Guardar ubicación
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table(os.environ["TABLE_LOCATIONS"])
    response = table.put_item(Item={
        'tenant_id': Message['tenant_id'],
        'route_id': Message['route_id'],
        'location_id': Message['location_id'],
        'data': json.dumps(Message['data'])
    })
    print(response)

    return {
        'statusCode': response['ResponseMetadata']['HTTPStatusCode'],
    }
