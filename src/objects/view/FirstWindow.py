import ast
import os

from copy import deepcopy as dc

import ttkbootstrap as ttk

from tkinter import filedialog
from ttkbootstrap import Button
from ttkbootstrap import Label
from ttkbootstrap import LabelFrame
from ttkbootstrap.constants import *
from ttkbootstrap.dialogs.dialogs import Messagebox
from src.objects.controller.constant import _COLUMNS_STOCK
from src.objects.model.db_conn import _DB_PATH
from src.objects.controller.constant import _NAME_STOCK
from src.objects.controller.constant import _MNEMO
from src.objects.controller.constant import _MNEMO_SRC
from src.objects.controller.constant import _LANG
from src.objects.controller.constant import _LANGS
from src.objects.controller.constant import _PORTFOLIO
from src.objects.controller.constant import _active_stock
from src.objects.controller.constant import _TEXTS
from src.objects.controller.logger import log_init as log
from src.objects.view.CRUD import CRUD
from src.objects.view.Lang import Lang
from src.objects.view.Portfolio import Portfolio
from src.objects.view.BDD import BDD
from src.objects.view.Dashboard import Dashboard

global DB_PATH
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

DB_PATH = _DB_PATH
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


class FirstWindow(ttk.Frame):
    global TEXTS
    global ACTIVE_STOCK

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.texts = dc(TEXTS)
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=3)
        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)
        self.rowconfigure(2, weight=1)
        btn_exit = ttk.Button(
            self, text=self.texts[1], bootstyle=PRIMARY, command=self.close_app
        )
        btn_exit.grid(column=1, row=2, sticky=SE, padx=5, pady=5)
        btn_download = ttk.Button(
            self, text=self.texts[24], bootstyle=PRIMARY, command=self.create_dashboard
        )
        btn_download.grid(column=0, row=2, sticky=S, padx=5, pady=5)

    def close_app(self):
        try:
            os.remove(DB_PATH)
        except FileNotFoundError:
            logger.debug("Database is not found")
        finally:
            self.quit()

    def create_save(self):
        global ACTIVE_STOCK
        file = filedialog.asksaveasfilename(
            parent=self, title=self.texts[11], defaultextension=".txt"
        )
        if file:
            with open(file, "w") as f:
                f.write("{\n")
                for it, (key, val) in enumerate(ACTIVE_STOCK.items()):
                    f.write("'" + key + "': " + str(val))
                    if it < len(ACTIVE_STOCK) - 1:
                        f.write(",")
                    if it % 4 == 0:
                        f.write("\n")
                f.write("\n}")

    def create_open(self):
        global ACTIVE_STOCK
        file = filedialog.askopenfilename()
        with open(file, "r") as f:
            content = "".join(f.readlines()).replace("\n", "")
        stocks = ast.literal_eval(content)
        ACTIVE_STOCK = stocks

    def create_new(self):
        global ACTIVE_STOCK
        mes = Messagebox.okcancel(self.texts[18])
        if mes == "OK":
            for key, value in ACTIVE_STOCK.items():
                ACTIVE_STOCK[key] = 0

    def create_apropos(self):
        wd_apropos = ttk.Toplevel(self)
        wd_apropos.wm_title(self.texts[8])
        lbl_soft_name = LabelFrame(wd_apropos, text=self.texts[15])
        lbl_soft_name.pack(fill="both", expand="yes")
        Label(lbl_soft_name, text=self.texts[16]).pack()
        bouton = Button(wd_apropos, text=self.texts[12], command=wd_apropos.destroy)
        bouton.pack()

    def create_portfolio(self):
        self.portfolio = Portfolio(self)

    def create_lang(self):
        self.lang = Lang(self)

    def create_bdd(self):
        self.bdd = BDD(self)

    def crud(self):
        self.crud = CRUD(self)

    def create_dashboard(self):
        self.dashboard = Dashboard(self)
