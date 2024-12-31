from customtkinter import *
from pywinstyles import *
from os import getlogin, path, makedirs
from PIL import Image, ImageTk
from pyglet import options, font
from tkmacosx import CircleButton
from webbrowser import open_new_tab

class API:

    def __init__(self):
        self.__board = [
            [" ", " ", " ", " ", " ", " ", " ", " "],
            [" ", " ", " ", " ", " ", " ", " ", " "],
            [" ", " ", " ", " ", " ", " ", " ", " "],
            [" ", " ", " ", "B", "W", " ", " ", " "],
            [" ", " ", " ", "W", "B", " ", " ", " "],
            [" ", " ", " ", " ", " ", " ", " ", " "],
            [" ", " ", " ", " ", " ", " ", " ", " "],
            [" ", " ", " ", " ", " ", " ", " ", " "]
        ]
        self.__previous_board = []
        self.black_move = True

    def get_score(self) -> list[int]:
        white_score = 0
        black_score = 0
        for i in self.__board:
            white_score += i.count("W")
            black_score += i.count("B")

        return [white_score, black_score]

    def __valid_coord(self, x, y) -> bool:
        return 0 <= x <= 7 and 0 <= y <= 7

    def __get_possible_moves(self) -> list[list[int]]:

        possible_move_coordinates = []

        for i in range(8):
            for j in range(8):
                trav_list = self.__check_valid_move(i, j)
                if trav_list:
                    possible_move_coordinates.append([i, j])
        return possible_move_coordinates

    def __check_valid_move(self, row: int, col: int) -> list[list[int]]:
        for i in range(8):
            for j in range(8):
                if self.__board[i][j] == "N":
                    self.__board[i][j] = " "

        if self.__board[row][col] != " ":
            return []
        player = "B" if self.black_move else "W"
        opponent = "B" if not self.black_move else "W"

        traverse_lists = []

        all_possible_directions = [[0, 1], [0, -1], [1, 0], [-1, 0], [1, 1], [1, -1], [-1, 1], [-1, -1]]
        for x, y in all_possible_directions:
            nx = x + row
            ny = y + col

            if self.__valid_coord(nx, ny) and self.__board[nx][ny] == opponent:
                travers_possible = True
                while self.__board[nx][ny] != player:
                    nx += x
                    ny += y
                    if not self.__valid_coord(nx, ny) or self.__board[nx][ny] == " ":
                        travers_possible = False
                        break
                if travers_possible and self.__board[nx][ny] != " ":
                    traverse_lists.append([x, y])

        return traverse_lists

    def make_move(self, row: int, col: int) -> None:
        # self.__previous_board = self.__board.copy()
        self.__previous_board.clear()
        for line in self.__board:
            temp = line.copy()
            self.__previous_board.append(temp)

        traversals = self.__check_valid_move(row, col)
        if not traversals:
            return

        player = "B" if self.black_move else "W"
        for x, y in traversals:
            nx = row + x
            ny = col + y
            while self.__board[nx][ny] != player:
                self.__board[nx][ny] = player
                nx += x
                ny += y

        if self.__get_possible_moves():
            self.black_move = not self.black_move
        self.__board[row][col] = player

    def get_board(self) -> list[list[str]]:
        coordinates = self.__get_possible_moves()
        for x, y in coordinates:
            self.__board[x][y] = "N"

        return self.__board

    def previous_board(self) -> list[list[str]]:
        return self.__previous_board
    
    def reset(self) -> None:
        self.__board = [
            [" ", " ", " ", " ", " ", " ", " ", " "],
            [" ", " ", " ", " ", " ", " ", " ", " "],
            [" ", " ", " ", " ", " ", " ", " ", " "],
            [" ", " ", " ", "B", "W", " ", " ", " "],
            [" ", " ", " ", "W", "B", " ", " ", " "],
            [" ", " ", " ", " ", " ", " ", " ", " "],
            [" ", " ", " ", " ", " ", " ", " ", " "],
            [" ", " ", " ", " ", " ", " ", " ", " "]
        ]
        self.__previous_board = []
        self.black_move = True
    
    def undo(self) -> None:
        self.__board = []
        for line in self.__previous_board:
            self.__board.append(line.copy())
        self.__previous_board = []
        self.black_move = not self.black_move

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
    "JetBrainsMono-Medium.ttf" : DIR+"\\assets\\fonts\\JetBrainsMono-Medium.ttf",
    "GitHub Logo.png" : DIR+"\\assets\\images\\GitHub Logo.png",
    "Board.png" : DIR+"\\assets\\images\\Board.png"
}

