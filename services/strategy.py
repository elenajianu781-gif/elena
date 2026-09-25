from domain.board import Move
from domain.exceptions import InvalidMoveError

class ComputerStrategy:
    """Defines a common interface for all computer AI strategies
      Inputs
      board: a Board instance representing the current game state
      ai_symbol: the symbol used by the AI player O
      human_symbol: the symbol used by the human player X
      Output
      Returns a Move object representing the AIs chosen move"""
    def choose_move(self, board, ai_symbol, human_symbol):
        raise NotImplementedError


class GreedyWinBlockStrategy(ComputerStrategy):

    # win daca poate,block daca trebuie
    def choose_move(self, board, ai_symbol, human_symbol):
        """Implements the minimum required AI strategy:
           win immediately when possible
           block the human’s immediate win when necessary
           otherwise choose a simple fallback move"""
        # find win move
        m = self._find_winning_move(board, ai_symbol)
        if m is not None:
            return m
        m = self._find_winning_move(board, human_symbol)
        #block
        if m is not None:
            return Move(m.row, m.col, ai_symbol)
        #fallback
        return self._fallback(board, ai_symbol)

    def _find_winning_move(self, board, symbol):
        for (r, c) in board.empty_cells():
            test = Move(r, c, symbol)

            try:
                board.place(test)  # poate arunca invalidmoveerror
            except InvalidMoveError:
                continue

            try:
                if board.check_winner_from(test):
                    return test
            finally:
                board.clear_cell(r, c)  #place and undo

        return None

    def _fallback(self, board,ai_symbol):
        n=board.size
        center=n//2
        if board.is_empty(center,center):
            return Move(center, center,ai_symbol)

        cells = board.empty_cells()
        if not cells:
          raise InvalidMoveError("No moves left.")
        r, c = cells[0]
        return Move(r, c, ai_symbol)
