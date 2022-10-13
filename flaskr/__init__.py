from crypt import methods
from flask import Flask, render_template, request
from flaskr.player import Player
from flaskr.scoreboard import Scoreboard
import os
import threading
import requests
import time

app = Flask(__name__)

players = {}
# scoreboard = Scoreboard(os.getenv('LENIENT'))
scoreboard = {}

@app.route("/")
def index():
    return render_template('leaderboard.html', leaderboard=scoreboard)

@app.route("/players", methods=['GET', 'POST'])
def add_player():
    if request.method == 'GET':
        return render_template('add_player.html')
    else:
        player = Player(request.form['name'], request.form['url'])
        # scoreboard.new_player(player)
        scoreboard[player] = 0
        players[player.uuid] = player
        player_thread = threading.Thread(target=sendQuestion, args=(player,))
        player_thread.start()
        return render_template('player_added.html')

def sendQuestion(player):
    while True:
        r = requests.get(player.url, params={'q': "What is your name?"}).content
        if r.decode("utf-8") == player.name:
            scoreboard[player] += 2
        else:
            scoreboard[player] -= 1
        time.sleep(1)
