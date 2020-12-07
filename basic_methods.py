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

        # Only check boxes with unknown value
        if box.value == 0:
            # if only one item in tally set, it's the value for the box
            if len(box.tally) == 1:
                # get the only value in the tally set
                value = max(box.tally)
                # and update the puzzle
                p.update_new_known(key, value)
                progress = True
            # if no values left in tally, the puzzle has an error
            if len(box.tally) == 0:
                p.no_solution = True
                p.error_description = f'No possible values for box {key}'

    p.method_log.append(["lone tally", progress])

    if p.num_unknown_boxes() == 0:
        p.solved = True
        p.set_solution_string()


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
            # the value is found in no tally sets, there's an error in the puzzle
            if count == 0:
                p.no_solution = True
                p.error_description = f'No place for {value} in axis {key}'

    p.method_log.append(["only place", progress])
    if p.num_unknown_boxes() == 0:
        p.solved = True
        p.set_solution_string()


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
        if p.solved or p.no_solution:
            break

        # second basic method
        lone_tally_check(p)
        if p.solved or p.no_solution:
            break

        # If there's no progress, end attempt
        if p.num_unknown_boxes() == blanks:
            break
