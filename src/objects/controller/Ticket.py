from pandas import read_csv
from src.objects.controller.logger import log_init as log
from src.objects.controller.constant import _MNEMO_SRC

global MNEMO_SRC
MNEMO_SRC = _MNEMO_SRC

DATE_DEBUT = "1983-01-01"
logger = log()


class Ticket:
    def __init__(self, name: str):
        self.name = name
        df = self.complete_list()
        self.mnemo = df.loc[df["name"] == self.name]["mnemo"].iloc[0]
        self.name_table = self.formatted_name()

    def formatted_name(self):
        return (
            self.name.lower()
            .replace("&", "")
            .replace("/", "")
            .replace("-", "")
            .replace("   ", " ")
            .replace("  ", " ")
            .replace(" ", "_")
            .replace("(", "")
            .replace(")", "")
            .replace("é", "e")
            .replace("è", "e")
        )

    def complete_list(self):
        return read_csv(MNEMO_SRC, sep=";")

if __name__ == "__main__":
    t = Ticket("ACCOR")