options['win32_gdi_font'] = True
font.add_file(PATHS["JetBrainsMono-Bold.ttf"])
font.add_file(PATHS["JetBrainsMono-Light.ttf"])
font.add_file(PATHS["JetBrainsMono-Medium.ttf"])

grid = [[None]*8 for _ in range(8)]

Othello = API()

class App(CTk):

    def __init__(app) -> None:
        super().__init__()
        app.geometry("700x700+10+10")
        app.resizable(False, False)
        app.title("Othello")

        app.rowconfigure(0, weight=1, uniform="a")
        app.rowconfigure(1, weight=6, uniform="a")
        app.columnconfigure(0, weight=1, uniform="a")
        app.columnconfigure(1, weight=6, uniform="a")

        change_border_color(app, "#48280e")
        change_header_color(app, "#48280e")
        change_title_color(app, "#48280e")

        app.iconbitmap(PATHS["empty.ico"])
        app.logo = CTkImage(
            Image.open(PATHS["Logo.png"]),
            Image.open(PATHS["Logo.png"]),
            (35, 35)
        )
        app.githubLogo = ImageTk.PhotoImage(
            Image.open(PATHS["GitHub Logo.png"]).resize((75, 75))
        )

        app.background = CTkLabel(
            app,
            text="",
            image=CTkImage(
                Image.open(PATHS["Wooden Background.png"]),
                Image.open(PATHS["Wooden Background.png"]),
                (800, 800)
            ), 
            anchor="center"
        )
        app.background.grid(row=0, column=0, sticky="nsew", rowspan=2, columnspan=2)

        app.header = Header(app, app.logo)
        app.header.grid(row=0, column=1, sticky="nsew", padx=10, pady=10)

        app.board = Board(app, app.header)
        app.board.grid(row=1, column=1, sticky="nsew", padx=10, pady=10)

        app.extension = Extension(
            app, 
            app.githubLogo, 
            app.board, 
            app.header
        )
        app.extension.grid(row=0, column=0, sticky="nsew", padx=10, pady=10, rowspan=2)

        app.mainloop()

