import datetime
import json
import types
import unittest
from typing import Dict

import yfinance as yf
import pandas as pd

from collector import stock_exchange


class TestCache(unittest.TestCase):
    def setUp(self) -> None:
        return

    def test_get_info(self):
        def mock_info(*_, **__) -> Dict[str, str]:
            with open("tests/assets/msft_info.json") as f:
                return json.load(f)

        yf.Ticker.get_info = mock_info
        info = stock_exchange.get_info("msft")
        must_fields = {"shortName", "quoteType"}
        self.assertTrue(must_fields <= set(info.keys()))

    def test_get_prices(self):
        def mock_history(*_, **__) -> pd.DataFrame:
            return pd.read_pickle("tests/assets/msft_jan20_df.pickle")

        yf.Ticker.history = mock_history
        prices = stock_exchange.get_prices("msft")
        self.assertIsInstance(prices, types.GeneratorType)
        count = 0
        for item in prices:
            count += 1
            self.assertIsInstance(item, tuple)
            self.assertIsInstance(item[0], datetime.date)
            self.assertIsInstance(item[1], float)
        self.assertEqual(count, 22)
