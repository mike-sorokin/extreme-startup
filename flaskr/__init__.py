from crypt import methods
from flask import Flask, render_template, request
from flaskr.player import Player
from flaskr.scoreboard import Scoreboard
import os

app = Flask(__name__)

players = set()
scoreboard = Scoreboard(os.getenv('LENIENT'))


@app.route("/")
def index():
    return render_template('leaderboard.html', leaderboard=players)

@app.route("/players", methods=['GET', 'POST'])
def add_player():
    if request.method == 'GET':
        return render_template('add_player.html')
    else:
        player = Player(request.form['name'], request.form['url'])
        players.add(player)
        return render_template('player_added.html')