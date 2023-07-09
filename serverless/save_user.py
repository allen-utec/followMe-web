import boto3
import json
import os

def lambda_handler(event, context):
    body = event['body']

    # Guardar usuario
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table(os.environ["TABLE_USERS"])
    response = table.put_item(
        Item={
            'tenant_id': body['tenant_id'],
            'user_id': body['user_id']
        }
        ConditionExpression='attribute_not_exists(tenant_id) AND attribute_not_exists(user_id)'
    )
    print(response)

    return {
        'statusCode': 200
    }
