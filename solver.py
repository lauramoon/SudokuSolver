import copy


def lone_tally_check(p):
    """
    standard evaluation method, checks each boxes tally set to see if there is only
    one possible value left for that box.
    :param p: the puzzle
    """
    # map = p.box_map
    progress = False
    
    # cycle through every box in the puzzle
    for key, box in p.box_map.items():

        # Only check boxes with unknown value and then see if only one item in tally set
        if box.value == 0 and len(box.tally) == 1:
            # get the only value in the tally set
            value = max(box.tally)
            # and update the puzzle
            p.update_new_known(key, value)
            progress = True

    p.method_log.append(["lone tally", progress])


def only_place_check(p):
    """
    standard evaluation method, checks each axis to see if any values are possible
    in only one box of the axis
    :param p: the puzzle
    """
    progress = False

    # Loop through all 27 axes
    for key, axis in p.axis_map.items():
        # If all values in axis are known, skip
        if len(axis.unknown) == 0:
            continue

        box_set = axis.box_set
        # need to copy because Unknown set can change
        unknowns = axis.unknown.copy()
            
        # loop through the values not yet known in the axis
        for value in unknowns:
            # how many tallies have the value as a possibility
            count = 0
            # box ID for last box where this value was a possibility
            latest = 0

            # loop through every box in axis
            for j in box_set:
                # if the value of the box is unknown and the tally set contains it
                if value in p.box_map[j].tally:
                    # increment the count and record the box ID
                    count += 1
                    latest = j
                # if find more than one instance, go on to the next value
                if count == 2:
                    break

            # if there's only one place for the value
            if count == 1:
                p.update_new_known(latest, value)
                progress = True

    p.method_log.append(["only place", progress])


def bare_tally_pair_check(p):
    """
    advanced method: looks for two boxes with exactly two identical possibilities
    in the same axis, removes those two possibilities from the other boxes in the axis
    :param p: the puzzle
    """
    progress = False

    # cycle through the 27 axes
    for key, axis in p.axis_map.items():

        # Impossible to get new info if 3 or fewer unknowns
        if len(axis.unknown) < 4:
            continue

        box_set = axis.box_set
        # copy of set of boxes in the axis
        box_set_copy = set(box_set.copy())
        # list of boxes with identical tally sets of size 2
        matches = []

        # cycle through boxes in axis
        for i in box_set:
            # remove self from the box_set
            box_set_copy = box_set_copy - {i}

            # if the tally set for box j is of size 2
            # and there are boxes left to compare with
            if len(p.box_map[i].tally) == 2 and len(box_set_copy) != 0:

                # Compare to remaining box tallies
                for j in box_set_copy:
                    # If tallies are identical
                    if p.box_map[i].tally == p.box_map[j].tally:
                        # Put the two box IDs and the tally set in match list
                        matches.append([i, j, p.box_map[j].tally])

        # if no matches found, skip to next axis
        if len(matches) == 0:
            continue

        # Cycle through matches
        for match in matches:
            # remove the boxes with the matching pair from the axis set
            others = box_set - {match[0], match[1]}
            two_set = match[2]

            # cycle through the other 7 boxes
            for j in others:
                # if one of the pair values is found in another tally
                if p.box_map[j].tally.isdisjoint(two_set) is False:
                    # Remove the set of those two values
                    p.box_map[j].tally = p.box_map[j].tally - two_set
                    progress = True
    
    p.method_log.append(["bare tally pair", progress])
        

def hidden_tally_pair_check(p):
    """
    advanced evaluation, looks at each axis to see if there are two values found in the
    tally sets of only two boxes, removes the other values from those box tally sets
    :param p: the puzzle
    """
    progress = False
    # Loop through the axes
    for key, axis in p.axis_map.items():
        box_set = axis.box_set
        unknowns = axis.unknown

        # Skip to next axis if three or fewer values are unknown
        if len(unknowns) < 4:
            continue

        # List of values found in exactly two tally sets with the boxes they're in
        pairs = []

        # Loop through each value not yet known in axis
        for value in unknowns:
            count = 0
            # list of tally sets where value is possible
            place = []
            # loop through each box in the axis
            for box in box_set:
                # check for value in tally set
                tally = p.box_map[box].tally
                if value in tally:
                    count += 1
                    place.append(box)

            # Add to list of possibles if value occurs twice
            if count == 2:
                # and if at least one tally set is longer than 2
                tally0 = p.box_map[place[0]].tally
                tally1 = p.box_map[place[1]].tally
                if len(tally0) > 2 or len(tally1) > 2:
                    # list containing value, first box, and second box
                    pairs.append([value, place[0], place[1]])

        # can't have a hidden pair without at least 2 possibilities
        if len(pairs) < 2:
            continue

        # Loop through all but last item in possibles
        for i in range(len(pairs) - 1):
            # Loop through all the items in possibles after current one
            for j in range(i+1, len(pairs)):
                # Compare lists of locations, if they match
                if pairs[i][1] == pairs[j][1] and pairs[i][2] == pairs[j][2]:
                    # identify the boxes and the values
                    box1 = pairs[i][1]
                    box2 = pairs[i][2]
                    value1 = pairs[i][0]
                    value2 = pairs[j][0]
                    # set tally sets for those boxes to have only those two values
                    p.box_map[box1].tally = {value1, value2}
                    p.box_map[box2].tally = {value1, value2}
                    progress = True

    p.method_log.append(["hidden tally pair", progress])


