import boto3
import base64

def lambda_handler(event, context):
    body = event['body']

    tenant_id = body['tenant_id']
    route_id = body['route_id']
    image = body['image']

    bucket_name = os.environ["BUCKET_ROUTE"]
    object_key = tenant_id + '/' + route_id + '.png'

    # Crear archivo en S3
    s3 = boto3.client('s3')
    response = s3.put_object(
        Bucket = bucket_name,
        Key = object_key,
        Body = base64.b64decode(image),
    )
    print(response)

    presigned_url = s3.generate_presigned_url(
        'get_object',
        Params = {'Bucket': bucket_name, 'Key': object_key},
        ExpiresIn = 3600
    )
    print(presigned_url)

    # Publicar en SNS
    sns_client = boto3.client('sns')
    response = sns_client.publish(
        TopicArn = os.environ["TOPIC_ROUTE_ARN"],
        Subject = 'Route Finished',
        Message = json.dumps({
            'tenant_id': tenant_id,
            'route_id': route_id,
            'route_snapshot_url': presigned_url
        })
    )
    print(response)

    return {
        'statusCode': response['ResponseMetadata']['HTTPStatusCode'],
    }
