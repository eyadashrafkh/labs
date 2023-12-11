import pygame
import sys

# Sudoku solver (backtracking algorithm)
def solve_sudoku(board):
    empty = find_empty(board)
    if not empty:
        return True

    row, col = empty

    for num in range(1, 10):
        if is_valid(board, num, (row, col)):
            board[row][col] = num

            if solve_sudoku(board):
                return True

            board[row][col] = 0

    return False

def find_empty(board):
    for i in range(9):
        for j in range(9):
            if board[i][j] == 0:
                return (i, j)
    return None

def is_valid(board, num, pos):
    # Check row
    if num in board[pos[0]]:
        return False

    # Check column
    if num in [board[i][pos[1]] for i in range(9)]:
        return False

    # Check 3x3 box
    box_row, box_col = pos[0] // 3 * 3, pos[1] // 3 * 3
    for i in range(box_row, box_row + 3):
        for j in range(box_col, box_col + 3):
            if board[i][j] == num:
                return False

    return True


def draw_board():
    screen.fill(WHITE)
    for i in range(1, 9):
        thickness = 4 if i % 3 == 0 else 1
        pygame.draw.line(screen, BLACK, (0, i * GRID_SIZE), (WIDTH, i * GRID_SIZE), thickness)        
        pygame.draw.line(screen, BLACK, (i * GRID_SIZE, 0), (i * GRID_SIZE, HEIGHT), thickness)

    for i in range(9):
        for j in range(9):
            if board[i][j] != 0:
                text = font.render(str(board[i][j]), True, BLACK)
                text_rect = text.get_rect(center=(j * GRID_SIZE + GRID_SIZE // 2, i * GRID_SIZE + GRID_SIZE // 2))
                screen.blit(text, text_rect)


# Pygame setup
pygame.init()

# Constants
WIDTH, HEIGHT = 600, 600
GRID_SIZE = WIDTH // 9

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (135, 206, 250)
GRAY = (200, 200, 200)

# Initialize the window
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Sudoku Solver")

# Fonts
font = pygame.font.Font(None, 36)

# Board setup
board = [
    [5, 3, 0, 0, 7, 0, 0, 0, 0],
    [6, 0, 0, 1, 9, 5, 0, 0, 0],
    [0, 9, 8, 0, 0, 0, 0, 6, 0],
    [8, 0, 0, 0, 6, 0, 0, 0, 3],
    [4, 0, 0, 8, 0, 3, 0, 0, 1],
    [7, 0, 0, 0, 2, 0, 0, 0, 6],
    [0, 6, 0, 0, 0, 0, 2, 8, 0],
    [0, 0, 0, 4, 1, 9, 0, 0, 5],
    [0, 0, 0, 0, 8, 0, 0, 7, 9],
]

# Main loop
running = True
selected = None

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()
            selected = (pos[1] // GRID_SIZE, pos[0] // GRID_SIZE)

        if event.type == pygame.KEYDOWN and selected:
            if event.unicode.isdigit() and 1 <= int(event.unicode) <= 9:
                if is_valid(board, int(event.unicode), (selected[0], selected[1])):
                    board[selected[0]][selected[1]] = int(event.unicode)
                else:
                    print("Invalid number!")

            if event.key == pygame.K_RETURN:
                solve_sudoku(board)

    # Drawing the board
    draw_board()

    # Highlight selected grid
    if selected:
        pygame.draw.rect(screen, (255, 0, 0), (selected[1] * GRID_SIZE, selected[0] * GRID_SIZE, GRID_SIZE, GRID_SIZE), 2)

    pygame.display.flip()

pygame.quit()
sys.exit()
