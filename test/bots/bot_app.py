from flask import Flask


@app.route("/")
def hello_world():

    return "<p>Hello, World!</p>"
