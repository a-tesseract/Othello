from othelloAPI import API
from customtkinter import *
from pywinstyles import *
from os import getlogin, path, makedirs
from PIL import Image

USER = getlogin()
DIR = f"C:\\Users\\{USER}\\AppData\\Local\\Othello"
if not path.exists(DIR): 
    makedirs(DIR)

PATHS = {
    "empty.ico" : DIR+"\\assets\\icons\\empty.ico",
    "Wooden Background.png" : DIR+"\\assets\\images\\Wooden Background.png",
    "Black Peice.png" : DIR+"\\assets\\images\\Black Peice.png",
    "White Peice.png" : DIR+"\\assets\\images\\White Peice.png",
    "Empty Peice.png" : DIR+"\\assets\\images\\Empty Peice.png",
}
Othello = API()

grid = [[None]*8 for i in range(8)]

class App(CTk):

    def __init__(app) -> None:
        super().__init__()
        app.geometry("600x700")
        app.resizable(False, False)

        app.rowconfigure(0, weight=1, uniform="a")
        app.rowconfigure(1, weight=6, uniform="a")
        app.columnconfigure(0, weight=1, uniform="a")

        change_border_color(app, "#48280e")
        change_header_color(app, "#48280e")
        change_title_color(app, "#48280e")

        app.iconbitmap(PATHS["empty.ico"])

        app.background = CTkLabel(
            app,
            text="",
            image=CTkImage(
                Image.open(PATHS["Wooden Background.png"]),
                Image.open(PATHS["Wooden Background.png"]),
                (700, 800)
            ), 
            anchor="center"
        )
        app.background.grid(row=0, column=0, sticky="nsew", rowspan=2)

        app.board = Board(app)
        app.board.grid(row=1, column=0, sticky="nsew", padx=10, pady=10)

        app.mainloop()

class Board(CTkFrame):

    def __init__(board, master: App) -> None:
        super().__init__(
            master,
            fg_color="#202224",
            border_width=10,
            border_color="#202224",
            corner_radius=10,
            bg_color="black"
        )
        set_opacity(board, color="black")

        board.rowconfigure((0, 1, 2, 3, 4, 5, 6, 7), weight=1, uniform="a")
        board.columnconfigure((0, 1, 2, 3, 4, 5, 6, 7), weight=1, uniform="a")

        for _row in range(8):
            for _column in range(8):
                CTkLabel(
                    board,
                    text="",
                    bg_color="#202224",
                    fg_color="#16995f",
                    corner_radius=10
                ).grid(row=_row, column=_column, sticky="nsew", padx=5, pady=5)

        board.makeBoard()

    def makeBoard(board) -> None:

        map_ = Othello.get_board()
        for row, line in enumerate(map_):
            for column, peice in enumerate(line):
                if grid[row][column]:
                    grid[row][column].destroy()
                    grid[row][column] = None

                if peice in "NBW":
                    grid[row][column] = Coin(board, peice, row, column)
                    grid[row][column].grid(row=row, column=column, sticky="nsew", padx=15, pady=15)

                if peice == "N":
                    grid[row][column].bind("<Button>", grid[row][column].N)

class Coin(CTkLabel):

    def __init__(coin, master: Board, peice: str, row: int, column: int) -> None:
        rename = {"W":"White", "B":"Black", "N":"Empty"}

        super().__init__(
            master,
            text="",
            image=CTkImage(
                Image.open(PATHS[f"{rename[peice]} Peice.png"]),
                Image.open(PATHS[f"{rename[peice]} Peice.png"]),
                (42, 42)
            ), 
            fg_color="#16995f",
            anchor="center",
            bg_color="#f0f0f0"
        )
        set_opacity(coin, color="#f0f0f0")
        coin.parent = master

        coin.row = row
        coin.column = column

    def N(coin, _):
        Othello.make_move(coin.row, coin.column)
        coin.parent.makeBoard()

app = App()