import unittest
from unittest.mock import Mock
import wordle_solver

class TestWordleSolverMethods(unittest.TestCase):
    def setUp(self) -> None:
        self.wordle = wordle_solver.Wordle(5, 6)

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