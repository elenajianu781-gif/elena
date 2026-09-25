from domain.board import Board
from domain.exceptions import InvalidMoveError


class Console:
    def __init__(self, service):
        self._srv = service

    def run(self):
        print("GOMOKU - Human vs Computer")
        print("Introduce: row col (ex: 8 8). Index 1..N")
        print(f"You: {self._srv.human_symbol()}  Computer: {self._srv.ai_symbol()}")
        print()
        while not self._srv.is_over():
            self._print_board()
            self._human_turn()
            if self._srv.is_over():
                break
            self._srv.computer_move()
            print("Computer moved\n")
        self._print_board()
        res=self._srv.result()
        if res.winner is None and res.draw:
            print("Draw!")
        elif res.winner==self._srv.human_symbol():
            print("You win 🎉!")
        else:
            print("Computer wins!")
    def _human_turn(self):
        n=self._srv.board.size
        while True:
            raw=input("Enter your move(row,col): ").strip()
            try:
                r,c=self._parse(raw,n)
                self._srv.human_move(r,c)
                return
            except (ValueError,InvalidMoveError) as e:
                print(e)
    def _parse(self,raw,n):
        raw=raw.replace(","," ")
        parts=raw.split()
        if len(parts) != 2:
            raise ValueError("There should be exactly 2 numbers")
        r=int(parts[0])
        c=int(parts[1])
        if r<1 or r>n or c<1 or c>n:
            raise ValueError("Invalid row or column")
        return r-1,c-1
    def _print_board(self):
        b = self._srv.board
        n = b.size

        header = "    " + " ".join(f"{i:2d}" for i in range(1, n + 1))
        print(header)

        lines = b.lines_for_print()
        for i, line in enumerate(lines, start=1):
            print(f"{i:2d}  {line}")
        print()
