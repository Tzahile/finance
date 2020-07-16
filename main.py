"""
This is a temporary template for our POC flow
"""
import datetime
import yaml

from collector import stock_exchange
from collector.psagot_collector import PsagotCollector
from database import cache


# 1. Extract data from Psagot

with open("credentials.yaml") as yaml_file:
    creds = yaml.safe_load(yaml_file)
collector = PsagotCollector(creds["username"], creds["password"], creds["account_number"])
collector.authenticate()
data = collector.get_data()

# 2. Store in Mongo


# 3. Get all tickers from Mongo

tickers = ["MSFT", "AAPL"]

# 4. Download historical closing-prices per ticker

start_date = datetime.date.fromisoformat("2020-01-01")
end_date = datetime.date.fromisoformat("2020-02-01")

prices = {}
for ticker in tickers:
    prices[ticker] = stock_exchange.get_prices(ticker, start_date, end_date)

# 5. Store prices in Redis

for ticker in prices:
    cache.add_records(ticker, prices[ticker])

# 6. Run calculations and output results
# -
# a. per paper: quantity, current-price, total-value, change-ILS, change-%, dividends
# b. per action: expenses(by type), taxes
# b. per portfolio: net-worth, change-ILS, change-%, assets-allocation-pie, worth-over-type
# -
