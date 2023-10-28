import os
import pandas as pd
from src.objects.model.db_conn import DB_CONNECT
from src.objects.controller.Ticket import Ticket
from src.objects.controller.Downloader import Downloader
from src.objects.model.db_conn import _DB_PATH

global DB_PATH

DB_PATH = _DB_PATH

class TestClass:
    def test_text_prg(self):
        df = pd.read_csv("src/lang/text_prg.csv")
        assert True not in df.isna().iloc[0].to_list()

    def test_two(self):
        class Perso:
            def check(self):
                pass

        x = Perso
        assert hasattr(x, "check")

    def test_three(self):
        x = DB_CONNECT()
        t = Ticket("AIRBUS SE")
        d = Downloader(t)
        os.remove(DB_PATH)
