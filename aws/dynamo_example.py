import boto3
from uuid import uuid4

dynamo_db = boto3.resource('dynamodb')
sqs = boto3.resource('sqs')

def create_sqs_fifo():
    sqs.create_queue(QueueName='example.fifo', 
    Attributes={
        'FifoQueue': 'true'
    })


# Returns <game_id> of newly create game 
def db_add_new_game(password, round=0):
    id = uuid4().hex[:8]

    # Creates table w/ name <game_id> 
    try: 
        game_table = dynamo_db.create_table(
            TableName = id, 
            KeySchema = [
                {
                    'AttributeName': 'ComponentId',
                    'KeyType': 'HASH'
                }
            ],
            AttributeDefinitions = [
                {
                    'AttributeName': 'ComponentId',
                    'AttributeType': 'S'
                }
            ],
            ProvisionedThroughput = { # BillingMode <- decide as group
                'ReadCapacityUnits': 1,
                'WriteCapacityUnits': 1
            }
        )
    except dynamo_db.exceptions.ResourceInUseException:
        return 'Game with id: {} already exists'.format(id)
    
    game_table.wait_until_exists()
    
    # Set default game state
    game_table.put_item(
        Item = {
            'ComponentId': 'State',
            'Password': password,
            'Round': round,
            'Running': True,
            'Ended': False,
            'AutoMode': False
        }
    )

    # Default players_to_assist and analysis events
    game_table.put_item(
        Item = {
            'ComponentId': 'PlayersToAssist',
            'NeedsAssistance': [],
            'BeingAssisted': []
        }
    )

    game_table.put_item(
        Item = {
            'ComponentId': 'AnalysisEvents',
            'Events': []
        }
    )
    
    return id


#db_add_new_game('Hello')
create_sqs_fifo()