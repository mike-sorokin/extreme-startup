import json

import requests

def lambda_handler(event, context):
    print(r = requests.get('http://google.com?q=helloworld'))
    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!')
    }
