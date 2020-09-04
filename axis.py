class Axis:
    """
    Each row, column, and 3x3 square is an Axis. Each of the 27 axes needs to contain exactly one
    of each possible value for the puzzle to be solved.
    """
    def __init__(self, ID):
        # 0 is row, 1 is column, 2 is square
        self.dimension = ID // 9
        # index is which of the 9 axes in the dimension this is
        self.index = ID % 9
        # ID's of the boxes in the axis
        self.box_set = set()
        # The values not yet known in the axis
        self.unknown = {1, 2, 3, 4, 5, 6, 7, 8, 9}

        # fill out the sets of the box ID's in the axis
        for i in range(0, 9):
            # if it's a row, add the ith box in row to the set
            if self.dimension == 0:
                self.box_set.add(self.index * 9 + i)
            # if it's a column, add the ith box in the column
            if self.dimension == 1:
                self.box_set.add(self.index + i * 9)
            # if it's a square, yes, this formula works
            if self.dimension == 2:
                self.box_set.add(9 * ((self.index // 3) * 3 + i // 3) + (self.index % 3) * 3 + i % 3)

