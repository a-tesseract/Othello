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
    "Wooden Background.png" : DIR+"\\assets\\images\\Wooden Background.png"
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
        for i in range(8):
            for j in range(8):
                if grid[i][j]:
                    grid[i][j].grid_forget()
                    grid[i][j] = None

        for row, line in enumerate(Othello.get_board()):
            for column, peice in enumerate(line):
                match peice:

                    case "W": 
                        grid[row][column] = Coin(board, "W", row, column)
                        grid[row][column].grid(row=row, column=column, sticky="nsew", padx=15, pady=15)

                    case "B": 
                        grid[row][column] = Coin(board, "B", row, column)
                        grid[row][column].grid(row=row, column=column, sticky="nsew", padx=15, pady=15)

                    case "N": 
                        grid[row][column] = Coin(board, "N", row, column)
                        grid[row][column].bind("<Button>", grid[row][column].N)
                        grid[row][column].grid(row=row, column=column, sticky="nsew", padx=15, pady=15)

class Coin(CTkCanvas):

    def __init__(coin, master: Board, peice: str, row: int, column: int) -> None:
        super().__init__(
            master,
            bg="#16995f",
            bd=0
        )
        set_opacity(coin, color="#f0f0f0")
        coin.parent = master

        coin.row = row
        coin.column = column

        dash = (1, 1)
        width = 0
        outline = "white"
        if peice == "W":
            fill = "white"
        elif peice == "B":
            fill = "black"
        else:
            fill = "#16995f"
            width = 5

        coin.create_oval(
            3, 3, 55, 55, 
            fill=fill,
            outline=outline,
            width=width,
            dash=dash
        )

    def N(coin, _):
        Othello.make_move(coin.row, coin.column)
        coin.parent.makeBoard()

app = App()