import json
import boto3
import requests
import random
from shared.dynamo_db import *

ALLOW_CHEATING = True

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
    else:
        print("Invalid message type")
        return


def administer_question(message):
    # Validate hash
    modification_hash = message["messageAttributes"].get("ModificationHash", {}).get("stringValue")

    message = json.loads(message["messageBody"])

    game_id = message.get("game_id")  # string
    player_id = message.get("player_id")  # string
    question_text = message.get("question_text")  # string
    question_answer = message.get("question_answer")  # string
    prev_delay = message.get("prev_delay")  # int
    question_score = message.get("question_score")  # int
    question_difficulty = message.get("question_difficulty")  # int

    if (game_id is None) or (player_id is None) or (question_text is None) or (question_answer is None) or (prev_delay is None) or (question_score is None) or (question_difficulty is None):
        print("Error: Some attributes do not exist")
        return

    if db_is_game_paused(game_id):
        # put event back on the queue and return?
        reschedule_message(message)
        return

    # 1. Send request to player, and check response
    player = db_get_player(player_id)
    try:
        response = requests.get(player["API"], params={"q": question_text})

        if response.status_code == 200:
            answer = response.text.strip().lower()
        else:
            answer = "ERROR_RESPONSE"

    except Exception:
        answer = "NO_SERVER_RESPONSE"

    if answer == "ERROR_RESPONSE" or answer == "NO_SERVER_RESPONSE":
        result = answer
    elif ALLOW_CHEATING and answer == "cheat":  # Allows cheating for demo/test purposes only (Remove)
        result = "CORRECT"
    elif answer == question_answer:
        result = "CORRECT"
    else:
        result = "WRONG"

    # 2. Update database based on result
    player_position = db_get_leaderboard_position(game_id, player_id)
    points_gained = calculate_points_gained(player_position, question_score, result)
    # This function should add event to a player's list of events, and update their score in the database, based on the result
    add_event(game_id, player_id, question_text, question_difficulty, points_gained, result)

    # 3. Schedule next question
    game_round = db_get_game_round(game_id)
    next_question = question_factory(game_round)
    next_delay = rate_controller(prev_delay, result)

    message = {
        "game_id": game_id,
        "player_id": player_id,
        "question_text": next_question.as_text(),
        "question_answer": next_question.correct_answer(),
        "prev_delay": next_delay,
        "question_score": next_question.points,
        "question_difficulty": question_difficulty
    }

    queue.send_message(
        MessageBody=json.dumps(message),
        DelaySeconds=next_delay,
        MessageAttributes={
            'MessageType': {
                'StringValue': 'AdministerQuestion',
                'DataType': 'String'
            },
            'ModificationHash': {
                'StringValue': modification_hash,  # Need to get a new modification hash
                'DataType': 'String'
            },
        }
    )
    return


def monitor_game(message):
    gid = int(message["messageBody"])
    game = db_get_game(gid)

    if not game['paused'] and len(game['players']) > 0:         # Does ended => paused
        if game['auto_mode'] and game['round'] != 0:
            auto_increment_round(game)
        update_player_to_assist()
        monitor_analysis_game()

    queue.send_message(
        MessageBody=str(gid),
        DelaySeconds=5,
        MessageAttributes={
            'MessageType': {
                'StringValue': 'Monitor',
                'DataType': 'String',
            }
        }
    )


def auto_increment_game(game):
    ratio_threshold = 0.4
    advancable_players = 0

    for pid in game["players"]:
        curr_player = db_get_player(pid)
        round_index = curr_player["round_index"]
        position = db_get_leaderboard_position(pid)       # TODO: Implement this function
        round_streak = curr_player["streak"][-round_index:] if round_index != 0 else ""

        c_tail = streak_length(round_streak, "1")

        if c_tail >= 6 and position <= max(0.6 * len(player_ids), 1):
            advancable_players += 1

    if advancable_players / len(player_ids) > ratio_threshold:
        db_advance_round(pid)


def update_players_to_assist(game):
    players_to_assist = db_get_players_to_assist(game["id"])
    needs_assistance = players_to_assist["needs_assistance"]
    being_assisted = players_to_assist["being_assisted"]

    for pid in game["players"]:
        curr_player = db_get_player(pid)
        curr_name = curr_player["name"]
        streak, round_index = curr_player["streak"], curr_player["round_index"]
        round_streak = streak[-round_index:] if round_index != 0 else ""

        # corect and incorrect tail(s)
        c_tail, ic_tail = (
            streak_length(round_streak, STREAK_CHARS[0]),
            streak_length(round_streak, "".join(STREAK_CHARS[1:])),
        )

        if c_tail > 0:
            try:
                if curr_name in needs_assistance:
                    needs_assistance.remove(curr_name)
                elif curr_name in being_assisted:
                    being_assisted.remove(curr_name)
            except:
                print("MONITOR THREAD: TRIED REMOVING " + curr_name + " FROM needs_assitance/being_assisted WHEN MAIN THREAD ATTEMPTED MODIFYING SAID LISTS. CONTINUING ON...")

        elif ic_tail > 15 and (curr_name not in needs_assistance and curr_name not in being_assisted):
            needs_assistance.append(curr_name)

    db_set_players_to_assist(game["id"], players_to_assist)          # TODO: Implement this function


def streak_length(response_history, streak_char):
    return len(response_history) - len(response_history.rstrip(streak_char))


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
