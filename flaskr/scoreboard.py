from flaskr.event import Event
import datetime as dt
from math import floor, ceil

PROBLEM_DECREMENT = 50
STREAK_LENGTH = 30

# Track player's score in a particular game. Scores players based on question type, positioning on scoreboard, and leniency mode.
class Scoreboard:
    def __init__(self, lenient=True):
        self.lenient = lenient

        # scores: { player_id -> player score }
        self.scores = {}

        # running_totals: [ {"time": timestamp, "pid": score} ]
        self.running_totals = [{"time": dt.datetime.now(dt.timezone.utc)}]

        self.correct_tally = {}
        self.incorrect_tally = {}
        self.request_counts = {}

    # Adjust score for player based on question result, update streak (capped to 6-question past), and log event
    def increment_score_for(self, player, question):
        increment = self.score(question, self.leaderboard_position(player))
        self.scores[player.uuid] += increment

        if increment > 0:
            self.correct_tally[player.uuid] += 1
            player.streak += "1"
            player.curr_streak_length += 1
            player.longest_streak = max(
                player.longest_streak, player.curr_streak_length
            )

        elif increment < 0:
            self.incorrect_tally[player.uuid] += 1

            if question.problem in ["ERROR_RESPONSE", "NO_SERVER_RESPONSE"]:
                player.streak += "0"
            else:
                player.streak += "X"

            player.curr_streak_length = 0

        player.score = self.scores[player.uuid]
        event = Event(
            player.uuid,
            player.game_id,
            question.as_text(),
            0,
            increment,
            question.result if question.problem == "" else question.problem,
        )
        # If the last event in the cache was less than 1sec ago, append it there.
        # Otherwise, make a new dict entry
        prev_time = self.running_totals[-1]["time"]
        diff = event.timestamp - prev_time
        if diff.total_seconds() < 1:
            self.running_totals[-1][player.uuid] = player.score
        else:
            self.running_totals.append(
                {"time": event.timestamp, f"{player.uuid}": player.score}
            )

        player.log_event(event)

        player.streak = player.streak[-STREAK_LENGTH:]
        player.round_index += 1

    def record_request_for(self, player):
        self.request_counts[player.uuid] += 1

    # Initialise new player in scoreboard, default values all to 0
    def new_player(self, player):
        self.request_counts[player.uuid] = 0
        self.correct_tally[player.uuid] = 0
        self.incorrect_tally[player.uuid] = 0
        self.scores[player.uuid] = 0

    def delete_player(self, player):
        del self.scores[player.uuid]
        del self.incorrect_tally[player.uuid]
        del self.correct_tally[player.uuid]
        del self.request_counts[player.uuid]

    def current_score(self, player):
        return self.scores[player.uuid]

    def reset_player(self, player):
        self.scores[player.uuid] = 0
        self.incorrect_tally[player.uuid] = 0
        self.correct_tally[player.uuid] = 0
        player.score = 0
        self.request_counts[player.uuid] = 0

    def current_total_correct(self, player):
        return self.correct_tally[player.uuid]

    def current_total_not_correct(self, player):
        return self.incorrect_tally[player.uuid]

    def total_requests_for(self, player):
        return self.request_counts[player.uuid]

    # Sort leaderboard in descending order from BEST PERFORMING PLAYER -> WORST PERFORMING PLAYER
    def leaderboard(self):
        return {
            k: v
            for k, v in sorted(
                self.scores.items(), key=lambda item: item[1], reverse=True
            )
        }

    def leaderboard_position(self, player):
        return list(self.leaderboard().keys()).index(player.uuid) + 1

    def leaderboard_position_id(self, player_id):
        return list(self.leaderboard().keys()).index(player_id) + 1

    def leaderboard_first_player_id(self):
        return list(self.leaderboard().keys())[0]

    def leaderboard_last_player_id(self):
        return list(self.leaderboard().keys())[-1]

    def player_in_top_k_percentile(self, player_id, k):
        return list(self.leaderboard().keys()).index(player_id) + 1 <= (
            k * len(self.scores) / 100
        )

    def player_in_bottom_k_percentile(self, player_id, k):
        return list(self.leaderboard().keys()).index(player_id) + 1 > (
            (100 - k) * len(self.scores) / 100
        )

    def leaderboard_top_k_percentile_players(self, k):
        end_index = floor(k * len(self.scores) / 100)
        return list(self.leaderboard())[0:end_index]

    def leaderboard_bottom_k_percentile_players(self, k):
        from_index = ceil((100 - k) * len(self.scores) / 100)
        end_index = len(self.scores)
        return list(self.leaderboard())[from_index:end_index]

    # Identity points delta based on question.result
    def score(self, question, leaderboard_position):
        res, problem = question.result, question.problem
        if res == "CORRECT":
            return question.points

        elif res == "WRONG":
            return (
                self.allow_passes(question, leaderboard_position)
                if self.lenient
                else self.penalty(question, leaderboard_position)
            )

        elif problem == "ERROR_RESPONSE" or problem == "NO_SERVER_RESPONSE":
            return -1 * PROBLEM_DECREMENT

        else:
            print(
                f"!!!!! unrecognized result '#{question.result}' from #{repr(question)} in Scoreboard#score"
            )

    # Based on game mode (lenient), let player "off" for incorrect response
    def allow_passes(self, question, leaderboard_position):
        return (
            0 if question.answer == "" else self.penalty(question, leaderboard_position)
        )

    # Penalty that adjusts based on leadeboard pos
    # Conceptually, better-ranked players get deducted more for wrong answers than worse-ranked players
    def penalty(self, question, leaderboard_position):
        return -1 * question.points / leaderboard_position
