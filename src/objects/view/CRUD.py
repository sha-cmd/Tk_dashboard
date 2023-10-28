from copy import deepcopy as dc

import sqlalchemy.exc
import ttkbootstrap as ttk

from sqlalchemy import (
    select,
    insert,
    inspect,
    update,
    delete,
    Table,
    MetaData,
    Column,
    String,
    Float,
    BigInteger,
)
from ttkbootstrap import Button
from ttkbootstrap import Entry
from ttkbootstrap import Label
from ttkbootstrap.constants import *
from ttkbootstrap.dialogs.dialogs import Messagebox

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
