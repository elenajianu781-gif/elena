import unittest
from domain.board import Board, Move
from services.strategy import GreedyWinBlockStrategy

class TestAI(unittest.TestCase):
    def test_ai_wins(self):
        b = Board(10)
        ai = "O"
        human = "X"
        for c in range(4):
            b.place(Move(0, c, ai))  # OOOO
        strat = GreedyWinBlockStrategy()
        m = strat.choose_move(b, ai, human)
        self.assertEqual((m.row, m.col), (0, 4))

    def test_ai_blocks(self):
        b = Board(10)
        ai = "O"
        human = "X"
        for c in range(4):
            b.place(Move(2, c, human))  # XXXX
        strat = GreedyWinBlockStrategy()
        m = strat.choose_move(b, ai, human)
        self.assertEqual((m.row, m.col), (2, 4))
        self.assertEqual(m.symbol, ai)

if __name__ == "__main__":
    unittest.main()