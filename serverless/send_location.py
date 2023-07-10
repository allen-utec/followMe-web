import boto3
import json
import os

def lambda_handler(event, context):
    body = event['body']

    tenant_id = body['tenant_id']
    user_id = body['user_id']
    route_id = body['route_id']
    counter = str(body['counter'])
    data = body['location']

    # Publicar en SNS
    sns_client = boto3.client('sns')
    response = sns_client.publish(
        TopicArn = os.environ["TOPIC_LOCATION_ARN"],
        Subject = 'New Location',
        Message = json.dumps({
            'tenant_id': tenant_id,
            'user_id': route_id,
            'route_id': route_id,
            'location_id': route_id + '-' + counter,
            'data': data
        }),
        MessageAttributes = {
            'tenant_id': { 'DataType': 'String', 'StringValue': tenant_id },
            'route_id': { 'DataType': 'String', 'StringValue': route_id },
            'counter': {'DataType': 'Number', 'StringValue': counter }
        }
    )
    print(response)

    return {
        'statusCode': response['ResponseMetadata']['HTTPStatusCode'],
    }
