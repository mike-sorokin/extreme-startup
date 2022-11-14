import pymongo, os, json, subprocess, shutil


def get_mongo_client(local=False):
    """
    Attempts to open flaskr/mongo_config.json and connect to the database there.
    Also attempts to read DB_ADDRESS, DB_USERNAME, DB_PASSWORD from environment variables.
    If not found, or if local=True, then connects to localhost:27017
    """
    connection_string = "mongodb://localhost:27017"
    config_path = os.path.join(os.path.dirname(__file__), "mongo_config.json")
    print("Connecting to MongoDB...")
    # Try to update connection_string to json config
    if not local:
        print("Attempting connection to server...")
        if os.path.isfile(config_path):
            print("Config file found!")
            with open(config_path) as f:
                cfg = json.load(f)
                try:
                    connection_string = (
                        f"mongodb+srv://{cfg['user']}:{cfg['password']}@{cfg['address']}"
                    )
                except KeyError:
                    print("Warning: malformed mongo_config.json. Attempting to read environment variables.")
        else:
            print("Reading environment variables...")
            try:
                print(os.environ["DB_USERNAME"], os.environ['DB_PASSWORD'], os.environ['DB_ADDRESS'])
                print(os.environ)
                pw = os.environ["DB_PASSWORD"]
                if pw != "":
                    connection_string = (
                        f"mongodb+srv://{os.environ['DB_USERNAME']}:{os.environ['DB_PASSWORD']}@{os.environ['DB_ADDRESS']}"
                    )
            except KeyError:
                print("Warning: environment variables not set. Using localhost DB")

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
