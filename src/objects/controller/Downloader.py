import datetime

import yfinance as yf
import pandas as pd

from src.objects.controller.Ticket import Ticket
from src.objects.model.db_conn import SingletonDBconnect

from src.objects.model.db_conn import DB_CONNECT

class Downloader:
    def __init__(self, ticket: Ticket):
        self.ticket = ticket
        db = SingletonDBconnect()
        mnemonic = yf.Ticker(ticket.mnemo)
        self.data = mnemonic.history(period="10y")
        self.rename_columns()
        self.sharpen()
        if len(self.data) > 0:
            name = self.ticket.name_table
            db.write_to_db(self.data, name)

    def rename_columns(self):
        col_list = [col.lower().replace(" ", "_") for col in list(self.data.columns)]
        self.data.columns = pd.Index(col_list)
        self.data.index.name = self.data.index.name.lower()
        self.data.index = pd.Index(
            pd.Series(self.data.index).apply(
                lambda x: datetime.datetime.strptime(
                    x.strftime("%Y%m%d"), "%Y%m%d"
                ).date()
            )
        )

    def sharpen(self):
        try:
            self.data = self.data[["open", "high", "low", "close", "volume"]]
        except KeyError as e:
            print(f"Pas de données dans {self.ticket.name} : {e}")


    def writer(self):
        db = DB_CONNECT()
        if db.db_exist():
            conn = db.engine.connect()
            db.write_to_db(self.data, self.ticket.name_table, conn)


if __name__ == "__main__":
    t = Ticket("ACCOR")
    d = Downloader(t)
