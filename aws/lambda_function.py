import json
import boto3
import requests
import random


def lambda_handler(event, context):
    # dynamodb = boto3.client('dynamodb')
    sqs_resource = boto3.resource('sqs')
    queue = sqs_resource.get_queue_by_name(QueueName='GameTasks')

    message = event.get("Records")[0]
    counter_attribute = message["messageAttributes"].get("Counter")
    if counter_attribute is not None:
        counter = counter_attribute.get("stringValue", 0)

    print("counter", counter)

    counter -= 1

    if counter <= 0:
        return

    # res = queue.send_message(
    #     MessageBody="Hello",
    #     DelaySeconds=1,
    #     MessageAttributes={
    #         'GameID': {
    #             'StringValue': 'test_id',
    #             'DataType': 'String'
    #         },
    #         'Counter': {
    #             'StringValue': str(counter),
    #             'DataType': 'Number'
    #         },
    #         'MessageType': {
    #             'StringValue': 'AdministerQuestion',
    #             'DataType': 'String'
    #         }
    #     }
    # )

    sqs = boto3.client('sqs')
    res = sqs.send_message(
        QueueUrl="https://sqs.eu-west-2.amazonaws.com/572990232030/GameTasks",
        MessageBody="hello",
        MessageAttributes={
            'GameID': {
                'StringValue': 'test_id',
                'DataType': 'String'
            },
            'Counter': {
                'StringValue': str(counter_attribute),
                'DataType': 'Number'
            },
            'MessageType': {
                'StringValue': 'AdministerQuestion',
                'DataType': 'String'
            }
        }
    )
    print(res)
    return {
        'statusCode': 200,
        'body': json.dumps(counter_attribute)
    }


# if db_is_game_paused(event["game_id"]):
#     # put event back on the queue and return?
#     pass

# # 1. Send request to player, and check response
# question = event["question"]
# try:
#     response = requests.get(event["player_api"], params={"q": question["text"]})

#     if response.status_code == 200:
#         answer = response.text.strip().lower()
#     else:
#         answer = "ERROR_RESPONSE"
# except Exception:
#     answer = "NO_SERVER_RESPONSE"

# # Allows cheating for demo/test purposes only
# if event["ALLOW_CHEATING"] and answer == "cheat":
#     result = "CORRECT"
# # Check response is correct
# # elif answer == event["correct_answer"]:
# #     result = "CORRECT"
# # else:
# #     result = "WRONG"
# result = answer == question["correct_answer"]

# # 2. Update database based on result
# if result:
#     pass
#     # db_correct_answer(game_id, player_id, question)?

if __name__ == "__main__":
    sqs = boto3.client('sqs')
    res = sqs.send_message(
        QueueUrl="https://sqs.eu-west-2.amazonaws.com/572990232030/GameTasks",
        MessageBody="hello",
        MessageAttributes={
            'GameID': {
                'StringValue': 'test_id',
                'DataType': 'String'
            },
            'Counter': {
                'StringValue': '10',
                'DataType': 'Number'
            },
            'MessageType': {
                'StringValue': 'AdministerQuestion',
                'DataType': 'String'
            }
        }
    )
    print(res)
