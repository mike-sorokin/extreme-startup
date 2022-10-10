import subprocess, os, requests, signal
import urllib.parse
import time


BOT_CWD = os.path.join("test", "bots")
SOME_PORT = 5003
REQUEST_ATEMPT_WAITING_TIME = 0.25
MAX_REQUESTS = 5


def query_bot(bot_type, query):
    '''Creates temporary Flask server and tests a query on it'''
    # TODO: TURN THIS INTO A DECORATOR TO REUSE THE SERVER CREATION
    #       Right now it creates and destroys new server for every query.

    process = subprocess.Popen(
        ["python3", "bot_entry.py", bot_type, str(SOME_PORT)],
        cwd=BOT_CWD,
    )

    count = 0
    while True:
        try:
            response = requests.get(
                f"http://localhost:{SOME_PORT}", params={"q": urllib.parse.quote(query)}
            )
            if response.status_code == 200:
                break
        except:
            count += 1
            if count >= MAX_REQUESTS:
                assert False
            time.sleep(REQUEST_ATEMPT_WAITING_TIME)


    os.kill(process.pid, signal.SIGTERM)

    return response.text


def test_bot_entry_ignorant():
    assert query_bot("ignorant", "What is 1 + 1?") == "I don't know"


def test_bot_entry_math():
    assert query_bot("math", "What is 1 + 1?") == "2"
    assert query_bot("math", "What is 1 + 0?") == "1"
