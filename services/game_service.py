from dataclasses import dataclass
from domain.board import Board, Move
from domain.exceptions import InvalidMoveError
from services.strategy import GreedyWinBlockStrategy

@dataclass
class GameResults:
    """Purpose

Represents the final or current outcome of the game.
Fields:
 winner
 "X" or "O" if a player has won
 None if there is no winner yet or the game ended in a draw
   draw
 True if the game ended in a draw
  False otherwise
 Invariants
  If winner is not None, then draw must be False
  If draw is True, then winner must be None"""
    winner: str | None   #winner simbol
    draw: bool


class GameService:
    def __init__(self, board_repo,human_symbol="X",ai_symbol="O",strategy=None):
        self._repo = board_repo
        self._human = human_symbol
        self._ai = ai_symbol
        self._strategy = strategy if strategy else GreedyWinBlockStrategy()
        self._result=GameResults(None,False)

    @property
    def board(self):
        return self._repo.get_board()

    def result(self):
        return self._result

    def is_over(self):
        return self._result.winner is not None or self._result.draw

    def human_symbol(self):
        return self._human

    def ai_symbol(self):
        return self._ai

    def human_move(self,row,col):
        self._ensure_not_over()
        b=self.board
        m=Move(row,col,self._human)
        b.place(m)
        self._update_result(b,m)

    def computer_move(self):
        self._ensure_not_over()
        b=self.board
        if b.is_full():
            self._result=GameResults(None,True)
            return
        m=self._strategy.choose_move(b,self._ai,self._human)
        b.place(m)
        self._update_result(b,m)

    def _update_result(self,b,m):
        if b.check_winner_from(m):
            self._result=GameResults(m.symbol,False)
        elif b.is_full():
            self._result=GameResults(None,True)

    def _ensure_not_over(self):
        if self.is_over():
            raise InvalidMoveError("Game over")
