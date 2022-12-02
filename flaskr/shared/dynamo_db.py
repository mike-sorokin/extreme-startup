import boto3
from uuid import uuid4
import datetime as dt

dynamo_client = boto3.client('dynamodb')
dynamo_resource = boto3.resource('dynamodb')


def convert_decimals(event_dic):
    event_dic['difficulty'] = int(event_dic['difficulty'])
    event_dic['points_gained'] = int(event_dic['points_gained'])
    return event_dic


def db_get_all_games():
    game_tables = list(dynamo_resource.tables.all())
    jsonified_games = {}
    for game_table in game_tables:
        game_json = {}
        game_state = game_table.get_item(Key={'ComponentId': 'State'})['Item']

        players_to_assist = game_table.get_item(Key={'ComponentId': 'PlayersToAssist'})['Item']
        del players_to_assist['ComponentId']

        game_json['id'] = game_table.name
        game_json['round'] = int(game_state['Round'])
        game_json['paused'] = not bool(game_state['Running'])
        game_json['auto_mode'] = bool(game_state['AutoMode'])
        game_json['players'] = game_state['PlayerIds']
        game_json['players_to_assist'] = players_to_assist

        jsonified_games[game_table.name] = game_json

    return jsonified_games


def db_get_game(game_id):
    game_table = dynamo_resource.Table(game_id)
    game_json = {}

    game_state = game_table.get_item(Key={'ComponentId': 'State'})['Item']

    players_to_assist = game_table.get_item(Key={'ComponentId': 'PlayersToAssist'})['Item']
    del players_to_assist['ComponentId']

    game_json['id'] = game_table.name
    game_json['round'] = int(game_state['Round'])
    game_json['paused'] = not bool(game_state['Running'])
    game_json['auto_mode'] = bool(game_state['AutoMode'])
    game_json['players'] = game_state['PlayerIds']
    game_json['players_to_assist'] = {"needs_assistance": players_to_assist["NeedsAssistance"],
                                      "being_assisted": players_to_assist["BeingAssisted"]}
    game_json['ended'] = game_state['Ended']
    game_json['modification_hash'] = game_state['ModificationHash']

    return game_json

# Returns <game_id> of newly create game


def db_add_new_game(password, round=0):
    id = uuid4().hex[:8]
    modification_hash = uuid4().hex[:16]

    # Creates table w/ name <game_id>
    try:
        game_table = dynamo_resource.create_table(
            TableName=id,
            KeySchema=[
                {
                    'AttributeName': 'ComponentId',
                    'KeyType': 'HASH'
                }
            ],
            AttributeDefinitions=[
                {
                    'AttributeName': 'ComponentId',
                    'AttributeType': 'S'
                }
            ],
            ProvisionedThroughput={  # BillingMode <- decide as group
                'ReadCapacityUnits': 10,
                'WriteCapacityUnits': 10
            }
        )
    except dynamo_client.exceptions.ResourceInUseException:
        print('Game with id: {} already exists'.format(id))
        raise
    except dynamo_client.exceptions.LimitExceededException:
        print('Limit Exceeded Exception -- Update AWS configuration')
        raise
    except dynamo_client.exceptions.InternalServerError:
        print('Internal Server Error')
        raise

    game_table.wait_until_exists()

    # Set default game state
    game_table.put_item(
        Item={
            'ComponentId': 'State',
            'AdminPassword': password,
            'Round': round,
            'Running': True,
            'Ended': False,
            'AutoMode': False,
            'PlayerIds': [],
            'ModificationHash': modification_hash
        }
    )

    # Default players_to_assist and analysis events
    game_table.put_item(
        Item={
            'ComponentId': 'PlayersToAssist',
            'NeedsAssistance': [],
            'BeingAssisted': []
        }
    )

    game_table.put_item(
        Item={
            'ComponentId': 'AnalysisEvents',
            'Events': []
        }
    )

    game_table.put_item(
        Item={
            'ComponentId': 'RunningTotals',
            'GraphData': [{"time": dt.datetime.now(dt.timezone.utc).isoformat()}]
        }
    )

    # Spin up game_monitor in SQS
    return id, modification_hash


