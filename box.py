class Box:
    """
    Each of the 81 cells in a standard sudoku problem is a Box. They are numbered 0 to 80
    from top left across the first row, then each following row across to bottom right.
    Each is part of a row, column, and square - three axes (see Axis class).
    A tally set of possible values contains the values currently considered possibilities.
    """

    def __init__(self, ID):
        # number from 0 to 80, 0 in top left, across each row, then each row top to bottom
        self.ID = ID
        # row num, top to bottom
        self.row = ID // 9
        # column number, left to right
        self.col = ID % 9
        # Sqr is number from 0 to 8 representing the large square top right across, then middle across, etc
        self.sqr = (self.row // 3) * 3 + self.col // 3
        # list of coordinates (row, column, square)
        self.coord = [self.row, self.col, self.sqr]
        # known value of box, 0 if unknown
        self.value = 0
        # set of nine possible values for the box
        self.tally = {1, 2, 3, 4, 5, 6, 7, 8, 9}
        # True if value given initially in puzzle
        self.given = False

    def set_value(self, x):
        # Set value
        self.value = x
        # update tally to only include set value
        self.tally = {x}
