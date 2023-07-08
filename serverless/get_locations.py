import boto3

def lambda_handler(event, context):
    print(event)

    tenant_id = event['pathParameters']['tenant_id']
    route_id = event['pathParameters']['route_id']

    # Obtener ubicaciones de la ruta
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table(os.environ["TABLE_LOCATIONS"])

    response = table.query(
        KeyConditionExpression=(
            Key('tenant_id').eq(tenant_id) & Key('route_id').eq(route_id)
        )
    )
    items = response['Items']

    return {
        'statusCode': 200,
        'data': items
    }
