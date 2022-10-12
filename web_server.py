from crypt import methods
from flask import Flask, render_template, request

app = Flask(__name__)

players = []

@app.route("/")
def index():
    return render_template('leaderboard.html', leaderboard=players)

@app.route("/players", methods=['GET', 'POST'])
def add_player():
    if request.method == 'GET':
        return render_template('add_player.html')
    else:
        players.append({'name': request.form['name'], "score": 0})
        return render_template('player_added.html')