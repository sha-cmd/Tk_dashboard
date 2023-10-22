import configparser
from configparser import ConfigParser
from pandas import read_csv
from pandas import DataFrame
from src.objects.controller.toolbox import cols_to_lower
from src.objects.controller.toolbox import reformat

global _LANG
global _LANGS
global _TEXTS
global _LANG_INI
global _MNEMO_SRC
global _NAME_STOCK
global _MNEMO
global _PORTFOLIO
global _active_stock
global _COLUMNS_STOCK

_LANG_INI: str = "src/lang/constant.ini"
_MNEMO_SRC: str = "src/mnemo/mnemo.csv"
_NAME_STOCK: list[str] = read_csv(_MNEMO_SRC, sep=";")["name"].to_list()
_MNEMO: list[str] = read_csv(_MNEMO_SRC, sep=";")["mnemo"].to_list()
_PORTFOLIO: list[str] = []
_active_stock: dict = {x: 0 for x in _NAME_STOCK}
_COLUMNS_STOCK: list[str] = list(read_csv(_MNEMO_SRC, sep=";").columns)

def text(country_code: str) -> list[str]:
    df: DataFrame = read_csv("src/lang/text_prg.csv", sep=",")
    df = cols_to_lower(df)
    code: str = reformat(country_code)
    texts: list = df[code].to_list()
    del df
    return texts


def get_langs() -> list[str]:
    df: DataFrame = read_csv("src/lang/text_prg.csv", sep=",", index_col="id")
    #df = cols_to_lower(df)
    # langs: list = sorted(list(df.columns[2:]))
    langs: list = sorted(list(df.iloc[17][1:]))
    return langs


def get_lang() -> str:
    df: DataFrame = read_csv("src/lang/text_prg.csv", sep=",", index_col="id")
    config_exist()
    config = get_config()
    return config["LANGUAGE"]["DEFAULT"]

def get_config():
    config: ConfigParser = ConfigParser()
    config.read(_LANG_INI)
    return config


def config_exist():
    try:
        with open(_LANG_INI, "r") as f:
            pass
    except FileNotFoundError as e:
        config = ConfigParser()
        config['LANGUAGE'] = {'DEFAULT': 'EN'}
        with open(_LANG_INI, 'w') as configfile:
            config.write(configfile)



def set_config(config: ConfigParser):
    with open(_LANG_INI, "w") as configfile:
        config.write(configfile)

_LANG: str = get_lang()
_LANGS: list[str] = get_langs()
_TEXTS: list[str] = text(get_lang())