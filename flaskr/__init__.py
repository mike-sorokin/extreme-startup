from crypt import methods
from uuid import uuid4
from flask import Flask, render_template, request, redirect, make_response
from flaskr.player import Player
from flaskr.event import Event
from flaskr.game import Game
from flaskr.scoreboard import Scoreboard
from flaskr.quiz_master import QuizMaster
from flaskr.json_encoder import JSONEncoder
from flaskr.questions import *
from flaskr.question_factory import QuestionFactory
import os
import threading
import requests
import time

# todo remove later
import pprint

app = Flask(__name__)

# games: game_id -> game object
games = {}

# players: player_id -> Player
players = {}

# scoreboards: game_id -> Scoreboard
scoreboards = {}

# player_threads: player_id -> player_thread
player_threads = {}

encoder = JSONEncoder()

# PRODUCTION CONSTANT(S)
QUESTION_TIMEOUT = 10
QUESTION_DELAY = 5


# This is a catch-all function that will redirect anything not caught by the other rules
# to the react webpages
@app.route("/", defaults={"path": ""})
@app.route("/<path:path>")
def serve_frontend(path):
    print("path is", path)
    return make_response(render_template("index.html", path=path))


@app.route("/api", methods=["GET", "POST", "DELETE"])
def api_index():
    if request.method == "GET":
        return encoder.encode(games)
    elif request.method == "POST": # create new game -- initially no players 
        new_game = Game()
        gid = new_game.id
        scoreboards[gid] = Scoreboard()
        games[gid] = new_game
        return encoder.encode(new_game)
    elif request.method == "DELETE": # delete all games
        remove_players(*[p for g in games.values() for p in g.players])
        # garbage collect each game's question_factory 
        games.clear()
        return ("", 204)


@app.route("/api/<game_id>", methods=["GET", "PUT", "DELETE"])
def game(game_id):
    if game_id not in games:
        return ("NOT FOUND", 404)

    if request.method == "GET": # fetch game with <game_id> 
        return encoder.encode(games[game_id])
    elif request.method == "PUT": # update game (advance round) 
        games[game_id].question_factory.advance_round()
        games[game_id].round += 1
        return ("ROUND_INCREMENTED", 200)
    elif request.method == "DELETE": # delete game with <game_id> 
        remove_players(*games[game_id].players)
        # garbage collect the question_factory 
        del games[game_id]
        return {"deleted": game_id}


@app.route("/api/<game_id>/players", methods=["GET", "POST", "DELETE"])
def all_players(game_id):
    if request.method == "GET":
        if game_id not in games:
            return ("", 404)

        players_ids = games[game_id].players
        players_dict = {id: players[id] for id in players_ids}
        r = make_response(encoder.encode({"players": players_dict}))
        r.mimetype = "application/json"
        return r

    elif request.method == "POST":
        player = Player(game_id, request.json["name"], api=request.json["api"])
        scoreboard[player] = 0
        games[game_id].players.append(player.uuid)
        players[player.uuid] = player
        quiz_master = QuizMaster(player, games[game_id].question_factory, scoreboards[game_id])
        player_thread = threading.Thread(target=quiz_master.start)
        player_threads[player.uuid] = player_thread
        player_thread.daemon = True
        player_thread.start()
        r = make_response(encoder.encode(player))
        r.mimetype = "application/json"
        return r
    elif request.method == "DELETE": # deletes all players in <game_id> game instance 
        remove_players(*games[game_id].players)
        games[game_id].players.clear()
        return ("", 204)


@app.route("/api/<game_id>/players/<player_id>", methods=["GET", "PUT", "DELETE"])
def player(game_id, player_id):
    if game_id not in games or player_id not in players:
        return ("NOT FOUND", 404)

    if request.method == "GET": # fetch player with <player_id> 
        return encoder.encode(players[player_id])
    elif request.method == "PUT": # update player (change name/api, NOT event management)
        if "name" in request.form:
            players[player_id].name = request.form["name"]
        if "api" in request.form:
            players[player_id].api = request.form["api"]
        return encoder.encode(players[player_id])
    elif request.method == "DELETE": # delete player with id 
        games[game_id].players.remove(player_id)
        remove_players(player_id)
        return {"deleted": player_id}


@app.route("/api/<game_id>/players/<player_id>/events", methods=["GET", "DELETE"])
def player_events(game_id, player_id):
    if game_id not in games or player_id not in players:
        return ("NOT FOUND", 404)

    if request.method == "GET": # fetch all events for <game_id> player <player_id>
        return encoder.encode({"events": players[player_id].events}) 
    elif request.method == "DELETE": # delets all events for <player_id> 
        players[player_id].events.clear()
        return ("", 204)

@app.route(
    "/api/<game_id>/players/<player_id>/events/<event_id>", methods=["GET", "DELETE"]
)
def player_event(game_id, player_id, event_id):
    if (game_id not in games or
        player_id not in players or
        event_id not in map(lambda e : e.event_id, players[player_id].events)):
        return ("NOT FOUND", 404)
        
    event = filter(lambda e: e.id == event_id, players[player_id].events)[0]

    if request.method == "GET": # fetch event with <event_id>
        return encoder.encode(event)
    elif request.method == "DELETE": # delete event with <event_id>
        players[player_id].events.remove(event)
        return ("", 204)

# Mark player as inactive, removes thread from player_threads dict
def remove_players(*player_id):
    for pid in player_id:
        assert pid in player_threads
        players[pid].active = False
        del player_threads[pid]
        del scoreboard[players[pid]]

        lock.acquire()
        del players[pid]
        lock.release()


def sendQuestion(player):
    while player.active:
        r = None
        try:
            r = requests.get(
                player.api, params={"q": "What is your name?"}, timeout=QUESTION_TIMEOUT
            ).text
        except Exception:
            pass
        lock.acquire()
        if player in scoreboard:
            if r == None:
                points_gained = -50
                response_type = "NO_RESPONSE"
            elif r == player.name:
                points_gained = +50
                response_type = "CORRECT"
            else:
                points_gained = -50
                response_type = "WRONG"
            event = Event(
                player.uuid, "What is your name?", 0, points_gained, response_type
            )
            player.log_event(event)
        lock.release()
        time.sleep(QUESTION_DELAY)


# FORGIVE ME
pp = pprint.PrettyPrinter(indent=4)
bot_responses = {1: "Hello world!"}

# /2/hi  style links, these update the response
@app.route("/api/bot/<int:bot_id>/<string:resp>", methods=["GET"])
def _update_response(bot_id, resp):
    print(f"Updated {bot_id} to {resp}")
    bot_responses[bot_id] = resp
    return redirect(url_for("api_response", bot_id=bot_id))


# Get a response
@app.route("/api/bot/<int:bot_id>", methods=["GET"])
def _api_response(bot_id):
    print(f"Received GET for {bot_id}\nResponding with {bot_responses[bot_id]}\n\n")
    return bot_responses[bot_id]


@app.route("/api/bot/cleanup", methods=["GET"])
def _cleanup():
    bot_responses = {}
    return "Restored bots"


@app.route("/api/bot/", methods=["GET"])
def _main_view():
    return pp.pformat(bot_responses)