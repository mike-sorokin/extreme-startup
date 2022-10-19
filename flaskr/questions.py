from uuid import uuid4
import random

class Question: 
    def __init__(self, points=10):
        self.uuid = str(uuid4())
        self.points = points
        self.answer = None
        self.result = ""
        self.problem =  ""

    def ask(self, player):
        try:
            response = requests.get(
                player.api, params={"q": self.as_text()}
            )

            if response.status_code == 200:
                self.answer = response.text.strip().lower()
            else:
                self.problem = "ERROR_RESPONSE"

        except Exception:
            self.problem = "NO_SERVER_RESPONSE"
        self.get_result()

    def get_result(self):
        if self.answer is None:
            self.result = self.problem
        elif self.answered_correctly():
            self.result = "CORRECT"
        else:
            self.result = "WRONG"
    
    def delay_before_next(self):
        if self.result == "CORRECT":
            return 5
        elif self.result == "WRONG":
            return 10
        else: 
            return 20

    def display_result(self):
        return f"\tQuestion: {self.__str__}\n\tAnswer: {self.answer}\n\tResult: {self.result}"

    def __str__(self):
        return f"{self.uuid}: {self.as_text()}"
    
    def as_text(self):
        return "Basic Question Class"

    def answered_correctly(self):
        return self.answer == self.correct_answer()

    def correct_answer(self):
        pass 


class WarmupQuestion(Question):
    def __init__(self, player_name="default_name"):
        self.player_name = player_name
        super().__init__()
    
    def correct_answer(self):
        return self.player_name
    
    def as_text(self):
        return "What is your name?"

class BinaryMathsQuestion(Question):
    def __init__(self, *numbers):
        super().__init__()
        if valid_num_arguments(2, numbers):
            self.n1 = numbers[0]
            self.n2 = numbers[1]
        else:
            self.n1 = random.randint(1,100)
            self.n2 = random.randint(1,100)

class TernaryMathsQuestion(Question):
    def __init__(self, *numbers):
        if valid_num_arguments(3, numbers):
            self.n1, self.n2, self.n3 = numbers
        else:
            self.n1, self.n2, self.n3 = random.sample(range(1, 100), 3)

class AdditionQuestion(BinaryMathsQuestion):
    def as_text(self):
        return f"What is {self.n1} plus {self.n2}"

    def correct_answer(self):
        return self.n1 + self.n2 

class SubtractionQuestion(BinaryMathsQuestion):
    def as_text(self):
        return f"What is {self.n1} minus {self.n2}"
    
    def correct_answer(self):
        return self.n1 - self.n2 


class MultiplicationQuestion(BinaryMathsQuestion):
    def as_text(self):
        return f"What is {self.n1} times {self.n2}"
    
    def correct_answer(self):
        return self.n1 * self.n2 

class AdditionAdditionQuestion(TernaryMathsQuestion):
    def __init__(self, points, *numbers):
        super().__init__(numbers)    
        self.points = 30
    
    def as_text(self):
        return f"What is {self.n1} plus {self.n2} plus {self.n3}"
    
    def correct_answer(self):
        return self.n1 + self.n2 + self.n3


def valid_num_arguments(arg_num, *numbers):
    return list(numbers) == arg_num and all(isinstance(num, int) for num in numbers)