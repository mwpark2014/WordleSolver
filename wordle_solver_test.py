import unittest
from unittest.mock import Mock
import wordle_solver

class TestWordleSolverMethods(unittest.TestCase):
    def setUp(self) -> None:
        self.wordle = wordle_solver.Wordle(5, 6)
        self.wordle_solver = wordle_solver.WordleSolver(5, 6)

    def test_make_attempt(self):
        self.wordle.make_attempt("point")
        self.wordle.make_attempt("PRICK")
        self.assertEqual(self.wordle.attempts[0], 'POINT')
        self.assertEqual(self.wordle.attempts[1], 'PRICK')
        self.assertEqual(len(self.wordle.attempts), 2)
        with self.assertRaises(ValueError):
            self.wordle.make_attempt("four")

    def test_play_wordle_alone_without_answer(self):
        wordle = wordle_solver.Wordle(5, 6)
        wordle.make_attempt_with_input = Mock(side_effect = lambda: wordle.make_attempt('POINT'))
        wordle.get_user_attempt_response = Mock(side_effect = lambda: wordle.get_attempt_response('OOOOO'))
        self.assertEqual(wordle.play_wordle_alone_without_answer(), True)

    def test_play_wordle_alone_with_answer(self):
        wordle = wordle_solver.Wordle(5, 6)
        wordle.make_attempt_with_input = Mock(side_effect = lambda: wordle.make_attempt('POINT'))
        self.assertEqual(wordle.play_wordle_alone_with_answer('POINT'), True)
        wordle = wordle_solver.Wordle(5, 6)
        wordle.make_attempt_with_input = Mock(side_effect=lambda: wordle.make_attempt('PINTS'))
        self.assertEqual(wordle.play_wordle_alone_with_answer('POINT'), False)
        wordle = wordle_solver.Wordle(5, 6)
        wordle.make_attempt_with_input = Mock(side_effect=lambda: wordle.make_attempt('POINT'))
        with self.assertRaises(ValueError):
            wordle.play_wordle_alone_with_answer(None)

    def test_wordle_solver_create_freq_dict(self):
        freq_dict = self.wordle_solver.create_freq_dict()
        self.assertEqual(len(freq_dict), 129)
        self.assertEqual(freq_dict['e2'], 580)
        self.assertEqual(freq_dict['s4'], 2785)
        with self.assertRaises(KeyError):
            test_freq = freq_dict['s5']

    def test_wordle_solver_create_word_freq_score_heap(self):
        freq_dict = self.wordle_solver.create_freq_dict()
        freq_score_heap = self.wordle_solver.create_word_freq_score_heap(freq_dict)
        self.assertEqual(len(freq_score_heap), 8938)
        self.assertEqual(freq_score_heap[0], (-7824, 'sores'))
        self.assertEqual(freq_score_heap[1], (-7757, 'sales'))

    def test_wordle_solver_get_best_freq_score_word(self):
        freq_dict = self.wordle_solver.create_freq_dict()
        best_freq_score_word = self.wordle_solver.get_best_freq_score_word(freq_dict)
        self.assertEqual(best_freq_score_word, 'sores')

    def test_wordle_solver_solve(self):
        self.assertTrue(self.wordle_solver.solve(self.wordle))
