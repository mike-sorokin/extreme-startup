import json
import boto3
import requests
from flaskr.shared.dynamo_db import *

dynamodb = boto3.client('dynamodb')

def lambda_handler(event, context):
    if db_is_game_paused(event["game_id"]):
        # put event back on the queue and return?
        pass

    # 1. Send request to player, and check response
    question = event["question"]
    try:
        response = requests.get(event["player_api"], params={"q": question["text"]})

        if response.status_code == 200:
            answer = response.text.strip().lower()
        else:
            answer = "ERROR_RESPONSE"
    except Exception:
        answer = "NO_SERVER_RESPONSE"

    # Allows cheating for demo/test purposes only
    if event["ALLOW_CHEATING"] and answer == "cheat":
        result = "CORRECT"
    # Check response is correct
    # elif answer == event["correct_answer"]:
    #     result = "CORRECT"
    # else:
    #     result = "WRONG"
    result = answer == question["correct_answer"]

    # 2. Update database based on result
    if result:
        pass
        # db_correct_answer(game_id, player_id, question)?


if __name__ == "__main__":
    lambda_handler(None, None)