def db_get_player_score(game_id, player_id):
    return dynamo_resource.Tbale(game_id).get_item(Key={'ComponentId': player_id})['Item']['Score']


def db_get_game_ids():
    """ Returns list of game ids """
    return [game_table.name for game_table in list(dynamo_resource.tables.all())]


def db_get_player_ids(game_id):
    """ Returns list of player ids in a game """
    return dynamo_resource.Table(game_id).get_item(Key={'ComponentId': 'State'})['Item']['PlayerIds']


def db_get_round(game_id):
    """ Returns game round """
    return int(dynamo_resource.Table(game_id).get_item(Key={'ComponentId': 'State'})['Item']['Round'])


def db_get_game_password(game_id):
    """ Returns game password """
    return dynamo_resource.Table(game_id).get_item(Key={'ComponentId': 'State'})['Item']['AdminPassword']


def db_game_paused(game_id):
    """ Returns true if game is paused false if not """
    return not dynamo_resource.Table(game_id).get_item(Key={'ComponentId': 'State'})['Item']['Running']


def db_set_paused(game_id, value: bool):
    """ Sets paused to given value (true/false) """
    dynamo_resource.Table(game_id).update_item(
        Key={
            'ComponentId': 'State'
        },
        UpdateExpression='SET Running = :pause',
        ExpressionAttributeValues={
            ':pause': not value
        }
    )

def db_end_game(game_id):
    """ Sets ended to true """
    # TODO
    # Process Post Game Analysis
    # Store Post Game Analysis in Database
    return


def db_advance_round(game_id):
    """ Increments round """
    dynamo_resource.Table(game_id).update_item(
        Key={
            'ComponentId': 'State'
        },
        UpdateExpression='SET Round = Round + :incr',
        ExpressionAttributeValues={
            ':incr': 1
        }
    )

# Potentially batch-update with PartiQL


def db_reset_round_indices(game_id):
    """ Reset each player's round index """
    pids = dynamo_resource.Table(game_id).get_item(Key={'ComponentId': 'State'})['Item']['PlayerIds']

    for pid in pids:
        dynamo_resource.Table(game_id).update_item(
            Key={
                'ComponentId': pid
            },
            UpdateExpression='SET RoundIndex = :zero',
            ExpressionAttributeValues={
                ':zero': 0
            }
        )


def db_set_auto_mode(game_id, value: bool):
    """ Sets auto to given value (true/false) """
    dynamo_resource.Table(game_id).update_item(
        Key={
            'ComponentId': 'State'
        },
        UpdateExpression='SET AutoMode = :auto',
        ExpressionAttributeValues={
            ':auto': value
        }
    )


def db_get_scores(game_id):
    """ Returns game scores as a list of objects in the form {"time": timestamp, "pid": score} """
    return dynamo_resource.Table(game_id).get_item(Key={'ComponentId': 'RunningTotals'})['Item']['GraphData']


def db_get_all_players(game_id):
    """ Returns players as a dict in the form {player_id: Player, player_id: Player, ...} """
    game_table = dynamo_resource.Table(game_id)
    pids = game_table.get_item(Key={'ComponentId': 'State'})['Item']['PlayerIds']
    jsonified_players = {}

    for pid in pids:
        player_json = {}
        player_item = game_table.get_item(Key={'ComponentId': pid})['Item']

        player_json['id'] = pid
        player_json['game_id'] = game_id
        player_json['name'] = player_item['Name']
        player_json['score'] = int(player_item['Score'])
        player_json['api'] = player_item['API']
        player_json['events'] = list(map(convert_decimals, player_item['Events']))
        player_json['streak'] = player_item['Streak']
        player_json["round_index"] = int(player_item['RoundIndex'])

        jsonified_players[pid] = player_json

    print(jsonified_players)

    return jsonified_players


