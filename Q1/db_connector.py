import json
import mysql.connector
import os
import boto3
from botocore.exceptions import ClientError

def get_secret(secret_name):
    region_name = "ap-southeast-2"

    # Create a Secrets Manager client
    session = boto3.session.Session()
    client = session.client(
        service_name='secretsmanager',
        region_name=region_name
    )

    try:
        get_secret_value_response = client.get_secret_value(
            SecretId=secret_name
        )
    except ClientError as e:
        # For a list of exceptions thrown, see
        # https://docs.aws.amazon.com/secretsmanager/latest/apireference/API_GetSecretValue.html
        raise e

    secret = get_secret_value_response['SecretString']
    return json.loads(secret)

def lambda_handler(event, context):
    secret_name = "rds!db-4c251e9a-5b77-483c-ab93-b48c1ff7e54b"
    secret = get_secret(secret_name)
    print(secret)

    # Connect to the MySQL database using credentials from Secrets Manager
    conn = mysql.connector.connect(
        host='database-1.c3eacmea6by0.ap-southeast-2.rds.amazonaws.com',
        user=secret['username'],
        password=secret['password'],
        database='pi_db'
    )

    cursor = conn.cursor()

    # Explicitly select the fields in the correct order
    query = """
        SELECT u.user_id, u.name, u.email, u.age, u.signup_date, 
        b.account_number, b.address, b.balance, b.debt
        FROM users u 
        JOIN bank_accounts b ON u.user_id = b.user_id
    """

    cursor.execute(query)
    rows = cursor.fetchall()

    # Process the results
    data = []
    for row in rows:
        data.append({
            "user_id": row[0],
            "name": row[1],
            "email": row[2],
            "age": row[3],
            "signup_date": str(row[4]),  # Convert date to string
            "account_number": row[5],
            "address": row[6],
            "balance": row[7],
            "debt": row[8]
        })

    # Close cursor and connection
    cursor.close()
    conn.close()

    return {
        'statusCode': 200,
        'body': data  
    }
