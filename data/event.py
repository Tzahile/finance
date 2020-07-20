from abc import ABC
from dataclasses import dataclass
import datetime


@dataclass
class Event(ABC):
    date: datetime.date


@dataclass
class Transaction(Event):
    symbol: str
    units: int
    price: float
    commission: float
