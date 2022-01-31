import argparse
import heapq

import twl

parser = argparse.ArgumentParser(description='A Wordle puzzle solver.')
parser.add_argument("-w", "--word_length", type=int, help="Set word length", default=5)
parser.add_argument("-n", "--num_attempts", type=int, help="Set number of attempts", default=6)


# The Wordle class defining a puzzle, console UI, and a basic way to get input from the user
class Wordle:
    CHAR_RESULT = {
        'NOT_CONTAINED': 0,
        'MISPLACED': 1,
        'CORRECT': 2,
    }

    # Defaults are defined in the ArgumentParser
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
    def get_automated_attempt_response(self, answer):
        response = ''
        for i in range(len(answer)):
            if self.attempts[-1][i] == answer[i]:
                response += 'O'
            elif self.attempts[-1][i] in answer:
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
            self.get_automated_attempt_response(answer)
        return False

    def _validate_word(self, word) -> None:
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


def _get_freq_dict_key(word, i) -> str:
    return word[i] + str(i)


# The automated solver that will solve a given Wordle
class WordleSolver:
    def __init__(self, word_length, num_attempts):
        self.word_length = word_length
        self.num_attempts = num_attempts
        self.filtered_words_by_length = set(word.upper() for word in twl.iterator() if len(word) == word_length)
        self.not_contained_letters = set()
        print("{} potential words".format(len(self.filtered_words_by_length)))

    # TODO: Fill in time complexity
    def create_freq_dict(self, words):
        freq_dict = {}
        for word in words:
            for i in range(len(word)):
                key = _get_freq_dict_key(word, i)
                freq_dict[key] = freq_dict.get(key, 0) + 1
        return freq_dict

    # TODO: Fill in time complexity
    def get_best_freq_score_word(self, freq_dict):
        freq_word_tuple = self.create_word_freq_score_heap(freq_dict)[0]
        # Tuple: (-freq_score, word). Sample tuple: (-7824, 'SORES')
        return freq_word_tuple[1]

    def create_word_freq_score_heap(self, freq_dict):
        if not freq_dict:
            print('Warning: There is no freq_dict defined, so freq_score_heap is completely randomized')
        freq_word_tuples = []
        for word in self.filtered_words_by_length:
            freq_score = 0
            for i in range(len(word)):
                key = _get_freq_dict_key(word, i)
                freq_score += freq_dict.get(key, 0)
            freq_word_tuples.append((-freq_score, word))
        heapq.heapify(freq_word_tuples)
        return freq_word_tuples

    # Filter eliminated words using response consisting of not contained letters and misplaced letters
    # TODO: Fill in time complexity
    def filter_eliminated_words(self, attempt, response) -> set:
        assert len(attempt) == len(response)
        misplaced_letter_by_index = {}
        for i in range(len(response)):
            if response[i] == 'X':
                self.not_contained_letters.add(attempt[i])
            elif response[i] == '?':
                misplaced_letter_by_index[i] = attempt[i]
        return set(filter(lambda word: self._filter_words_by_invalid_letters(word, misplaced_letter_by_index),
                          self.filtered_words_by_length))

    def _filter_words_by_invalid_letters(self, word, misplaced_letter_by_index):
        for i in range(len(word)):
            if word[i] in self.not_contained_letters or word[i] == misplaced_letter_by_index.get(i):
                return False
        return True

    def solve(self, answer=None) -> bool:
        wordle = Wordle(self.word_length, self.num_attempts)
        freq_dict = self.create_freq_dict(self.filtered_words_by_length)
        next_word = self.get_best_freq_score_word(freq_dict)
        wordle.make_attempt(next_word)
        response = wordle.get_user_attempt_response() if answer is None else wordle.get_automated_attempt_response(
            answer)

        return False


if __name__ == '__main__':
    args = parser.parse_args()
    wordle_solver = WordleSolver(args.word_length, args.num_attempts)
    wordle_solver.solve()
