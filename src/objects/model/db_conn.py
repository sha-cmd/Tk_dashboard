from os.path import exists
from src.objects.controller.logger import log_init as log
from sqlalchemy import create_engine
from sqlalchemy import Table, Column, Integer, String, Float, BigInteger
from sqlalchemy import MetaData

global _DB_PATH
global IF_EXIST

_DB_PATH = "bdd/Databases.Stocks"
IF_EXIST = "replace"

logger = log()


class DB_CONNECT:
    global _DB_PATH
    global IF_EXIST

    def __init__(self):
        self.path = _DB_PATH
        self.engine = create_engine("sqlite+pysqlite:///" + self.path, echo=True)

    def schema(self):
        self.metadata_obj = MetaData()
        self.user_table = Table(
            "user_account",
            self.metadata_obj,
            Column("id", Integer, primary_key=True),
            Column("name", String(30)),
            Column("password", String),
        )
        self.metadata_obj.create_all(self.engine)

    def db_exist(self):
        """
        Contrôle existence de la base de données.
        :return:
        """
        file_exists = exists(_DB_PATH)
        return file_exists

    def write_to_db(self, df, name, if_exist=IF_EXIST):
        self.metadata_obj = MetaData()
        self.user_table = Table(
            name,
            self.metadata_obj,
            Column("date", String, primary_key=True),
            Column("open", Float),
            Column("high", Float),
            Column("low", Float),
            Column("close", Float),
            Column("volume", BigInteger),
        )
        self.metadata_obj.create_all(self.engine)
        with self.engine.connect() as conn:
            df.to_sql(name, conn, if_exists=if_exist)
            logger.debug("Écriture de " + name + " en base")


class SingletonDBconnect(DB_CONNECT):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(SingletonDBconnect, cls).__class__(
                *args, **kwargs
            )
        return cls._instances[cls]
