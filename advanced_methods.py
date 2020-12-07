from basic_methods import basic_solve_attempt


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
            for j in range(i + 1, len(pairs)):
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
        square_boxes = p.axis_map[18 + i].box_set

        # list of the 3 rows and 3 columns that intersect this square
        crosses = []
        for j in range(0, 3):
            # The three rows
            crosses.append(3 * (i // 3) + j)
            # The three columns
            crosses.append(9 + 3 * (i % 3) + j)

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


def use_advanced_methods(p):
    """
    Try to solve the puzzle with advanced methods
    :param p: the puzzle
    """
    method_list = [hidden_tally_pair_check, bare_tally_pair_check, intersection_check]
    for method in method_list:
        method(p)
        basic_solve_attempt(p)

        # if solution or error found, break
        if p.solved or p.no_solution:
            break
