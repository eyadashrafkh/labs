import pygame
import sys

class SudokuSolver:
    def __init__(self):
        # Pygame setup
        pygame.init()

        # Constants
        self.WIDTH, self.HEIGHT = 600, 600
        self.GRID_SIZE = self.WIDTH // 9

        # Colors
        self.WHITE = (255, 255, 255)
        self.BLACK = (0, 0, 0)
        self.RED = (255, 0, 0)
        self.GRAY = (200, 200, 200)

        # Initialize the window
        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        pygame.display.set_caption("Sudoku Solver")

        # Fonts
        self.font = pygame.font.Font(None, 36)

        # Board setup
        self.board = [
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

        self.highlighted_cells = set()

        self.selected = None

        

    def solve_sudoku(self):
        empty = self.find_empty()
        if not empty:
            return True

        row, col = empty

        for num in range(1, 10):
            if self.is_valid(num, (row, col)):
                self.board[row][col] = num

                if self.solve_sudoku():
                    return True

                self.board[row][col] = 0

        return False

    def find_empty(self):
        for i in range(9):
            for j in range(9):
                if self.board[i][j] == 0:
                    return (i, j)
        return None

    def is_valid(self, num, pos):
        # Check row
        if num in self.board[pos[0]]:
            conflicting_cells_row = [(pos[0], col) for col, value in enumerate(self.board[pos[0]]) if value == num]
            self.selected = conflicting_cells_row[0]
            # print("Row:",conflicting_cells_row[0])
            return False

        # Check column
        if num in [self.board[i][pos[1]] for i in range(9)]:
            conflicting_cells_column = [(row, pos[1]) for row in range(9) if self.board[row][pos[1]] == num]
            # print("Row:",conflicting_cells_column[0])
            self.selected = conflicting_cells_column[0]
            return False

        # Check 3x3 box
        box_row, box_col = pos[0] // 3 * 3, pos[1] // 3 * 3
        conflicting_cells_box = [(i, j) for i in range(box_row, box_row + 3) for j in range(box_col, box_col + 3) if self.board[i][j] == num]
        if conflicting_cells_box:
            # print("Box:",conflicting_cells_box[0])
            self.selected = conflicting_cells_box[0]
            return False

        return True
    
    # def is_valid2(self, num, pos):
    #     # Check row
    #     row = pos[0]
    #     conflicting_cells_row = [col for col, value in enumerate(self.board[row]) if value == num]
    #     if conflicting_cells_row:
    #         return False, {"row": conflicting_cells_row, "column": [], "box": []}

    #     # Check column
    #     col = pos[1]
    #     conflicting_cells_column = [row for row in range(9) if self.board[row][col] == num]
    #     if conflicting_cells_column:
    #         return False, {"row": [], "column": conflicting_cells_column, "box": []}

    #     # Check 3x3 box
    #     box_row, box_col = pos[0] // 3 * 3, pos[1] // 3 * 3
    #     conflicting_cells_box = [(i, j) for i in range(box_row, box_row + 3) for j in range(box_col, box_col + 3) if self.board[i][j] == num]
    #     if conflicting_cells_box:
    #         return False, {"row": [], "column": [], "box": conflicting_cells_box}

    #     return True, {"row": [], "column": [], "box": []}

    def draw_board(self):
        self.screen.fill(self.WHITE)
        for i in range(1, 9):
            thickness = 4 if i % 3 == 0 else 1
            pygame.draw.line(self.screen, self.BLACK, (0, i * self.GRID_SIZE), (self.WIDTH, i * self.GRID_SIZE), thickness)        
            pygame.draw.line(self.screen, self.BLACK, (i * self.GRID_SIZE, 0), (i * self.GRID_SIZE, self.HEIGHT), thickness)

        for i in range(9):
            for j in range(9):
                if self.board[i][j] != 0:
                    text = self.font.render(str(self.board[i][j]), True, self.BLACK)
                    text_rect = text.get_rect(center=(j * self.GRID_SIZE + self.GRID_SIZE // 2, i * self.GRID_SIZE + self.GRID_SIZE // 2))
                    self.screen.blit(text, text_rect)


    def draw_highlights(self, num):
        for i in range(9):
            for j in range(9):
                if self.board[i][j] == num:
                    pygame.draw.rect(self.screen, self.RED,
                                        (j * self.GRID_SIZE, i * self.GRID_SIZE, self.GRID_SIZE, self.GRID_SIZE), 3)
    
    def highlight_selected_cell(self):
        row, col = self.selected
        if self.board[row][col] != 0 :
            self.draw_highlights(self.board[row][col])
            self.draw_highlights_grids(row, col)
    
    
    def draw_highlights_grids(self, row, col):
        # Highlight entire row
        pygame.draw.rect(self.screen, self.RED,
                         (0, row * self.GRID_SIZE, self.WIDTH, self.GRID_SIZE), 3)

        # Highlight entire column
        pygame.draw.rect(self.screen, self.RED,
                         (col * self.GRID_SIZE, 0, self.GRID_SIZE, self.HEIGHT), 3)

        # Highlight entire 3x3 box
        box_row, box_col = row // 3 * 3, col // 3 * 3
        pygame.draw.rect(self.screen, self.RED,
                         (box_col * self.GRID_SIZE, box_row * self.GRID_SIZE, 3 * self.GRID_SIZE, 3 * self.GRID_SIZE), 3)

    def run(self):
        running = True

        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

                if event.type == pygame.MOUSEBUTTONDOWN:
                    pos = pygame.mouse.get_pos()
                    self.selected = (pos[1] // self.GRID_SIZE, pos[0] // self.GRID_SIZE)
                    print(self.selected)
                
                if event.type == pygame.KEYDOWN and self.selected:
                    if event.unicode.isdigit() and 1 <= int(event.unicode) <= 9:
                        if self.is_valid(int(event.unicode), (self.selected[0], self.selected[1])):
                            self.board[self.selected[0]][self.selected[1]] = int(event.unicode)
                        else:
                            print("Invalid number!")
                    if event.key == pygame.K_RETURN:
                        self.solve_sudoku()

            # Drawing the board
            self.draw_board()

            if self.selected:
                self.highlight_selected_cell()
                pygame.draw.rect(self.screen, self.RED, (self.selected[1] * self.GRID_SIZE, self.selected[0] * self.GRID_SIZE, self.GRID_SIZE, self.GRID_SIZE), 3)

            pygame.display.flip()

        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    sudoku_solver = SudokuSolver()
    sudoku_solver.run()
