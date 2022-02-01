import heapq
import unittest
from unittest.mock import Mock

import wordle_solver as ws


class TestWordleSolverMethods(unittest.TestCase):
    def setUp(self) -> None:
        self.wordle = ws.Wordle(5, 6)
        self.wordle_solver = ws.WordleSolver(5, 6)
        self.initial_letter_position_freq_dict = ws.create_letter_position_freq_dict(
            self.wordle_solver.filtered_words_by_length)
        self.initial_letter_freq_dict = ws.create_letter_freq_dict(
            self.wordle_solver.filtered_words_by_length)

    def test_make_attempt(self):
        self.wordle.make_attempt("point")
        self.wordle.make_attempt("PRICK")
        self.assertEqual('POINT', self.wordle.attempts[0])
        self.assertEqual('PRICK', self.wordle.attempts[1])
        self.assertEqual(2, len(self.wordle.attempts))
        with self.assertRaises(ValueError):
            self.wordle.make_attempt("four")

    def test_get_automated_attempt_response(self):
        self.wordle.make_attempt("HILLY")
        self.wordle.get_automated_attempt_response("LIGHT")
        self.assertEqual("?O?XX", self.wordle.responses[-1])
        self.wordle.make_attempt("DIGIT")
        self.wordle.get_automated_attempt_response("LIGHT")
        self.assertEqual("XOOXO", self.wordle.responses[-1])
        self.wordle = ws.Wordle(5, 6)

    def test_play_wordle_alone_without_answer(self):
        wordle = ws.Wordle(5, 6)
        wordle.make_attempt_with_input = Mock(side_effect=lambda: wordle.make_attempt('POINT'))
        wordle.get_user_attempt_response = Mock(side_effect=lambda: wordle.get_attempt_response('OOOOO'))
        self.assertEqual(wordle.play_wordle_alone_without_answer(), True)

    def test_play_wordle_alone_with_answer(self):
        wordle = ws.Wordle(5, 6)
        wordle.make_attempt_with_input = Mock(side_effect=lambda: wordle.make_attempt('POINT'))
        self.assertEqual(wordle.play_wordle_alone_with_answer('POINT'), True)
        wordle = ws.Wordle(5, 6)
        wordle.make_attempt_with_input = Mock(side_effect=lambda: wordle.make_attempt('PINTS'))
        self.assertEqual(wordle.play_wordle_alone_with_answer('POINT'), False)
        wordle = ws.Wordle(5, 6)
        wordle.make_attempt_with_input = Mock(side_effect=lambda: wordle.make_attempt('POINT'))
        with self.assertRaises(ValueError):
            wordle.play_wordle_alone_with_answer(None)

    def test_solver_create_letter_position_freq_dict(self):
        freq_dict = ws.create_letter_position_freq_dict(self.wordle_solver.filtered_words_by_length)
        self.assertEqual(len(freq_dict), 129)
        self.assertEqual(freq_dict['E2'], 580)
        self.assertEqual(freq_dict['S4'], 2785)
        with self.assertRaises(KeyError):
            test_freq = freq_dict['S5']

    def test_solver_create_word_freq_score_heap(self):
        freq_score_heap = self.wordle_solver.create_word_freq_score_heap(self.wordle_solver.filtered_words_by_length,
                                                                         self.initial_letter_position_freq_dict,
                                                                         self.initial_letter_freq_dict)
        self.assertEqual(8938, len(freq_score_heap))
        self.assertEqual((-9011.28, 'SORES'), heapq.heappop(freq_score_heap))
        self.assertEqual((-9001.480000000001, 'SANES'), heapq.heappop(freq_score_heap))
        freq_score_heap = self.wordle_solver.create_word_freq_score_heap(self.wordle_solver.filtered_words_by_length,
                                                                         {}, {})
        self.assertEqual(len(freq_score_heap), 8938)

    def test_solver_get_best_freq_score_word(self):
        best_freq_score_word = self.wordle_solver.get_best_freq_score_word(self.wordle_solver.filtered_words_by_length,
                                                                           self.initial_letter_position_freq_dict,
                                                                           self.initial_letter_freq_dict)
        self.assertEqual('SORES', best_freq_score_word)

    def test_solver_parse_response_and_filter_all_wrong(self):
        self.assertEqual(len(self.wordle_solver.parse_response_and_filter(
            self.wordle_solver.filtered_words_by_length, 'OPERA', 'XXXXX')), 789)
        # Need to clean up state side effects
        self.wordle_solver = ws.WordleSolver(5, 6)

    def test_solver_parse_response_and_filter_all_right(self):
        self.assertEqual(len(self.wordle_solver.parse_response_and_filter(
            self.wordle_solver.filtered_words_by_length, 'OPERA', 'OOOOO')), 1)
        self.assertEqual(self.wordle_solver.parse_response_and_filter(
            self.wordle_solver.filtered_words_by_length, 'OPERA', 'OOOOO').pop(), 'OPERA')
        # Need to clean up state side effects
        self.wordle_solver = ws.WordleSolver(5, 6)

    def test_solver_parse_response_and_filter_some_wrong(self):
        self.assertEqual(len(self.wordle_solver.parse_response_and_filter(
            self.wordle_solver.filtered_words_by_length, 'OPERA', 'OOOXX')), 1)
        # Need to clean up state side effects
        self.wordle_solver = ws.WordleSolver(5, 6)

    def test_solver_parse_response_and_filter_some_misplaced(self):
        filtered_words = self.wordle_solver.parse_response_and_filter(
            self.wordle_solver.filtered_words_by_length, 'OPERA', 'OOOXX')
        self.assertEqual(1, len(filtered_words))
        self.assertEqual('OPENS', filtered_words.pop())
        # Need to clean up state side effects
        self.wordle_solver = ws.WordleSolver(5, 6)
        filtered_words = self.wordle_solver.parse_response_and_filter(
            self.wordle_solver.filtered_words_by_length, 'OPERA', 'OOO??')
        self.assertEqual(0, len(filtered_words))
        # Need to clean up state side effects
        self.wordle_solver = ws.WordleSolver(5, 6)

    def test_solver_parse_response_and_filter_some_misplaced_dupes(self):
        filtered_words = self.wordle_solver.parse_response_and_filter(
            self.wordle_solver.filtered_words_by_length, 'DIGIT', 'XOOXO')
        self.assertEqual(13, len(filtered_words))
        self.assertTrue('LIGHT' in filtered_words)
        # Need to clean up state side effects
        self.wordle_solver = ws.WordleSolver(5, 6)
        filtered_words = self.wordle_solver.parse_response_and_filter(
            self.wordle_solver.filtered_words_by_length, 'SALES', '?XX?X')
        self.assertEqual(348, len(filtered_words))
        self.assertTrue('THOSE' in filtered_words)
        # Need to clean up state side effects
        self.wordle_solver = ws.WordleSolver(5, 6)

    def test_solver_parse_response_and_filter_some_misplaced_dupes_2(self):
        filtered_words = self.wordle_solver.parse_response_and_filter(
            self.wordle_solver.filtered_words_by_length, 'HILLY', '?O?XX')
        self.assertEqual(6, len(filtered_words))
        self.assertTrue('LIGHT' in filtered_words)
        # Need to clean up state side effects
        self.wordle_solver = ws.WordleSolver(5, 6)
