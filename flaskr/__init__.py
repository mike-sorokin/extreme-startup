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
    session
)
from flaskr.player import Player
from flaskr.game import Game
from flaskr.scoreboard import Scoreboard
from flaskr.quiz_master import QuizMaster
from flaskr.json_encoder import JSONEncoder
from flaskr.questions import *
import threading

# todo remove later
import pprint

app = Flask(__name__)
app.secret_key = b'_5#2L"F4Q8Z\n\xec]/'

# games: game_id -> game object
games = {}

# players: player_id -> Player
players = {}

# Scoreboard lock
lock = threading.Lock()

# scoreboards: game_id -> Scoreboard
scoreboards = {}

# player_threads: player_id -> player_thread
player_threads = {} 

encoder = JSONEncoder()

# PRODUCTION CONSTANT(S)
QUESTION_TIMEOUT = 10
QUESTION_DELAY = 5
DELETE_SUCCESSFUL = ("Successfully deleted", 204)
NOT_ACCEPTABLE = ("Unacceptable request - Requested resource not found", 406)
UNAUTHORIZED = ("Unauthenticated request", 401)

# This is a catch-all function that will redirect anything not caught by the other rules
# to the react webpages
@app.route("/", defaults={"path": ""})
@app.route("/<path:path>")
def serve_frontend(path):
    print("path is", path)
    return make_response(render_template("index.html", path=path))


@app.route("/favicon.ico")
def favicon():
    return send_from_directory(app.root_path, "favicon.ico")


# Game Management
@app.route("/api", methods=["GET", "POST", "DELETE"])
def api_index():
    if request.method == "GET":  # fetch all games
        return encoder.encode(games)

    elif request.method == "POST":  # create new game -- initially no players -- passkey for administrators 
        if "password" not in request.get_json():
            return NOT_ACCEPTABLE

        password = request.get_json()["password"]
        new_game = Game(password)

        gid = new_game.id
        scoreboards[gid] = Scoreboard()
        games[gid] = new_game
        add_session_admin(gid, session) 
        return encoder.encode(new_game)

    elif request.method == "DELETE":  # delete all games 
        for gid in session['admin']:
            if not is_admin(gid, session):
                return UNAUTHORIZED

        remove_players(*[p for g in games.values() for p in g.players])
        # garbage collect each game's question_factory
        games.clear()
        return DELETE_SUCCESSFUL

@app.route("/api/<game_id>/auth", methods=["POST"])
def admin_authentication(game_id): # check if passkey valid for <game_id> and authenticate user with session if yes
    if game_id not in games or 'password' not in request.get_json():
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

    elif request.method == "PUT":  # update game settings
        if not is_admin(game_id, session):
            return UNAUTHORIZED

        r = request.get_json()

        if "round" in r:  # increment <game_id>'s round by 1
            games[game_id].question_factory.advance_round()
            games[game_id].round += 1
            return ("ROUND_INCREMENTED", 200)

        elif "pause" in r:
            if r["pause"]:  # pause <game_id>
                pause_successful = games[game_id].pause_wlock.acquire(timeout=15)
                if not pause_successful:
                    return ("Race condition with lock", 429)
                games[game_id].paused = True
                return ("GAME_PAUSED", 200)

            else:
                try:
                    games[game_id].pause_wlock.release()
                    games[game_id].paused = False
                except RuntimeError:
                    return ("Race condition wtih lock", 429)
                return ("GAME_UNPAUSED", 200)

        return NOT_ACCEPTABLE

    elif request.method == "DELETE":  # delete game with <game_id>
        if not is_admin(game_id, session):
            return UNAUTHORIZED

        remove_players(*games[game_id].players)

        # garbage collect the question_factory
        del games[game_id]
        return {"deleted": game_id}


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

        player_thread = threading.Thread(target=quiz_master.start)
        player_threads[player.uuid] = player_thread
        player_thread.daemon = True
        player_thread.start()

        r = make_response(encoder.encode(player))
        r.mimetype = "application/json"
        return r

    elif request.method == "DELETE":  # deletes all players in <game_id> game instance
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
        if "name" in request.get_json():
            players[player_id].name = request.get_json()["name"]

        if "api" in request.get_json():
            players[player_id].api = request.get_json()["api"]

        return encoder.encode(players[player_id])

    elif request.method == "DELETE":  # delete player with id
        if not is_admin(game_id, session):
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
    "/api/<game_id>/players/<player_id>/events/<event_id>", methods=["GET", "DELETE"]
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


@app.get("/api/<game_id>/leaderboard")
def leaderboard(game_id):
    if game_id not in scoreboards:
        return NOT_ACCEPTABLE

    score_dict = scoreboards[game_id].leaderboard()
    res = []

    for k, s in score_dict.items():
        res.append({"name": players[k].name, "id": k, "score": s})

    return encoder.encode(res)


# Mark player as inactive, removes thread from player_threads dict
def remove_players(*player_id):
    for pid in player_id:
        assert pid in player_threads
        players[pid].active = False

        del player_threads[pid]
        del players[pid]

def add_session_admin(game_id, session):
    if 'admin' in session:
        session['admin'].append(game_id)
    else:
        session['admin'] = [game_id]

def is_admin(game_id, session):
    return 'admin' in session and game_id in session['admin']

# FORGIVE ME
bot_responses = {n: (f"Bot{n}", 0) for n in range(100)}

# /2/hi  style links, these update the response
@app.route("/api/bot/<int:bot_id>/<string:resp>", methods=["GET"])
def _update_response(bot_id, resp):
    bot_responses[bot_id][0] = resp
    bot_responses[bot_id][1] += 1
    return redirect(url_for("api_response", bot_id=bot_id))


# Get a response
@app.route("/api/bot/<int:bot_id>", methods=["GET"])
def _api_response(bot_id):
    return bot_responses[bot_id][0]


@app.route("/api/bot/cleanup", methods=["GET"])
def _cleanup():
    bot_responses = {}
    return "Restored bots"


@app.route("/api/bot/", methods=["GET"])
def _main_view():
    return "<br>".join(list(str(x) for x in bot_responses.values()))
