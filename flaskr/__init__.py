from crypt import methods
from uuid import uuid4
from flask import Flask, render_template, request, redirect, make_response
from flaskr.player import Player
from flaskr.event import Event
from flaskr.game import Game
from flaskr.scoreboard import Scoreboard
from flaskr.json_encoder import JSONEncoder
import os
import threading
import requests
import time

app = Flask(__name__, static_folder="frontend", static_url_path="/")

# games: game_id -> game object
games = {}

# players: player_id -> player
players = {}

# scoreboard: player_id -> score
scoreboard = {}

# player_threads: player_id -> player_thread
player_threads = {}

encoder = JSONEncoder()
lock = threading.Lock()

# PRODUCTION CONSTANT(S)
QUESTION_TIMEOUT = 10
QUESTION_DELAY = 5


@app.route("/", methods=["GET"])
def index():
    return app.send_static_file("index.html")


@app.route("/api", methods=["GET", "POST", "DELETE"])
def api_index():
    if request.method == "GET":
        return encoder.encode(games)
    elif request.method == "POST":
        new_game = Game()
        games[new_game.id] = new_game
        return encoder.encode(new_game)
    elif request.method == "DELETE":
        remove_players(*[p for g in games.values() for p in g.players])
        games.clear()
        return ("", 204)


@app.route("/api/<game_id>", methods=["GET", "PUT", "DELETE"])
def game(game_id):
    if request.method == "GET":
        return (
            encoder.encode(games[game_id]) if game_id in games else ("NOT FOUND", 404)
        )
    elif request.method == "PUT":
        games[game_id].round += 1
        return ("ROUNDS_INCREMENTED", 200)
    elif request.method == "DELETE":
        remove_players(*games[game_id].players)
        del games[game_id]
        return {"deleted": game_id}


@app.route("/api/<game_id>/players", methods=["GET", "POST", "DELETE"])
def all_players(game_id):
    if request.method == "GET":
        players_ids = games[game_id].players
        players_dict = {id: players[id] for id in players_ids}
        r = make_response(encoder.encode({"players": players_dict}))
        r.mimetype = "application/json"
        return r

    elif request.method == "POST":
        player = Player(game_id, request.form["name"], api=request.form["api"])
        scoreboard[player] = 0
        games[game_id].players.append(player.uuid)
        players[player.uuid] = player
        player_thread = threading.Thread(target=sendQuestion, args=(player,))
        player_threads[player.uuid] = player_thread
        player_thread.daemon = True
        player_thread.start()
        r = make_response(encoder.encode(player))
        r.mimetype = "application/json"
        return encoder.encode(player)

    elif request.method == "DELETE":
        remove_players(*games[game_id].players)
        games[game_id].players.clear()
        return ("", 204)


@app.route("/api/<game_id>/players/<player_id>", methods=["GET", "PUT", "DELETE"])
def player(game_id, player_id):
    if request.method == "GET":
        return encoder.encode(players[player_id])
    elif request.method == "PUT":
        if "name" in request.form:
            players[player_id].name = request.form["name"]
        if "api" in request.form:
            players[player_id].api = request.form["api"]
        return encoder.encode(players[player_id])
    elif request.method == "DELETE":
        games[game_id].players.remove(player_id)
        remove_players(player_id)
        return {"deleted": player_id}


@app.route("/api/<game_id>/players/<player_id>/events", methods=["GET", "DELETE"])
def player_events(game_id, player_id):
    if request.method == "GET":
        pass
    elif request.method == "DELETE":
        pass


@app.route(
    "/api/<game_id>/players/<player_id>/events/<event_id>", methods=["GET", "DELETE"]
)
def player_event(game_id, player_id, event_id):
    if request.method == "GET":
        pass
    elif request.method == "DELETE":
        pass


def remove_players(*player_id):
    for pid in player_id:
        assert pid in player_threads
        players[pid].active = False
        # player_threads[pid].join()
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
