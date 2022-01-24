import argparse

parser = argparse.ArgumentParser(description='A Wordle puzzle solver.')
parser.add_argument("-w", "--word_length", type=int, help="Set word length", default=5)
parser.add_argument("-n", "--num_attempts", type=int, help="Set number of attempts", default=6)

class Wordle:
    # If answer is none, this Wordle does not have insight to the answer
    # and needs outside help from the user to determine how correct attempts are
    def __init__(self, word_length, num_attempts, answer = None):
        self.word_length = word_length
        self.num_attempts = num_attempts
        self.answer = answer
        self.attempts = []

    # Make an attempt
    def make_attempt(self, attempt_word):
        if not attempt_word:
            raise ValueError('Invalid None value for attempt_word')
        if len(attempt_word) != self.word_length:
            raise ValueError('Invalid string length for attempt_word')
        self.attempts.append(attempt_word.upper())

    # Prompt user for the response to the solver's attempt
    def get_attempt_response_input(self):
        print('Please input the response to the last attempt')
        # TODO:

    def pretty_print(self):
        print(self.word_length)
        for attempt in range(self.num_attempts):
            for row in range(self.word_length):
               print('_', end='')
            print('\n')


# class WordleSolver:

if __name__ == '__main__':
    args = parser.parse_args()
    wordle = Wordle(args.word_length, args.num_attempts)
    wordle.pretty_print()