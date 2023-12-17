from PQ import PQ

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
            return False

        # if arcs are consistent, start solving
        return self.backtrack()

    def backtrack(self):
        # if heap is empty, return True
        if self.heap.__len__() == 0:
            return True

        # get the next variable to assign
        _, ind = self.heap.pop()

        # save a copy of the domain in case we backtrack
        domain_temp = self.variables[ind].copy()

        # loop over the domain
        for i in range(9):

            # try assigning all values in the domain
            if self.variables[ind][i]:

                # assign value to the variable
                self.variables[ind] = domain_of(i+1)

                # add arcs
                self.add_affected_arcs(ind)

                # check consistency
                if not self.check_arcs_consistency():
                    # if not consistent, backtrack
                    self.variables[ind] = domain_temp
                else:
                    # if consistent, continue
                    if self.backtrack():
                        return True

                    # if not solvable, backtrack
                    self.variables[ind] = domain_temp


    def create_variables(self):
        self.variables = []

        # Create variable's domain
        for i in range(9*9):
            if self.board[i] != 0:
                # domain is current value if already assigned
                domain = EMPTY_DOMAIN.copy()
                domain[self.board[i] - 1] = True

                # set the count of the value to 1
                domain[9] = 1

                # add to counts
                self.counts[self.board[i] - 1] += 1

                # append to heap
                self.variables.append(domain)

            else:
                # domain is 1-9 if not assigned and add all possible arcs
                self.variables.append(FULL_DOMAIN.copy())

                # append to heap
                self.heap.append((9, i))

                # add arcs
                self.add_arcs(i)

    def add_affected_arcs(self, ind):
        # calculate row, column and box
        row = ind // 9
        col = ind % 9
        box = (row // 3)*3 + col // 3
        box_start = (box//3)*9 + (box % 3)*3

        my_print(f"row: {row}, col: {col}, box: {box}, box_start: {box_start}")

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
        box_start = (box//3)*9 + (box % 3)*3

        my_print(f"row: {row}, col: {col}, box: {box}, box_start: {box_start}")

        # add all arcs from the current cell
        for i in range(9):
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

            # get the domains of the two variables
            a = self.variables[arc[0]]
            b = self.variables[arc[1]]

            # check if the arc is consistent
            res = self.check_consistency(a, b)

            match res:
                case 1:
                    # if the arc is consistent after changes, add all arcs from the second variable
                    self.add_arcs(arc[1])
                case -1:
                    # if the arc is not consistent, the board is not solvable
                    return False
                case 0:
                    # if the arc is consistent without changes, continue
                    pass

        return True

    def check_consistency(self, a, b):
        # loop over Domain of A to find the first available value
        for i in range(9):
            # one value in a is enough to validate all values of B except for the same value
            if a[i]:
                # if the same value exists in B, check for any other value in A to validate it
                if b[i]:
                    for j in range(i+1, 9):
                        if a[j]:
                            # if there is a value to validate it then arc is consistent
                            return 0

                    # if there is no value to validate it then arc is not consistent and the value in B is removed
                    solvable = self.remove_value(b, i)

                    # if the domain becomes empty then the board is not solvable
                    if not solvable:
                        return -1

                    # return 1 if changes were made to make the arc consistent
                    return 1

    def remove_value(self, domain, ind):
        domain[ind] = False
        domain[9] -= 1

        return domain[9] != 0



if __name__ == "__main__":
    my_print("msa")
    CSP([0 for _ in range(9*9)])
