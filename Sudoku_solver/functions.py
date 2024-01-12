# functions.py
from tkinter import messagebox
import sys
import random
import pygame

# Global Variables 

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
GRAY = (128,128,128)
LIGHT_BLUE = (100, 150, 255)  # Light blue color


# Defined values
PUZZLE_SIZE = 9
EMPTY_VALUE = 0
values = [1,2,3,4,5,6,7,8,9]
numberOfSolution = 1


def count_values(puzzle):
    """
    Counts the number of occurrences of each value in the puzzle.

    Args:
        puzzle (list): The Sudoku puzzle board.

    Returns:
        dict: A dictionary containing the count of each value.
    """
    value_count = {}
    for value in values:
        value_count[value] = puzzle.count(value)
    return value_count


def init_puzzle():
    return [EMPTY_VALUE] * 81


def print_puzzle(puzzle):
    """
    Prints the Sudoku puzzle board.

    Args:
        board (list): The Sudoku puzzle board.

    Returns:
        None
    """
    for i in range(PUZZLE_SIZE):
        if i % 3 == 0 and i != 0:
            print("- - - - - - - - - - - -  ")

        for j in range(PUZZLE_SIZE):
            if j % 3 == 0 and j != 0:
                print(" | ", end="")

            if j == 8:
                print(puzzle[i * PUZZLE_SIZE + j])
            else:
                print(str(puzzle[i * PUZZLE_SIZE + j]) + " ", end="")


def finish_game():
    """
    Displays a message box indicating that the Sudoku puzzle has been solved.
    Asks the user if they want to quit or continue the game.

    Returns:
        None
    """
    messagebox.showinfo("Sudoku Solved", "Congratulations! You have solved the Sudoku puzzle!")
    choice = messagebox.askquestion("Quit or Continue", "Do you want to quit or continue?")
    if choice == "yes":
        messagebox.showinfo("Thank You", "Thank you for playing! Goodbye!")
        # Quit the game
        sys.exit()
    else:
        # Continue the game
        pass


def is_solvable(puzzle):
    """
    Checks if the Sudoku puzzle board is solvable.

    Args:
        board (list): The Sudoku puzzle board.

    Returns:
        bool: True if the board is solvable, False otherwise.
    """
    if solve_sudoku(puzzle):
        return True
    else:
        return False


def solve_sudoku(puzzle):
    """
    Solves the Sudoku puzzle using backtracking algorithm.

    Args:
        board (list): The Sudoku puzzle board.

    Returns:
        bool: True if the board is solvable, False otherwise.
    """
    empty = find_empty_cell(puzzle)
    if not empty:
        return True

    index = empty

    for num in values:
        if is_valid(num, index, puzzle)[0]:
            puzzle[index] = num

            if is_solvable(puzzle):
                return True

            puzzle[index] = 0

    return False


def find_empty_cell(puzzle):
    """
    Finds the index of the first empty cell in the Sudoku puzzle board.

    Args:
        puzzle (list): The Sudoku puzzle board.

    Returns:
        int: The index of the first empty cell, or None if there are no empty cells.
    """
    for i in range(0, PUZZLE_SIZE * PUZZLE_SIZE):
        if puzzle[i] == EMPTY_VALUE:
            return i
    return None


def has_empty_cell(puzzle):
    """
    Checks if the Sudoku puzzle board has any empty cells.

    Args:
        puzzle (list): The Sudoku puzzle board.

    Returns:
        bool: True if there are empty cells, False otherwise.
    """
    return EMPTY_VALUE in puzzle


def is_valid(puzzle, num, index):
    """
    Checks if a number can be placed in a specific cell of the Sudoku puzzle board.

    Args:
        puzzle (list): The Sudoku puzzle board.
        num (int): The number to be placed.
        index (int): The index of the cell.

    Returns:
        tuple: A tuple containing a boolean value indicating if the number is valid and the index of the conflicting cell.
    """
    # Check 3x3 box
    box_start = (index // 27) * 27 + (index % 9) // 3 * 3
    for i in range(box_start, box_start + 3):
        for j in range(3):
            if puzzle[i + j * 9] == num and (i + j * 9) != index:
                return False, i+j*9
    
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

    return True, None


def redraw_window(win, puzzle, time, strikes):
    """
    Redraws the game window.

    Args:
        win (pygame.Surface): The game window surface.
        board (SudokuBoard): The Sudoku board object.
        time (int): The elapsed time in seconds.
        strikes (int): The number of strikes.

    Returns:
        None
    """
   
    # Draw time
    fnt = pygame.font.SysFont("comicsans", 40)
    text = fnt.render("Time: " + format_time(time), 1, BLACK)
    win.blit(text, (300, 540))
   
    # Draw Strikes
    fnt = pygame.font.SysFont("comicsans", 30)
    text = fnt.render("X " * strikes, 1, RED)
    win.blit(text, (10, 580))
    
    # # Draw numbers
    numbers_text = fnt.render(" ".join(str(i) if count_values(puzzle.get_puzzle())[i] < 9 else " " for i in range(1, 10)), 1, LIGHT_BLUE)
    win.blit(numbers_text, (10, 550))
    
    # Draw grid and board
    puzzle.draw()


def format_time(secs):
    """
    Formats the time in seconds to a string in the format "MM:SS".

    Args:
        secs (int): The time in seconds.

    Returns:
        str: The formatted time string.
    """
    sec = secs % 60
    minute = secs // 60
    time = f"{minute:02d}:{sec:02d}"
    return time

