from domain.board import Move, EMPTY
from domain.exceptions import InvalidMoveError
from services.strategy import ComputerStrategy

class MinimaxEasyStrategy(ComputerStrategy):
    def __init__(self, radius=2):
        self._radius = radius


