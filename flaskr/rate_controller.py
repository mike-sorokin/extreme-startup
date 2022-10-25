import time 

MIN_REQUEST_INTERVAL_SECS = 1
MAX_REQUEST_INTERVAL_SECS = 20 
AVG_REQUEST_INTERVAL = 10
REQUEST_DELTA = 0.1 
SLASHDOT_THRESHOLD_SCORE = 2000

# Controller that regulates frequency of requests sent to players
# based on the result of the previous question response
class RateController():

    def __init__(self, delay=5):
        self.delay = min(delay, MAX_REQUEST_INTERVAL_SECS)
    
    def delay_before_next_request(self, question):
        error_problem = question.problem != ""
        correct_answer = question.answered_correctly()
        
        if error_problem:
            if self.delay < AVG_REQUEST_INTERVAL:
                self.delay = AVG_REQUEST_INTERVAL
            return MAX_REQUEST_INTERVAL_SECS
        elif correct_answer and self.delay > MIN_REQUEST_INTERVAL_SECS:
            self.delay -= REQUEST_DELTA
        elif not correct_answer and self.delay < MAX_REQUEST_INTERVAL_SECS:
            self.delay += REQUEST_DELTA
        else: # Error case
            print(f"!!!!! unrecognized result '#{question.result}' from #{repr(question)} in Scoreboard#score")
            return MAX_REQUEST_INTERVAL_SECS

        return self.delay 

    def wait_for_next_request(self, question):
        time.sleep(self.delay_before_next_request(question))

    def update_algorithm_based_on_score(self, score):
        return self

# TODO: Implement Slashdot and other more specialised RateControllers
class SlashdotRateController(RateController):
    pass 