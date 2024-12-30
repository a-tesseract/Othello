from othelloAPI import API
from customtkinter import *
from pywinstyles import *
from os import getlogin, path, makedirs
from PIL import Image
from pyglet import options, font

USER = getlogin()
DIR = f"C:\\Users\\{USER}\\AppData\\Local\\Othello"
if not path.exists(DIR): 
    makedirs(DIR)

PATHS = {
    "empty.ico" : DIR+"\\assets\\icons\\empty.ico",
    "Wooden Background.png" : DIR+"\\assets\\images\\Wooden Background.png",
    "Black Peice.png" : DIR+"\\assets\\images\\Black Peice.png",
    "White Peice.png" : DIR+"\\assets\\images\\White Peice.png",
    "White Empty Peice.png" : DIR+"\\assets\\images\\White Empty Peice.png",
    "Black Empty Peice.png" : DIR+"\\assets\\images\\Black Empty Peice.png",
    "Logo.png" : DIR+"\\assets\\icons\\Logo.png",
    "JetBrainsMono-Bold.ttf" : DIR+"\\assets\\fonts\\JetBrainsMono-Bold.ttf",
    "JetBrainsMono-Light.ttf" : DIR+"\\assets\\fonts\\JetBrainsMono-Light.ttf",
    "JetBrainsMono-Medium.ttf" : DIR+"\\assets\\fonts\\JetBrainsMono-Medium.ttf"
}

options['win32_gdi_font'] = True
font.add_file(PATHS["JetBrainsMono-Bold.ttf"])
font.add_file(PATHS["JetBrainsMono-Light.ttf"])
font.add_file(PATHS["JetBrainsMono-Medium.ttf"])

grid = [[None]*8 for i in range(8)]

Othello = API()

class App(CTk):

    def __init__(app) -> None:
        super().__init__()
        app.geometry("600x700+10+10")
        app.resizable(False, False)

        app.rowconfigure(0, weight=1, uniform="a")
        app.rowconfigure(1, weight=6, uniform="a")
        app.columnconfigure(0, weight=1, uniform="a")

        change_border_color(app, "#48280e")
        change_header_color(app, "#48280e")
        change_title_color(app, "#48280e")

        app.iconbitmap(PATHS["empty.ico"])
        app.logo = CTkImage(
            Image.open(PATHS["Logo.png"]),
            Image.open(PATHS["Logo.png"]),
            (35, 35)
        )

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

        app.header = Header(
            app,
            app.logo
        )
        app.header.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)

        app.board = Board(app, app.header)
        app.board.grid(row=1, column=0, sticky="nsew", padx=10, pady=10)

        app.mainloop()

class Header(CTkFrame):

    def __init__(header, master: App, logo: Image) -> None:
        super().__init__(
            master,
            fg_color="#aa7138",
            bg_color="#aa7138"
        )
        set_opacity(header, color="#aa7138")

        header.columnconfigure(0, weight=16, uniform="a")
        header.columnconfigure(1, weight=7, uniform="a")
        header.columnconfigure((2, 3), weight=4, uniform="a")
        header.rowconfigure(0, weight=1, uniform="a")

        header.name = Name(header, logo)
        header.name.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)

        header.toPlay = ToPlay(header)
        header.toPlay.grid(row=0, column=1, sticky="nsew", padx=10, pady=10)

        header.whiteScore = Score(header, True)
        header.whiteScore.grid(row=0, column=2, sticky="nsew", padx=7, pady=10)

        header.blackScore = Score(header, False)
        header.blackScore.grid(row=0, column=3, sticky="nsew", padx=7, pady=10)

class Name(CTkFrame):

    def __init__(name, master: Header, logo: Image) -> None:
        super().__init__(
            master,
            fg_color="#16995f",
            corner_radius=10
        )

        name.columnconfigure(0, weight=1)
        name.columnconfigure(1, weight=3)
        name.rowconfigure(0, weight=1)

        name.logo = CTkLabel(
            name,
            text="",
            image=logo,
            anchor="center"
        )
        name.logo.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)

        name.name = CTkLabel(
            name,
            text="Othello",
            font=("JetBrains Mono Bold", 50),
            text_color="#202224"
        )
        name.name.grid(row=0, column=1, sticky="nsew", padx=10, pady=10)

