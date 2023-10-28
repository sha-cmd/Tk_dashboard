from copy import deepcopy as dc

import pandas as pd
import ttkbootstrap as ttk

from sqlalchemy import (
    inspect,
    text,
)
from ttkbootstrap.constants import *
from src.objects.controller.constant import _COLUMNS_STOCK
from src.objects.controller.constant import _NAME_STOCK
from src.objects.controller.constant import _MNEMO
from src.objects.controller.constant import _MNEMO_SRC
from src.objects.controller.constant import _LANG
from src.objects.controller.constant import _LANGS
from src.objects.controller.constant import _PORTFOLIO
from src.objects.controller.constant import _active_stock
from src.objects.controller.constant import _TEXTS
from src.objects.controller.Downloader import Downloader
from src.objects.controller.logger import log_init as log
from src.objects.controller.Ticket import Ticket
from src.objects.model.db_conn import SingletonDBconnect

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


class BDD(ttk.Toplevel):
    global TEXTS
    global COLUMNS_STOCK
    global NAME_STOCK
    global PORTFOLIO
    global ACTIVE_STOCK

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.prog_value = 0
        self.columns_stock = dc(COLUMNS_STOCK)
        self.texts = dc(TEXTS)
        self.name_stock: list = dc(NAME_STOCK)
        self.geometry("360x290")
        self.title(self.texts[21])
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=3)
        self.columnconfigure(2, weight=1)
        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)
        self.create_bdd()

    def create_bdd(self):
        global ACTIVE_STOCK
        self.lbl = ttk.Label(
            master=self, textvariable="prog-message", font="Helvetica 10 bold"
        )
        self.lbl.grid(row=0, column=1, columnspan=1, sticky=W)
        self.setvar("prog-message", self.texts[21])
        self.pb = ttk.Progressbar(
            master=self,
            variable="prog-value",
            bootstyle=SUCCESS,
            length=100,
            mode="determinate",
        )
        self.pb.grid(row=1, column=1, columnspan=1, sticky=EW, pady=(10, 5))
        db = SingletonDBconnect()
        inspector = inspect(db.engine)
        tables = inspector.get_table_names()
        print(tables)
        for stock, active in ACTIVE_STOCK.items():
            if int(active) == 0 and stock.lower().replace(" ", "_") in tables:
                print(stock, active)
                with db.engine.connect() as conn:
                    sql = text(
                        f"DROP TABLE IF EXISTS {stock.lower().replace(' ', '_')};"
                    )
                    conn.execute(sql)
        self.download_portfolio()
        self.destroy()

    def download_portfolio(self):
        global MNEMO_SRC
        global ACTIVE_STOCK
        global TEXTS
        df: pd.DataFrame = pd.read_csv(MNEMO_SRC, sep=";")
        df_ = pd.DataFrame()
        for it, (key, val) in enumerate(ACTIVE_STOCK.items()):
            if int(val) == 1:
                df_ = pd.concat(
                    [df_, df.loc[df[self.columns_stock[0]] == key]], ignore_index=True
                )
        df_.reset_index(drop=True, inplace=True)
        for it, row in df_.iterrows():
            df_stk_ct = len(df_)
            self.lbl.setvar("prog-message", TEXTS[23] + row["name"])
            self.pb["value"] = (100 / df_stk_ct) * (int(it) + 1)
            self.update_idletasks()
            tck = Ticket(row["name"])
            Downloader(tck)
