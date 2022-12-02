import json
import boto3
from botocore.exceptions import ClientError
import requests
from datetime import datetime
from flaskr.shared.dynamo_db import *
from flaskr.shared.question_factory import QuestionFactory
from flaskr.shared.rate_controller import RateController

ALLOW_CHEATING = True
PROBLEM_DECREMENT = 50
STREAK_LENGTH = 30

sqs_resource = boto3.resource('sqs')
queue = sqs_resource.get_queue_by_name(QueueName='GameTasks')

def print_dict_nicely(dic):
    print(json.dumps(dic, sort_keys=True, indent=4))


def lambda_handler(event, context):

    print("The event is as follows:")
    print_dict_nicely(event)

    message = event["Records"][0]
    message_type = message["messageAttributes"].get("MessageType", {}).get("stringValue")

    if message_type == "AdministerQuestion":
        administer_question(message)
    elif message_type == "Monitor":
        monitor_game(message)
    else:
        print("Invalid message type")
        return


def administer_question(sqs_message):
    # TODO: validate modification hash
    modification_hash = sqs_message["messageAttributes"].get("ModificationHash", {}).get("stringValue")

    try:
        message = json.loads(sqs_message["body"])
    except json.decoder.JSONDecodeError as e:
        print(f"Json error occured when trying to parse message {sqs_message['body']}")
        print(e)
        return

    game_id = message.get("game_id")  # string
    player_id = message.get("player_id")  # string
    question_text = message.get("question_text")  # string
    question_answer = message.get("question_answer")  # string
    prev_delay = message.get("prev_delay")  # int
    question_points = message.get("question_points")  # int
    question_difficulty = message.get("question_difficulty")  # int



    try:
        game = db_get_game(game_id)
    except ClientError as e:
        print(f"Error! Game with id {game_id} DOES NOT EXIST or cannot be accessed or eradicated by Andrey")
        print(e)
        return


    if not all(map(lambda it: it is not None, [
        game_id, player_id, question_text, question_answer,
        prev_delay, question_points, question_difficulty
    ])):
        print("ERROR: Some attributes do not exist. The attribute values are as follows:")
        print(f"""
            game_id: {game_id},
            player_id: {player_id},
            question_text: {question_text},
            question_answer: {question_answer},
            prev_delay: {prev_delay},
            question_points: {question_points},
            question_difficulty: {question_difficulty}
        """)
        return

    player = None
    try:
        player = db_get_player(game_id, player_id)
    except ClientError as e:
        print(f"Error occured when trying to get player with id {player_id} in game {game_id}")
        print(e)
        return


    if db_game_ended(game_id) or not player['active']:
        print("Game is ended")
        return  # Terminate lambda loop

    if db_is_game_paused(game_id):
        # Put equivalent message on SQS queue again
        print("Game is paused. Resending message")
        queue.send_message(sqs_message)
        return

    # 1. Send request to player, and check response
    if db_get_game(game_id)['round'] == 1 and player['round_index'] == 0:
        # Reset score to 0 once warmup ends, add to running_totals
        db_set_player_score(game_id, player_id, 0)
        db_set_player_streak(game_id, player_id, "")
        db_set_player_correct_tally(game_id, player_id, 0)
        db_set_player_incorrect_tally(game_id, player_id, 0)
        db_set_request_count(game_id, player_id, 0)

        db_add_running_total(game_id, player_id, 0, dt.datetime.now(dt.timezone.utc))

    try:
        response = requests.get(player["api"], params={"q": question_text})

        if response.status_code == 200:
            answer = response.text.strip().lower()
        else:
            answer = "ERROR_RESPONSE"
    except Exception as e:
        print("Player's server did not respond!")
        print(e)
        answer = "NO_SERVER_RESPONSE"

    # Get result of question
    if answer == "ERROR_RESPONSE" or answer == "NO_SERVER_RESPONSE":
        result = answer
    elif ALLOW_CHEATING and answer == "cheat":  # Allows cheating for demo/test purposes only (Remove)
        result = "CORRECT"
    elif answer == question_answer:
        result = "CORRECT"
    else:
        result = "WRONG"

    # 2. Update database based on result
    player_position = player_leaderboard_position(game_id, player_id)
    points_gained = int(calculate_points_gained(player_position, question_points, result))
    new_score = points_gained + int(player["score"])
    # This function should add event to a player's list of events, and update their score in the database, based on the result
    add_event(game_id, player_id, question_text, question_difficulty, points_gained, result)
    db_add_running_total(game_id, player_id, new_score, datetime.now(dt.timezone.utc))
    db_set_player_score(game_id, player_id, new_score)

    # 3. Schedule next question on queue
    game_round = db_get_game_round(game_id)
    next_question = QuestionFactory().next_question(game_round)
    next_delay = RateController().delay_before_next_question(prev_delay, result)
    print("next delay is", next_delay)

    message = {
        "game_id": game_id,
        "player_id": player_id,
        "question_text": next_question.as_text(),
        "question_answer": next_question.correct_answer(),
        "prev_delay": next_delay,
        "question_points": next_question.points,
        "question_difficulty": question_difficulty
    }

    res = queue.send_message(
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
    print(f"sent message as follows:")
    print_dict_nicely(message)
    return json.dumps(res)



def add_event(game_id, player_id, question_text, question_difficulty, points_gained, result):
    db_add_event(game_id, player_id, question_text, question_difficulty, points_gained, result)



def calculate_points_gained(player_position, question_points, result, lenient=True):
    if result == "CORRECT":
        return question_points

    # What is lenient mode and do we need it - Dev?
    elif result == "WRONG":
        return -1 * question_points / player_position
        # return (
        #     self.allow_passes(question, leaderboard_position)
        #     if lenient
        #     else self.penalty(question, leaderboard_position)
        # )

    elif result == "ERROR_RESPONSE" or result == "NO_SERVER_RESPONSE":
        return -1 * PROBLEM_DECREMENT

    else:
        print(f"Error: unrecognized result {result}")

# # Based on game mode (lenient), let player "off" for incorrect response
# def allow_passes(self, question, leaderboard_position):
#     return (
#         0 if question.answer == "" else self.penalty(question, leaderboard_position)
#     )

# # Penalty that adjusts based on leadeboard pos
# # Conceptually, better-ranked players get deducted more for wrong answers than worse-ranked players
# def penalty(self, question, leaderboard_position):
#     return -1 * question.points / leaderboard_position


def monitor_game(message):
    gid = message["body"]
    modification_hash = message["messageAttributes"].get("ModificationHash", {}).get("stringValue")

    try:
        game = db_get_game(gid)
        print(f"The game obtained from db is {game}")
    except ClientError as e:
        print(f"Error! Game with id {gid} DOES NOT EXIST or cannot be accessed or eradicated by Andrey")
        print(e)
        return

    if game['ended'] and not db_check_state_modification_hash(gid, modification_hash):
        return

    if not game['paused'] and len(game['players']) > 0:
        if game['auto_mode'] and game['round'] != 0:
            auto_increment_round(game)
        update_player_to_assist(game)
        monitor_analysis_game()

    queue.send_message(
        MessageBody=str(gid),
        DelaySeconds=40,
        MessageAttributes={
            'MessageType': {
                'StringValue': 'Monitor',
                'DataType': 'String',
            }
        }
    )


def auto_increment_round(game):
    ratio_threshold = 0.4
    advancable_players = 0

    for pid in game["players"]:
        curr_player = db_get_player(game['id'], pid)
        round_index = curr_player["round_index"]
        position = player_leaderboard_position(game['id'], pid)
        round_streak = curr_player["streak"][-round_index:] if round_index != 0 else ""

        c_tail = streak_length(round_streak, "1")

        if c_tail >= 6 and position <= max(0.6 * len(game['players']), 1):
            advancable_players += 1

    if advancable_players / len(game['players']) > ratio_threshold:
        db_advance_round(pid)


def update_player_to_assist(game):
    players_to_assist = db_get_players_to_assist(game["id"])
    needs_assistance = players_to_assist["needs_assistance"]
    being_assisted = players_to_assist["being_assisted"]

    for pid in game["players"]:
        curr_player = db_get_player(game["id"], pid)
        curr_name = curr_player["name"]
        streak, round_index = curr_player["streak"], curr_player["round_index"]
        round_streak = streak[-round_index:] if round_index != 0 else ""

        # corect and incorrect tail(s)
        c_tail, ic_tail = (
            streak_length(round_streak, "1"),
            streak_length(round_streak, "X0"),
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

    db_set_players_to_assist(game["id"], players_to_assist)


def monitor_analysis_game():
    # TODO
    pass


def streak_length(response_history, streak_char):
    return len(response_history) - len(response_history.rstrip(streak_char))


def player_leaderboard_position(game_id, player_id):
    scoreboard = db_get_scoreboard(game_id)
    leaderboard = {k: v
                   for k, v in sorted(
                       scoreboard.items(), key=lambda item: item[1]['score'], reverse=True
                   )
                   }
    return list(leaderboard.keys()).index(player_id) + 1


if __name__ == "__main__":
    pass
