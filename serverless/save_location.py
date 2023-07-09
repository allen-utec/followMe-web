import boto3
import json

def lambda_handler(event, context):
    print(event)

    body = json.loads(event['Records'][0]['body'])

    # Guardar ubicación
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table(os.environ["TABLE_LOCATIONS"])
    response = table.put_item(Item={
        'tenant_id': body['tenant_id'],
        'route_id': body['route_id'],
        'location': body['location']
    })
    print(response)

    return {
        'statusCode': 200
    }
