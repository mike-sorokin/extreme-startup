import subprocess, os, requests, signal
import urllib.parse
import time


BOT_CWD = os.path.join("test", "bots")
SOME_PORT = 5003
REQUEST_ATEMPT_WAITING_TIME = 0.25
MAX_REQUESTS = 5


def with_bot_server(bot_type, bot_name="default"):
    """Creates a Flask server for a bot player to test requsts on it"""

    def inner(test_func):
        def wrapper():
            # Running server and waiting for successfull response
            # before running the actual test
            process = subprocess.Popen(
                [
                    "python3",
                    "bot_entry.py",
                    bot_name,
                    bot_type,
                    str(SOME_PORT)
                ],
                cwd=BOT_CWD
            )
            count = 0
            while True:
                try:
                    response = requests.get(f"http://localhost:{SOME_PORT}")
                    if response.status_code == 200:
                        break
                except:
                    count += 1
                    if count >= MAX_REQUESTS:
                        assert False
                    time.sleep(REQUEST_ATEMPT_WAITING_TIME)

            # Running test body
            test_func()

            # Removing server
            os.kill(process.pid, signal.SIGTERM)

        return wrapper

    return inner


def query_bot(query):
    response = requests.get(
        f"http://localhost:{SOME_PORT}", params={"q": urllib.parse.quote(query)}
    )
    return response.text


@with_bot_server("ignorant")
def test_bot_entry_ignorant():
    assert query_bot("What is 1 + 1?") == "I don't know"


@with_bot_server("math")
def test_bot_entry_math():
    assert query_bot("What is 1 + 1?") == "2"
    assert query_bot("What is 1 + 0?") == "1"
