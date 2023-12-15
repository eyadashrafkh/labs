# functions.py
import random
from tkinter import messagebox
import sys
import pygame

# Global Variables 

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
GRAY = (128,128,128)



# Functoins

def print_board(board):
    for i in range(len(board)//9):
        if i % 3 == 0 and i != 0:
            print("- - - - - - - - - - - -  ")

        for j in range(len(board)//9):
            if j % 3 == 0 and j != 0:
                print(" | ", end="")

            if j == 8:
                print(board[i * 9 + j])
            else:
                print(str(board[i * 9 + j]) + " ", end="")


def finish_game():
    messagebox.showinfo("Sudoku Solved", "Congratulations! You have solved the Sudoku puzzle!")
    choice = messagebox.askquestion("Quit or Continue", "Do you want to quit or continue?")
    if choice == "yes":
        messagebox.showinfo("Thank You", "Thank you for playing! Goodbye!")
        # Quit the game
        sys.exit()
    else:
        # Continue the game
        pass


def generate_random_board():
    board = [0] * 81

    # Fill the board with random numbers
    for i in range(81):
        num = random.choices([0, 1, 2, 3, 4, 5, 6, 7, 8, 9], weights=[1, 1, 1, 1, 1, 1, 1, 1, 1, 1])[0]
        if is_valid(board, num, i)[0]:# and is_solvable(board):
            board[i] = num
        else:
            board[i] = 0

    return board


def is_solvable(board):
    if solve_sudoku(board):
        return True
    else:
        return False


def solve_sudoku(board):
    empty = find_empty(board)
    if not empty:
        return True

    index = empty

    for num in range(1, 10):
        if is_valid(num, index, board)[0]:
            board[index] = num

            if is_solvable(board):
                return True

            board[index] = 0

    return False


def find_empty(board):
    for i in range(81):
        if board[i] == 0:
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


def redraw_window(win, board, time, strikes):
    win.fill((255,255,255))
    # Draw time
    fnt = pygame.font.SysFont("comicsans", 40)
    text = fnt.render("Time: " + format_time(time), 1, BLACK)
    win.blit(text, (540 - 220, 540))
    # Draw Strikes
    text = fnt.render("X " * strikes, 1, RED)
    win.blit(text, (20, 540))
    # Draw grid and board
    board.draw()


def format_time(secs):
    sec = secs % 60
    minute = secs // 60
    time = f"{minute:02d}:{sec:02d}"
    return time


# Board setup
board = [
    5, 3, 0, 0, 7, 0, 0, 0, 0,
    6, 0, 0, 1, 9, 5, 0, 0, 0,
    0, 9, 8, 0, 0, 0, 0, 6, 0,
    8, 0, 0, 0, 6, 0, 0, 0, 3,
    4, 0, 0, 8, 0, 3, 0, 0, 1,
    7, 0, 0, 0, 2, 0, 0, 0, 6,
    0, 6, 0, 0, 0, 0, 2, 8, 0,
    0, 0, 0, 4, 1, 9, 0, 0, 5,
    0, 0, 0, 0, 8, 0, 0, 7, 9,
]

board2 = generate_random_board()
print_board(board2)