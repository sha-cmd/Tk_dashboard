import ast
import os

from copy import deepcopy as dc

import ttkbootstrap as ttk

from ttkbootstrap.constants import *
from ttkbootstrap.dialogs.dialogs import Messagebox

from src.objects.controller.constant import get_lang
from src.objects.controller.constant import get_config
from src.objects.controller.constant import set_config
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

class Lang(ttk.Toplevel):
    global TEXTS
    global LANGS
    global LANG

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # application variables
        self.texts = dc(TEXTS)
        self.langs = dc(LANGS)
        self.title(self.texts[5])
        self.create_legend()
        self.create_menu()
        self.cbbx_langs.pack(fill=BOTH, expand=YES)
        self.select_button()
        self.btn_select.pack(fill=BOTH, expand=YES)
        self.cancel_button()
        self.btn_cancel.pack(fill=BOTH, expand=YES)

    def create_legend(self):
        l1 = ttk.Label(self, text=self.texts[6], anchor=N)
        l1.pack(fill=X)

    def create_menu(self):
        self.cbbx_langs = ttk.Combobox(
            self,
            values=self.langs,
            textvariable=LANG,
            state="readonly",
            bootstyle=PRIMARY,
            postcommand=get_lang,
        )

    def change_language(self):
        config = get_config()
        try:
            config["LANGUAGE"]["DEFAULT"] = (
                self.cbbx_langs.get().split("-")[1].strip().upper()
            )
            set_config(config)
            Messagebox.ok(self.texts[14])
            self.destroy()
        except IndexError:
            pass

    def select_button(self):
        self.btn_select = ttk.Button(
            self, text=self.texts[3], command=self.change_language
        )

    def cancel_button(self):
        self.btn_cancel = ttk.Button(self, text=self.texts[4], command=self.destroy)