def db_get_player(game_id, player_id):
    """ Returns player object """
    player_json = {}
    player_item = dynamo_resource.Table(game_id).get_item(Key={'ComponentId': player_id})['Item']

    player_json['id'] = player_id
    player_json['game_id'] = game_id
    player_json['name'] = player_item['Name']
    player_json['score'] = int(player_item['Score'])
    player_json['api'] = player_item['API']
    player_json['events'] = list(map(convert_decimals, player_item['Events']))
    player_json['streak'] = player_item['Streak']
    player_json['round_index'] = int(player_item['RoundIndex'])
    player_json['active'] = player_item['Active']

    return player_json


def db_delete_player(game_id, player_id):
    """ Deletes player """
    dynamo_resource.Table(game_id).update_item(
        Key={'ComponentId': player_id},
        UpdateExpression='SET Active = :false',
        ExpressionAttributeValues={
            ':false': False
        }
    )

    pids = dynamo_resource.Table(game_id).get_item(Key={'ComponentId': 'State'})['Item']['PlayerIds']
    pids.remove(player_id)

    dynamo_resource.Table(game_id).update_item(
        Key={'ComponentId': 'State'},
        UpdateExpression='SET PlayerIds = :newPlayerIds',
        ExpressionAttributeValues={
            ':newPlayerIds': pids
        }
    )
    return


def db_delete_all_players(game_id):
    """ Deletes all players """
    game_table = dynamo_resource.Table(game_id)
    pids = game_table.get_item(Key={'ComponentId': 'State'})['Item']['PlayerIds']

    for pid in pids:
        dynamo_resource.Table(game_id).update_item(
            Key={'ComponentId': pid},
            UpdateExpression='SET Active = :false',
            ExpressionAttributeValues={
                ':false': False
            }
        )

    dynamo_resource.Table(game_id).update_item(
        Key={'ComponentId': 'State'},
        UpdateExpression='SET PlayerIds = :newPlayerIds',
        ExpressionAttributeValues={
            ':newPlayerIds': []
        }
    )

    return


def db_add_player(game_id, name, api):
    """ Add player to DB """
    pid = uuid4().hex[:8]
    modification_hash = uuid4().hex[:16]

    dynamo_resource.Table(game_id).put_item(
        Item={
            'ComponentId': pid,
            'Name': name,
            'API': api,
            'Score': 0,
            'Streak': "",
            'Events': [],
            'Active': True,
            'RoundIndex': 0,
            'CurrentStreakLength': 0,
            'LongestStreak': 0,
            'CorrectTally': 0,
            'IncorrectTally': 0,
            'RequestCount': 0,
            'ModificationHash': modification_hash
        }
    )

    pids = dynamo_resource.Table(game_id).get_item(Key={'ComponentId': 'State'})['Item']['PlayerIds']
    pids.append(pid)

    dynamo_resource.Table(game_id).update_item(
        Key={'ComponentId': 'State'},
        UpdateExpression='SET PlayerIds = :newPlayerIds',
        ExpressionAttributeValues={
            ':newPlayerIds': pids
        }
    )

    db_add_running_total(game_id, pid, 0, dt.datetime.now(dt.timezone.utc))

    return {'id': pid, 'game_id': game_id, 'score': 0, 'api': api, 'events': [], 'streak': ""}, modification_hash


def db_add_running_total(game_id, player_id, score, event_timestamp):
    '''
    Args:
    game_id {String}
    player_id {String}
    score {int}
    event_timestamp {dt_datetime}: creation timestamp for event

    Note:
    In running_totals, must be stored strings, not datetime objects.
    datetime object -> string: isoformat()
    string -> datetime object: fromisoformat() 
    '''
    game_table = dynamo_resource.Table(game_id)
    current_running_totals = game_table.get_item(Key={'ComponentId': 'RunningTotals'})['Item']['GraphData']

    prev_time = dt.datetime.fromisoformat(current_running_totals[-1]["time"]).replace(tzinfo=dt.timezone.utc)
    diff = event_timestamp - prev_time

    if diff.total_seconds() < 1:
        current_running_totals[-1][player_id] = score
    else:
        current_running_totals.append(
            {"time": event_timestamp.isoformat(), f"{player_id}": score}
        )

    game_table.update_item(
        Key={'ComponentId': 'RunningTotals'},
        UpdateExpression='SET GraphData = :newGraphData',
        ExpressionAttributeValues={
            ':newGraphData': current_running_totals
        }
    )


