import unittest
from domain.board import Board, Move
from domain.exceptions import InvalidMoveError

class TestBoard(unittest.TestCase):
    def test_place_and_get(self):
        b = Board(5)
        b.place(Move(0, 0, "X"))
        self.assertEqual(b.get_cell(0, 0), "X")

    def test_occupied_cell(self):
        b = Board(5)
        b.place(Move(0, 0, "X"))
        with self.assertRaises(InvalidMoveError):
            b.place(Move(0, 0, "O"))

    def test_out_of_bounds(self):
        b = Board(5)
        with self.assertRaises(InvalidMoveError):
            b.place(Move(5, 0, "X"))

    def test_winner_horizontal(self):
        b = Board(10)
        for c in range(5):
            b.place(Move(0, c, "X"))
        self.assertTrue(b.check_winner_from(Move(0, 4, "X")))

    def test_not_winner_4(self):
        b = Board(10)
        for c in range(4):
            b.place(Move(0, c, "X"))
        self.assertFalse(b.check_winner_from(Move(0, 3, "X")))

    def test_winner_vertical(self):
        b = Board(10)
        for r in range(5):
            b.place(Move(r, 3, "X"))
        self.assertTrue(b.check_winner_from(Move(4, 3, "X")))

    def test_winner_diag_main(self):
        b = Board(10)
        for i in range(5):
            b.place(Move(i, i, "X"))
        self.assertTrue(b.check_winner_from(Move(4, 4, "X")))

    def test_winner_diag_anti(self):
        b = Board(10)
        # (0,4)(1,3)(2,2)(3,1)(4,0)
        for i in range(5):
            b.place(Move(i, 4 - i, "X"))
        self.assertTrue(b.check_winner_from(Move(4, 0, "X")))

    def test_winner_through_middle(self):
        b = Board(10)
        # XXXXX cu mutarea "verificată" în mijloc (0,2)
        for c in range(5):
            b.place(Move(0, c, "X"))
        self.assertTrue(b.check_winner_from(Move(0, 2, "X")))

    def test_winner_more_than_five(self):
        b = Board(10)
        for c in range(6):
            b.place(Move(1, c, "X"))  # 6 la rând
        self.assertTrue(b.check_winner_from(Move(1, 5, "X")))

if __name__ == "__main__":
    unittest.main()