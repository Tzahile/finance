import unittest
import datetime
from typing import Iterable, Tuple, List, Set

import fakeredis
from hypothesis import given
import hypothesis.strategies as st

from database import cache


class TestCache(unittest.TestCase):
    def setUp(self) -> None:
        cache.client = fakeredis.FakeStrictRedis()
        assert not cache.client.keys("*")

    @given(symbol=st.text(), date=st.datetimes(), price=st.floats(allow_infinity=False, allow_nan=False))
    def test_add_record(self, symbol: str, date: datetime.date, price: float):
        cache.add_record(symbol, date, price)
        self.assertEqual(cache.get_price(symbol, date), price)

        price += 1
        cache.add_record(symbol, date, price)
        self.assertEqual(cache.get_price(symbol, date), price)

    @given(
        symbol=st.text(min_size=1),
        records=st.lists(st.tuples(st.dates(), st.floats(allow_infinity=False, allow_nan=False)), unique=True),
    )
    def test_add_many_records(self, symbol: str, records: Iterable[Tuple[datetime.date, float]]):
        # remove date-duplicates:
        seen: Set[datetime.date] = set()
        tmp_records: List[Tuple[datetime.date, float]] = []
        for tup in records:
            if tup[0] not in seen:
                seen.add(tup[0])
                tmp_records.append(tup)
        records = tmp_records

        cache.client.delete(symbol)
        cache.add_records(symbol, records)

        records.sort(key=lambda x: x[0])
        self.assertEqual(cache.get_prices(symbol), [p for _, p in records])
