from curses import noecho
import uuid


class Player:
    def __init__(self, name, url):
        self.name = name
        self.url = url
        self.uuid = str(uuid.uuid4())
        self.log = []

    def log_result(id, msg, point):
        pass

    def __str__():
        return f"{self.name} ({self.url})"


    

