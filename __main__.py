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

class App(CTk):

    def __init__(app) -> None:
        super().__init__()
        app.geometry("600x700")
        app.resizable(False, False)

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
        app.background.pack(expand=True, fill="both")

        app.mainloop()

app = App()