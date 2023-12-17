from functions import *

# Functions

def fill_puzzle(puzzle):
    """
    Fill the puzzle with valid values recursively.

    Args:
        puzzle (list): The puzzle grid.

    Returns:
        bool: True if the puzzle is filled successfully, False otherwise.
    """
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


def generate_puzzle(difficulty=1):
    """
    Generate a Sudoku puzzle by filling the puzzle grid and removing values.

    Args:
        puzzle (list): The puzzle grid.
        difficulty (int, optional): The difficulty level of the puzzle. Defaults to 1.
    """
    puzzle = init_puzzle()

    fill_puzzle(puzzle)
    random.seed()
    attempt = difficulty

    while attempt > 0:
        index = random.randint(0, PUZZLE_SIZE * PUZZLE_SIZE - 1)

        while puzzle[index] == EMPTY_VALUE:
            index = random.randint(0, PUZZLE_SIZE * PUZZLE_SIZE - 1)

        backup_value = puzzle[index]
        puzzle[index] = EMPTY_VALUE
        global numberOfSolution
        numberOfSolution = 0 
        solve_sudoku(puzzle)
        if numberOfSolution != 1:
            puzzle[index] = backup_value
            attempt -= 1

    return puzzle


def solve_sudoku(puzzle):
    """
    Solve the Sudoku puzzle recursively.

    Args:
        puzzle (list): The puzzle grid.

    Returns:
        bool: True if the puzzle is solved successfully, False otherwise.
    """
    global numberOfSolution  # Use the global keyword to access the global variable
    index = find_empty_cell(puzzle)
    if index is None:
        # Puzzle is solved
        numberOfSolution += 1
        return True

    for value in values:
        if is_valid(puzzle, value, index)[0]:
            puzzle[index] = value
            if solve_sudoku(puzzle):
                break

    puzzle[index] = EMPTY_VALUE
    return False


# Example usage:
# Define the puzzle as a 9x9 grid

# puzzle = generate_puzzle(difficulty=1)

# print_puzzle(puzzle)