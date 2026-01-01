import json
import boto3
import os
import uuid
from datetime import datetime
import traceback  # Helps us see the error message

# Initialize DB connection
try:
    dynamodb = boto3.resource('dynamodb')
    table_name = os.environ.get('TABLE_NAME') # Use .get() to avoid crashing if missing
    if table_name:
        table = dynamodb.Table(table_name)
    else:
        table = None
except Exception as e:
    print(f"INIT ERROR: {str(e)}")
    table = None

def handler(event, context):
    try:
        # DEBUG: Print the event to CloudWatch logs (optional, but good for debugging)
        print("Received event:", json.dumps(event))

        if not table:
            raise Exception("Table name not found in environment variables.")

        # 1. robust Body Parsing
        body = event.get('body')
        if not body:
            return {'statusCode': 400, 'body': json.dumps('Error: No body found')}
            
        # If body is a string, parse it. If it's already a dict, use it.
        if isinstance(body, str):
            data = json.loads(body)
        else:
            data = body

        # 2. Validation
        if 'name' not in data or 'budget' not in data:
            return {
                'statusCode': 400, 
                'body': json.dumps(f"Error: Missing fields. Received: {data.keys()}")
            }

        # 3. Structure Data
        lead_id = str(uuid.uuid4())
        item = {
            'lead_id': lead_id,
            'name': data['name'],
            'budget': int(data['budget']), # Ensure it's a number
            'email': data.get('email', 'N/A'),
            'status': 'NEW',
            'created_at': datetime.utcnow().isoformat(),
            'ai_score': 0 
        }

        # 4. Save to DynamoDB
        table.put_item(Item=item)

        return {
            'statusCode': 200,
            'body': json.dumps({'message': 'Lead Ingested', 'id': lead_id})
        }

    except Exception as e:
        # This will print the actual error to the logs and return it to you
        traceback.print_exc()
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e), 'trace': traceback.format_exc()})
        }