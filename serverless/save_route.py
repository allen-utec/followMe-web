import boto3
import base64

def lambda_handler(event, context):
    body = event['body']

    tenant_id = body['tenant_id']
    route_id = body['route_id']
    image = body['image']

    # Crear archivo en S3
    s3 = boto3.client('s3')
    response = s3.put_object(
        Bucket = os.environ["BUCKET_ROUTE"],
        Key = tenant_id + '/' + route_id + '.png'
        Body = base64.b64decode(image),
    )
    print(response)

    return {
        'statusCode': response['ResponseMetadata']['HTTPStatusCode'],
    }
