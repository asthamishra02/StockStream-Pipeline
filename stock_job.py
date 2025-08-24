import os, sys
sys.path.append(os.path.join(os.path.dirname(__file__), "..", "..", "scripts"))
from fetch_stock_data import fetch_stock_data, store_in_db

def run_stock_etl():
    symbol = "AAPL"
    data = fetch_stock_data(symbol)
    store_in_db(symbol, data)
