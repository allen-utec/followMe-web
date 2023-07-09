import boto3
import json
import os

def lambda_handler(event, context):
    body = json.loads(event['Records'][0]['body'])
    Message = json.loads(body['Message'])

    # Guardar usuario
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table(os.environ["TABLE_USERS"])
    response = table.put_item(
        Item={
            'tenant_id': Message['tenant_id'],
            'user_id': Message['user_id']
        }
        ConditionExpression='attribute_not_exists(tenant_id) AND attribute_not_exists(user_id)'
    )
    print(response)

    return {
        'statusCode': response['ResponseMetadata']['HTTPStatusCode'],
    }
