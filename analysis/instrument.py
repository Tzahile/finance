from typing import List
import datetime

import pandas as pd
from pandas import DataFrame

from data.currency import Currency
from data.event import Transaction
from database import cache


class Instrument:
    """
    A trade-able financial asset
    """

    def __init__(self, symbol: str, currency: Currency):
        self._symbol = symbol.upper()
        self._currency = currency
        self._units = 0
        self._transactions: List[Transaction] = []
        self._price_matrix: DataFrame = pd.DataFrame(columns=["date", "units_accumulative", "price", "change"])

    def __str__(self) -> str:
        return (
            f"{self.__class__.__name__}"
            f"(symbol={self._symbol},"
            f" currency={self._currency},"
            f" units={self._units},"
            # f" change={self._change}/{self._change_percentage}%)"
        )

    @property
    def symbol(self) -> str:
        return self._symbol

    @property
    def is_active(self) -> bool:
        return self._units > 0

    @property
    def units(self) -> int:
        return self._units

    def _init_matrix(self) -> None:
        self._price_matrix = self._price_matrix.iloc[0:0]  # clear
        self._price_matrix.loc[0] = [datetime.date.min, 0, 0.0, 0.0]

    def _get_prev_units(self) -> int:
        return self._price_matrix.iloc[-1]["units_accumulative"]

    def _get_prev_price(self) -> float:
        return self._price_matrix.iloc[-1]["price"]

    def _append_to_matrix(self, date: datetime.date, total_units: int, price: float, change: float) -> None:
        self._price_matrix.loc[len(self._price_matrix)] = [
            date,
            total_units,
            price,
            change,
        ]

    @property
    def transactions(self) -> List[Transaction]:
        return self._transactions

    @transactions.setter
    def transactions(self, records: List[Transaction]) -> None:
        records = [r for r in records if r.symbol == self._symbol]
        sorted_records = sorted(records, key=lambda r: r.date)

        if sorted_records != records:
            raise ValueError("Transaction sequence is not sorted by date.")

        self._units = 0
        self._transactions.clear()
        self._init_matrix()

        for rec in records:
            self._units += rec.units
            self._transactions.append(rec)

            if self._units < 0:
                raise ValueError("Illegal transaction sequence - negative number of units.")

            prev_units = self._get_prev_units()
            prev_price = self._get_prev_price()

            curr_price = cache.get_price(key=self._symbol, date=rec.date)
            self._append_to_matrix(
                date=rec.date,
                total_units=prev_units + rec.units,
                price=curr_price,
                change=prev_units * (curr_price - prev_price),
            )

    def calc_change(self, from_date: datetime.date = None, to_date: datetime.date = None) -> float:
        min_date = self._price_matrix["date"].values[1]
        today = datetime.date.today()

        from_date = max(min_date, from_date) if from_date else min_date
        to_date = min(today, to_date) if to_date else today

        range_change = self._price_matrix.loc[
            (from_date <= self._price_matrix["date"]) & (self._price_matrix["date"] < to_date)
        ]["change"].sum()

        if to_date == today:
            range_change += cache.get_price(key=self._symbol, date=today) - self._get_prev_price()
        return range_change
