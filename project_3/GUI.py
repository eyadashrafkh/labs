# GUI.py
import time
from functions import *
pygame.font.init()

class Grid:

    board = [
        7, 8, 0, 4, 0, 0, 1, 2, 0,
        6, 0, 0, 0, 7, 5, 0, 0, 9,
        0, 0, 0, 6, 0, 1, 0, 7, 8,
        0, 0, 7, 0, 4, 0, 2, 6, 0,
        0, 0, 1, 0, 5, 0, 9, 3, 0,
        9, 0, 4, 0, 6, 0, 0, 0, 5,
        0, 7, 0, 3, 0, 0, 0, 1, 2,
        1, 2, 0, 0, 0, 7, 4, 0, 0,
        0, 4, 9, 2, 0, 6, 0, 0, 7
    ]
    pygame.display.set_mode

    def __init__(self, rows, cols, width, height, win):
        
        # Window, Grid and Cells Dimensions
        self.rows = rows
        self.cols = cols
        self.cubes = [Cube(self.board[i*self.cols + j], i, j, width, height) for i in range(rows) for j in range(cols)]
        self.width = width
        self.height = height
        self.win = win
        
        # Board Setup
        self.model = None
        self.update_model()
        self.selected = None
        self.color = "Blue"


    def update_model(self):
        self.model = [self.cubes[i*self.cols + j].value for i in range(self.rows) for j in range(self.cols)]
        

    def place(self, val):
        row, col = self.selected
        if self.cubes[row*self.cols + col].value == 0:
            self.cubes[row*self.cols + col].set(val)
            self.update_model()

            is_valid_result, conflicted_cell_index = is_valid(self.model, val, row*self.cols + col)
            if is_valid_result and self.solve():
                self.color = "Green"
                return True
            else:
                self.cubes[row*self.cols + col].set(0)
                self.cubes[row*self.cols + col].set_temp(0)
                self.update_model()
                row, col = conflicted_cell_index//9, conflicted_cell_index%9
                self.select(row, col)
                self.color = "Red"
                return False


    def sketch(self, val):
        row, col = self.selected
        self.cubes[row*self.cols + col].set_temp(val)


    def draw(self):
        # Draw Grid Lines
        gap = self.width / 9
        for i in range(self.rows+1):
            if i % 3 == 0 and i != 0:
                thick = 4
            else:
                thick = 1
            pygame.draw.line(self.win, BLACK, (0, i*gap), (self.width, i*gap), thick)
            pygame.draw.line(self.win, BLACK, (i * gap, 0), (i * gap, self.height), thick)

        # Draw Cubes
        for i in range(self.rows):
            for j in range(self.cols):
                self.cubes[i*self.cols + j].draw(self.win, self.color)

    def select(self, row, col):
        # Reset all other
        for i in range(self.rows):
            for j in range(self.cols):
                self.cubes[i*self.cols + j].selected = False

        self.cubes[row*self.cols + col].selected = True
        self.selected = (row, col)

    def clear(self):
        row, col = self.selected
        if self.cubes[row*self.cols + col].value == 0:
            self.cubes[row*self.cols + col].set_temp(0)

    def click(self, pos):
        if pos[0] < self.width and pos[1] < self.height:
            gap = self.width / 9
            x = pos[0] // gap
            y = pos[1] // gap
            self.color = "Blue"
            return (int(y),int(x))
        else:
            return None

    def is_finished(self):
        for i in range(self.rows):
            for j in range(self.cols):
                if self.cubes[i*self.cols + j].value == 0:
                    return False
        return True

    def solve(self):
        find = find_empty(self.model)
        if not find:
            return True
        else:
            index = find

        for i in range(1, 10):
            if is_valid(self.model, i, index):
                self.model[index] = i

                if self.solve():
                    return True
                
                self.model[index] = 0

        return False

    def solve_gui(self):
        self.update_model()
        find = find_empty(self.model)
        if not find:
            return True
        else:
            index = find

        for i in range(1, 10):
            if is_valid(self.model, i, index)[0]:
                self.model[index] = i
                self.cubes[index].set(i)
                self.cubes[index].draw_change(self.win, True)
                self.update_model()
                pygame.display.update()
                pygame.time.delay(100)

                if self.solve_gui():
                    return True

                self.model[index] = 0
                self.cubes[index].set(0)
                self.update_model()
                self.cubes[index].draw_change(self.win, False)
                pygame.display.update()
                pygame.time.delay(100)

        return False


