from __future__ import annotations
from dataclasses import dataclass
from .exceptions import InvalidMoveError

EMPTY = "."


@dataclass(frozen=True)
class Move:
    row: int
    col: int
    symbol: str    #Mutarea din joc


class Board:
    def __init__(self, size=15):
        if size < 5:
            raise ValueError("Board size must be at least 5.")
        self._size = size
        self._grid = []
        for i in range(size):
            row = []
            for j in range(size):
                row.append(EMPTY)
            self._grid.append(row)
        self._moves = 0

    @property
    def size(self):
        return self._size

    def get_cell(self, row, col):
        self._check_bounds(row, col)
        return self._grid[row][col]

    def is_empty(self, row, col):
        self._check_bounds(row, col)
        return self._grid[row][col] == EMPTY

    def place(self, move: Move):
        self._check_bounds(move.row, move.col)
        if move.symbol not in ("X", "O"):
            raise InvalidMoveError("Invalid symbol.")

        if not self.is_empty(move.row, move.col):
            raise InvalidMoveError("Row and col must be empty.")
        self._grid[move.row][move.col] = move.symbol
        self._moves += 1

    def clear_cell(self, row, col):

        # pentru AI simulare simpla place  undo
        self._check_bounds(row, col)
        if self._grid[row][col] != EMPTY:
            self._grid[row][col] = EMPTY
            self._moves -= 1


    def is_full(self):
        return self._moves == self._size * self._size #setter


    def lines_for_print(self):
        lines = []
        for row in self._grid:
            line = " ".join(f"{cell:2s}" for cell in row)
            lines.append(line)
        return lines


    def empty_cells(self):
        #lista simpla cu toate celulele libere
        cells = []
        for r in range(self._size):
            for c in range(self._size):
                if self._grid[r][c] == EMPTY:
                    cells.append((r, c))
        return cells

    def check_winner_from(self, last_move: Move, win_len=5):
        r, c = last_move.row, last_move.col
        self._check_bounds(r, c)

        s = self._grid[r][c]
        if s == EMPTY:
            return False

        dirs = [(0, 1), (1, 0), (1, 1), (1, -1)]
        for dr, dc in dirs:
            cnt = 1
            cnt += self._count_dir(r, c, dr, dc, s)
            cnt += self._count_dir(r, c, -dr, -dc, s)
            if cnt >= win_len:
                return True
        return False

    def _count_dir(self, r, c, dr, dc, sym):
        # numara cate piese consecutive cu acelasi simbol sunt intr o directie pornind de la o mutare data
        # nu numara piesa de start
        cnt = 0
        rr = r + dr
        cc = c + dc
        while 0 <= rr < self._size and 0 <= cc < self._size and self._grid[rr][cc] == sym:
            cnt += 1
            rr += dr
            cc += dc
        return cnt


    def _check_bounds(self, row, col):
        if row < 0 or row >= self._size or col < 0 or col >= self._size:
            raise InvalidMoveError("Out of bounds.")


    #for Ai part not finished
    """
    def candidate_moves(self, radius=2):
        if self._moves == 0:
            center = self._size // 2
            return [(center, center)]

        cand = set()   #searching the pieces on the board,for every piece it checks around it
        for r in range(self._size):
            for c in range(self._size):
                if self._grid[r][c] != EMPTY:
                    for dr in range(-radius, radius + 1):
                        for dc in range(-radius, radius + 1):
                            rr, cc = r + dr, c + dc
                            if 0 <= rr < self._size and 0 <= cc < self._size and self._grid[rr][cc] == EMPTY:
                                cand.add((rr, cc))    #verifies if it s in board and it s empty
        return list(cand)
    """