def db_get_players_to_assist(game_id):
    """ Returns names of players to assist in the form { "needs_assistance": [], "being_assisted": [] } """
    game_table = dynamo_resource.Table(game_id)
    players_to_assist = game_table.get_item(Key={'ComponentId': 'PlayersToAssist'})['Item']
    return {"needs_assistance": players_to_assist['NeedsAssistance'], "being_assisted": players_to_assist['BeingAssisted']}


def db_set_players_to_assist(game_id, players_to_assist):
    game_table = dynamo_resource.Table(game_id)
    game_table.update_item(
        Key={'ComponentId': 'PlayersToAssist'},
        UpdateExpression='SET NeedsAssistance = :newNeedsAssistance, BeingAssisted = :beingAssisted',
        ExpressionAttributeValues={
            ':newNeedsAssistance': players_to_assist["needs_assistance"],
            ':beingAssisted': players_to_assist["being_assisted"],
        }
    )

def db_assist_player(game_id, player_name):
    """ Updates a player's state from 'needing assistance' to 'being assisted' """
    game_table = dynamo_resource.Table(game_id)
    players_to_assist = game_table.get_item(Key={'ComponentId': 'PlayersToAssist'})['Item']
    needs_assistance = players_to_assist['NeedsAssistance']
    being_assisted = players_to_assist['BeingAssisted']

    if player_name not in needs_assistance:
        return False

    needs_assistance.remove(player_name)
    being_assisted.append(player_name)

    game_table.update_item(
        Key={'ComponentId': 'PlayersToAssist'},
        UpdateExpression='SET NeedsAssistance = :newNeedsAssistance, BeingAssisted = :beingAssisted',
        ExpressionAttributeValues={
            ':newNeedsAssistance': needs_assistance,
            ':beingAssisted': being_assisted,
        }
    )
    return True

def db_update_player(game_id, player_id, name, api):
    """ Updates name and api of player """
    game_table = dynamo_resource.Table(game_id)

    if name:
        game_table.update_item(
            Key={'ComponentId': player_id},
            UpdateExpression='SET #Name = :newName',
            ExpressionAttributeValues={
                ':newName': name,
            },
            ExpressionAttributeNames={
                "#Name": "Name"
            }
        )

    if api:
        game_table.update_item(
            Key={'ComponentId': player_id},
            UpdateExpression='SET API = :newAPI',
            ExpressionAttributeValues={
                ':newAPI': api,
            }
        )

def db_set_player_score(game_id, player_id, new_score):
    dynamo_resource.Table(game_id).update_item(
        Key={'ComponentId': player_id},
            UpdateExpression='SET Score = :newScore',
            ExpressionAttributeValues={
                ':newScore': new_score,
            }
    )

def db_set_player_incorrect_tally(game_id, player_id, new_incorrect_tally):
    dynamo_resource.Table(game_id).update_item(
        Key={'ComponentId': player_id},
            UpdateExpression='SET IncorrectTally = :newIncorrectTally',
            ExpressionAttributeValues={
                ':newIncorrectTally': new_incorrect_tally,
            }
    )

def db_set_player_streak(game_id, player_id, new_streak):
    dynamo_resource.Table(game_id).update_item(
        Key={'ComponentId': player_id},
            UpdateExpression='SET Streak = :newStreak',
            ExpressionAttributeValues={
                ':newStreak': new_streak,
            }
    )
    
def db_set_player_correct_tally(game_id, player_id, new_correct_tally):
    dynamo_resource.Table(game_id).update_item(
        Key={'ComponentId': player_id},
            UpdateExpression='SET CorrectTally = :newCorrectTally',
            ExpressionAttributeValues={
                ':newCorrectTally': new_correct_tally,
            }
    )

