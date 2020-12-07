from box import Box
from axis import Axis


def print_row(x, v):
    """
    used in print_pic method
    """
    i = x*9
    print(f"||  {v[i]}  |  {v[1+i]}  |  {v[2+i]}  ||  " +
          f"{v[3+i]}  |  {v[4+i]}  |  {v[5+i]}  ||  " +
          f"{v[6+i]}  |  {v[7+i]}  |  {v[8+i]}  ||  ")


class Puzzle:

    def __init__(self, name, puzzle_string):
        self.name = name
        # string of 81 digits representing the original puzzle
        self.puzzle_string = puzzle_string
        # string of 81 digits representing valid, unique solution
        self.solution = ""
        # string representing valid but not necessarily unique solution
        self.valid_completion_list = []
        # dictionary of the 81 boxes in the puzzle
        self.box_map = {}
        # dictionary of the 27 row/column/square axes
        self.axis_map = {}
        self.solved = False
        self.no_solution = False
        self.multiple_solution = False
        self.error_description = ""
        # List of functions applied to solve puzzle and whether progress made
        self.method_log = []

        # initialize axis map
        for i in range(0, 27):
            self.axis_map[i] = Axis(i)

        # initialize box map
        for i in range(0, 81):
            self.box_map[i] = Box(i)

        # put the known box values into the box map
        for i in range(0, 81):
            value = int(puzzle_string[i])
            if value != 0:
                self.update_new_known(i, value)
                self.box_map[i].given = True

    def get_axis(self, dimension, index):
        """
        returns the 9 box indices for a particular row, column, or box
        :param dimension: 0, 1, or 2 for row, column, or square
        :param index: which of the nine axes in the dimension
        :return: list of nine box indices
        """
        ID = 9 * dimension + index
        axis_box_set = self.axis_map[ID].box_set
        return axis_box_set

    def update_tallies(self, ID):
        """
        when a value is found, this function removes the value from the sets of possibilities
        (the tally) for all the other boxes in the same row, column, and square
        :param ID: box with known value
        """
        # value in box
        v = self.box_map[ID].value

        # Ensures tallies are updated only if value in box is known
        if v == 0:
            print("box value not set, can't update tallies")
            return

        # Loop through the 3 axes the box is in
        for i in range(0, 3):
            index = self.box_map[ID].coord[i]
            # Get list of boxes in axis
            axis = self.get_axis(i, index)

            # Loop through 8 boxes in axis other than the one updated
            for j in axis.difference({ID}):
                # Remove value from tally set
                self.box_map[j].tally.discard(v)

    def update_axis_unknowns(self, ID):
        """
        Update sets of the values not yet known for the three axes of a given box
        :param ID: box with known value
        :return:
        """
        # value in box
        v = self.box_map[ID].value

        # Ensures axis unknowns are only updated if value in box is known
        if v == 0:
            print("box value not set, can't update axis")
            return

        # Loop through the three dimensions
        for i in range(0, 3):
            # get the axis the box is in
            axis = i*9 + self.box_map[ID].coord[i]
            # remove the value from the axis unknowns
            self.axis_map[axis].unknown.discard(v)

    def update_new_known(self, boxID, value):
        """
        Updates box value, tallies, and unknowns when box value discovered
        :param boxID: ID of box whose value has been identified
        :param value: value in box
        """
        self.box_map[boxID].set_value(value)
        self.update_tallies(boxID)
        self.update_axis_unknowns(boxID)
    
    def num_unknown_boxes(self):
        count = 0
        for i in range(0, 81):
            if self.box_map[i].value == 0:
                count += 1
        return count
        
    def print_initial_string(self):
        s = str()
        for i in range(0, 81):
            if self.box_map[i].given:
                s += str(self.box_map[i].value)
            else:
                s += str(0)
        print("Initial string: ", s)

    def print_current_string(self):
        s = str()
        for i in range(0, 81):
            s += str(self.box_map[i].value)
        print("Current string: ", s)

    def print_solution_string(self):
        s = self.solution
        print("Final string: ", s)

    def set_solution_string(self):
        if self.num_unknown_boxes() == 0:
            s = str()
            for i in range(0, 81):
                s += str(self.box_map[i].value)
            self.solution = s

        else:
            print("Puzzle not yet solved; no solution string")

    def add_valid_completion(self):
        if self.num_unknown_boxes() == 0:
            s = str()
            for i in range(0, 81):
                s += str(self.box_map[i].value)
            if s not in self.valid_completion_list:
                self.valid_completion_list.append(s)
            if len(self.valid_completion_list) >= 2:
                self.multiple_solution = True

        else:
            print("Puzzle not yet solved; no solution string")

    def update_valid_completion(self, valid_string):
        if valid_string not in self.valid_completion_list:
            self.valid_completion_list.append(valid_string)
            if len(self.valid_completion_list) >= 2:
                self.multiple_solution = True

    def print_pic(self, version):
        # replace zeros with blanks for display of puzzle
        print_list = []
        for i in range(81):

            if version == "blank":
                box_value = self.puzzle_string[i]
            elif version == "solution":
                box_value = self.solution[i]
            elif version == "completion0":
                box_value = self.valid_completion_list[0][i]
            elif version == "completion1":
                box_value = self.valid_completion_list[1][i]
            else:
                box_value = str(self.box_map[i].value)

            if box_value == 0:
                print_list.append(" ")
            else:
                print_list.append(box_value)

        # define rows that don't depend on puzzle values
        # width in characters
        w = 59
        # thick and thin horizontal lines, with verticals where appropriate
        thick_outer = "="*w
        thick_inner = "||" + ((("="*5) + "|")*2 + ("="*5) + "||")*3
        thin = "||" + ((("-"*5) + "|")*2 + ("-"*5) + "||")*3

        # print the top horizontal, then loop three times
        print(thick_outer)
        for i in range(0, 3):
            j = i*3
            # print(spaces)
            print_row(j, print_list)
            # print(spaces)
            print(thin)
            # print(spaces)
            print_row(j+1, print_list)
            # print(spaces)
            print(thin)
            # print(spaces)
            print_row(j+2, print_list)
            # print(spaces)
            if i == 2:
                print(thick_outer)
            else:
                print(thick_inner)
