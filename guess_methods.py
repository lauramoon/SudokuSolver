import copy
from basic_methods import basic_solve_attempt
from advanced_methods import use_advanced_methods


def guess_tester(p):
    """
    Guesses each possible tally with no other changes to puzzle.
    Removes a possible value if it produces an error when tried,
    and identifies if multiple valid solutions are possible.
    """
    # print("Running guess tester")
    progress = False
    for i in range(81):
        # Go on to next box if this box's value is known
        if p.box_map[i].value != 0:
            continue

        # the possible values in the box
        possibles = sorted(p.box_map[i].tally)
        # print(f'Testing {possibles} in box {i}')

        for possible in possibles:
            # create deep copy of puzzle; no changes to original while guessing
            test_puzzle = copy.deepcopy(p)
            # try the possible value in test puzzle
            test_puzzle.update_new_known(i, possible)

            # run the basic solve attempt on the puzzle with the guessed value
            basic_solve_attempt(test_puzzle)
            # and then the advanced methods
            use_advanced_methods(test_puzzle)

            # if the possible value leads to a no-solution error, it cannot be correct
            if test_puzzle.no_solution:
                # remove value from box tally in real puzzle
                p.box_map[i].tally.discard(possible)
                progress = True

            # If the possible value gives valid solution, update valid completion list
            if test_puzzle.solved:
                test_puzzle.add_valid_completion()

        # If more than one valid solution is found, puzzle is invalid
        if len(test_puzzle.valid_completion_list) >= 2:
            print("More than one valid solution found; puzzle invalid")
            p.multiple_solution = True
            p.error_description = f"Multiple values possible in box {i}"
            break

        # See if puzzle can be solved
        basic_solve_attempt(p)

        if p.solved or p.no_solution:
            break

    p.method_log.append(["Basic Guess", progress])
    return progress


def guess(p):
    """
    If all algorithmic methods provide no more progress, guess.
    This method removes a possible value if it produces an error when tried,
    and identifies if multiple valid solutions are possible.
    :param p: the puzzle
    """
    progress = True
    while progress:
        progress = guess_tester(p)

    if progress is False:
        guess_recursive(p, 0)


def guess_recursive(p, start_index):
    """
    If simply trying each possible value alone doesn't work, use recursion
    :param p: the puzzle
    :param start_index: puzzle box index to start at (one more than last guess)
    """
    print(f"Guess level two, start index {start_index}")

    for i in range(start_index, 81):
        # Go on to next box if this box's value is known
        if p.box_map[i].value != 0:
            continue

        # the possible values in the box
        possibles = sorted(p.box_map[i].tally)

        for possible in possibles:
            # create deep copy of puzzle; no changes to parent while guessing
            test_puzzle = copy.deepcopy(p)
            # try the possible value in test puzzle
            test_puzzle.update_new_known(i, possible)

            # run the basic solve attempt on the puzzle with the guessed value
            basic_solve_attempt(test_puzzle)
            # and then the advanced methods
            if test_puzzle.solved is False and test_puzzle.no_solution is False:
                use_advanced_methods(test_puzzle)

            # if the possible value leads to a no-solution error, it cannot be correct
            if test_puzzle.no_solution:
                # remove value from box tally in parent puzzle
                p.box_map[i].tally.discard(possible)

            # If the possible value gives valid solution, update valid completion list
            elif test_puzzle.solved:
                test_puzzle.print_pic("current")
                test_puzzle.add_valid_completion()
                p.update_valid_completion(test_puzzle.solution)

            # If nothing interesting happened, guess in the next empty box
            else:
                guess_recursive(test_puzzle, i+1)
                # remove this guess from parent puzzle if no solution
                if test_puzzle.no_solution:
                    p.box_map[i].tally.discard(possible)
                # update multiple solution error if found
                if test_puzzle.multiple_solution:
                    p.multiple_solution = True
                    p.error_description = test_puzzle.error_description
                    for completion in test_puzzle.valid_completion_list:
                        p.update_valid_completion(completion)
                    break
                # add valid completion if found
                if test_puzzle.solved:
                    test_puzzle.add_valid_completion()
                    p.update_valid_completion(test_puzzle.solution)

            # no need to test more possibilities in this box if multiple solutions found
            if p.multiple_solution:
                break

        # Check if more than one valid solution is found for this box
        if p.multiple_solution and p.error_description == "":
            print("More than one valid solution found; puzzle is invalid")
            p.error_description = f"Multiple values possible in box {i}"

        # No need to go to next box if multiple solutions
        if p.multiple_solution:
            break

        # See if puzzle can be solved
        basic_solve_attempt(p)