class Cube:
    rows = 9
    cols = 9

    def __init__(self, value, row, col, width, height):
        self.value = value
        self.temp = 0
        self.row = row
        self.col = col
        self.width = width
        self.height = height
        self.selected = False

    def draw(self, win, color):
        fnt = pygame.font.SysFont("comicsans", 40)

        gap = self.width / 9
        x = self.col * gap
        y = self.row * gap

        if self.temp != 0 and self.value == 0:
            text = fnt.render(str(self.temp), 1, GRAY)
            win.blit(text, (x+5, y+5))
        elif not(self.value == 0):
            text = fnt.render(str(self.value), 1, BLACK)
            win.blit(text, (x + (gap/2 - text.get_width()/2), y + (gap/2 - text.get_height()/2)))

        if self.selected:
            if color=="Blue":
                pygame.draw.rect(win, BLUE, (x,y, gap ,gap), 3)
            elif color == "Green":
                pygame.draw.rect(win, GREEN, (x, y, gap, gap), 3)
            elif color == "Red":
                pygame.draw.rect(win, RED, (x, y, gap, gap), 3)

    def draw_change(self, win, g=True):
        fnt = pygame.font.SysFont("comicsans", 40)

        gap = self.width / 9
        x = self.col * gap
        y = self.row * gap

        pygame.draw.rect(win, WHITE, (x, y, gap, gap), 0)

        text = fnt.render(str(self.value), 1, BLACK)
        win.blit(text, (x + (gap / 2 - text.get_width() / 2), y + (gap / 2 - text.get_height() / 2)))
        if g:
            pygame.draw.rect(win, GREEN, (x, y, gap, gap), 3)
        else:
            pygame.draw.rect(win, RED, (x, y, gap, gap), 3)

    def set(self, val):
        self.value = val

    def set_temp(self, val):
        self.temp = val



def is_valid(board, num, index):
    # Check row
    row_start = (index // 9) * 9
    for i in range(row_start, row_start + 9):
        if board[i] == num and i != index:
            return False, i

    # Check column
    col_start = index % 9
    for i in range(col_start, 81, 9):
        if board[i] == num and i != index:
            return False, i

    # Check 3x3 box
    box_start = (index // 27) * 27 + (index % 9) // 3 * 3
    for i in range(box_start, box_start + 3):
        for j in range(3):
            if board[i + j * 9] == num and (i + j * 9) != index:
                return False, i

    return True, None


def main():
    win = pygame.display.set_mode((540,600))
    pygame.display.set_caption("Sudoku Solver")
    board = Grid(9, 9, 540, 540, win)
    key = None
    run = True
    start = time.time()
    strikes = 0
    while run:

        play_time = round(time.time() - start)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    key = 1
                if event.key == pygame.K_2:
                    key = 2
                if event.key == pygame.K_3:
                    key = 3
                if event.key == pygame.K_4:
                    key = 4
                if event.key == pygame.K_5:
                    key = 5
                if event.key == pygame.K_6:
                    key = 6
                if event.key == pygame.K_7:
                    key = 7
                if event.key == pygame.K_8:
                    key = 8
                if event.key == pygame.K_9:
                    key = 9
                if event.key == pygame.K_KP1:
                    key = 1
                if event.key == pygame.K_KP2:
                    key = 2
                if event.key == pygame.K_KP3:
                    key = 3
                if event.key == pygame.K_KP4:
                    key = 4
                if event.key == pygame.K_KP5:
                    key = 5
                if event.key == pygame.K_KP6:
                    key = 6
                if event.key == pygame.K_KP7:
                    key = 7
                if event.key == pygame.K_KP8:
                    key = 8
                if event.key == pygame.K_KP9:
                    key = 9
                if event.key == pygame.K_DELETE:
                    board.clear()
                    key = None

                if event.key == pygame.K_SPACE:
                    board.solve_gui()

                if event.key == pygame.K_RETURN:
                    i, j = board.selected
                    index = i * 9 + j  # Convert 2D index to 1D index
                    if board.cubes[index].temp != 0:
                        if board.place(board.cubes[index].temp):
                            print("Success")
                        else:
                            print("Wrong")
                            strikes += 1
                        key = None

                        if board.is_finished():
                            finish_game()
                            print("Game over")

            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                clicked = board.click(pos)
                if clicked:
                    board.select(clicked[0], clicked[1])
                    key = None

        if board.selected and key != None:
            board.sketch(key)

        redraw_window(win, board, play_time, strikes)
        pygame.display.update()


main()
pygame.quit()