import pymongo, os, json, subprocess, shutil, os


def get_mongo_client(local=False):
    """
    Attempts to open flaskr/mongo_config.json and connect to the database there.
    If not found, or if local=True, then boots a local server and connects to it.
    This local server will be completely fresh
    """

    if "USE_LOCAL_MONGO_DB" in os.environ:
        try:
            cli = pymongo.MongoClient("mongodb://localhost:27017")
        except pymongo.errors.ConnectionFailure:
            cli = pymongo.MongoClient("mongodb://mongo:27017")
        return cli

    if local:
        destructive_start_localhost_mongo()
        try:
            cli = pymongo.MongoClient("mongodb://localhost:27017")
        except pymongo.errors.ConnectionFailure:
            cli = pymongo.MongoClient("mongodb://mongo:27017")

    config_path = os.path.join(os.path.dirname(__file__), "mongo_config.json")

    # Try to update connect to json config, if it exists
    if os.path.isfile(config_path):
        with open(config_path) as f:
            cfg = json.load(f)
            try:
                conn_str = (
                    f"mongodb+srv://{cfg['user']}:{cfg['password']}@{cfg['address']}"
                )
                return pymongo.MongoClient(conn_str)
            except KeyError:
                print("Warning: malformed mongo_config.json. Using localhost DB.")
                return get_mongo_client(local=True)
    else:
        print("Warning: mongo_config.json not found. Using localhost DB")
        return get_mongo_client(local=True)


def destructive_start_localhost_mongo():
    """
    Kill any existing mongo server instance.
    Clean flaskr/_db.
    Starts a local mongod database using flaskr/db as the store.
    """

    # This kills any running mongo instance. Try using mongo first, but if not found, use mongosh.
    try:
        subprocess.run(["mongo", "--eval", "db.getSiblingDB('admin').shutdownServer()"])
    except FileNotFoundError:
        subprocess.run(
            ["mongosh", "--eval", "db.getSiblingDB('admin').shutdownServer()"]
        )

    # Remove and remake flaskr/db
    db_path = os.path.join(os.path.dirname(__file__), "_db")
    shutil.rmtree(db_path, ignore_errors=True)
    os.mkdir(db_path)

    subprocess.Popen(["mongod", "--dbpath", db_path], stdout=subprocess.DEVNULL)
