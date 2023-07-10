import boto3
import json
import os

def lambda_handler(event, context):
    body = event['body']

    tenant_id = body['tenant_id']
    route_id = body['route_id']
    counter = str(body['counter'])

    # Publicar en SNS
    sns_client = boto3.client('sns')
    response = sns_client.publish(
        TopicArn = os.environ["TOPIC_LOCATION_ARN"],
        Subject = 'New Location',
        Message = json.dumps({
            'tenant_id': tenant_id,
            'location_id': route_id + '-' + counter,
            'route_id': route_id,
            'data': body['location']
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
