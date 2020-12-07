from basic_methods import basic_solve_attempt
from advanced_methods import use_advanced_methods
from guess_methods import guess


def solve_puzzle(p):
    """
    Try to solve the puzzle with the various methods defined above. Loops until either
    a solution or an error is found.
    :param p: the puzzle
    """
    # use the two standard methods to get as far as possible
    basic_solve_attempt(p)

    # if solution or error found, nothing more to do
    if p.solved or p.no_solution:
        return

    while p.solved is False:
        # track number of unknown boxes
        blanks = p.num_unknown_boxes()
        # try the advanced methods
        use_advanced_methods(p)

        # check if puzzle solved or no progress
        if p.solved or blanks == p.num_unknown_boxes():
            break

    # if puzzle not yet solved, guess
    if p.solved is False:
        guess(p)
