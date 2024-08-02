from collections import Counter
from copy import deepcopy
from dataclasses import dataclass
from heapq import heappush, heappop


@dataclass
class OpenSquare:
    row: int
    col: int
    candidates: list[int]

    def __lt__(self, other: "OpenSquare") -> bool:
        return len(self) < len(other)

    def __len__(self) -> int:
        return len(self.candidates)


class Sudoku:
    def __init__(self, board: list[list[int]]):
        self.board = board
        self._validate_initial_board()

    def _validate_initial_board(self):
        if len(self.board) != 9:
            raise ValueError("Board must have 9 rows")
        for row in self.board:
            if len(row) != 9:
                raise ValueError("Board must have 9 columns")

    def copy(self) -> "Sudoku":
        board_copy = deepcopy(self.board)
        return Sudoku(board=board_copy)

    def is_valid(self) -> bool:
        for i in range(9):
            row = self._get_row(i)
            if not self._is_valid_nine(row):
                return False
        for i in range(9):
            col = self._get_col(i)
            if not self._is_valid_nine(col):
                return False
        for i in range(0, 9, 3):
            for j in range(0, 9, 3):
                box = self._get_box(i, j)
                if not self._is_valid_nine(box):
                    return False
        return True

    def _get_candidates_for_square(self, row_index: int, col_index: int) -> OpenSquare:
        row = self._get_row(row_index)
        col = self._get_col(col_index)
        box = self._get_box(row_index, col_index)
        used_nums = set(row + col + box)
        candidates = set(range(1, 10)) - used_nums
        return OpenSquare(row_index, col_index, list(candidates))

    def _open_squares(self) -> list[tuple[int, int]]:
        open_squares = []
        for i in range(9):
            for j in range(9):
                if self.board[i][j] == 0:
                    open_squares.append((i, j))
        return open_squares

    def fill_until_conflict(self) -> OpenSquare | None:
        open_squares = self._open_squares()
        sorted_squares: list[OpenSquare] = []
        for i, j in open_squares:
            candidates = self._get_candidates_for_square(i, j)
            heappush(sorted_squares, candidates)
        sq: OpenSquare | None = None
        while sorted_squares:
            sq = heappop(sorted_squares)
            if len(sq) == 1:
                self.board[sq.row][sq.col] = sq.candidates[0]
            else:
                return sq
        return None

    def is_solved(self) -> bool:
        return self.is_valid() and len(self._open_squares()) == 0

    def _is_valid_nine(self, numbers: list[int]) -> bool:
        counter = Counter(numbers)
        return not any(v > 1 for k, v in counter.items() if k != 0)

    def _get_row(self, index: int) -> list[int]:
        return self.board[index]

    def _get_col(self, index: int) -> list[int]:
        return [row[index] for row in self.board]

    def _get_box(self, row: int, col: int) -> list[int]:
        row_start = self._get_box_start(row)
        col_start = self._get_box_start(col)
        box = []
        for i in range(row_start, row_start + 3):
            for j in range(col_start, col_start + 3):
                box.append(self.board[i][j])
        return box

    def _get_box_start(self, index: int) -> int:
        if index >= 6:
            start = 6
        elif index >= 3:
            start = 3
        else:
            start = 0
        return start

    def __str__(self):
        board = deepcopy(self.board)
        for row in board:
            row.insert(3, "|")
            row.insert(7, "|")
        str_rows = [" ".join(map(lambda i: str(i) if i else " ", row)) for row in board]
        str_rows.insert(3, "------+-------+------")
        str_rows.insert(7, "------+-------+------")
        return "\n".join(str_rows)
