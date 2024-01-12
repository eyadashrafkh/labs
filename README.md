#  Sudoko_solver

Sudoku is a logic-based number-placement game that challenges players to fill
a 9x9 grid with digits from 1 to 9. The goal
of this project is to provide a full game with GUI to show the AI agent solving the
game and allow user to input board representation then agent solves it.

## Table of Contents

1. [State Representation](#state-representation)
2. [Algorithms](#algorithms)
    1. [Backtracking Algorithm](#backtracking-algorithm)
    2. [Puzzle Generation](#puzzle-generation)
3. [CSP](#csp)
4. [Data Structure Used](#data-structure-used)
    1. [Lists](#lists)
    2. [Sets](#sets)
    3. [Dictionaries](#dictionaries)
    4. [Priority Queue (Heap)](#priority-queue-heap)
    5. [Tuples](#tuples)
    6. [Booleans](#booleans)
5. [GUI](#gui)

## State Representation

To represent the Sudoku board, we can use a 2D array. However, this approach has a drawback as it requires a large amount of memory. The size of the 2D array is 9x9 times the size of an integer. This limits the agent's ability to search deeply and find solutions.

To overcome this limitation, we have chosen to represent the board state using a 1D array of integers. This allows the agent to solve the game more efficiently and reach deeper search depths.


## Algorithms
### Backtracking Algorithm
- The game supports Backtracking to be able to validate the input (to check that input puzzle is solvable), Backtracking is also needed to generate random puzzle (fill random places of puzzle) to ensure that the puzzle generated is solvable.
    - Validate the input puzzle using Backtracking.
    - Generate a random puzzle by filling random places of the puzzle.

### Puzzle Generation
Puzzle Generation includes the following key functions:
- 'fill puzzle' Function:
    - Recursively fills a given Sudoku puzzle grid with valid values.
    - Utilizes functions like 'find empty cell', 'is valid', and 'has empty cell'.
- 'solve sudoko' Function:
    - Recursively solves a Sudoku puzzle using a backtracking approach.
    - Keeps track of the number of solutions using the global variable 'numberOfSolution'.
- 'generate puzzle' Function:
    - Generates a Sudoku puzzle by first filling the puzzle grid completely and then selectively removing values to achieve the desired difficulty level.
    - Uses the 'fill puzzle' and 'solve sudoko' functions to ensure a valid and unique solution.

### CSP
We defined the CSP as a class named ‘CSP‘ (Constraint Satisfaction Problem) for solving
Sudoku puzzles. Here is a summary of its key components:
- Initialization:
    - The constructor ‘ init ‘ initializes the CSP object with a given Sudoku board.
    - It sets up various data structures like ‘arcs‘, ‘variables‘, ‘heap‘, and ‘counts‘.
- ‘solve‘ Method:
    - Checks the consistency of the input Sudoku board using ‘check arcs consistency‘.
    - If the board is consistent, initiates the solving process using the ‘backtrack‘ method.
    - If a solution is found, updates the original board with the solution.
- ‘backtrack‘ Method:
    - Recursive backtracking algorithm for solving Sudoku.
    - Chooses the next variable to assign using a priority queue (‘heap‘).
    - Saves a copy of the domain for backtracking purposes.
    - Tries assigning values from the domain and recursively explores possible solutions.
    - Backtracks if a solution is not found.
- ‘create variables‘ Method:
    - Initializes the variables for each cell in the Sudoku grid.
    - Populates domains based on the initial board values.
    - Sets up the priority queue (‘heap‘) for variable selection.
- ‘add affected arcs‘ and ‘add arcs‘ Methods:
    - Adds arcs (constraints) for each variable based on its row, column, and box.
    - ‘add affected arcs‘ specifically adds arcs for a variable that has been assigned a value.
- ‘check arcs consistency‘ Method:
    - Checks the consistency of arcs (constraints) in the CSP.
    - Uses the ‘check consistency‘ method to determine consistency between two variables.
- ‘check consistency‘ Method:
    - Checks consistency between the domains of two variables based on the arcs.
    - Helps identify values that need to be removed to maintain consistency.
- ‘clear arcs‘ Method:
    - Clears the set of arcs, primarily used during the consistency-checking process.
- ‘remove value‘ Method:
    - Removes a specific value from a variable’s domain and updates related data structures.

## Data Structure Used

The project uses several data structures and algorithms to generate and solve Sudoku
puzzles. Here’s a brief overview of the data structures used and the reasons for their
selection:

### Lists
Lists in Python are used extensively throughout the project. They are used to represent
the Sudoku puzzle itself, the values that can be filled in the puzzle, and the domains
of the variables in the CSP (Constraint Satisfaction Problem) solver. Lists were chosen
because they provide efficient access and modification of elements at any index, which is
crucial for representing and manipulating the Sudoku grid.

### Sets
Sets are used to represent the arcs in the CSP solver. An arc is a pair of cells in the
Sudoku grid that are in the same row, column, or 3x3 box. Sets were chosen because they
provide efficient operations for adding elements, removing elements, and checking if an
element exists, all of which are used in the arc consistency algorithm.

### Dictionaries
Dictionaries are used in the count values function to count the number of occurrences of
each value in the puzzle. Dictionaries were chosen because they provide efficient mapping
from keys (the values in the puzzle) to values (the counts of each value).

### Priority Queue (Heap)
A priority queue implemented as a binary heap is used in the CSP solver to select the next
variable to assign a value to. The priority queue was chosen because it provides efficient
operations to insert elements, remove the element with the highest priority, and update
the priority of an element. This is used in the CSP solver to implement the Minimum
Remaining Values (MRV) heuristic, which selects the variable with the fewest remaining
values in its domain.

### Tuples
Tuples are used to represent the return value of the is valid function, which checks if a
number can be placed in a specific cell of the Sudoku puzzle. Tuples were chosen because
they are an efficient and convenient way to return multiple values from a function.

### Booleans
Booleans are used in several places in the project, such as the domains of the variables in
the CSP solver, the return values of functions like isv valid and has empty cell, and the
flags in the PQ class. Booleans were chosen because they are a simple and efficient way
to represent binary (true/false) information.

## GUI