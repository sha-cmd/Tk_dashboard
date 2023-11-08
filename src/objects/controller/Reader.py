import pandas as pd
from sqlalchemy import create_engine

from src.objects.controller.logger import log_init
from src.objects.model.db_conn import _DB_PATH

logger = log_init()


global DB_PATH
DB_PATH = _DB_PATH


class Reader:
    global DB_PATH

    def __init__(self):
        pass

    def read(self, name):
        self.engine = create_engine("sqlite+pysqlite:///" + DB_PATH, echo=True)
        with self.engine.connect() as conn:
            df = pd.read_sql_table(name, conn, index_col="date")
        return df
