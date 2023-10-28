from copy import deepcopy as dc

import tkinter
import ttkbootstrap as ttk

from ttkbootstrap import Style

from src.objects.controller.constant import _COLUMNS_STOCK
from src.objects.controller.constant import _NAME_STOCK
from src.objects.controller.constant import _MNEMO
from src.objects.controller.constant import _MNEMO_SRC
from src.objects.controller.constant import _LANG
from src.objects.controller.constant import _LANGS
from src.objects.controller.constant import _PORTFOLIO
from src.objects.controller.constant import _active_stock
from src.objects.controller.constant import _TEXTS
from src.objects.controller.logger import log_init as log
from src.objects.view.FirstWindow import FirstWindow

global LANG
global LANGS
global MNEMO
global MNEMO_SRC
global COLUMNS_STOCK
global NAME_STOCK
global PORTFOLIO
global TEXTS
global ACTIVE_STOCK
global SELECTED_TABLE

LANG = _LANG
LANGS = _LANGS
MNEMO = _MNEMO
MNEMO_SRC = _MNEMO_SRC
COLUMNS_STOCK = _COLUMNS_STOCK
NAME_STOCK = _NAME_STOCK
PORTFOLIO = _PORTFOLIO
TEXTS = _TEXTS
ACTIVE_STOCK = _active_stock

logger = log()


class Application(tkinter.Tk):
    global TEXTS
    global LANGS

    def __init__(self):
        super().__init__()
        self.texts = dc(TEXTS)
        self.langs = dc(LANGS)
        self.geometry("360x290")
        self.title(self.texts[15])
        self.resizable(0, 0)

        self.style = Style("sandstone")

        self.first_wd = FirstWindow(self, padding=10)
        self.first_wd.pack(fill="both", expand="yes")

        menubar = ttk.Menu()
        self.config(menu=menubar)

        file_menu = ttk.Menu(menubar)
        portfolio_menu = ttk.Menu(menubar)
        database_menu = ttk.Menu(menubar)
        help_menu = ttk.Menu(menubar)

        menubar.add_cascade(menu=file_menu, label=self.texts[0])
        menubar.add_cascade(menu=portfolio_menu, label=self.texts[13])
        menubar.add_cascade(menu=database_menu, label=self.texts[20])
        menubar.add_cascade(menu=help_menu, label=self.texts[9])

        file_menu.add_command(label=self.texts[7], command=self.first_wd.create_new)
        file_menu.add_command(label=self.texts[11], command=self.first_wd.create_save)
        file_menu.add_command(label=self.texts[10], command=self.first_wd.create_open)
        file_menu.add_command(label=self.texts[12], command=self.destroy)
        file_menu.add_command(label=self.texts[1], command=self.destroy)

        portfolio_menu.add_command(
            label=self.texts[19], command=self.first_wd.create_portfolio
        )

        database_menu.add_command(label=self.texts[22], command=self.first_wd.crud)

        help_menu.add_command(label=self.texts[8], command=self.first_wd.create_apropos)
        help_menu.add_command(label=self.texts[5], command=self.first_wd.create_lang)
