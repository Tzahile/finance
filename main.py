"""
This is a temporary template for our POC flow
"""
import datetime

import yaml
from bson import ObjectId

from collector import stock_exchange
from collector.psagot_collector import PsagotCollector
from analysis.instrument import Instrument
from converters.converters import convert_list
from database import cache
from database import mongo_raw_data_wrapper, mongo_normalized_data_wrapper
from data.psagot_raw_data import PsagotRawData
from data.currency import Currency
from data.event import Transaction

# 1. Extract data from Psagot

with open("credentials.yaml") as yaml_file:
    creds = yaml.safe_load(yaml_file)
collector = PsagotCollector(creds["username"], creds["password"], creds["account_number"])
data = collector.get_data()

# 2. Store in Mongo
user_id = ObjectId()
raw_data_list = [PsagotRawData(user_id=user_id, **transaction) for transaction in data]

# 2.1 Store Raw data in Mongo
status = mongo_raw_data_wrapper.insert_bulk(raw_data_list)

if status.acknowledged:
    for idx, raw_data_object_id in enumerate(status.inserted_ids):
        raw_data_list[idx].uid = raw_data_object_id

# 2.2 Convert Raw data to normalized_data_list
normalized_data_list = convert_list(raw_data_list)

# 2.3 Store Normalized data in Mongo
status = mongo_normalized_data_wrapper.insert_bulk(normalized_data_list)

# 3. Get all tickers from Mongo

tickers = ["MSFT", "AAPL"]

# 4. Download historical closing-prices per ticker

start_date = datetime.date.fromisoformat("2020-01-01")
end_date = datetime.date.fromisoformat("2020-01-04")

prices = {}
for ticker in tickers:
    prices[ticker] = stock_exchange.get_prices(ticker, start_date, end_date)


# 5. Store prices in Redis

for ticker in prices:
    cache.add_records(ticker, prices[ticker])
    cache.add_record(ticker, datetime.date.today(), stock_exchange.get_latest_price(ticker))

# 6. Run calculations and output results

transactions = [
    Transaction(date=datetime.date.fromisoformat("2020-01-02"), symbol="MSFT", units=10, price=100, commission=8,),
    Transaction(date=datetime.date.fromisoformat("2020-01-02"), symbol="AAPL", units=10, price=100, commission=8,),
]

instruments = [Instrument(symbol="MSFT", currency=Currency.USD), Instrument(symbol="AAPL", currency=Currency.USD)]
for inst in instruments:
    inst.transactions = transactions
    print(inst.calc_change())

# a. per paper: quantity, current-price, total-value, change-ILS, change-%, dividends
# b. per action: expenses(by type), taxes
# b. per portfolio: net-worth, change-ILS, change-%, assets-allocation-pie, worth-over-type
# -
