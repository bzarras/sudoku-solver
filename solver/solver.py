from time import time
from solver.sudoku import Sudoku


class Solver:
    def __init__(self, sudoku: Sudoku, debug: bool = False):
        self.initial_sudoku = sudoku
        self.sudoku_stack: list[Sudoku] = [self.initial_sudoku]
        self.debug = debug
        # state for stats:
        self.iterations = 0
        self.guesses = 0
        self.time = 0.0

    def solve(self) -> None:
        start_time = time()
        while self.sudoku_stack:
            self.iterations += 1
            sudoku = self.sudoku_stack.pop()
            square = sudoku.fill_until_conflict()
            if square is None:
                if sudoku.is_valid():
                    # we solved it, break here
                    break
                else:
                    continue
            elif len(square) > 0:
                self.guesses += 1
                # for each candidate, push a new sudoku onto stack
                for candidate in square.candidates:
                    new_sudoku = sudoku.copy()
                    new_sudoku.board[square.row][square.col] = candidate
                    self.sudoku_stack.append(new_sudoku)
            # if we've hit the end, it means the current path led to
            # a bad solution, so we'll loop to the top and pop this board
        self.time = time() - start_time
        # put the solution back into the stack for tracing
        self.sudoku_stack.append(sudoku)
        # print solution
        print("Solved!")
        print(sudoku)

    def print_stats(self):
        print(f"Iterations: {self.iterations}")
        print(f"Guesses: {self.guesses}")
        print(f"Path length: {len(self.sudoku_stack)}")
        print(f"Total time: {round(self.time, 3)}s")

    def print_solution_trail(self):
        for i, sudoku in enumerate(self.sudoku_stack):
            print(f"Step {i + 1}:")
            print(sudoku)
            print()
