import json
import boto3
import requests

dynamodb = boto3.client('dynamodb')

def lambda_handler(event, context):
    print(r = requests.get('http://google.com?q=helloworld'))

    dynamodb.put_item(
        TableName='Games', 
        Item={
            'fruitName':{
                'S':'Banana'
            },
            'key2':{
                'N':'value2'
            }
        }
    )

    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!')
    }
