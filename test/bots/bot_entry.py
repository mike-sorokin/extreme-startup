import sys
from flask import Flask, request
from bot_resp import *


def print_usage():
    print("Please, use the bot entry script with one of the following arguments:")
    print("\n  - " + "\n  - ".join(bot_resp_functions.keys()))


bot_resp_functions = {
    "ignorant": ignorant_response,
    "math": math_response
}

if __name__ == '__main__':
    bot_type = sys.argv[1]

    if bot_type not in bot_resp_functions and sys.argc != 2:
        print_usage()
        sys.exit(1)

    app = Flask(__name__)

    @app.route("/")
    def hello_world():
        query = request.get("q")
        get_resp = bot_resp_functions[bot_type]
        return get_resp(query)

    app.run()
