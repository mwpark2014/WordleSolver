import argparse

parser = argparse.ArgumentParser(description='A Wordle puzzle solver.')
parser.add_argument("-w", "--word_length", type=int, help="Set word length", default=5)
parser.add_argument("-n", "--num_attempts", type=int, help="Set number of attempts", default=6)


class Wordle:
    CHAR_RESULT = {
        'NOT_CONTAINED': 0,
        'MISPLACED': 1,
        'CORRECT': 2,
    }

    # If answer is none, this Wordle does not have insight to the answer
    # and needs outside help from the user to determine how correct attempts are
    def __init__(self, word_length, num_attempts):
        self.word_length = word_length
        self.num_attempts = num_attempts
        self.attempts = []
        self.responses = []
        self.correct_response = ''.join(['O' for _ in range(word_length)])

    def make_attempt_with_input(self) -> None:
        self.make_attempt(input('Please input a word attempt!\n'))

    def make_attempt(self, attempt_word) -> None:
        self._validate_word(attempt_word)
        self.attempts.append(attempt_word.upper())
        self._pretty_print_attempts()

    # Automatically respond with "closeness to answer"
    def get_automated_attempt_response(self, attempt, answer):
        response = ''
        for i in range(len(answer)):
            if attempt[i] == answer[i]:
                response += 'O'
            elif attempt[i] in answer:
                response += '?'
            else:
                response += 'X'
        self.get_attempt_response(response)

    # Prompt user for the "closeness to answer" response to the solver's attempt
    def get_user_attempt_response(self):
        response = input('Please input the response to the last attempt with not contained = X, '
                         'misplaced = ?, and correct = O. Example for word_length = 5: XXOX?\n')
        self.get_attempt_response(response)

    def get_attempt_response(self, response):
        self._validate_word(response)
        self.responses.append(response.upper())
        self._pretty_print_responses()

    # Returns true if game finished with a win. Returns false if game is left unfinished
    def play_wordle_alone_without_answer(self):
        for attempt in range(self.num_attempts):
            self.make_attempt_with_input()
            self.get_user_attempt_response()
            if self.responses[-1] == self.correct_response:
                print('Congratz, you solved the wordle!')
                return True
        return False

    # Returns true if game finished with a win. Returns false if game is left unfinished
    def play_wordle_alone_with_answer(self, answer):
        self._validate_word(answer)
        answer = answer.upper()
        for attempt in range(self.num_attempts):
            self.make_attempt_with_input()
            if self.attempts[-1] == answer:
                print('Congratz, you solved the wordle!')
                return True
            self.get_automated_attempt_response(self.attempts[-1], answer)
        return False

    def _validate_word(self, word):
        if not word:
            raise ValueError('Invalid None value for response')
        if len(word) != self.word_length:
            raise ValueError('Invalid string length for response')

    def _pretty_print_attempts(self):
        for attempt in range(self.num_attempts):
            for char in range(self.word_length):
                display_char = self.attempts[attempt][char] if attempt < len(self.attempts) else '_'
                print(display_char, end='')
            print()
        print()

    def _pretty_print_responses(self):
        for attempt in range(self.num_attempts):
            for char in range(self.word_length):
                display_char = self.responses[attempt][char] if attempt < len(self.responses) else '_'
                print(display_char, end='')
            print()
        print()


# class WordleSolver:

if __name__ == '__main__':
    args = parser.parse_args()
    wordle = Wordle(args.word_length, args.num_attempts, 'BULLY')
    wordle.play_wordle_alone_with_answer()