class Extension(CTkFrame):

    def __init__(ext, master: App, logo: ImageTk.PhotoImage, board: "Board", header: "Header") -> None:
        super().__init__(
            master,
            fg_color="#aa7138",
            bg_color="#aa7138"
        )
        set_opacity(ext, color="#aa7138")

        ext.header = header
        ext.board = board

        ext.columnconfigure(0, weight=1, uniform="a")
        ext.rowconfigure(0, weight=3, uniform="a")
        ext.rowconfigure(1, weight=1, uniform="a")
        ext.rowconfigure((2, 3), weight=12, uniform="a")

        ext.github = CircleButton(
            ext,
            borderless=1,
            image=logo,
            bg='#202224',
            focuscolor="#202224",
            radius=40,
            command=lambda: open_new_tab("https://github.com/a-tesseract")
        )
        ext.github.grid(row=0, column=0)

        ext.restartButton = CTkButton(
            ext,
            fg_color="#16995f",
            text="R\nE\nS\nT\nA\nR\nT",
            font=("JetBrains Mono Bold", 25),
            text_color="#202224",
            hover_color="#202224",
            command=ext.restart
        )
        ext.restartButton.bind("<Enter>", lambda _: ext.restartButton.configure(text_color="#16995f", fg_color="#202224"))
        ext.restartButton.bind("<Leave>", lambda _: ext.restartButton.configure(text_color="#202224", fg_color="#16995f"))
        ext.restartButton.grid(row=2, column=0, sticky="nsew", padx=10, pady=5)

        ext.undoButton = CTkButton(
            ext,
            fg_color="#16995f",
            text="U\nN\nD\nO",
            font=("JetBrains Mono Bold", 25),
            text_color="#202224",
            hover_color="#202224",
            command=ext.undo
        )
        ext.undoButton.bind("<Enter>", lambda _: ext.undoButton.configure(text_color="#16995f", fg_color="#202224"))
        ext.undoButton.bind("<Leave>", lambda _: ext.undoButton.configure(text_color="#202224", fg_color="#16995f"))
        ext.undoButton.grid(row=3, column=0, sticky="nsew", padx=10, pady=5)

    def restart(ext) -> None:    
        if sum(Othello.get_score()) != 4:
            for row in range(8):
                for column in range(8):
                    if grid[row][column] != None:
                        grid[row][column].destroy()
                        grid[row][column] = None

            Othello.reset()
            ext.board.makeBoard()

            ext.header.toPlay.switchPlay()

            ext.header.blackScore.scoreVar.set(2)
            ext.header.whiteScore.scoreVar.set(2)

    def undo(ext) -> None:
        if Othello.previous_board():
            for row in range(8):
                for column in range(8):
                    if grid[row][column] != None:
                        grid[row][column].destroy()
                        grid[row][column] = None

            Othello.undo()
            ext.board.makeBoard()

            ext.header.toPlay.switchPlay()

            ext.header.blackScore.scoreVar.set(Othello.get_score()[1])
            ext.header.whiteScore.scoreVar.set(Othello.get_score()[0])

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
        header.name.bind("<Button>", lambda _: open_new_tab("https://github.com/a-tesseract/Othello"))
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
            text_color="#eff1f5",
            font=("JetBrains Mono Bold", 20),
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

    def winner(card, winner: str) -> None:
        card.configure(border_color="#000000" if winner == "black" else "#eff1f5")
        card.nameVar.set("BLACK" if winner == "black" else "WHITE")
        card.name.configure(text_color="#eff1f5" if winner == "black" else "#000000")
        card.name.configure(fg_color="#000000" if winner == "black" else "#eff1f5")
        card.subtext.configure(text_color="#000000" if winner == "black" else "#eff1f5")
        card.subtext.configure(text="WINS")

    def tie(card, turn: str) -> None:
        card.configure(border_color="#000000" if turn == "black" else "#eff1f5")
        card.nameVar.set("TIE")
        card.name.configure(text_color="#eff1f5" if turn == "black" else "#000000")
        card.name.configure(fg_color="#000000" if turn == "black" else "#eff1f5")
        card.subtext.configure(text_color="#000000" if turn == "black" else "#eff1f5")
        card.subtext.configure(text="IT'S A")

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
        board.parent = master

        set_opacity(board, color="black")

        board.rowconfigure((0, 1, 2, 3, 4, 5, 6, 7), weight=1, uniform="a")
        board.columnconfigure((0, 1, 2, 3, 4, 5, 6, 7), weight=1, uniform="a")

        board.board = CTkLabel(
            board,
            image=CTkImage(
                Image.open(PATHS["Board.png"]),
                Image.open(PATHS["Board.png"]),
                (580, 579)
            ),
            text=""
        )
        board.board.place(relx=0, rely=0, relwidth=1, relheight=1)

        board.makeBoard()

    def makeBoard(board) -> None:
        n = False
        for _ in Othello.get_board():
            for __ in _:
                if __ == "N": n = True
        if not n:
            Othello.black_move = not Othello.black_move

        board.header.toPlay.switchPlay()

        for row in range(8):
            for col in  range(8):
                if grid[row][col]:
                    if grid[row][col].peice == "N":
                        grid[row][col].destroy()
                        grid[row][col] = None

        for row, line in enumerate(Othello.get_board()):
            for column, peice in enumerate(line):
                if peice in "BW":
                    if grid[row][column]:
                        if grid[row][column].peice == peice:
                            continue
                        else: 
                            grid[row][column].destroy()
                    grid[row][column] = Coin(board, peice, row, column)
                    grid[row][column].grid(row=row, column=column, sticky="nsew", padx=15, pady=15)

                elif peice == "N":
                    grid[row][column] = Coin(board, peice, row, column)
                    grid[row][column].grid(row=row, column=column, sticky="nsew", padx=15, pady=15)
                    grid[row][column].bind("<Button>", grid[row][column].button)

        board.header.blackScore.scoreVar.set(Othello.get_score()[1])
        board.header.whiteScore.scoreVar.set(Othello.get_score()[0])

        if sum(Othello.get_score()) == 64 or min(Othello.get_score()) == 0:
            if Othello.get_score()[0] == Othello.get_score()[1]:
                turn = "white" if Othello.black_move else "black"

                board.tieScreen = TieScreen(
                    board, 
                    turn
                )
                board.tieScreen.place(relx=0, rely=0, relheight=1, relwidth=1)

                board.header.toPlay.tie(turn)
            else:
                winner = "white" if Othello.get_score()[0] > Othello.get_score()[1] else "black"

                board.winScreen = WinScreen(
                    board, 
                    winner
                )
                board.winScreen.place(relx=0, rely=0, relheight=1, relwidth=1)

                board.header.toPlay.winner(winner)

