import random
import time
import copy

PUZZLE_SIZE = 9
EMPTY_VALUE = 0
values = [1,2,3,4,5,6,7,8,9]
numberOfSolution = 1

def fill_puzzle(puzzle):
    global values
    index = find_empty_cell(puzzle)

    if index is None:
        return True

    random.shuffle(values)

    for value in values:
        if is_valid(puzzle, value, index)[0]:
            puzzle[index] = value
            if not has_empty_cell(puzzle) or fill_puzzle(puzzle):
                return True

    puzzle[index] = EMPTY_VALUE
    return False


def find_empty_cell(puzzle):
    for i in range(PUZZLE_SIZE * PUZZLE_SIZE):
        if puzzle[i] == EMPTY_VALUE:
            return i
    return None


def is_valid(puzzle, num, index):
    # Check row
    row_start = (index // 9) * 9
    for i in range(row_start, row_start + 9):
        if puzzle[i] == num and i != index:
            return False, i

    # Check column
    col_start = index % 9
    for i in range(col_start, 81, 9):
        if puzzle[i] == num and i != index:
            return False, i

    # Check 3x3 box
    box_start = (index // 27) * 27 + (index % 9) // 3 * 3
    for i in range(box_start, box_start + 3):
        for j in range(3):
            if puzzle[i + j * 9] == num and (i + j * 9) != index:
                return False, i

    return True, None


def has_empty_cell(puzzle):
    return EMPTY_VALUE in puzzle


def generate_puzzle(puzzle, difficulty=1):
    for i in range(PUZZLE_SIZE * PUZZLE_SIZE):
        puzzle[i] = EMPTY_VALUE

    fill_puzzle(puzzle)
    random.seed(time.time())
    attempt = difficulty

    while attempt > 0:
        index = random.randint(0, PUZZLE_SIZE * PUZZLE_SIZE - 1)

        while puzzle[index] == EMPTY_VALUE:
            index = random.randint(0, PUZZLE_SIZE * PUZZLE_SIZE - 1)

        backup_value = puzzle[index]
        puzzle[index] = EMPTY_VALUE
        temp = copy.deepcopy(puzzle)  # Make a deep copy of puzzle
        global numberOfSolution
        numberOfSolution = 0 
        solve_sudoku(temp)
        if numberOfSolution != 1:
            puzzle[index] = backup_value
            attempt -= 1

def solve_sudoku(puzzle):
    global numberOfSolution  # Use the global keyword to access the global variable
    index = find_empty_cell(puzzle)
    if index is None:
        # Puzzle is solved
        numberOfSolution += 1
        return True

    for value in range(1, PUZZLE_SIZE + 1):
        if is_valid(puzzle, value, index)[0]:
            puzzle[index] = value
            if solve_sudoku(puzzle):
                break

    puzzle[index] = EMPTY_VALUE
    return False


def print_puzzle(puzzle):
    for i in range(len(puzzle)//9):
        if i % 3 == 0 and i != 0:
            print("- - - - - - - - - - - -  ")

        for j in range(len(puzzle)//9):
            if j % 3 == 0 and j != 0:
                print(" | ", end="")

            if j == 8:
                print(puzzle[i * 9 + j])
            else:
                print(str(puzzle[i * 9 + j]) + " ", end="")



# Example usage:
# Define the puzzle as a 9x9 grid
puzzle = [0] * 81


generate_puzzle(puzzle, difficulty=1)

print_puzzle(puzzle)