import copy
import datetime
import numpy as np
import pandas as pd
import sys

from decimal import Decimal

import matplotlib as mpl
import matplotlib.pyplot as plt
import mplfinance as mpf

from src.objects.controller.Reader import Reader

COLUMNS = [
    "Nom",
    "Prix",
    "Achat",
    "Vente",
    "Perf",
    "Cac 40",
    "5 ans",
    "3 ans",
    "1er janv",
    "Moy/ans",
    "Mois",
    "Semaine",
    "Séance",
    "Rôle",
    "Secteur",
    "Activité",
]


class Analyse:
    def __init__(self):
        self.avg = {}
        self.avg_d_log = {}
        self.avg_a_log = {}
        self.avg_d_dis = {}
        self.avg_a_dis = {}
        self.avg1 = {}
        self.avg3 = {}
        self.avg5 = {}
        self.avg10 = {}
        self.avg25j = {}
        self.avg5j = {}
        self.perf_shot = {}
        self.price = {}
        self.risk = {}

    def last_day_perf(self, data, name):
        self.perf_shot.update(
            {
                name: round(
                    ((data.iloc[-1]["close"] / data.iloc[-2]["close"]) - 1) * 100, 2
                )
            }
        )
        self.price.update({name: copy.deepcopy(round(data.iloc[-1]["close"], 2))})

        self.avg.update(
            {
                name: round(
                    ((data.iloc[-1]["close"] / data.iloc[0]["close"]) - 1) * 100, 2
                )
            }
        )
        data["Log_ror"] = np.log(data["close"] / data["close"].shift(1))
        self.avg_d_log.update({name: round(data["Log_ror"].mean() * 100, 2)})
        self.avg_a_log.update({name: round(data["Log_ror"].mean() * 250 * 100, 2)})
        data["Dis_ror"] = (data["close"] / data["close"].shift(1)) - 1
        self.avg_d_dis.update({name: round(data["Dis_ror"].mean() * 100, 2)})
        self.avg_a_dis.update({name: round(data["Dis_ror"].mean() * 250 * 100, 2)})

        today = datetime.date.today()
        diff = np.busday_offset(str(today.year) + "-01", 0, roll="forward")
        days = np.busday_count(diff, today)
        if data["close"].count() >= days:
            self.avg1.update(
                {
                    name: round(
                        (
                            (
                                data.iloc[-1]["close"]
                                / data.loc[data.index == diff]["close"].iloc[0]
                            )
                            - 1
                        )
                        * 100,
                        2,
                    )
                }
            )
        else:
            self.avg1.update({name: None})
        print(f"{today.year - 3}-{today.month:>02}-{today.day:>02}")
        diff = np.busday_offset(
            f"{today.year - 3}-{today.month:>02}-{today.day:>02}", 0, roll="forward"
        )
        days = np.busday_count(diff, today)
        if data["close"].count() >= int(days):
            self.avg3.update(
                {
                    name: round(
                        (
                            (
                                data.iloc[-1]["close"]
                                / data.loc[data.index == diff]["close"].iloc[0]
                            )
                            - 1
                        )
                        * 100,
                        2,
                    )
                }
            )
        else:
            self.avg3.update({name: None})
        diff = np.busday_offset(
            f"{today.year - 5}-{today.month:>02}-{today.day:>02}", 0, roll="forward"
        )
        days = np.busday_count(diff, today)
        if data["close"].count() >= days:
            self.avg5.update(
                {
                    name: round(
                        (
                            (
                                data.iloc[-1]["close"]
                                / data.loc[data.index == diff]["close"].iloc[0]
                            )
                            - 1
                        )
                        * 100,
                        2,
                    )
                }
            )
        else:
            self.avg5.update({name: None})
        diff = np.busday_offset(
            f"{today.year - 9}-{today.month:>02}-{today.day:>02}", 0, roll="forward"
        )
        days = np.busday_count(diff, today)
        # if data["close"].count() >= days:
        self.avg10.update(
            {
                name: round(
                    (
                        (
                            data.iloc[-1]["close"]
                            / data.loc[data.index == diff]["close"].iloc[0]
                        )
                        - 1
                    )
                    * 100,
                    2,
                )
            }
        )
        # else:
        #     self.avg5.update({name: None})
        self.avg5j.update(
            {
                name: round(
                    ((data.iloc[-1]["close"] / data.iloc[-5]["close"]) - 1) * 100, 2
                )
            }
        )
        self.avg25j.update(
            {
                name: round(
                    ((data.iloc[-1]["close"] / data.iloc[-25]["close"]) - 1) * 100, 2
                )
            }
        )
        self.risk.update({name: round((data["Log_ror"].std() * 250**0.5) * 10, 1)})
        if data["Log_ror"].count() < 250:
            self.risk.update({name: 0})
        return data

    def graph(self, name):
        print("Graph 01", name)
        data = Reader().read(name)
        filename = name
        if len(data) == 0:
            sys.exit(name, "n'a pas de données dans la base, retirer là des securities")
        data.index = pd.DatetimeIndex(
            [pd.to_datetime(x).tz_localize(None) for x in data.index]
        )
        methode = "close"
        mpl.use("TkAgg")
        plt.figure(figsize=(10, 6))
        mpf.plot(
            data.iloc[:, 0:5],
            type="line",
            title=name,
            savefig="img/long_"
            + methode
            + "_"
            + str(filename).replace(" ", "_")
            + ".png",
        )
        plt.close()
        mpf.plot(
            data.iloc[-500:, 0:5],
            type="line",
            mav=(12, 20, 50),
            volume=True,
            title=name,
            savefig="img/short_"
            + methode
            + "_"
            + str(filename).replace(" ", "_")
            + ".png",
        )
        plt.close()
