# SudokuSolver

This python program solves sudoku problems. 

## How To Use It

Download the folder and run main.py with python 3.6 or later (I think there's an f string or two in there somewhere.)

Puzzles must be entered as 81-digit strings, no spaces, with blank cells represented by '0'. The first nine digits are the first row, the next nine the second row, etc.

A single puzzle may be entered at the command line, or a text file may be placed in the 'puzzles' folder.

If using a text file, each line represents a single puzzle. Each line must contain two strings separated by a comma. The first string is the unsolved puzzle, as 81 digits, no spaces. The second string is either the solution as an 81-digit string or '0' if no solution is provided.

If a solution is provided, the program checks it against hte solution it finds. If no solution is provided, the program prints a representation of the solved puzzle.

## Future Work

Currently, the solver assumes the puzzle provided has exacty one valid solution. It will detect some errors, but may provide one of several solutions if the puzzle entered has more than one solution. Future work will improve the solver to identify if the puzzle entered has 0, 1, or more than one solution.

The methods used were created without any research on sudoku solving methods. Some difficult puzzles use guessing to solve. Future work includes researching whether additional non-guessing methods exist to solve the most difficult problems.
