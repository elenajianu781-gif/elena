import unittest
from domain.board import Board, Move
from repo.board_repo import BoardRepo
from services.game_service import GameService
from domain.exceptions import InvalidMoveError

class TestService(unittest.TestCase):
    def test_game_over_blocks_moves(self):
        board = Board(10)
        repo = BoardRepo(board)
        srv = GameService(repo)

        # facem win direct pt X apoi trebuie sa nu mai permita mutari
        for c in range(5):
            srv.human_move(0, c)

        self.assertTrue(srv.is_over())
        with self.assertRaises(InvalidMoveError):
            srv.human_move(1, 1)

if __name__ == "__main__":
    unittest.main()
