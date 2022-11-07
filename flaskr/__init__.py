from crypt import methods
from uuid import uuid4
from flask import (
    Flask,
    render_template,
    request,
    redirect,
    make_response,
    url_for,
    send_from_directory,
    session,
    jsonify,
)
from flaskr.player import Player
from flaskr.game import Game
from flaskr.scoreboard import Scoreboard
from flaskr.quiz_master import QuizMaster
from flaskr.json_encoder import JSONEncoder
from flaskr.questions import *
from datetime import datetime
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

DELETE_SUCCESSFUL = ("Successfully deleted", 204)
NOT_ACCEPTABLE = ("Unacceptable request - Requested resource not found", 406)
UNAUTHORIZED = ("Unauthenticated request", 401)
METHOD_NOT_ALLOWED = ("HTTP Method not allowed", 405)


def create_app():
    app = Flask(__name__, static_folder="vite")
    app.url_map.strict_slashes = False

    app.config["SECRET_KEY"] = secrets.token_hex()

    # games: game_id -> game object
    games = {}

    # players: player_id -> Player
    players = {}

    # Scoreboard lock
    lock = threading.Lock()

    # scoreboards: game_id -> Scoreboard
    scoreboards = {}

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
            return encoder.encode(games)

        elif (
            request.method == "POST"
        ):  # create new game -- initially no players -- passkey for administrators
            if "password" not in request.get_json():
                return NOT_ACCEPTABLE

            password = request.get_json()["password"]
            new_game = Game(password)
            gid = new_game.id
            scoreboards[gid] = Scoreboard()
            games[gid] = new_game

            spawn_game_monitor(new_game)
            add_session_admin(gid, session)
            return encoder.encode(new_game)

        elif (
            request.method == "DELETE"
        ):  # delete all games - only for admin of all games
            all_gids = list(games.keys())
            for gid in all_gids:
                if not is_admin(gid, session):
                    return UNAUTHORIZED

            remove_players(*[p for g in games.values() for p in g.players])

            # garbage collect each game's question_factory
            remove_games(*all_gids)
            return DELETE_SUCCESSFUL

    @app.route("/api/<game_id>/auth", methods=["GET", "POST"])
    def admin_authentication(
        game_id,
    ):  # check if passkey valid for <game_id> and authenticate user with session if yes
        if game_id not in games:
            return NOT_ACCEPTABLE

        if request.method == "GET":
            return {"authorized": is_admin(game_id, session)}

        elif request.method == "POST":
            if "password" not in request.get_json():
                return NOT_ACCEPTABLE

            password = request.get_json()["password"]
            if password == games[game_id].admin_password:
                add_session_admin(game_id, session)
                return {"valid": True}

            return {"valid": False}

    # Managing a specific game
    @app.route("/api/<game_id>", methods=["GET", "PUT", "DELETE"])
    def game(game_id):
        if game_id not in games:
            return NOT_ACCEPTABLE

        if request.method == "GET":  # fetch game with <game_id>
            return encoder.encode(games[game_id])

        elif request.method == "PUT":  # update game settings --- only admin can do this
            if not is_admin(game_id, session):
                return UNAUTHORIZED

            r = request.get_json()

            if "round" in r:  # increment <game_id>'s round by 1
                games[game_id].question_factory.advance_round()
                games[game_id].round += 1  # for event logging

                # wake up all sleeping threads in game if going from WARMUP -> ROUND 1
                games[game_id].first_round_event.set()

                return ("ROUND_INCREMENTED", 200)

            elif "pause" in r:
                if r["pause"]:  # pause <game_id>
                    pause_successful = games[game_id].pause_wlock.acquire(timeout=15)
                    if not pause_successful:
                        return ("Race condition with lock", 429)

                    games[game_id].paused = True  # Kill monitor thread
                    return ("GAME_PAUSED", 200)

                else:  # Unpause the game
                    try:
                        games[game_id].pause_wlock.release()
                        games[game_id].paused = False
                        spawn_game_monitor(games[game_id])
                    except RuntimeError:
                        return ("Race condition wtih lock", 429)
                    return ("GAME_UNPAUSED", 200)

            return NOT_ACCEPTABLE

        elif request.method == "DELETE":  # delete game with <game_id>
            if not is_admin(game_id, session):
                return UNAUTHORIZED

            remove_players(*games[game_id].players)

            # garbage collect the question_factory
            remove_games(game_id)
            return {"deleted": game_id}

    @app.route("/api/<game_id>/scores", methods=["GET"])
    def game_scores(game_id):
        if game_id not in games:
            return NOT_ACCEPTABLE

        cumulative_sums = scoreboards[game_id].running_totals
        r = make_response(encoder.encode(cumulative_sums))
        r.mimetype = "application/json"
        return r

    # Managing all players
    @app.route("/api/<game_id>/players", methods=["GET", "POST", "DELETE"])
    def all_players(game_id):
        if game_id not in games:
            return NOT_ACCEPTABLE

        if request.method == "GET":  # fetch game players
            players_ids = games[game_id].players
            players_dict = {id: players[id] for id in players_ids}
            r = make_response(encoder.encode({"players": players_dict}))
            r.mimetype = "application/json"
            return r

        elif request.method == "POST":  # create a new player -- initialise thread
            player = Player(
                game_id, request.get_json()["name"], api=request.get_json()["api"]
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
                target=quiz_master.start, args=(games[game_id].first_round_event,)
            )
            player_thread.daemon = True  # for test termination
            player_thread.start()

            session["player"] = player.uuid

            r = make_response(encoder.encode(player))
            r.mimetype = "application/json"
            return r

        elif (
            request.method == "DELETE"
        ):  # deletes all players in <game_id> game instance
            if not is_admin(game_id, session):
                return UNAUTHORIZED

            remove_players(*games[game_id].players)
            games[game_id].players.clear()
            return DELETE_SUCCESSFUL

    # Managing <player_id> player
    @app.route("/api/<game_id>/players/<player_id>", methods=["GET", "PUT", "DELETE"])
    def player(game_id, player_id):
        if game_id not in games or player_id not in players:
            return NOT_ACCEPTABLE

        if request.method == "GET":  # fetch player with <player_id>
            return encoder.encode(players[player_id])
        elif (
            request.method == "PUT"
        ):  # update player (change name/api, NOT event management)
            if not (is_admin(game_id, session) or is_player(player_id, session)):
                return UNAUTHORIZED

            if "name" in request.get_json():
                players[player_id].name = request.get_json()["name"]

            if "api" in request.get_json():
                players[player_id].api = request.get_json()["api"]

            return encoder.encode(players[player_id])

        elif request.method == "DELETE":  # delete player with id
            if not (is_admin(game_id, session) or is_player(player_id, session)):
                return UNAUTHORIZED

            games[game_id].players.remove(player_id)
            remove_players(player_id)
            return {"deleted": player_id}

    # Managing events for <player_id>
    @app.route("/api/<game_id>/players/<player_id>/events", methods=["GET", "DELETE"])
    def player_events(game_id, player_id):
        if game_id not in games or player_id not in players:
            return NOT_ACCEPTABLE

        if request.method == "GET":  # fetch all events for <game_id> player <player_id>
            return encoder.encode({"events": players[player_id].events})

        elif request.method == "DELETE":  # delets all events for <player_id>
            if not is_admin(game_id, session):
                return UNAUTHORIZED

            players[player_id].events.clear()
            return DELETE_SUCCESSFUL

    # Managing one event
    @app.route(
        "/api/<game_id>/players/<player_id>/events/<event_id>",
        methods=["GET", "DELETE"],
    )
    def player_event(game_id, player_id, event_id):
        if (
            game_id not in games
            or player_id not in players
            or event_id not in map(lambda e: e.event_id, players[player_id].events)
        ):
            return NOT_ACCEPTABLE

        event = filter(lambda e: e.id == event_id, players[player_id].events)[0]

        if request.method == "GET":  # fetch event with <event_id>
            return encoder.encode(event)

        elif request.method == "DELETE":  # delete event with <event_id>
            if not is_admin(game_id, session):
                return UNAUTHORIZED

            players[player_id].events.remove(event)
            return DELETE_SUCCESSFUL

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
                target=quiz_master.start, args=(games[game_id].first_round_event,)
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
            games[curr_gid].paused = True
            del games[curr_gid]

    def spawn_game_monitor(game):
        game_monitor_thread = threading.Thread(
            target=game.monitor, args=[players, scoreboards[game.id]]
        )
        game_monitor_thread.daemon = True  # for test termination
        game_monitor_thread.start()

    def add_session_admin(game_id, session):
        if "admin" in session:
            session["admin"] += [game_id]
        else:
            session["admin"] = [game_id]

    def is_admin(game_id, session):
        return ("admin" in session) and (game_id in session["admin"])

    def is_player(player_id, session):
        return ("player" in session) and (player_id in session["player"])

    return app