def intersection_check(p):
    """
    advanced method: checks 3-box intersection of a square and either row or column
    if possible value found ony in that intersection for one axis,
    it can't be anywhere else in the other axis
    :param p: the puzzle
    """
    progress = False

    # cycle through the 9 squares
    for i in range(0, 9):
        # set of boxes in the square
        square_boxes = p.axis_map[18+i].box_set

        # list of the 3 rows and 3 columns that intersect this square
        crosses = []
        for j in range(0, 3):
            # The three rows
            crosses.append(3*(i//3) + j)
            # The three columns
            crosses.append(9 + 3*(i % 3) + j)

        for j in crosses:
            # set of boxes in the row or column
            box_set = p.axis_map[j].box_set
            # Get the three box in common with the square and row/column
            intersect = square_boxes.intersection(box_set)

            # create set of values in tallies of boxes with unknown values
            big_set = set()
            # boxes with known values
            count = 0

            # loop through the three boxes in the intersection
            for k in intersect:
                if p.box_map[k].value != 0:
                    count += 1
                else:
                    big_set = big_set | p.box_map[k].tally

            # if two or three boxes have known values, this function can't provide progress
            if count > 1:
                continue

            # check if value in big_set is
            # (1) found somewhere in other six boxes of square OR row/column
            # but (2) nowhere in the other six boxes of the other.
            for k in big_set:
                # is the value somewhere in other six boxes of square
                in_square = False
                # is the value somewhere in other six boxes of row/column
                in_cross = False

                # check if k is found somewhere else in the square
                for m in (square_boxes - intersect):
                    if k in p.box_map[m].tally:
                        in_square = True
                        break

                # check if k somewhere else in the row/column
                for m in (box_set - intersect):
                    if k in p.box_map[m].tally:
                        in_cross = True
                        break
                
                # if k is elsewhere in square but not row/col
                if in_square and not in_cross:
                    # Then k must only be in the intersection and can be removed
                    # from the rest of the square
                    for m in (square_boxes - intersect):
                        p.box_map[m].tally.discard(k)
                        progress = True

                # and the opposite - k is elsewhere in row/col but not in square
                if not in_square and in_cross:
                    for m in (box_set - intersect):
                        progress = True
                        p.box_map[m].tally.discard(k)

    p.method_log.append(["intersection", progress])


def two_tally_guess(p):
    """
    If all other methods provide no more progress, guess.
    This method assumes that the puzzle has exactly one valid solution.
    :param p: the puzzle
    """
    # loop through all 81 boxes until solution found
    progress = False
    for i in range(81):
        # Go on to next box if this box does not have two values
        if len(p.box_map[i].tally) != 2:
            continue

        # the two possible values in the box
        value = sorted(p.box_map[i].tally)
        # create deep copy of puzzle; no changes to original while guessing
        test_puzzle = copy.deepcopy(p)

        # try the first value in test puzzle
        test_puzzle.update_new_known(i, value[0])
        # run the basic solve attempt on the puzzle with the guessed value
        basic_solve_attempt(test_puzzle)

        # if value[0] leads to an error, value[1] must be correct
        if test_puzzle.error_found:
            p.update_new_known(i, value[1])
            progress = True
            # don't break because we don't know if this value is enough to solve the puzzle

        # If value[0] gives valid solution, set the box to value[0]
        if test_puzzle.solved:
            p.update_new_known(i, value[0])
            progress = True
            # break, as standard methods will get solution
            break

        # reset puzzle copy
        test_puzzle = copy.deepcopy(p)
        # Try other value for box[i]
        test_puzzle.update_new_known(i, value[1])
        # see if it works or fails
        basic_solve_attempt(test_puzzle)

        # If value[1] leads to error
        if test_puzzle.error_found:
            # then value[0] must be in the box
            p.update_new_known(i, value[0])
            progress = True
            # No break because we know that testing this value earlier was inconclusive

        # if value[1] leads to valid solution
        if test_puzzle.solved:
            # put it in the real puzzle
            p.update_new_known(i, value[1])
            progress = True
            # No need to go further, puzzle will solve with standard methods
            break

    p.method_log.append(["Guess", progress])
        

def basic_solve_attempt(p):
    """
    run through the two basic solving methods until there's no more progress
    :param p: the puzzle
    """

    while p.num_unknown_boxes() != 0:
        # track how many unknowns there are at the beginning of the loop
        blanks = p.num_unknown_boxes()

        # first basic method
        only_place_check(p)
        # if no blanks left, done
        if p.num_unknown_boxes() == 0:
            p.solved = True
            break

        # second basic method
        lone_tally_check(p)

        # look for error - box with no possible values
        if p.tally_zero_error_check():
            p.error_found = True
            break

        # If there's no progress, end attempt
        if p.num_unknown_boxes() == blanks:
            break


def solve_puzzle(p):
    """
    Try to solve the puzzle with the various methods defined above. Loops until either
    a solution or an error is found.
    :param p: the puzzle
    """
    # Start with standard method, then try more advanced methods

    while p.solved is False:
        # use the two standard methods to get as far as possible
        basic_solve_attempt(p)

        # if solution found, set the solution string and break
        if p.solved:
            p.set_solution_string()
            break

        # if error found, break
        if p.error_found:
            print("Error in puzzle. Is it a valid puzzle?")
            break

        # try the more advanced algorithmic methods
        hidden_tally_pair_check(p)
        bare_tally_pair_check(p)
        intersection_check(p)

        # if the three advanced methods provided no progress, guess
        if p.method_log[-1][1] is False and p.method_log[-2][1] is False and p.method_log[-3][1] is False:
            two_tally_guess(p)
    
    if p.num_unknown_boxes() != 0:
        print("No further progress possible")
        print("Did you enter a valid puzzle?")
