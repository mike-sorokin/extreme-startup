import time

# Constants below in seconds
MIN_REQUEST_INTERVAL_SECS = 1
MAX_REQUEST_INTERVAL_SECS = 20
AVG_REQUEST_INTERVAL = DEFAULT_DELAY = 5
REQUEST_DELTA = 0.1

SLASHDOT_THRESHOLD_SCORE = 2000

# Controller that regulates frequency of requests sent to players
# based on the result of the previous question response
class RateController:
    def __init__(self, delay=DEFAULT_DELAY):
        self.delay = min(delay, MAX_REQUEST_INTERVAL_SECS)

    def delay_before_next_question(self, prev_delay, result):
        if result == "CORRECT":
            return max(MIN_REQUEST_INTERVAL_SECS, prev_delay - 1)
        elif result == "WRONG":
            return min(MAX_REQUEST_INTERVAL_SECS, prev_delay + 1)
        else:
            return min(MAX_REQUEST_INTERVAL_SECS, prev_delay + 2)


    def delay_before_next_request(self, question):
        error_problem = question.problem != ""
        correct_answer = question.answered_correctly()

        if error_problem:

            if self.delay < AVG_REQUEST_INTERVAL:
                self.delay = AVG_REQUEST_INTERVAL

            return MAX_REQUEST_INTERVAL_SECS

        elif correct_answer:
            self.delay = max(self.delay - REQUEST_DELTA, MIN_REQUEST_INTERVAL_SECS)

        elif not correct_answer:
            self.delay = min(self.delay + REQUEST_DELTA, MAX_REQUEST_INTERVAL_SECS)

        else:  # Error case -- SHOULD NOT ENTER 
            print(
                f"!!!!! unrecognized result '#{question.result}' from #{repr(question)} in Scoreboard#score"
            )
            return MAX_REQUEST_INTERVAL_SECS

        return self.delay

    def wait_for_next_request(self, question, warmup_over):
        if warmup_over.is_set():
            time.sleep(self.delay_before_next_request(question))
        else:
            warmup_over.wait(timeout=self.delay_before_next_request(question))

    def update_algorithm_based_on_score(self, score):
        return self

    def reset(self):
        self.delay = DEFAULT_DELAY
        time.sleep(self.delay)


# TODO: Implement Slashdot and other more specialised RateControllers
class SlashdotRateController(RateController):
    pass
