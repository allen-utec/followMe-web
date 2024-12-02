import boto3
import json
import os

def lambda_handler(event, context):
    Message = json.loads(event['Records'][0]['Sns']['Message'])

    tenant_id = Message['tenant_id']
    user_id = Message['user_id']

    t_users = os.environ["TABLE_USERS"]

    # Guardar usuario
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table(t_users)
    response = table.put_item(Item={
        'tenant_id': tenant_id,
        'user_id': user_id
    })
    print(response)

    return {
        'statusCode': response['ResponseMetadata']['HTTPStatusCode'],
    }
