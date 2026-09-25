import tkinter as tk
from tkinter import messagebox
from domain.exceptions import InvalidMoveError

class GomokuGUI:
    def __init__(self, service):
        self._srv = service
        self._n = self._srv.board.size

        self._root = tk.Tk() #creeaza fereastra aplicatiei
        self._root.title("Gomoku") #titlul

        # status label
        self._status = tk.Label(self._root, text="Your turn (X)") #textul din fereastra
        self._status.pack(pady=6) #pun sus vertical

        # frame for grid buttons
        self._grid_frame = tk.Frame(self._root) #frame ul pt grila
        self._grid_frame.pack(padx=8, pady=8)  #spatiu in jur axe x si y

        self._buttons = [[None for _ in range(self._n)] for _ in range(self._n)]
        for r in range(self._n):
            for c in range(self._n):
                btn = tk.Button(
                    self._grid_frame,
                    text=".",
                    width=2,
                    height=1,
                    command=lambda rr=r, cc=c: self._on_cell_click(rr, cc)
                )
                btn.grid(row=r, column=c)
                self._buttons[r][c] = btn  #pt fiecare coordonata creez un buton

        # reset buton
        self._reset_btn = tk.Button(self._root, text="Reset (restart app for now)", command=self._not_implemented)
        self._reset_btn.pack(pady=6)

        self._refresh_board()

    def run(self):
        self._root.mainloop()

    def _on_cell_click(self, r, c):
        if self._srv.is_over():
            return

        # human move
        try:
            self._srv.human_move(r, c)
        except InvalidMoveError as e:
            messagebox.showwarning("Invalid move", str(e))
            return

        self._refresh_board()
        if self._handle_end_if_any():
            return

        # computer move
        self._srv.computer_move()
        self._refresh_board()
        self._handle_end_if_any()

    def _refresh_board(self):
        b = self._srv.board
        for r in range(self._n):
            for c in range(self._n):
                val = b.get_cell(r, c)
                self._buttons[r][c]["text"] = val
                # optional: disable occupied cells
                if val != ".":
                    self._buttons[r][c]["state"] = "disabled"
                else:
                    self._buttons[r][c]["state"] = "normal"

    def _handle_end_if_any(self):
        res = self._srv.result()
        if not self._srv.is_over():
            self._status.config(text="Your turn (X)")
            return False

        if res.draw:
            self._status.config(text="Draw!")
            messagebox.showinfo("Game Over", "Draw!")
        else:
            if res.winner == self._srv.human_symbol():
                self._status.config(text="You win!")
                messagebox.showinfo("Game Over", "You win!")
            else:
                self._status.config(text="Computer wins!")
                messagebox.showinfo("Game Over", "Computer wins!")

        #disable all buttons at end
        for r in range(self._n):
            for c in range(self._n):
                self._buttons[r][c]["state"] = "disabled"
        return True

    def _not_implemented(self):
        messagebox.showinfo("Info", "Simplu: pentru reset, repornești aplicația.\n(Poți implementa reset ca bonus extra.)")