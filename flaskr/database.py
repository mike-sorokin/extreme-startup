import pymongo, os, json, subprocess, shutil, time


def get_mongo_client(local=False):
    """
    Attempts to open flaskr/mongo_config.json and connect to the database there.
    If not found, or if local=True, then connects to localhost:27017
    """
    connection_string = "mongodb://localhost:27017"
    config_path = os.path.join(os.path.dirname(__file__), "mongo_config.json")

    # Try to update connection_string to json config
    if os.path.isfile(config_path):
        with open(config_path) as f:
            cfg = json.load(f)
            try:
                connection_string = (
                    f"mongodb+srv://{cfg['user']}:{cfg['password']}@{cfg['address']}"
                )
            except KeyError:
                print("Warning: malformed mongo_config.json. Using localhost DB.")

    client = pymongo.MongoClient(connection_string)
    return client


def destructive_start_localhost_mongo():
    """
    Kill any existing mongo server instance.
    Clean flaskr/_db.
    Starts a local mongod database using flaskr/db as the store.
    """
    # This kills any running mongo instance
    os.system("mongo --eval \"db.getSiblingDB('admin').shutdownServer()\"")

    # Remove and remake flaskr/db
    db_path = os.path.join(os.path.dirname(__file__), "_db")
    shutil.rmtree(db_path, ignore_errors=True)
    os.mkdir(db_path)

    subprocess.Popen(["mongod", "--dbpath", db_path], stdout=subprocess.DEVNULL)


destructive_start_localhost_mongo()
cli = get_mongo_client()
print(cli.xs.game.insert_one({"test_event": "hello_world"}))
