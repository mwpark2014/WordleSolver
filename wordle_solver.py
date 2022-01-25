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
    def __init__(self, word_length, num_attempts, answer=None):
        self.word_length = word_length
        self.num_attempts = num_attempts
        self.answer = answer and answer.upper()
        self.attempts = []
        self.responses = []
        self.correct_response = ''.join(['O' for _ in range(word_length)])

    def make_attempt_with_input(self) -> None:
        self.make_attempt(input('Please input a word attempt!\n'))

    def make_attempt(self, attempt_word) -> None:
        if not attempt_word:
            raise ValueError('Invalid None value for attempt_word')
        if len(attempt_word) != self.word_length:
            raise ValueError('Invalid string length for attempt_word')
        self.attempts.append(attempt_word.upper())
        self._pretty_print_attempts()

    # Automatically respond with "closeness to answer"
    def get_automated_attempt_response(self, attempt):
        assert self.answer is not None
        response = ''
        for i in range(len(self.answer)):
            if attempt[i] == self.answer[i]:
                response += 'O'
            elif attempt[i] in self.answer:
                response += '?'
            else:
                response += 'X'
        self._pretty_print_responses()
        self.responses.append(response)
        return response

    # Prompt user for the "closeness to answer" response to the solver's attempt
    def get_user_attempt_response(self):
        assert self.answer is None
        response = input('Please input the response to the last attempt with not contained = X, '
                         'misplaced = ?, and correct = O. Example for word_length = 5: XXOX?\n')
        if not response:
            raise ValueError('Invalid None value for response')
        if len(response) != self.word_length:
            raise ValueError('Invalid string length for response')
        self.responses.append(response.upper())
        self._pretty_print_responses()
        return response

    def play_wordle_alone_without_answer(self):
        for attempt in range(self.num_attempts):
            self.make_attempt_with_input()
            self.get_user_attempt_response()
            if self.responses[-1] == self.correct_response:
                print('Congratz, you solved the wordle!')
                break

    # def play_wordle_alone_with_answer(self):
    #     for attempt in range(self.num_attempts):

    def _pretty_print_attempts(self):
        for attempt in range(self.num_attempts):
            for char in range(self.word_length):
                display_char = self.attempts[attempt][char] if attempt < len(self.attempts) else '_'
                print(display_char, end='')
            print()

    def _pretty_print_responses(self):
        for attempt in range(self.num_attempts):
            for char in range(self.word_length):
                display_char = self.responses[attempt][char] if attempt < len(self.responses) else '_'
                print(display_char, end='')
            print()


# class WordleSolver:

if __name__ == '__main__':
    args = parser.parse_args()
    wordle = Wordle(args.word_length, args.num_attempts)
    wordle.play_wordle_alone_without_answer()