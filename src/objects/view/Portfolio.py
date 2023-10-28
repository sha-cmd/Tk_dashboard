from copy import deepcopy as dc
import ttkbootstrap as ttk
from ttkbootstrap import Variable
from ttkbootstrap.constants import *
from ttkbootstrap.scrolled import ScrolledFrame

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
from src.objects.view.BDD import BDD

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


class Portfolio(ttk.Toplevel):
    global TEXTS
    global NAME_STOCK
    global PORTFOLIO
    global ACTIVE_STOCK

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.texts = dc(TEXTS)
        self.name_stock: list = dc(NAME_STOCK)
        self.geometry("360x290")
        self.title(self.texts[13])
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=3)
        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)
        self.rowconfigure(2, weight=1)
        self.create_selector()

    def create_selector(self):
        global ACTIVE_STOCK
        sf = ScrolledFrame(self, autohide=True)
        sf.pack(fill=BOTH, expand=YES, padx=10, pady=10)
        self.chckbtton_list = {name: Variable() for name in self.name_stock}
        for it, stock in enumerate(self.name_stock):
            t: ttk.Checkbutton = ttk.Checkbutton(
                sf,
                bootstyle="round-toggle",
                text=f"{stock}",
                variable=self.chckbtton_list[stock],
                state=NORMAL,
                command=lambda val=stock: self.isChecked(val),
            )
            t.pack(anchor=W)
            if int(ACTIVE_STOCK[stock]) == 1:
                self.chckbtton_list[stock].set(1)
            else:
                self.chckbtton_list[stock].set(0)
        self.btn_ok = ttk.Button(self, text=self.texts[2], command=self.make_bdd).pack()

    def make_bdd(self):
        self.bdd = BDD(self)
        self.destroy()

    def isChecked(self, value):
        global ACTIVE_STOCK
        ACTIVE_STOCK[value] = int(self.chckbtton_list[value].get())
        for key, val in ACTIVE_STOCK.items():
            if ACTIVE_STOCK[key] == 1:
                self.chckbtton_list[key].set(1)
            else:
                self.chckbtton_list[key].set(0)
