import json
import os
import boto3
import datetime

s3 = boto3.client('s3')
bucket_name = os.environ['BUCKET_NAME']

def handler(event, context):
    # Create a sample JSON object
    data = {
        'timestamp': datetime.datetime.now().isoformat(),
        'message': 'Hello, world!'
    }
    
    # Create a JSON file in S3
    file_name = f"sample-{datetime.datetime.now().strftime('%Y-%m-%d-%H-%M-%S')}.json"
    s3.put_object(Bucket=bucket_name, Key=file_name, Body=json.dumps(data))
    return {
        'statusCode': 200,
        'body': json.dumps(f'Successfully created {file_name} in {bucket_name}')
    }
