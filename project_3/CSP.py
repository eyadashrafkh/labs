from PQ import PQ
from copy import deepcopy
from functions import *

# Domain is a list of 10 values, each value is True if it is available. the 10th value is the number of available values
FULL_DOMAIN = ([True]*9) + [9]
EMPTY_DOMAIN = ([False]*9) + [0]

DEBUG = True
my_print = print if DEBUG else lambda *args, **kwargs: None


def domain_of(val):
    domain = EMPTY_DOMAIN.copy()
    domain[val-1] = True
    domain[9] = 1
    return domain


class CSP:
    def __init__(self, board):
        print(board)
        self.board = board
        self.arcs = set()
        self.variables = []
        self.heap = PQ(9*9)
        self.counts = [0 for _ in range(9)]
        self.create_variables()
        my_print(f"arcs: {self.arcs}")

    def solve(self):
        # check arcs consistency
        if not self.check_arcs_consistency():
            my_print("board is unsolvable")
            return False
        my_print("board is solvable")

        # if arcs are consistent, start solving
        solvable = self.backtrack()

        if solvable:
            for i in range(9*9):
                if self.board[i] == 0:
                    self.board[i] = self.variables[i].index(True)+1
                    # print(self.variables[i])
            return self.board
        else:
            return False

    def backtrack(self):
        # if heap is empty, return True
        if self.heap.__len__() == 0:
            return True

        # check consistency
        if not self.check_arcs_consistency():
            return False

        # get the next variable to assign
        ind = self.heap.pop()
        print(f"Current cell: {ind//9}, {ind%9}")

        if ind == 9 or ind == 20:
            print("here: ", self.variables[68])

        # save a copy of the domain in case we backtrack
        domain_temp = self.variables[ind].copy()

        variables_temp = deepcopy(self.variables)
        heap_temp = deepcopy(self.heap)

        # loop over the domain
        for i in range(9):

            # try assigning all values in the domain
            if self.variables[ind][i]:
                my_print(f"Current value {i+1}")

                # assign value to the variable
                self.variables[ind] = domain_of(i+1)

                # add arcs
                self.add_affected_arcs(ind)

                # recurse and check if the board is solvable
                solvable = self.backtrack()

                if solvable:
                    return True

                # if the board is not solvable, backtrack
                self.variables = variables_temp
                self.heap = heap_temp

        # if no value in the domain is valid, return False
        return False

    def create_variables(self):
        self.variables = []

        # Create variable's domain
        for i in range(9*9):
            if self.board[i] != 0:
                # domain is current value if already assigned
                domain = EMPTY_DOMAIN.copy()
                domain[self.board[i] - 1] = True

                # set the available values to 1
                domain[9] = 1

                # add to counts
                self.counts[self.board[i] - 1] += 1

                # append to domains
                self.variables.append(domain)

            else:
                # domain is 1-9 if not assigned and add all possible arcs
                self.variables.append(FULL_DOMAIN.copy())

                # append to heap
                self.heap.append(9, i)

                # add arcs
                self.add_arcs(i)

        # heapify
        self.heap.heapify()

    def add_affected_arcs(self, ind):
        # calculate row, column and box
        row = ind // 9
        col = ind % 9
        box = (row // 3)*3 + col // 3
        box_start = (box//3)*9*3 + (box % 3)*3

        # my_print(f"row: {row}, col: {col}, box: {box}, box_start: {box_start}")

        # add all arcs from the current cell
        for i in range(9):
            # calculate the row and column of the next cell in the box
            sub_row = i // 3
            sub_col = i % 3
            # insert next cell in row, column and box
            self.arcs.add((ind, box_start+sub_row*9+sub_col))
            self.arcs.add((ind, row*9+i))
            self.arcs.add((ind, i*9+col))

    def add_arcs(self, ind):
        # calculate row, column and box
        row = ind // 9
        col = ind % 9
        box = (row // 3)*3 + col // 3
        box_start = (box//3)*9*3 + (box % 3)*3

        # my_print(f"row: {row}, col: {col}, box: {box}, box_start: {box_start}")

        # add all arcs from the current cell
        for i in range(0, 9):
            # calculate the row and column of the next cell in the box
            sub_row = i // 3
            sub_col = i % 3
            # insert next cell in row, column and box
            self.arcs.add((box_start+sub_row*9+sub_col, ind))
            self.arcs.add((row*9+i, ind))
            self.arcs.add((i*9+col, ind))

    def check_arcs_consistency(self):
        # Check all arcs
        while self.arcs.__len__() > 0:
            arc = self.arcs.pop()
            if arc[0] == arc[1]:
                continue

            # get the domains of the two variables
            a = self.variables[arc[0]]
            b = self.variables[arc[1]]

            # check if the arc is consistent
            my_print(f"checking consistency between ({arc[0] // 9}, {arc[0] % 9}) and ({arc[1] // 9}, {arc[1] % 9})")
            res = self.check_consistency(a, b)

            if res >= 0:
                # if there is no value to validate it then arc is not consistent and the value in B is removed
                solvable = self.remove_value(arc[1], res)

                # if the domain becomes empty then the board is not solvable
                if not solvable:
                    return -1
            my_print(f"A: {a}\nB: {b}\n")

        return True

    def check_consistency(self, a, b):
        # loop over Domain of A to find the first available value
        for i in range(9):
            # one value in a is enough to validate all values of B except for the same value
            if a[i]:
                my_print(f"{i+1} is available in A: {a}")
                # if the same value exists in B, check for any other value in A to validate it
                if b[i]:
                    my_print(f"{i+1} also available in B: {b}")
                    for j in range(i+1, 9):
                        # if there is a value to validate it then arc is consistent
                        if a[j]:
                            return -1

                    # if domain needs update return the index to remove
                    return i
                # if the same value does not exist in B, then arc is consistent
                return -1

    def clear_arcs(self):
        self.arcs = set()

    def remove_value(self, index, value):
        self.variables[index][value] = False
        self.variables[index][9] -= 1
        self.heap.update(index, self.variables[index][9])
        self.heap.heapify()

        return self.variables[index][9] > 0


if __name__ == "__main__":
    my_print("msa")
    # p = [1, 0, 0, 0, 5, 0, 3, 0, 4, 3, 7, 4, 0, 0, 2, 0, 0, 9, 5, 2, 0, 4, 0, 9, 8, 1, 7, 6, 3, 1, 0, 2, 0, 4, 0, 5, 0, 8, 0, 5, 6, 4, 0, 0, 0, 4, 0, 2, 3, 8, 0, 7, 0, 0, 8, 0, 0, 6, 9, 0, 2, 0, 3, 9, 0, 3, 2, 0, 0, 6, 5, 1, 2, 0, 5, 0, 4, 3, 0, 7, 0]
    p = [0, 7, 0, 2, 0, 6, 3, 4, 0, 0, 0, 9, 5, 0, 1, 7, 0, 0, 2, 5, 0, 7, 4, 0, 8, 9, 0, 0, 6, 0, 1, 0, 0, 0, 0, 0, 5, 0, 0, 0, 0, 4, 1, 6, 2, 1, 3, 0, 8, 0, 0, 4, 0, 0, 4, 2, 0, 0, 5, 8, 0, 1, 3, 0, 1, 5, 4, 0, 0, 0, 0, 0, 6, 8, 0, 0, 0, 0, 0, 5, 0]
    # CSP([0 for _ in range(9*9)])

    ai = CSP(p)
    print_puzzle(p)

    print(ai.heap.pointers)
    print(ai.heap.heap)
    print_puzzle(ai.solve())


