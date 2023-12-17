# GUI.py
import time
from functions import *
from puzzle_genetator import generate_puzzle
pygame.font.init()


# Puzzle class
class Puzzle:

    pygame.display.set_mode

    def __init__(self, width, height, win):
        
        # Window, Grid and Cells Dimensions
        self.puzzle = generate_puzzle()
        self.rows = PUZZLE_SIZE
        self.cols = PUZZLE_SIZE
        self.cubes = [Cube(self.puzzle[i*self.cols + j], i, j, width, height) for i in range(self.rows) for j in range(self.cols)]
        self.width = width
        self.height = height
        self.win = win
        
        # Board Setup
        self.update_puzzle()
        self.selected = None
        self.color = "Blue"


    def set_puzzle(self, puzzle):
        self.puzzle = puzzle
        self.cubes = [Cube(self.puzzle[i*self.cols + j], i, j, self.width, self.height) for i in range(self.rows) for j in range(self.cols)]
        
    def get_puzzle(self):
        self.update_puzzle()
        return self.puzzle

    def update_puzzle(self):
        self.puzzle = [self.cubes[i*self.cols + j].value for i in range(self.rows) for j in range(self.cols)]
        

    def place(self, val):
        row, col = self.selected
        if self.cubes[row*self.cols + col].value == 0:
            self.cubes[row*self.cols + col].set(val)
            self.update_puzzle()
            is_valid_result, conflicted_cell_index = is_valid(self.puzzle, val, row*self.cols + col)
            if is_valid_result and self.solve():
                self.color = "Green"
                return True
            else:
                self.cubes[row*self.cols + col].set(0)
                self.cubes[row*self.cols + col].set_temp(0)
                self.update_puzzle()
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
        find = find_empty_cell(self.puzzle)
        if not find:
            return True
        else:
            index = find

        for i in range(1, 10):
            if is_valid(self.puzzle, i, index):
                self.puzzle[index] = i

                if self.solve():
                    return True
                
                self.puzzle[index] = 0

        return False

    def solve_gui(self):
        self.update_puzzle()
        find = find_empty_cell(self.puzzle)
        if find == None:
            print()
            print_puzzle(self.puzzle)
            return True
        else:
            index = find

        for i in range(1, 10):
            if is_valid(self.puzzle, i, index)[0]:
                self.puzzle[index] = i
                self.cubes[index].set(i)
                self.cubes[index].draw_change(self.win, True)
                self.update_puzzle()
                pygame.display.update()
                pygame.time.delay(100)

                if self.solve_gui():
                    return True

                self.puzzle[index] = 0
                self.cubes[index].set(0)
                self.update_puzzle()
                self.cubes[index].draw_change(self.win, False)
                pygame.display.update()
                pygame.time.delay(100)

        return False


# Cube class
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


# Button class
class Button:
    def __init__(self, x, y, text, click_function):
        self.text = text
        self.x = x
        self.y = y
        self.rect = None
        self.click_function = click_function
        self.puzzle = None
        self.hovered = False

    def draw(self, win):
        fnt = pygame.font.SysFont("comicsans", 20)
        text_surface = fnt.render(str(self.text), True, BLACK)
        text_rect = text_surface.get_rect()
        width = text_rect.width + 10  # Add some padding
        height = text_rect.height + 10  # Add some padding
        rect = pygame.Rect(self.x, self.y, width, height)
        if self.hovered:
            pygame.draw.rect(win, WHITE, (self.x, self.y, width, height), 3)
        else:
            pygame.draw.rect(win, GRAY, (self.x, self.y, width, height), 3)
        text_rect.center = rect.center
        self.rect = rect
        win.blit(text_surface, text_rect)

    def is_cursor_in_button(self, cursor_pos):
        if self.rect:
            return self.rect.collidepoint(cursor_pos)
        return False

    def handle_event(self, event):
        if event.type == pygame.MOUSEMOTION:
            self.hovered = self.rect.collidepoint(pygame.mouse.get_pos())
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            self.puzzle = self.click_function()
            return True

    def get_puzzle(self):
        return self.puzzle


def main():
    win = pygame.display.set_mode((540,680))
    pygame.display.set_caption("Sudoku Solver")
    puzzle = Puzzle(540, 540, win)
    key = None
    run = True
    start = time.time()
    strikes = 0

    # Create buttons
    button1 = Button(20, 640, "AI generate Puzzle", generate_puzzle)
    button2 = Button(390, 640, "Insert Puzzle", init_puzzle)

    buttons = [button1, button2]

    while run:

        play_time = round(time.time() - start)

        for event in pygame.event.get():

            for button in buttons:
                if button.is_cursor_in_button(pygame.mouse.get_pos()):
                    if button.handle_event(event):
                        if button.get_puzzle() is not None:
                            puzzle.set_puzzle(button.get_puzzle())
                else:
                    button.hovered = False
            if event.type == pygame.QUIT:
                run = False

            if event.type == pygame.KEYDOWN:
                match event.key:
                    case pygame.K_1 | pygame.K_KP1:
                        key = 1
                    case pygame.K_2 | pygame.K_KP2:
                        key = 2
                    case pygame.K_3 | pygame.K_KP3:
                        key = 3
                    case pygame.K_4 | pygame.K_KP4:
                        key = 4
                    case pygame.K_5 | pygame.K_KP5:
                        key = 5
                    case pygame.K_6 | pygame.K_KP6:
                        key = 6
                    case pygame.K_7 | pygame.K_KP7:
                        key = 7
                    case pygame.K_8 | pygame.K_KP8:
                        key = 8
                    case pygame.K_9 | pygame.K_KP9:
                        key = 9
                    case pygame.K_DELETE:
                        puzzle.clear()
                    case _:
                        key = None

                if event.key == pygame.K_ESCAPE:
                    run = False

                if event.key == pygame.K_SPACE:
                    if puzzle.solve_gui():
                        finish_game()
                    else:
                        print("No solution")

                if event.key == pygame.K_RETURN:
                    i, j = puzzle.selected
                    index = i * 9 + j  # Convert 2D index to 1D index
                    if puzzle.cubes[index].temp != 0:
                        if puzzle.place(puzzle.cubes[index].temp):
                            print("Success")
                        else:
                            print("Wrong")
                            strikes += 1
                        key = None

                        if puzzle.is_finished():
                            finish_game()

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                pos = pygame.mouse.get_pos()
                clicked = puzzle.click(pos)
                if clicked:
                    puzzle.select(clicked[0], clicked[1])
                    key = None

        win.fill(WHITE)

        if puzzle.selected and key != None:
            puzzle.sketch(key)

        for button in buttons:
            button.draw(win)

        redraw_window(win, puzzle, play_time, strikes)
        pygame.display.update()


main()
pygame.quit()