class TieScreen(CTkFrame):

    def __init__(screen, master: Board, turn: str) -> None:
        super().__init__(
            master,
            fg_color="#eff1f5" if turn == "white" else "#000000",
            corner_radius=10
        )
        set_opacity(screen, 0.8)

        screen.winner = CTkLabel(
            screen,
            font=("JetBrains Mono Bold", 100),
            text="TIE",
            text_color="#eff1f5" if turn == "black" else "#000000",
            fg_color="#eff1f5" if turn == "white" else "#000000",
        )
        screen.winner.place(relx=0.5, rely=0.56, anchor="center")

        screen.sub = CTkLabel(
            screen,
            font=("JetBrains Mono Medium", 40),
            text="IT'S A",
            text_color="#eff1f5" if turn == "black" else "#000000",
            fg_color="#eff1f5" if turn == "white" else "#000000",
        )
        screen.sub.place(relx=0.5, rely=0.44, anchor="center")

class WinScreen(CTkFrame):

    def __init__(screen, master: Board, winner: str) -> None:
        super().__init__(
            master,
            fg_color="#eff1f5" if winner == "white" else "#000000",
            corner_radius=10
        )
        set_opacity(screen, 0.8)

        screen.winner = CTkLabel(
            screen,
            font=("JetBrains Mono Bold", 100),
            text=winner.upper(),
            text_color="#eff1f5" if winner == "black" else "#000000",
            fg_color="#eff1f5" if winner == "white" else "#000000",
        )
        screen.winner.place(relx=0.5, rely=0.44, anchor="center")

        screen.sub = CTkLabel(
            screen,
            font=("JetBrains Mono Medium", 40),
            text="WINS",
            text_color="#eff1f5" if winner == "black" else "#000000",
            fg_color="#eff1f5" if winner == "white" else "#000000",
        )
        screen.sub.place(relx=0.5, rely=0.56, anchor="center")

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

        coin.peice = peice

    def button(coin, _):
        Othello.make_move(coin.row, coin.column)
        coin.configure(
            image=CTkImage(
                Image.open(PATHS[f"{"Black" if Othello.black_move else "White"} Peice.png"]),
                Image.open(PATHS[f"{"Black" if Othello.black_move else "White"} Peice.png"]),
                (42, 42)
            ), 
        )
        coin.peice = "B" if Othello.black_move else "W"
        coin.parent.makeBoard()

app = App()