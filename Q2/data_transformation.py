import json
import boto3
import pandas as pd
import re
from io import StringIO

s3_client = boto3.client('s3')

lambda_client = boto3.client('lambda')

def is_valid_email(email):
    email_regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
    return bool(re.match(email_regex, email))

def format_balance_group(interval):
    if pd.isnull(interval):
        return "0-50K"
    else:
        lower_bound = int(interval.left) // 1000
        upper_bound = int(interval.right) // 1000
        return f"{lower_bound}K-{upper_bound}K"

def lambda_handler(event, context):

    response = lambda_client.invoke(
        FunctionName='db-connector', 
        InvocationType='RequestResponse',
        Payload=json.dumps(event)
    )
    

    response_payload = json.loads(response['Payload'].read())
    extracted_data = response_payload['body']


    df = pd.DataFrame(extracted_data)
    

    df['balance'] = pd.to_numeric(df['balance'], errors='coerce').fillna(0)
    df['age'] = pd.to_numeric(df['age'], errors='coerce').fillna(0)
    

    df = df[df['email'].apply(is_valid_email)]
    df = df[(df['age'] > 0) & (df['age'] <= 100)]
    


    df['age_group'] = pd.cut(df['age'], bins=range(0, 101, 5), right=False, labels=[f'{i}-{i+4}' for i in range(0, 100, 5)])
    

    max_balance = int(df['balance'].max()) + 50000
    df['balance_group'] = pd.cut(df['balance'], bins=range(0, max_balance, 50000), right=False)
    

    df['balance_group'] = df['balance_group'].apply(format_balance_group)
    

    transformed_data_json = df.to_json(orient='records')
    


    bucket_name = 'transformed-assessment'
    file_name = 'transformed_data.json'

    s3_client.put_object(
        Bucket=bucket_name,
        Key=file_name,
        Body=transformed_data_json,
        ContentType='application/json'
    )
    

    return {
        'statusCode': 200,
        'body': f'File uploaded to S3 bucket "{bucket_name}" as "{file_name}"'
    }
