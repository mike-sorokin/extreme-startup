from crypt import methods
from flask import (
    Flask,
    request,
    redirect,
    make_response,
    url_for,
    send_from_directory,
    session,
)
from flaskr.player import Player
from flaskr.aws_games_manager import AWSGamesManager
from flaskr.json_encoder import JSONEncoder
from flaskr.shared.questions import *
import threading
import secrets
from random import randint

# PRODUCTION CONSTANT(S)
QUESTION_TIMEOUT = 10
QUESTION_DELAY = 5

# HTTP CODES
ALL_GOOD = 200
FAULTY_REQUEST = 400
NOT_FOUND = 404
NOT_ACCEPTED = 406
ERROR_405 = 405
DELETE_SUCCESS = 204
UNAUTHORIZED_CODE = 401

DELETE_SUCCESSFUL = ("Successfully deleted", DELETE_SUCCESS)
NOT_ACCEPTABLE = ("Unacceptable request - Requested resource not found", NOT_ACCEPTED)
UNAUTHORIZED = ("Unauthenticated request", UNAUTHORIZED_CODE)
METHOD_NOT_ALLOWED = ("HTTP Method not allowed", ERROR_405)


def create_app():
    app = Flask(__name__, static_folder="vite")
    app.url_map.strict_slashes = False

    app.config["SECRET_KEY"] = secrets.token_hex()

    games_manager = AWSGamesManager()

    # Temporary list of ended game ids
    ended_games = []

    encoder = JSONEncoder()

    # This is a catch-all function that will redirect anything not caught by the other rules
    # to the react webpages
    @app.route("/", defaults={"path": ""})
    @app.route("/<path:path>")
    def serve_frontend(path):
        if path != "" and os.path.exists(app.static_folder + "/" + path):
            return send_from_directory(app.static_folder, path)
        else:
            return send_from_directory(app.static_folder, "index.html")

    @app.route("/favicon.ico")
    def favicon():
        return send_from_directory(app.root_path, "favicon.ico")

    # Game Management
    @app.route("/api", methods=["GET", "POST", "DELETE"])
    def api_index():
        if request.method == "GET":  # fetch all games
            return games_manager.get_all_games()

        elif (
            request.method == "POST"
        ):  # create new game -- initially no players -- passkey for administrators
            if "password" not in request.get_json():
                return NOT_ACCEPTABLE

            new_game = games_manager.new_game(request.get_json()["password"])
            add_session_admin(new_game, session)
            return games_manager.get_game(new_game)

        elif (
            request.method == "DELETE"
        ):  # delete all games - only for admin of all games
            for gid in list(games_manager.get_all_games().keys()):
                if is_admin(gid, session):
                    continue
                return UNAUTHORIZED

            games_manager.delete_games()
            return DELETE_SUCCESSFUL

    @app.route("/api/<game_id>/auth", methods=["GET", "POST"])
    def admin_authentication(
        game_id,
    ):  # check if passkey valid for <game_id> and authenticate user with session if yes
        if not games_manager.game_exists(game_id):
            return NOT_ACCEPTABLE

        if request.method == "GET":
            res = {"authorized": is_admin(game_id, session), "player" : ""}

            if get_player(session)[0]:
                res["player"] = get_player(session)[1]

            return res

        elif request.method == "POST":
            if "password" not in request.get_json():
                return NOT_ACCEPTABLE

            password = request.get_json()["password"]

            if games_manager.game_has_password(game_id, password):
                add_session_admin(game_id, session)
                return {"valid": True}

            return {"valid": False}

    # Managing a specific game
    @app.route("/api/<game_id>", methods=["GET", "PUT", "DELETE"])
    def game(game_id):
        if not games_manager.game_exists(game_id):
            return NOT_ACCEPTABLE

        if request.method == "GET":  # fetch game with <game_id>
            return games_manager.get_game(game_id)

        elif request.method == "PUT":  # update game settings --- only admin can do this
            if not is_admin(game_id, session):
                return UNAUTHORIZED

            r = request.get_json()

            if "round" in r:  # increment <game_id>'s round by 1
                if games_manager.game_in_last_round(game_id):
                    games_manager.delete_games(game_id)
                    return ("GAME_ENDED", 200)

                games_manager.advance_game_round(game_id)
                return ("ROUND_INCREMENTED", 200)

            elif "pause" in r:
                if r["pause"]:  # pause <game_id>
                    games_manager.pause_game(game_id)  # Kill monitor thread
                    return ("GAME_PAUSED", 200)

                else:  # Unpause the game
                    games_manager.unpause_game(game_id)
                    return ("GAME_UNPAUSED", 200)

            elif "auto" in r:
                if r["auto"]:  # turn on auto mode
                    games_manager.set_auto_mode(game_id)
                    return ("GAME_AUTO_ON", 200)
                else:  # turn off auto mode
                    games_manager.clear_auto_mode(game_id)
                    return ("GAME_AUTO_OFF", 200)

            elif "end" in r:  # End the <game_id> instance
                games_manager.delete_games(game_id)
                ended_games.append(game_id)           # <-------------------- TODO REMOVE LATER AND ASAP(AP)
                return ("GAME_ENDED", 200)

            elif "assisting" in r: # r["assisting"] is player_name
                if games_manager.assist_player(game_id, r["assisting"]):
                    return ("ASSISTING {}".format(r["assisting"].upper()), 200)
                else:
                    return ("{} not in needs_assistance list".format(r["assisting"]), NOT_ACCEPTED)

            return NOT_ACCEPTABLE

        elif request.method == "DELETE":  # delete game with <game_id>
            if not is_admin(game_id, session):
                return UNAUTHORIZED

            games_manager.delete_games(game_id)
            return {"deleted": game_id}

    @app.route("/api/<game_id>/scores", methods=["GET"])
    def game_scores(game_id):
        if not games_manager.game_exists(game_id):
            return NOT_ACCEPTABLE

        cumulative_sums = games_manager.get_game_running_totals(game_id)
        r = make_response(cumulative_sums)
        r.mimetype = "application/json"
        return r

    # Managing all players
    @app.route("/api/<game_id>/players", methods=["GET", "POST", "DELETE"])
    def all_players(game_id):
        if not games_manager.game_exists(game_id):
            return NOT_ACCEPTABLE

        if request.method == "GET":  # fetch all <game_id>'s players
            r = make_response(
                encoder.encode({"players": games_manager.get_game_players(game_id)})
            )
            r.mimetype = "application/json"
            return r

        elif request.method == "POST":  # create a new player -- initialise thread
            new_player = games_manager.add_player_to_game(
                game_id, request.get_json()["name"], request.get_json()["api"]
            )
            session["player"] = new_player["id"]

            r = make_response(encoder.encode(new_player))
            r.mimetype = "application/json"
            return r

        elif (
            request.method == "DELETE"
        ):  # deletes all players in <game_id> game instance
            if not is_admin(game_id, session):
                return UNAUTHORIZED

            games_manager.remove_game_players(game_id)
            return DELETE_SUCCESSFUL

    # List of players who need assistance
    @app.get("/api/<game_id>/assist")
    def assist(game_id):
        if not games_manager.game_exists(game_id):
            return NOT_ACCEPTABLE

        return games_manager.get_players_to_assist(game_id)

    @app.get("/api/<game_id>/gameover")                                     # <-------------------- TODO WHY WE NEED THIS
    def gameover(game_id):
        r = make_response(encoder.encode({"game_over": game_id in ended_games}))
        r.mimetype = "application/json"
        return r

    # Managing <player_id> player
    @app.route("/api/<game_id>/players/<player_id>", methods=["GET", "PUT", "DELETE"])
    def player(game_id, player_id):
        if not (
            games_manager.game_exists(game_id)
            and games_manager.player_exists(game_id, player_id)
        ):
            return NOT_ACCEPTABLE

        if request.method == "GET":  # fetch player with <player_id>
            return encoder.encode(
                games_manager.get_game_players(game_id, player_id)[player_id]
            )
        elif (
            request.method == "PUT"
        ):  # update player (change name/api, NOT event management)
            if not (is_admin(game_id, session) or is_player(player_id, session)):
                return UNAUTHORIZED

            if "name" in request.get_json():
                games_manager.update_player(
                    game_id, player_id, name=request.get_json()["name"]
                )

            if "api" in request.get_json():
                games_manager.update_player(
                    game_id, player_id, api=request.get_json()["api"]
                )

            return encoder.encode(
                games_manager.get_game_players(game_id, player_id)[player_id]
            )

        elif request.method == "DELETE":  # delete player with id
            if not (is_admin(game_id, session) or is_player(player_id, session)):
                return UNAUTHORIZED

            games_manager.remove_game_players(game_id, player_id)
            return {"deleted": player_id}

    # Managing events for <player_id>
    @app.route("/api/<game_id>/players/<player_id>/events", methods=["GET"])
    def player_events(game_id, player_id):
        if not (
            games_manager.game_exists(game_id)
            and games_manager.player_exists(game_id, player_id)
        ):
            return NOT_ACCEPTABLE

        if request.method == "GET":  # fetch all events for <game_id> player <player_id>
            return encoder.encode(
                {"events": games_manager.get_player_events(game_id, player_id)}
            )

    # Managing one event
    @app.route(
        "/api/<game_id>/players/<player_id>/events/<event_id>",
        methods=["GET"],
    )
    def player_event(game_id, player_id, event_id):
        if not (
            games_manager.game_exists(game_id)
            and games_manager.player_exists(game_id, player_id)
        ) or event_id not in map(
            lambda e: e.event_id, games_manager.get_player_events(game_id, player_id)
        ):
            return NOT_ACCEPTABLE

        event = filter(
            lambda e: e.id == event_id,
            games_manager.get_player_events(game_id, player_id),
        )[0]
        if request.method == "GET":  # fetch event with <event_id>
            return encoder.encode(event)

    @app.get("/api/<game_id>/review/players")
    def game_existed_players(game_id):
        # Make sure game exists
        if not f"{game_id}_players" in db_client.xs.list_collection_names():
            return NOT_ACCEPTABLE

        curs = db_client.xs[f"{game_id}_players"].find({}, {"id": 1})
        player_list = [doc["id"] for doc in curs]
        return encoder.encode(player_list)

    @app.get("/api/<game_id>/review/existed")
    def game_existed(game_id):
        return {"existed": games_manager.game_exists(game_id) and games_manager.review_exists(game_id)}

    @app.get("/api/<game_id>/review/finalboard")
    def total_player_scores(game_id):
        if not f"{game_id}_players" in db_client.xs.list_collection_names():
            return ("Game id not found", NOT_FOUND)
        return db_client.xs[f"{game_id}_review"].find_one({"item": "finalboard"})[
            "stats"
        ]

    @app.get("/api/<game_id>/review/finalgraph")
    def final_game_graph(game_id):
        if not f"{game_id}_players" in db_client.xs.list_collection_names():
            return ("Game id not found", NOT_FOUND)
        out = db_client.xs[f"{game_id}_review"].find_one({"item": "finalgraph"})
        return encoder.encode(out["stats"])

    @app.get("/api/<game_id>/review/stats")
    def review_stats(game_id):
        if not f"{game_id}_players" in db_client.xs.list_collection_names():
            return ("Game id not found", NOT_FOUND)
        return db_client.xs[f"{game_id}_review"].find_one({"item": "finalstats"})["stats"]

    @app.get("/api/<game_id>/review/analysis")
    def review_analysis(game_id):
        if not f"{game_id}_players" in db_client.xs.list_collection_names():
            return ("Game id not found", NOT_FOUND)
        out = db_client.xs[f"{game_id}_review"].find_one({"item": "analysis"})
        return encoder.encode(out["stats"])

    # FORGIVE ME
    bot_responses = {n: [f"Bot{n}", 0] for n in range(100)}

    # /2/hi  style links, these update the response
    @app.route("/api/bot/<int:bot_id>/<string:resp>", methods=["GET"])
    def _update_response(bot_id, resp):
        bot_responses[bot_id][0] = resp
        bot_responses[bot_id][1] += 1
        return redirect(url_for("_api_response", bot_id=bot_id))

    # Get a response
    @app.route("/api/bot/<int:bot_id>", methods=["GET"])
    def _api_response(bot_id):
        if bot_responses[bot_id][0] == "cheat":
            return "cheat"
        if randint(0, max(bot_id - 5, 0)) == 0:
            return bot_responses[bot_id][0]
        else:
            return "Wrong response"

    @app.route("/api/bot/ddos/<game_id>", methods=["GET"])
    def _spam_with_bots(game_id):
        for i in range(20):
            player = Player(
                game_id, f"Bot{i}", api=f"http://localhost:5000/api/bot/{i}"
            )

            games[game_id].new_player(player.uuid)
            scoreboards[game_id].new_player(player)
            players[player.uuid] = player

            quiz_master = QuizMaster(
                player,
                games[game_id].question_factory,
                scoreboards[game_id],
                games[game_id].pause_rlock,
            )

            player_thread = threading.Thread(
                target=quiz_master.start,
                args=(games[game_id].first_round_event, games[game_id].running),
            )
            player_thread.daemon = True  # for test termination
            player_thread.start()

    @app.route("/api/bot/", methods=["GET"])
    def _main_view():
        return "<br>".join(list(str(x) for x in bot_responses.values()))

    # Mark player as inactive. Thread will be killed automatically when target function returns
    def remove_players(*player_id):
        for pid in player_id:
            players[pid].active = False
            del players[pid]

    # Mark game as paused. Monitor thread will be killed automatically when target function returns.
    def remove_games(*gid):
        for curr_gid in gid:
            games[curr_gid].running.set()
            del games[curr_gid]

    def add_session_admin(game_id, session):
        if "admin" in session:
            session["admin"] += [game_id]
        else:
            session["admin"] = [game_id]

    def is_admin(game_id, session):
        return ("admin" in session) and (game_id in session["admin"])

    def is_player(player_id, session):
        return ("player" in session) and (player_id in session["player"])

    def get_player(session):
        if "player" in session:
            return True, session["player"]
        return False, None

    return app
