import sys
from flask import Flask, request
from bot_resp import *

REQUIRED_ARGC = 4


def print_usage_and_exit():
    print("... <bot_name> <bot_type_argument> <port>")
    print(
        "Please, use the bot entry script \
        with one of the following bot type arguments:"
    )
    print("\n  - " + "\n  - ".join(bot_resp_functions.keys()))
    sys.exit(1)


bot_resp_functions = {"ignorant": ignorant_response, "math": math_response}

if __name__ == "__main__":

    if len(sys.argv) != REQUIRED_ARGC:
        print_usage_and_exit()

    bot_name = sys.argv[1]
    bot_type = sys.argv[2]
    port = int(sys.argv[3])

    if bot_type not in bot_resp_functions:
        print_usage_and_exit()

    app = Flask(__name__)

    @app.route("/", methods=["GET"])
    def hello_world():
        query = request.args.get("q")
        print(query)
        print(repr(query))
        if query is None:
            return "None"
        if query == "What is your name?":
            return bot_name
        get_resp = bot_resp_functions[bot_type]
        return get_resp(query)

    app.run(host="localhost", port=port, debug=True)
