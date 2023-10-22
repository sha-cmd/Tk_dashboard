import ast
import os

from copy import deepcopy as dc

import pandas as pd
import sqlalchemy.exc
import tkinter
import ttkbootstrap as ttk

from sqlalchemy import (
    select,
    insert,
    inspect,
    update,
    text,
    delete,
    Table,
    MetaData,
    Column,
    String,
    Float,
    BigInteger,
)
from tkinter import filedialog
from ttkbootstrap import Button
from ttkbootstrap import Entry
from ttkbootstrap import Label
from ttkbootstrap import LabelFrame
from ttkbootstrap import Style
from ttkbootstrap import Variable
from ttkbootstrap.constants import *
from ttkbootstrap.dialogs.dialogs import Messagebox
from ttkbootstrap.scrolled import ScrolledFrame

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
            self, text=self.texts[21], bootstyle=PRIMARY, command=self.create_bdd
        )
        btn_download.grid(column=0, row=2, sticky=S, padx=5, pady=5)

    def close_app(self):
        try:
            os.remove("bdd/Databases.Stocks")
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
                    f.write("'" + key + "': '" + str(val) + "'")
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


class CRUD(ttk.Toplevel):
    global TEXTS
    global COLUMNS_STOCK
    global NAME_STOCK
    global PORTFOLIO
    global ACTIVE_STOCK
    global SELECTED_TABLE

    def __init__(self, *args, **kwargs):
        global SELECTED_TABLE
        super().__init__(*args, **kwargs)
        self.prog_value = 0
        self.columns_stock = dc(COLUMNS_STOCK)
        self.texts = dc(TEXTS)
        self.name_stock: list = dc(NAME_STOCK)
        self.geometry("360x290")
        self.title(self.texts[22])
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=3)
        self.columnconfigure(2, weight=1)
        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)
        self.rowconfigure(2, weight=1)
        db = SingletonDBconnect()
        inspector = inspect(db.engine)
        self.table_names = inspector.get_table_names()
        SELECTED_TABLE = self.table_names[0]
        self.create_crud()

    def create_crud(self):
        global SELECTED_TABLE
        self.title("Stock Action")
        self.geometry("1000x650+451+274")
        self.lblDate = Label(
            self,
            text="date",
            font=("Helvetica", 10),
        )
        self.lblOpen = Label(
            self,
            text="open",
            font=("Helvetica", 10),
        )
        self.lblHigh = Label(
            self,
            text="high",
            font=("Helvetica", 10),
        )
        self.lblLow = Label(
            self,
            text="low",
            font=("Helvetica", 10),
        )
        self.lblClose = Label(
            self,
            text="close",
            font=("Helvetica", 10),
        )
        self.lblVolume = Label(
            self,
            text="volume",
            font=("Helvetica", 10),
        )
        self.entDate = Entry(self)
        self.entOpen = Entry(self)
        self.entHigh = Entry(self)
        self.entLow = Entry(self)
        self.entClose = Entry(self)
        self.entVolume = Entry(self)
        self.entSelect = Entry(self)
        self.entSearch = Entry(self)
        self.btn_insert = Button(
            self,
            text="Insert",
            command=self.insert,
        )
        self.btn_clear = Button(
            self,
            text="Clear",
            command=self.clear_form,
        )
        self.btn_delete = Button(
            self,
            text="Delete",
            command=self.delete,
        )
        self.btn_update = Button(
            self,
            text="Update",
            command=self.update,
        )

        self.select_stocks = ttk.Combobox(
            self,
            values=self.table_names,
            textvariable=SELECTED_TABLE,
            state="readonly",
            bootstyle=PRIMARY,
        )
        self.select_stocks.set(SELECTED_TABLE)
        self.btn_load = Button(
            self,
            text="Load",
            command=self.load_stock_data,
        )

        self.btn_ok = Button(
            self,
            text="OK",
            command=self.destroy,
        )
        columns = ("#1", "#2", "#3", "#4", "#5", "#6")
        self.stocks = ttk.Treeview(self, show="headings", height="6", columns=columns)
        self.stocks.heading("#1", text="date", anchor="center")
        self.stocks.column("#1", width=60, anchor="center", stretch=True)
        self.stocks.heading("#2", text="open", anchor="center")
        self.stocks.column("#2", width=75, anchor="center", stretch=True)
        self.stocks.heading("#3", text="high", anchor="center")
        self.stocks.column("#3", width=75, anchor="center", stretch=True)
        self.stocks.heading("#4", text="low", anchor="center")
        self.stocks.column("#4", width=75, anchor="center", stretch=True)
        self.stocks.heading("#5", text="close", anchor="center")
        self.stocks.column("#5", width=75, anchor="center", stretch=True)
        self.stocks.heading("#6", text="volume", anchor="center")
        self.stocks.column("#6", width=55, anchor="center", stretch=True)
        # Scroll bars are set up below considering placement position(x&y) ,height and width of treeview widget
        vsb = ttk.Scrollbar(self, orient=VERTICAL, command=self.stocks.yview)
        vsb.place(x=40 + 840 + 1 + 40, y=310, height=280 + 20)
        self.stocks.configure(yscrollcommand=vsb.set)
        hsb = ttk.Scrollbar(self, orient=HORIZONTAL, command=self.stocks.xview)
        hsb.place(x=40, y=410 + 200 + 1, width=820 + 20 + 40)
        self.stocks.configure(xscrollcommand=hsb.set)
        self.stocks.bind("<<TreeviewSelect>>", self.show_selected_record)
        self.lblDate.place(x=175, y=30, height=50, width=100)
        self.lblOpen.place(x=175, y=58, height=50, width=100)
        self.lblHigh.place(x=175, y=88, height=45, width=100)
        self.lblLow.place(x=175, y=117, height=50, width=100)
        self.lblClose.place(x=175, y=146, height=50, width=100)
        self.lblVolume.place(x=175, y=175, height=50, width=100)
        self.entDate.place(x=277, y=44, height=27, width=186)
        self.btn_ok.place(x=835, y=44, height=27, width=76)
        self.entOpen.place(x=277, y=72, height=27, width=186)
        self.entHigh.place(x=277, y=100, height=27, width=186)
        self.entLow.place(x=277, y=129, height=27, width=186)
        self.entClose.place(x=277, y=158, height=27, width=186)
        self.entVolume.place(x=277, y=188, height=27, width=186)
        self.btn_insert.place(x=45, y=230, height=27, width=76)
        self.btn_update.place(x=190, y=230, height=27, width=76)
        self.btn_delete.place(x=335, y=230, height=27, width=76)
        self.btn_clear.place(x=485, y=230, height=27, width=76)
        self.select_stocks.place(x=635, y=230, height=27, width=130)
        self.btn_load.place(x=835, y=230, height=27, width=76)
        self.stocks.place(x=40, y=310, height=300, width=880)
        self.load_stock_data()

    def insert(self):
        global SELECTED_TABLE
        date = self.entDate.get()
        open = self.entOpen.get()
        high = self.entHigh.get()
        low = self.entLow.get()
        close = self.entClose.get()
        volume = self.entVolume.get()
        # validating Entry Widgets
        if date == "":
            Messagebox.show_info("Information", "Please Enter Date")
            self.entDate.focus_set()
            return
        if open == "":
            Messagebox.show_info("Information", "Please Enter Open")
            self.entOpen.focus_set()
            return
        if high == "":
            Messagebox.show_info("Information", "Please Enter High")
            self.entHigh.focus_set()
            return
        if low == "":
            Messagebox.show_info("Information", "Please Enter Low")
            self.entLow.focus_set()
            return
        if close == "":
            Messagebox.show_info("Information", "Please Enter Close")
            self.entClose.focus_set()
            return
        if volume == "":
            Messagebox.show_info("Information", "Please Enter Volume")
            self.entVolume.focus_set()
            return

        metadata_obj = MetaData()
        stock = Table(
            self.select_stocks.get(),
            metadata_obj,
            Column("date", String, primary_key=True),
            Column("open", Float),
            Column("high", Float),
            Column("low", Float),
            Column("close", Float),
            Column("volume", BigInteger),
        )
        try:
            db = SingletonDBconnect()
            with db.engine.connect() as conn:
                conn.execute(
                    insert(stock),
                    [
                        {
                            "date": date,
                            "open": open,
                            "high": high,
                            "low": low,
                            "close": close,
                            "volume": volume,
                        }
                    ],
                )
                Messagebox.show_info("Information", "Stock Inserted Successfully")
                conn.commit()
            self.load_stock_data()
        except sqlalchemy.exc.DBAPIError as err:
            print(err)
            conn.rollback()
            Messagebox.show_info("Information", "Data insertion failed!")
        finally:
            conn.close()

    def delete(self):
        date = self.entDate.get()
        metadata_obj = MetaData()
        stock = Table(
            self.select_stocks.get(),
            metadata_obj,
            Column("date", String, primary_key=True),
            Column("open", Float),
            Column("high", Float),
            Column("low", Float),
            Column("close", Float),
            Column("volume", BigInteger),
        )
        MsgBox = Messagebox.okcancel(
            "Delete Record",
            "Are you sure! you want to delete selected stock record",
        )

        print(MsgBox)
        if MsgBox == "OK":
            try:
                db = SingletonDBconnect()
                with db.engine.connect() as conn:
                    stmt = delete(stock).where(stock.c.date == date)
                    conn.execute(stmt)
                    conn.commit()
                self.load_stock_data()
            except sqlalchemy.exc.DBAPIError as err:
                print(err)
                conn.rollback()
                Messagebox.show_info("Delete", "Data delete failed!")
            finally:
                conn.close()
            self.load_stock_data()
            self.entDate.delete(0, END)
            self.entOpen.delete(0, END)
            self.entHigh.delete(0, END)
            self.entLow.delete(0, END)
            self.entClose.delete(0, END)
            self.entVolume.delete(0, END)

    def update(self):
        global SELECTED_TABLE
        date = self.entDate.get()
        open = self.entOpen.get()
        high = self.entHigh.get()
        low = self.entLow.get()
        close = self.entClose.get()
        volume = self.entVolume.get()
        if date == "":
            Messagebox.show_info("Information", "Please Enter Date")
            self.entDate.focus_set()
            return
        if open == "":
            Messagebox.show_info("Information", "Please Enter Open")
            self.entOpen.focus_set()
            return
        if high == "":
            Messagebox.show_info("Information", "Please Enter High")
            self.entHigh.focus_set()
            return
        if low == "":
            Messagebox.show_info("Information", "Please Enter Low")
            self.entLow.focus_set()
            return
        if close == "":
            Messagebox.show_info("Information", "Please Enter Close")
            self.entClose.focus_set()
            return
        if volume == "":
            Messagebox.show_info("Information", "Please Enter Volume")
            self.entVolume.focus_set()
            return

        metadata_obj = MetaData()
        stock = Table(
            self.select_stocks.get(),
            metadata_obj,
            Column("date", String, primary_key=True),
            Column("open", Float),
            Column("high", Float),
            Column("low", Float),
            Column("close", Float),
            Column("volume", BigInteger),
        )
        try:
            db = SingletonDBconnect()
            with db.engine.connect() as conn:
                stmt = (
                    update(stock)
                    .where(stock.c.date == date)
                    .values(
                        date=date,
                        open=open,
                        high=high,
                        low=low,
                        close=close,
                        volume=volume,
                    )
                )
                conn.execute(stmt)
                Messagebox.show_info("Information", "Student Registration Successfully")
                conn.commit()
            self.load_stock_data()
        except sqlalchemy.exc.DBAPIError as err:
            print(err)
            conn.rollback()
            Messagebox.show_info("Information", "Data insertion failed!")
        finally:
            conn.close()

    def load_stock_data(self, val=""):
        self.select_stocks.update()
        self.select_stocks.update_idletasks()
        global SELECTED_TABLE
        SELECTED_TABLE = self.select_stocks.get()
        self.stocks.delete(*self.stocks.get_children())  # clears the treeview tvStudent
        db = SingletonDBconnect()
        metadata_obj = MetaData()
        stock = Table(
            SELECTED_TABLE,
            metadata_obj,
            Column("date", String, primary_key=True),
            Column("open", Float),
            Column("high", Float),
            Column("low", Float),
            Column("close", Float),
            Column("volume", BigInteger),
        )

        with db.engine.connect() as conn:
            sql = select(stock)
            try:
                rows = conn.execute(sql).all()
                total = len(rows)
                if total == 0:
                    Messagebox.show_info(
                        "Information", "Nothing To Display, Please add data"
                    )
                    return
                logger.debug("Total Data Entries:" + str(total))
            except IndexError as e:
                logger("IndexError :", e)
                rows = [["", "", "", "", "", ""]]
            finally:
                for row in rows:
                    date = row[0]
                    open_ = row[1]
                    high = row[2]
                    low = row[3]
                    close = row[4]
                    volume = row[5]
                    self.stocks.insert(
                        "",
                        "end",
                        text=date,
                        values=(date, open_, high, low, close, volume),
                    )

    def clear_form(self):
        self.entDate.delete(0, END)
        self.entOpen.delete(0, END)
        self.entHigh.delete(0, END)
        self.entLow.delete(0, END)
        self.entClose.delete(0, END)
        self.entVolume.delete(0, END)

    def show_selected_record(self, event):
        self.clear_form()
        for selection in self.stocks.selection():
            item = self.stocks.item(selection)
            date, open_, high, low, close, volume = item["values"][0:6]
            self.entDate.insert(0, date)
            self.entOpen.insert(0, open_)
            self.entHigh.insert(0, high)
            self.entLow.insert(0, low)
            self.entClose.insert(0, close)
            self.entVolume.insert(0, volume)
            return


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
                    sql = text(f"DROP TABLE IF EXISTS {stock.lower().replace(' ', '_')};")
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
