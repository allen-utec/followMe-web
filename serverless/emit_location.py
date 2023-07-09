import boto3
import json
import os

def lambda_handler(event, context):
    body = event['body']

    # Publicar en SNS
    sns_client = boto3.client('sns')
    response = sns_client.publish(
        TopicArn = os.environ["TOPIC_LOCATION_ARN"],
        Subject = 'New Location',
        Message = json.dumps({
            'tenant_id': body['tenant_id'],
            'route_id': body['route_id'],
            'location': body['location']
        }),
        MessageAttributes = {
            'tenant_id': { 'DataType': 'String', 'StringValue': body['tenant_id'] },
            'counter': {'DataType': 'Number', 'StringValue': str(body['counter']) }
        }
    )
    print(response)

    return {
        'statusCode': response['ResponseMetadata']['HTTPStatusCode'],
    }
