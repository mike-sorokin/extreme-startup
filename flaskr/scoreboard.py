from flaskr.event import Event 

class Scoreboard:
    def __init__(self, lenient=True):
        self.lenient = lenient

        # scores: { player_id -> player score }
        self.scores = {}

        self.correct_tally = {}
        self.incorrect_tally = {}
        self.request_counts = {}

    def increment_score_for(self, player, question):
        increment = self.score(question, self.leaderboard_position(player))
        self.scores[player.uuid] += increment
        if increment > 0:
            self.correct_tally[player.uuid] += 1
        elif increment < 0:
            self.incorrect_tally[player.uuid] += 1
        event = Event(player.uuid, player.game_id, question.as_text(), 0, increment, question.result if question.problem == "" else question.problem)
        player.log_event(event)

    def record_request_for(self, player):
        self.request_counts[player.uuid] += 1

    def new_player(self, player):
        self.request_counts[player.uuid] = 0
        self.correct_tally[player.uuid] = 0
        self.incorrect_tally[player.uuid] = 0 
        self.scores[player.uuid] = 0

    def delete_player(self, player):
        del self.scores[player.uuid]

    def current_score(self, player):
        return self.scores[player.uuid]

    def current_total_correct(self, player):
        return self.correct_tally[player.uuid]

    def current_total_not_correct(self, player):
        return self.incorrect_tally[player.uuid]

    def total_requests_for(self, player):
        return self.request_counts[player.uuid]

    def leaderboard(self):
        return {k: v for k, v in sorted(self.scores.items(), key=lambda item: item[1])}

    def leaderboard_position(self, player):
        return list(self.leaderboard().keys()).index(player.uuid) + 1

    def score(self, question, leaderboard_position):
        res, problem = question.result, question.problem
        if res == "CORRECT":
            return question.points
        elif res == "WRONG":
            return self.allow_passes(question, leaderboard_position) if self.lenient else self.penalty(question, leaderboard_position)
        elif problem == "ERROR_RESPONSE" or problem == "NO_SERVER_RESPONSE":
            return -50
        else: 
            print(f"!!!!! unrecognized result '#{question.result}' from #{repr(question)} in Scoreboard#score")

    def allow_passes(self, question, leaderboard_position):
        return (
            0 if question.answer == "" else self.penalty(question, leaderboard_position)
        )

    def penalty(self, question, leaderboard_position):
        return -1 * question.points / leaderboard_position