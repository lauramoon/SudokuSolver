import unittest
from puzzle import Puzzle
from solver import solve_puzzle


class PuzzleCreationTests(unittest.TestCase):
    def setUp(self):
        self.p = Puzzle("Puzzle Name",
                        '286000004530208100000030082000400610002315800054006000640070000005904068300000479')

    def test_puzzle_name(self):
        self.assertEqual(self.p.name, "Puzzle Name")

    def test_puzzle_puzzle_string(self):
        self.assertEqual(self.p.puzzle_string,
                         "286000004530208100000030082000400610002315800054006000640070000005904068300000479")

    def test_puzzle_solution(self):
        self.assertEqual(self.p.solution, '')

    def test_puzzle_valid_completion_list(self):
        self.assertEqual(self.p.valid_completion_list, [])

    def test_puzzle_solved(self):
        self.assertFalse(self.p.solved)

    def test_puzzle_no_solution(self):
        self.assertFalse(self.p.no_solution)

    def test_puzzle_multiple_solution(self):
        self.assertFalse(self.p.multiple_solution)

    def test_puzzle_error_description(self):
        self.assertEqual(self.p.error_description, '')

    def test_puzzle_method_log(self):
        self.assertEqual(self.p.method_log, [])

    def test_axes(self):
        self.assertEqual(self.p.axis_map[0].dimension, 0)
        self.assertEqual(self.p.axis_map[0].index, 0)
        self.assertEqual(self.p.axis_map[0].box_set, {0, 1, 2, 3, 4, 5, 6, 7, 8})
        self.assertEqual(self.p.axis_map[0].unknown, {1, 3, 5, 7, 9})
        self.assertEqual(self.p.axis_map[11].dimension, 1)
        self.assertEqual(self.p.axis_map[11].index, 2)
        self.assertEqual(self.p.axis_map[11].box_set, {2, 11, 20, 29, 38, 47, 56, 65, 74})
        self.assertEqual(self.p.axis_map[11].unknown, {1, 3, 7, 8, 9})
        self.assertEqual(self.p.axis_map[23].dimension, 2)
        self.assertEqual(self.p.axis_map[23].index, 5)
        self.assertEqual(self.p.axis_map[23].box_set, {33, 34, 35, 42, 43, 44, 51, 52, 53})
        self.assertEqual(self.p.axis_map[23].unknown, {2, 3, 4, 5, 7, 9})

    def test_box_0(self):
        self.assertEqual(self.p.box_map[0].ID, 0)
        self.assertEqual(self.p.box_map[0].row, 0)
        self.assertEqual(self.p.box_map[0].col, 0)
        self.assertEqual(self.p.box_map[0].sqr, 0)
        self.assertEqual(self.p.box_map[0].coord, [0, 0, 0])
        self.assertEqual(self.p.box_map[0].value, 2)
        self.assertTrue(self.p.box_map[0].given)
        self.assertEqual(self.p.box_map[0].tally, {2})

    def test_box_13(self):
        self.assertEqual(self.p.box_map[13].ID, 13)
        self.assertEqual(self.p.box_map[13].row, 1)
        self.assertEqual(self.p.box_map[13].col, 4)
        self.assertEqual(self.p.box_map[13].sqr, 1)
        self.assertEqual(self.p.box_map[13].coord, [1, 4, 1])
        self.assertEqual(self.p.box_map[13].value, 0)
        self.assertFalse(self.p.box_map[13].given)
        self.assertEqual(self.p.box_map[13].tally, {4, 6, 9})


class PuzzleSolvedTests(unittest.TestCase):
    def setUp(self):
        self.p = Puzzle("Puzzle Name",
                        '286000004530208100000030082000400610002315800054006000640070000005904068300000479')
        solve_puzzle(self.p)

    def test_puzzle_name(self):
        self.assertEqual(self.p.name, "Puzzle Name")

    def test_puzzle_puzzle_string(self):
        self.assertEqual(self.p.puzzle_string,
                         "286000004530208100000030082000400610002315800054006000640070000005904068300000479")

    def test_puzzle_solution(self):
        self.assertEqual(self.p.solution,
                         "286159734537248196491637582873492615962315847154786923649873251715924368328561479")

    def test_puzzle_valid_completion_list(self):
        self.assertEqual(self.p.valid_completion_list, [])

    def test_puzzle_solved(self):
        self.assertTrue(self.p.solved)

    def test_puzzle_no_solution(self):
        self.assertFalse(self.p.no_solution)

    def test_puzzle_multiple_solution(self):
        self.assertFalse(self.p.multiple_solution)

    def test_puzzle_error_description(self):
        self.assertEqual(self.p.error_description, '')

    def test_puzzle_method_log(self):
        self.assertEqual(self.p.method_log[0][0], 'only place')
        self.assertTrue(self.p.method_log[0][1])
        self.assertEqual(self.p.method_log[1][0], 'lone tally')
        self.assertTrue(self.p.method_log[1][1])
        self.assertEqual(len(self.p.method_log), 2)


class PuzzleMultipleSolutionTests(unittest.TestCase):
    def setUp(self):
        self.p = Puzzle("Puzzle Name",
                        '000801000000000430500000000000070800000000100020030000600000075003400000000200600')
        solve_puzzle(self.p)

    def test_puzzle_name(self):
        self.assertEqual(self.p.name, "Puzzle Name")

    def test_puzzle_puzzle_string(self):
        self.assertEqual(self.p.puzzle_string,
                         "000801000000000430500000000000070800000000100020030000600000075003400000000200600")

    def test_puzzle_solution(self):
        self.assertEqual(self.p.solution, "")

    def test_puzzle_valid_completion_list(self):
        self.assertEqual(len(self.p.valid_completion_list), 2)

    def test_puzzle_solved(self):
        self.assertFalse(self.p.solved)

    def test_puzzle_no_solution(self):
        self.assertFalse(self.p.no_solution)

    def test_puzzle_multiple_solution(self):
        self.assertTrue(self.p.multiple_solution)

    def test_puzzle_error_description(self):
        self.assertEqual(self.p.error_description, 'Multiple values possible in box 32')


if __name__ == '__main__':
    unittest.main()
