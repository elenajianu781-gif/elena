# main.py
import sys
from domain.board import Board
from repo.board_repo import BoardRepo
from services.game_service import GameService
from ui.console_ui import Console
from ui.ui_gui import GomokuGUI
from services.minmax import MinimaxEasyStrategy

def build_service(size=15):
    board = Board(size=size)
    repo = BoardRepo(board)

    service = GameService(repo, human_symbol="X", ai_symbol="O")
    #For AI
    # service = GameService(
    #     repo,
    #     human_symbol="X",
    #     ai_symbol="O",
    #     strategy=MinimaxEasyStrategy(radius=2)
    # )
    return service

def main():
    ui = "console"
    if len(sys.argv) >= 2:
        ui = sys.argv[1].lower()   # "console" sau "gui"

    service = build_service(size=15)

    if ui == "gui":
        GomokuGUI(service).run()
    else:
        Console(service).run()

if __name__ == "__main__":
    main()
