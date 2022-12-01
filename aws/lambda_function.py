import json
import boto3
import requests
import random
from shared.dynamo_db import *

ALLOW_CHEATING = True

# dynamodb = boto3.client('dynamodb')
sqs_resource = boto3.resource('sqs')
queue = sqs_resource.get_queue_by_name(QueueName='GameTasks')


def lambda_handler(event, context):
    message = event["Records"][0]

    # Get counter attribute from message object (will return None if "Counter" key does not exist)
    message_type = message["messageAttributes"].get("MessageType", {}).get("stringValue")

    if message_type == "AdministerQuestion":
        administer_question(message)
    elif message_type == "Monitor":
        monitor_game(message)


def administer_question(message):
    modification_hash = message["messageAttributes"].get("ModificationHash", {}).get("stringValue")
    question_text = message["messageBody"]

    game_id = message["messageAttributes"].get("GameID", {}).get("stringValue")
    player_id = message["messageAttributes"].get("PlayerID", {}).get("stringValue")
    question_score = message["messageAttributes"].get("QuestionScore", {}).get("stringValue")
    question_delay = message["messageAttributes"].get("QuestionDelay", {}).get("stringValue")
    question_difficulty = message["messageAttributes"].get("QuestionDifficulty", {}).get("stringValue", 0)

    if (game_id is None) or (player_id is None) or (question_score is None) or (question_delay is None):
        print("some attributes don't exist")

    question_score = int(question_score)
    question_delay = int(question_delay)

    # Check modification hash
    if db_is_game_paused(game_id):
        # put event back on the queue and return?
        reschedule_message(message)
        return

    # 1. Send request to player, and check response
    player = db_get_player(player_id)
    answer = None
    try:
        response = requests.get(player["player_api"], params={"q": question_text})

        if response.status_code == 200:
            answer = response.text.strip().lower()
        else:
            problem = "ERROR_RESPONSE"
    except Exception:
        problem = "NO_SERVER_RESPONSE"

    if answer is None:
        result = problem
    elif ALLOW_CHEATING and answer == "cheat":  # Allows cheating for demo/test purposes only (Remove)
        result = "CORRECT"
    elif answer == question_text["correct_answer"]:
        result = "CORRECT"
    else:
        result = "WRONG"

    player_position = db_get_player_position(game_id, player_id)
    points_gained = calculate_points_gained(player_position, question_score, result)

    # 2. Update database based on result

    # This function should add event to a player's list of events, and update their score in the database, nased on the result
    add_event(game_id, player_id, question_text, question_difficulty, points_gained, result)

    # 3. Schedule next question
    game_round = db_get_game_round(game_id)
    next_question = question_factory(game_round)


def monitor_game(message):
    gid = message["messageBody"]
    game = db_get_game(gid)

    if not game['paused'] and len(game['players']) > 0:         # Does ended => paused
        if game['auto_mode'] and game['round'] != 0:
            auto_increment_round(game['players'])
        update_player_to_assist()
        monitor_analysis_game()

    queue.send_message(
        MessageBody=str(gid)
        DelaySeconds=2,
        MessageAttributes={
            'MessageType': {
                'StringValue': 'Monitor',
                'DataType': 'String',
            }
        }
    )


def auto_increment_game(player_ids):
    ratio_threshold = 0.4
    advancable_players = 0

    for pid in player_ids:
        curr_player = db_get_player(pid)
        round_index = curr_player["round_index"]


def reschedule_message(message):
    pass
#     game_id = message["messageAttributes"].get("GameID", {}).get("stringValue")
#     player_id = message["messageAttributes"].get("PlayerID", {}).get("stringValue")
#     question_score = message["messageAttributes"].get("QuestionScore", {}).get("stringValue")
#     question_delay = message["messageAttributes"].get("QuestionDelay", {}).get("stringValue")
#     question_difficulty = message["messageAttributes"].get("QuestionDifficulty", {}).get("stringValue", -1)


# }
#     queue.send_message(
#         DelaySeconds = 10,
#         MessageBody = message["messageBody"],
#         MessageAttributes = message["messageAttributes"],
#     )


# def lambda_handler(event, context):

#     # Get message object
#     message = event.get("Records")[0]

#     # Get counter attribute from message object (will return None if "Counter" key does not exist)
#     counter = message["messageAttributes"].get(
#         "Counter", {}).get("stringValue")

#     if counter is not None:
#         counter = int(counter)
#     else:
#         print("counter attribute does not exist")
#         return

#     print("counter", counter)

#     counter -= 1

#     if counter <= 0:
#         return

#     res = queue.send_message(
#         DelaySeconds=10,
#         MessageBody="hello",
#         MessageAttributes={
#             'GameID': {
#                 'StringValue': 'test_id',
#                 'DataType': 'String'
#             },
#             'Counter': {
#                 'StringValue': str(counter),
#                 'DataType': 'Number'
#             },
#             'MessageType': {
#                 'StringValue': 'AdministerQuestion',
#                 'DataType': 'String'
#             }
#         }
#     )
#     print(res)
#     return


if __name__ == "__main__":
    pass
    # res = queue.send_message(
    #     # QueueUrl="https://sqs.eu-west-2.amazonaws.com/572990232030/GameTasks",
    #     DelaySeconds=10,
    #     MessageBody="hello",
    #     MessageAttributes={
    #         'GameID': {
    #             'StringValue': 'test_id',
    #             'DataType': 'String'
    #         },
    #         'Counter': {
    #             'StringValue': str(10),
    #             'DataType': 'Number'
    #         },
    #         'MessageType': {
    #             'StringValue': 'AdministerQuestion',
    #             'DataType': 'String'
    #         }
    #     }
    # )
    # print(res)