def db_set_player_round_index(game_id, player_id, new_round_index):
    dynamo_resource.Table(game_id).update_item(
        Key={'ComponentId': player_id},
            UpdateExpression='SET RoundIndex = :newRoundIndex',
            ExpressionAttributeValues={
                ':newRoundIndex': new_round_index,
            }
    )

def db_set_request_count(game_id, player_id, new_request_count):
    dynamo_resource.Table(game_id).update_item(
        Key={'ComponentId': player_id},
            UpdateExpression='SET RequestCount = :newRequestCount',
            ExpressionAttributeValues={
                ':newRequestCount': new_request_count,
            }
    )

def db_get_events(game_id, player_id):
    """ Returns list of event objects for a player """
    return dynamo_resource.Table(game_id).get_item(Key={'ComponentId': player_id})['Item']['Events']


def db_add_event(game_id, player_id, query, difficulty, points_gained, response_type):
    game_table = dynamo_resource.Table(game_id)

    event = {
        'event_id': uuid4().hex[:8],
        'player_id': player_id,
        'game_id': game_id,
        'query': query,
        'difficulty': int(difficulty),
        'points_gained': int(points_gained),
        'response_type': response_type,
        'timestamp': dt.datetime.now(dt.timezone.utc).isoformat()
    }
    events = list(map(convert_decimals, game_table.get_item(Key={'ComponentId': player_id})['Item']['Events']))
    events.append(event)

    game_table.update_item(
        Key={'ComponentId': player_id},
        UpdateExpression='SET Events = :newEvent',
        ExpressionAttributeValues={
            ':newEvent': events,
        }
    )


def db_get_scoreboard(game_id):
    """ Returns Scoreboard object for a game (or at least a mock version) """ 
    # TODO
    # Might not be neccessary
    game_table = dynamo_resource.Table(game_id)
    scoreboard_data = game_table.scan(
        ProjectionExpression="ComponentId, Score, CorrectTally, IncorrectTally, RequestCount, Active",
        FilterExpression="attribute_exists(Score)"
    )["Items"]

    res = {}
    for entry in scoreboard_data:
        if not entry['Active']:
            continue
        res[entry['ComponentId']] = {'score': entry['Score'],
                                     'correct_tally': entry["CorrectTally"],
                                     'incorrect_tally': entry["IncorrectTally"],
                                     'request_counts': entry["RequestCount"]
                                     }
    return res


def db_add_analysis_event(game_id, event):
    game_table = dynamo_resource.Table(game_id)

    events = game_table.get_item(Key={'ComponentId': 'AnalysisEvents'})['Item']['Events']
    events.append(event)

    game_table.update_item(
        Key={'ComponentId': 'AnalysisEvents'},
        UpdateExpression='SET Events = :newEvent',
        ExpressionAttributeValues={
            ':newEvent': events,
        }
    )

def db_get_analysis_events(game_id):
    """ Returns analysis events for a game (not sure what this means) """ 
    return dynamo_resource.Table(game_id).get_item(Key = {'ComponentId': 'AnalysisEvents'})['Item']['Events']

def db_review_exists(game_id):
    return 'Item' in dynamo_resource.Table(game_id).get_item(Key = {'ComponentId': 'Review'})

def db_game_ended(game_id):
    return dynamo_resource.Table(game_id).get_item(Key = {'ComponentId': 'State'})['Item']['Ended']

def db_is_game_paused(game_id):
    res = dynamo_resource.Table(game_id).get_item(Key = {'ComponentId': 'State'})['Item']['Running']
    assert type(res) == bool
    return not res

def db_get_game_round(game_id):
    return dynamo_resource.Table(game_id).get_item(Key = {'ComponentId': 'State'})['Item']['Round']

def db_check_state_modification_hash(game_id, modification_hash):
    # TODO: implement whatever it is
    return True

