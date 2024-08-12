from solver.sudoku import Sudoku
from solver.solver import Solver
from solver.test_boards import HARD_UNSOLVED


def main():
    sudoku = Sudoku(HARD_UNSOLVED)
    print(sudoku)
    solver = Solver(sudoku=sudoku)
    solver.solve()
    solver.print_stats()


if __name__ == "__main__":
    main()
