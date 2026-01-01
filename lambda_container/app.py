import json
import boto3
import os
import uuid
import sys
from datetime import datetime

model = None
load_error = None

def load_ai_assets():
    """ Safely loads heavy AI libraries """
    global model
    try:
        print("INIT: Importing Scikit-Learn & Pandas...")
        import joblib
        import pandas as pd
        
        print("INIT: Loading Model File...")
        model = joblib.load('lead_scoring_model.joblib')
        print("INIT: Model Loaded Successfully!")
        return True, None
    except Exception as e:
        import traceback
        err = f"AI CRASH: {str(e)}\n{traceback.format_exc()}"
        print(err)
        return False, err

success, load_error = load_ai_assets()

def handler(event, context):
    """ Main Lambda Entrypoint """
    global model, load_error

    if load_error:
        return {
            'statusCode': 200, # Return 200 so we see the error!
            'body': json.dumps({
                'status': 'CRITICAL_FAILURE',
                'error': load_error,
                'python_version': sys.version
            })
        }

    try:
        body = event.get('body')
        if isinstance(body, str):
            data = json.loads(body)
        else:
            data = body or {}

        #predict
        import pandas as pd
        
        budget = int(data.get('budget', 0))
        clicks = int(data.get('email_clicks', 0))
        days = int(data.get('days_on_market', 1))

        features = pd.DataFrame([[budget, clicks, days]], 
                              columns=['budget', 'email_clicks', 'days_on_market'])

        probability = model.predict_proba(features)[0][1]
        ai_score = int(probability * 100)

        table_name = os.environ.get('TABLE_NAME')
        if table_name:
            dynamodb = boto3.resource('dynamodb')
            table = dynamodb.Table(table_name)
            item = {
                'lead_id': str(uuid.uuid4()),
                'name': data.get('name', 'Unknown'),
                'ai_score': ai_score,
                'timestamp': datetime.utcnow().isoformat()
            }
            table.put_item(Item=item)

        return {
            'statusCode': 200,
            'body': json.dumps({
                'message': 'Lead Analyzed',
                'ai_score': ai_score,
                'status': 'HOT' if ai_score > 50 else 'COLD'
            })
        }

    except Exception as e:
        import traceback
        return {
            'statusCode': 200,
            'body': json.dumps({
                'status': 'RUNTIME_ERROR',
                'error': str(e),
                'trace': traceback.format_exc()
            })
        }