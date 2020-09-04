from puzzle import Puzzle
from solver import solve_puzzle
import csv
import os


def get_puzzles_from_file():
    """
    Get the puzzles out of a file selected by the user
    :return: tuple consisting of
    - the filename selected and
    - list of puzzles, each puzzle a two-item list of (0) the 81-digit string representing
     the blank puzzle and (1) either the 81-digit solution or "0"
    """
    puzzle_files = os.listdir("puzzles")
    count = 1
    choices = []

    print("Enter the number for the file containing the puzzles to solve:")

    for file in puzzle_files:
        print(count, " - ", file)
        choices.append(str(count))
        count += 1

    selection = input()

    while selection not in choices:

        print("Please enter a number from the file list")
        selection = input()

    file_name = puzzle_files[int(selection)-1]

    # Read file to get puzzles and solutions
    path = "puzzles\\" + file_name
    file = open(path, newline='')
    reader = csv.reader(file)
    data = []
    count = 0

    # Read through the rows in the file
    for row in reader:
        count += 1
        # ignore rows without two elements
        if len(row) != 2:
            continue
        puzzle_string = row[0].strip()
        if len(puzzle_string) != 81 and puzzle_string.isdigit() is False:
            print(f"Error loading puzzle: puzzle string in row {row}is not 81 digits")
            continue
        solution_string = row[1].strip()
        if len(solution_string) != 81 and solution_string != "0" and solution_string.isdigit() is False:
            print("Error loading puzzle: solution string in row", row, "is not 81 digits or 0")
            continue

        data.append([puzzle_string, solution_string])

    return file_name, data


def puzzle_string_input():
    """
    Gets a valid puzzle string from the user and returns the name "puzzle"
    along with the puzzle data
    :return: tuple of puzzle name "puzzle" and the puzzle data - a single-item list of a list
    of the puzzle string and '0' (indicating no solution provided)
    """
    print("Please enter an 81-digit string representing your puzzle")
    puzzle_string = input()

    while len(puzzle_string) != 81 or puzzle_string.isdigit() is False:
        puzzle_string = input("Please enter 81 digits in a single line, no spaces or letters:")

    return "puzzle", [[puzzle_string, "0"]]


def puzzle_selection():
    """
    Has user select to either enter puzzle as a string at the console or
    to pick a file from the puzzle folder
    :return: the result of the function for the input method selected
    """
    print("How would you like to enter the sudoku puzzle?")
    print("1 - Enter 81 digit string representing the puzzle")
    print("2 - Select file containing puzzle(s) in puzzle folder")
    method = input()

    # validate selection, ask again until selection valid
    while method not in ["1", "2"]:
        method = input("Please enter 1 or 2: ")

    # get puzzle string if selected
    if method == "1":
        return puzzle_string_input()
    # get data from file if selected
    else:
        return get_puzzles_from_file()


def main():
    """
    runs through puzzles provided and prints out results
    """
    # get file name (to name puzzles) and the list of puzzles
    file_name, puzzle_list = puzzle_selection()

    # for each puzzle in the list
    for num in range(0, len(puzzle_list)):
        # create the puzzle
        current_puzzle = Puzzle(file_name + "-" + str(num+1), puzzle_list[num][0])
        # print info
        print("Puzzle", current_puzzle.name, "loaded")
        print("Unknown boxes:", current_puzzle.num_unknown_boxes())

        # if no solution given, print depiction of puzzle
        if puzzle_list[num][1] == "0":
            current_puzzle.print_pic()

        # try to solve puzzle
        solve_puzzle(current_puzzle)

        # if solution found
        if current_puzzle.solved:
            # check if a solution was provided
            if puzzle_list[num][1] != "0":
                # if solution provided, check if solution found matches
                if current_puzzle.solution == puzzle_list[num][1]:
                    print("PASS: Solution matches given solution")
                else:
                    print("FAIL: Solution found does not match solution given")
                    print("Solution found: " + current_puzzle.solution)
                    print("Solution given: " + puzzle_list[num][1])
            # if no solution given, show solution found
            else:
                print("Solution found:")
                current_puzzle.print_pic()

        # if no solution found:
        else:
            print("Unable to solve puzzle")
            if current_puzzle.error_found:
                print("Contradiction found while attempting to solve")
                print("Puzzle may not be valid")
            else:
                print("Progress on puzzle")
                current_puzzle.print_pic()


main()
