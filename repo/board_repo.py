from domain.board import Board

class BoardRepo:
    def __init__(self,board:Board):
        self._board = board

    def get_board(self):
        return self._board
    def set_board(self,board:Board):
        self._board = board