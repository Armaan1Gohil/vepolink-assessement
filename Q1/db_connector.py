import json
import mysql.connector
import os

def lambda_handler(event, context):
    # Connect to the MySQL database
    conn = mysql.connector.connect(
        host='database-1.c3eacmea6by0.ap-southeast-2.rds.amazonaws.com',
        user='admin',
        password='s-3g0ywfMLyA<(_9P6BNUpra?t?d',
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
            "balance": row[7],  # Now the correct balance is mapped
            "debt": row[8]
        })
    
    # Close cursor and connection
    cursor.close()
    conn.close()
    
    return {
        'statusCode': 200,
        'body': data  # Convert to JSON string
    }