class Score(CTkFrame):

    def __init__(card, master: Header, white: bool) -> None:
        super().__init__(
            master,
            border_width=4,
            border_color="#eff1f5" if white else "#000000",
            fg_color="#16995f"
        )

        card.rowconfigure(0, weight=1, uniform="a")
        card.rowconfigure(1, weight=3, uniform="a")
        card.rowconfigure(2, weight=5, uniform="a")
        card.rowconfigure(3, weight=3, uniform="a")
        card.rowconfigure(4, weight=1, uniform="a")
        card.columnconfigure(0, weight=1, uniform="a")

        card.up = CTkLabel(
            card,
            text=f"{"WHITE" if white else "BLACK"} HAS",
            fg_color="#16995f",
            font=("JetBrains Mono Light", 9),
            text_color="#eff1f5" if white else "#000000"
        )
        set_opacity(card.up, color="#16995f")
        card.up.grid(column=0, row=1, sticky="new")

        card.scoreVar = IntVar(value=2)
        card.score = CTkLabel(
            card,
            textvariable=card.scoreVar,
            font=("JetBrains Mono Medium", 20),
            text_color="#eff1f5" if white else "#000000"
        )
        card.score.grid(column=0, row=2, sticky="snew")

        card.down = CTkLabel(
            card,
            text="COINS",
            fg_color="#16995f",
            font=("JetBrains Mono Light", 9),
            text_color="#eff1f5" if white else "#000000"
        )
        set_opacity(card.down, color="#16995f")
        card.down.grid(column=0, row=3, sticky="sew")

class ToPlay(CTkFrame):

    def __init__(card, master: Header) -> None:
        super().__init__(
            master,
            border_width=5,
            border_color="#000000",
            fg_color="#16995f"
        )

        card.rowconfigure(0, weight=2, uniform="a")
        card.rowconfigure(1, weight=8, uniform="a")
        card.rowconfigure(2, weight=3, uniform="a")
        card.rowconfigure(3, weight=2, uniform="a")
        card.columnconfigure(0, weight=1, uniform="a")

        card.nameVar = StringVar(value="BLACK")
        card.name = CTkLabel(
            card,
            textvariable=card.nameVar,
            fg_color="#000000",
            font=("JetBrains Mono Bold", 20),
            text_color="#eff1f5",
            corner_radius=5
        )
        set_opacity(card.name, color="#16995f")
        card.name.grid(column=0, row=1, sticky="nsew", padx=10,)

        card.subtext = CTkLabel(
            card,
            text="TO PLAY",
            fg_color="#16995f",
            font=("JetBrains Mono Light", 10),
            text_color="#000000"
        )
        set_opacity(card.subtext, color="#16995f")
        card.subtext.grid(column=0, row=2, sticky="new")

    def switchPlay(card) -> None:
        card.configure(border_color="#000000" if Othello.black_move else "#eff1f5")
        card.nameVar.set("BLACK" if Othello.black_move else "WHITE")
        card.name.configure(text_color="#eff1f5" if Othello.black_move else "#000000")
        card.name.configure(fg_color="#000000" if Othello.black_move else "#eff1f5")
        card.subtext.configure(text_color="#000000" if Othello.black_move else "#eff1f5")

class Board(CTkFrame):

    def __init__(board, master: App, header: Header) -> None:
        super().__init__(
            master,
            fg_color="#202224",
            border_width=10,
            border_color="#202224",
            corner_radius=10,
            bg_color="black"
        )
        board.header = header

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
        n = False
        for _ in Othello.get_board():
            for __ in _:
                if __ == "N": n = True
        if not n:
            Othello.black_move = not Othello.black_move

        board.header.toPlay.switchPlay()

        for row, line in enumerate(Othello.get_board()):
            for column, peice in enumerate(line):
                if grid[row][column]:
                    grid[row][column].destroy()
                    grid[row][column] = None

                if peice in "NBW":
                    grid[row][column] = Coin(board, peice, row, column)
                    grid[row][column].grid(row=row, column=column, sticky="nsew", padx=15, pady=15)

                if peice == "N":
                    grid[row][column].bind("<Button>", grid[row][column].button)

        board.header.blackScore.scoreVar.set(Othello.get_score()[1])
        board.header.whiteScore.scoreVar.set(Othello.get_score()[0])

        if sum(Othello.get_score()) == 64 or min(Othello.get_score()) == 0:
            if Othello.get_score()[0] == Othello.get_score()[1]:
                print("Tie")
            else:
                print("White" if Othello.get_score()[0] > Othello.get_score()[1] else "Black", "wins")

class Coin(CTkLabel):

    def __init__(coin, master: Board, peice: str, row: int, column: int) -> None:
        rename = {"W":"White", "B":"Black", "N":("Black Empty" if Othello.black_move else "White Empty")}

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
            bg_color="#16995f"
        )
        set_opacity(coin, color="#f0f0f0")
        coin.parent = master

        coin.row = row
        coin.column = column

    def button(coin, _):
        Othello.make_move(coin.row, coin.column)
        coin.parent.makeBoard()

app = App()