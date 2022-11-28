import json
import boto3
import requests

db = boto3.client('dynamodb').Table("Games")

def lambda_handler(event, context):
    print(r = requests.get('http://google.com?q=helloworld'))

    db.put_item(
        Item={
            'game_id':{
                'S':'Banana'
            },
            'players':{
                'N':'value2'
            }
        }
    )

    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!')
    }
