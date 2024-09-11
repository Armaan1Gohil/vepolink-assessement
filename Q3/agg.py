import json
import boto3
import pandas as pd
import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)

s3_client = boto3.client('s3')

def lambda_handler(event, context):

    bucket_name = 'transformed-assessment'
    file_key = event['Records'][0]['s3']['object']['key']
    

    logger.info(f"Processing file from S3 bucket: {bucket_name}, file key: {file_key}")
    

    response = s3_client.get_object(Bucket=bucket_name, Key=file_key)
    content = response['Body'].read().decode('utf-8')
    

    data = json.loads(content)
    df = pd.DataFrame(data)
    

    age_group_counts = df['age_group'].value_counts().to_dict()
    balance_group_counts = df['balance_group'].value_counts().to_dict()
    

    logger.info(f"Age group counts: {age_group_counts}")
    logger.info(f"Balance group counts: {balance_group_counts}")
    

    return {
        'statusCode': 200,
        'body': {
            'age_group_counts': age_group_counts,
            'balance_group_counts': balance_group_counts
        }
    }
