from typing import Iterator, Tuple, Dict
from datetime import date as date_t

import yfinance as yf


def get_info(ticker: str) -> Dict[str, str]:
    fields = {"shortName", "sector", "quoteType", "market", "industry", "currency", "country", "symbol", "longName"}
    return {k: v for k, v in yf.Ticker(ticker).info.items() if k in fields}


def get_prices(ticker: str, start_date: date_t = None, end_date: date_t = None) -> Iterator[Tuple[date_t, float]]:
    period = None if start_date or end_date else "max"
    df = yf.Ticker(ticker).history(period=period, start=start_date, end=end_date)[["Close"]]
    return ((row[0].date(), float(row[1])) for row in df.iterrows())


def get_latest_price(ticker: str) -> float:
    return yf.Ticker(ticker).info["regularMarketPrice"]  # BUG: there's no "closePrice" fields?
