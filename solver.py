from basic_methods import basic_solve_attempt
from advanced_methods import use_advanced_methods
from guess_methods import guess_recursive
from puzzle import Puzzle


def solve_puzzle(puzzle_string, puzzle_name):
    """
    Try to solve the puzzle with the various methods in the methods scripts. First check that enough clues
    were provided for it to possibly be a valid puzzle. Then use the basic methods. If not solved,
    try the advanced methods, and finally guess if necessary.
    :param puzzle_string: the string representing the puzzle
    :param puzzle_name: the name for the puzzle
    :return: the puzzle analyzed
    """
    # create puzzle
    p = Puzzle(puzzle_name, puzzle_string)

    # Check for errors detected in initialization
    if p.no_solution:
        return p

    # First check that at least 17 clues were provided
    if p.num_unknown_boxes() >= 65:
        p.too_few_clues = True
        return p

    # use the two standard methods to get as far as possible
    basic_solve_attempt(p)

    # if solution found, set difficulty rating
    if p.solved:
        p.difficulty = 'Easy'

    # if solution or error found, nothing more to do
    if p.solved or p.no_solution:
        return p

    # Try advanced algorithmic methods
    while p.solved is False:
        # track number of unknown boxes
        blanks = p.num_unknown_boxes()
        # try the advanced methods
        use_advanced_methods(p)

        # check if puzzle solved or no progress
        if p.solved or blanks == p.num_unknown_boxes():
            break

    # if puzzle solved, set difficulty
    if p.solved:
        p.difficulty = "Medium"

    if p.solved or p.no_solution:
        return p

    # if not yet solved and no error found, guess
    guess_recursive(p, 0)

    # if guessing solved it, label Difficult
    if p.solved:
        p.difficulty = "Difficult"

    return p
