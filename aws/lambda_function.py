import json
import boto3
import requests

dynamodb = boto3.client('dynamodb')

def lambda_handler(event, context):
    print(requests.get('http://google.com?q=helloworld'))

    dynamodb.put_item(
        TableName='Games', 
        Item={
            'game_id': {
                'S': 'alkdfjbasldfjn'
            },
            'fruitName':{
                'S':'Banana'
            },
            'vegetableName':{
                'S':'Potato'
            },
            'exampleNumber':{
                'N':'123'
            }
        }
    )

    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!')
    }


if __name__ == "__main__":
    lambda_handler(None, None)