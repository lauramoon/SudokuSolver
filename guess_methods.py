import copy
from basic_methods import basic_solve_attempt
from advanced_methods import use_advanced_methods


def guess_recursive(p, start_index):
    """
    Guess value in first unknown box, if that doesn't solve the puzzle or find an error,
    recursively guess in the next box, and then the next, until solutions or errors found
    Found to be much faster than simply guessing each single possible value individually first
    :param p: the puzzle
    :param start_index: puzzle box index to start at (one more than last guess)
    """
    for i in range(start_index, 81):
        # Go on to next box if this box's value is known
        if p.box_map[i].value != 0:
            continue

        # Reset local_progress
        local_progress = False

        # list of possible values in the box
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
                local_progress = True

            # If the possible value gives valid solution, update valid completion list
            elif test_puzzle.solved:
                p.update_valid_completion(test_puzzle.solution)

            # If nothing interesting happened, guess in the next empty box
            else:
                guess_recursive(test_puzzle, i+1)
                # remove this guess from parent puzzle if no solution
                if test_puzzle.no_solution:
                    p.box_map[i].tally.discard(possible)
                    local_progress = True
                # update multiple solution error if found
                if test_puzzle.multiple_solution:
                    p.multiple_solution = True
                    p.error_description = test_puzzle.error_description
                    for completion in test_puzzle.valid_completion_list:
                        p.update_valid_completion(completion)
                    break
                # add valid completion if found
                if test_puzzle.solved:
                    p.update_valid_completion(test_puzzle.solution)

            # no need to test more possibilities in this box if multiple solutions found
            if p.multiple_solution:
                break

            if len(p.valid_completion_list) >= 2:
                p.multiple_solution = True
                p.error_description = f"Multiple values possible in box {i}"
                break

        # Check if more than one valid solution is found for the first time for this box
        if p.multiple_solution and p.error_description == "":
            p.error_description = f"Multiple values possible in box {i}"

        # update method log to track guessing
        p.method_log.append([f'Recursive guess box {i}', local_progress])

        # No need to go to next box if multiple solutions
        if p.multiple_solution:
            break

        # If something changed, see if puzzle can be solved or if error identified
        if local_progress:
            basic_solve_attempt(p)
            # if so, break
            if p.solved or p.no_solution:
                break
