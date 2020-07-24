from typing import Tuple, Iterable, List, Dict, Optional
import datetime
import redis


client = redis.Redis(host="localhost", port=6379)


def _to_date_obj(date: bytes) -> datetime.date:
    return datetime.date.fromisoformat(str(date, "ascii"))


def add_record(key: str, date: datetime.date, price: float) -> None:
    client.hset(key, str(date), price)


def add_records(key: str, records: Iterable[Tuple[datetime.date, float]]) -> None:
    with client.pipeline() as pipe:
        for date, price in records:
            pipe.hset(key, str(date), price)
        pipe.execute()


def get_price(key: str, date: datetime.date) -> Optional[float]:
    result = client.hget(key, str(date))
    return float(result) if result else None


def get_prices(key: str, start_date: datetime.date = None, end_date: datetime.date = None) -> List[float]:
    start_date = start_date or datetime.date.min
    end_date = end_date or datetime.date.max

    records: Dict[bytes, bytes] = client.hgetall(key)

    # filter dates out of provided range
    dates_in_range: List[Tuple[datetime.date, float]] = []
    for date_bytes, price in records.items():
        date = _to_date_obj(date_bytes)
        if start_date <= date < end_date:
            dates_in_range.append((date, float(price)))

    # return prices sorted by date
    return [price for _, price in sorted(dates_in_range, key=lambda x: x[0])]
