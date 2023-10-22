from pandas import DataFrame


def cols_to_lower(df: DataFrame) -> DataFrame:
    cols: dict = {x: x.lower() for x in list(df.columns)}
    df.rename(columns=cols, inplace=True)
    return df


def reformat(string: str) -> str:
    cut: str = string.lower().strip()
    return cut
