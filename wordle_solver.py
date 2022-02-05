import argparse
import heapq

import twl

parser = argparse.ArgumentParser(description='A Wordle puzzle solver.')
parser.add_argument("-w", "--word_length", type=int, help="Set word length", default=5)
parser.add_argument("-n", "--num_attempts", type=int, help="Set number of attempts", default=6)

FREQ_LETTER_ANYWHERE_FACTOR = .3


# The Wordle class defining a puzzle, console UI, and a basic way to get input from the user
class Wordle:
    # Defaults are defined in the ArgumentParser
    def __init__(self, word_length, num_attempts) -> None:
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
    def get_user_attempt_response(self) -> str:
        response = input('Please input the response to the last attempt with not contained = X, '
                         'misplaced = ?, and correct = O. Example for word_length = 5: XXOX?\n')
        return self.get_attempt_response(response)

    def get_attempt_response(self, response) -> str:
        self._validate_word(response)
        self.responses.append(response.upper())
        self._pretty_print_responses()
        return response.upper()

    # Returns true if game finished with a win. Returns false if game is left unfinished
    def play_wordle_alone_without_answer(self):
        for attempt in range(self.num_attempts):
            self.make_attempt_with_input()
            self.get_user_attempt_response()
            if self.is_solved():
                return True
        return False

    # Returns true if game finished with a win. Returns false if game is left unfinished
    def play_wordle_alone_with_answer(self, answer):
        self._validate_word(answer)
        answer = answer.upper()
        for attempt in range(self.num_attempts):
            self.make_attempt_with_input()
            self.get_automated_attempt_response(answer)
            if self.is_solved():
                return True
        return False

    def is_solved(self):
        if self.responses[-1] == self.correct_response:
            print('Congratz, you solved the wordle!')
            return True
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


def get_letter_position_freq_dict_key(word, i) -> str:
    return word[i] + str(i)


# O(num_words*num_length)
# This frequency dict roughly maps letters to how often they are correct (O/green)
def create_letter_position_freq_dict(words):
    freq_dict = {}
    for word in words:
        for i in range(len(word)):
            key = get_letter_position_freq_dict_key(word, i)
            freq_dict[key] = freq_dict.get(key, 0) + 1
    return freq_dict


# O(num_words*num_length)
# This frequency dict roughly maps letters to how often they are misplaced (?/yellow)
def create_letter_freq_dict(words):
    freq_dict = {}
    for word in words:
        for i in range(len(word)):
            freq_dict[word[i]] = freq_dict.get(word[i], 0) + 1
    return freq_dict


class WordleSolver:
    def __init__(self, word_length, num_attempts):
        self.word_length = word_length
        self.num_attempts = num_attempts
        self.filtered_words_by_length = set(word.upper() for word in twl.iterator() if len(word) == word_length)
        self.not_contained_letters = set()
        print("{} potential words".format(len(self.filtered_words_by_length)))

    # O(num_words*num_length)
    def get_best_freq_score_word(self, words: set, letter_position_freq_dict: dict, letter_freq_dict: dict) -> str:
        freq_word_tuple = heapq.heappop(
            self.create_word_freq_score_heap(words, letter_position_freq_dict, letter_freq_dict))
        # Tuple: (-freq_score, word). Sample tuple: (-7824, 'SORES')
        return freq_word_tuple[1]

    # The automated solver that will solve a given Wordle
    def create_word_freq_score_heap(self, words: set, letter_position_freq_dict: dict, letter_freq_dict: dict) -> list:
        if not letter_position_freq_dict and letter_freq_dict:
            print('Warning: There are no freq dicts defined, so freq_score_heap is completely randomized')
        freq_word_tuples = []
        for word in words:
            freq_score = 0
            for i in range(len(word)):
                key = get_letter_position_freq_dict_key(word, i)
                freq_score += letter_position_freq_dict.get(key, 0)
                freq_score += FREQ_LETTER_ANYWHERE_FACTOR * letter_freq_dict.get(word[i], 0) / self.word_length
            freq_word_tuples.append((-freq_score, word))
        heapq.heapify(freq_word_tuples)
        return freq_word_tuples

    # Filter eliminated words using response consisting of not contained letters and misplaced letters
    # O(num_words*word_length)
    def parse_response_and_filter(self, words: set, attempt: str, response: str) -> set:
        assert len(attempt) == len(response)
        correct_letters_by_index = {}
        misplaced_letters_by_index = {}
        uncontained_letters = set()
        for i in range(len(response)):
            if response[i] == 'X':
                uncontained_letters.add(attempt[i])
            elif response[i] == '?':
                misplaced_letters_by_index[i] = attempt[i]
            elif response[i] == 'O':
                correct_letters_by_index[i] = attempt[i]
            else:
                raise ValueError('Invalid character in received response')
        return set(filter(
            lambda word: self._filter_eliminated_words(
                word, correct_letters_by_index, misplaced_letters_by_index, uncontained_letters),
            words))

    def _filter_eliminated_words(self, word: str, correct_letters: dict, misplaced_letters: dict,
                                 uncontained_letters: set) -> bool:
        misplaced_letters_list = list(misplaced_letters.values())
        for i in range(self.word_length):
            # Letter at this position matches a correct (O/green) letter, ignore other checks
            if word[i] == correct_letters.get(i):
                continue
            # There is a correct (O/green) letter at this position,
            # but it doesn't match the letter at this position in the current word
            elif correct_letters.get(i) and word[i] != correct_letters.get(i):
                return False
            # There is a misplaced (?/yellow) letter at this position,
            # but it does match the letter at this position in the current word
            elif word[i] == misplaced_letters.get(i):
                return False
            # There is a letter at this position in the current word that matches a misplaced (?/yellow) letter, so
            # let's continue and ignore any uncontained (X/gray) letters matching the same letter for now
            elif word[i] in misplaced_letters_list:
                misplaced_letters_list.remove(word[i])
                continue
            # This letter is not contained (X/gray), so this word should be eliminated
            elif word[i] in uncontained_letters:
                return False
        # If we make it to the end and there are misplaced letters that have not been found in the current word,
        # then this word should be eliminated
        if len(misplaced_letters_list) > 0:
            return False
        return True

    def solve(self, answer=None) -> bool:
        wordle = Wordle(self.word_length, self.num_attempts)
        possible_words = self.filtered_words_by_length
        # Taking most expensive parts of what's in this loop, 
        # the time complexity of WordleSolver.solve is O(num_words*word_length*num_attempts)
        for attempt in range(self.num_attempts):
            letter_position_freq_dict = create_letter_position_freq_dict(possible_words)
            letter_freq_dict = create_letter_freq_dict(possible_words)
            if attempt == 0:
                next_word = "SALET"
            else:
                next_word = self.get_best_freq_score_word(possible_words, letter_position_freq_dict, letter_freq_dict)
            wordle.make_attempt(next_word)
            response = wordle.get_user_attempt_response() if answer is None else wordle.get_automated_attempt_response(
                answer)
            if wordle.is_solved():
                return True
            possible_words = self.parse_response_and_filter(possible_words, next_word, response)
            print("{} possible words left".format(len(possible_words)))
        return False


if __name__ == '__main__':
    args = parser.parse_args()
    wordle_solver = WordleSolver(args.word_length, args.num_attempts)
    wordle_solver.solve()
