import unittest
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
            self.assertRaises(ValueError, self.wordle.make_attempt("four"))
