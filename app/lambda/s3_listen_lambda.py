import json
import boto3

s3 = boto3.client('s3')

def handler(event, context):
    for record in event['Records']:
        bucket_name = record['s3']['bucket']['name']
        file_name = record['s3']['object']['key']
        
        # Fetch the JSON file from S3
        response = s3.get_object(Bucket=bucket_name, Key=file_name)
        content = response['Body'].read().decode('utf-8')
        data = json.loads(content)
        
        print(f"Processed file {file_name} from bucket {bucket_name}")
        print("Content:", data)

    return {
        'statusCode': 200,
        'body': json.dumps('Successfully processed S3 event')
    }
