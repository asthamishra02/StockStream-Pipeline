import os
import requests
import psycopg2
from dotenv import load_dotenv

# ----------------------------
# Load environment variables
# ----------------------------
load_dotenv()

API_KEY = os.getenv("ALPHA_VANTAGE_API_KEY")
DB_HOST = os.getenv("DB_HOST")
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_PORT = os.getenv("DB_PORT")

# ----------------------------
# Fetch hourly stock data
# ----------------------------
def fetch_stock_data(symbol="AAPL"):
    url = "https://www.alphavantage.co/query"
    params = {
        "function": "TIME_SERIES_INTRADAY",
        "symbol": symbol,
        "interval": "60min",
        "apikey": API_KEY
    }
    try:
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()
        time_series = data.get("Time Series (60min)")
        if not time_series:
            print(f"Unexpected API response: {data}")
            return None
        print(f"Fetched {len(time_series)} hourly records for {symbol}")
        return time_series
    except Exception as e:
        print(f"Error fetching stock data: {e}")
        return None

# ----------------------------
# Store data in PostgreSQL
# ----------------------------
def store_in_db(symbol, stock_data):
    if not stock_data:
        print("No stock data to insert.")
        return
    try:
        with psycopg2.connect(
            host=DB_HOST,
            dbname=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD,
            port=DB_PORT
        ) as conn:
            with conn.cursor() as cursor:
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS stock_prices_hourly (
                        symbol TEXT,
                        date TIMESTAMP,
                        open NUMERIC,
                        high NUMERIC,
                        low NUMERIC,
                        close NUMERIC,
                        volume BIGINT,
                        PRIMARY KEY (symbol, date)
                    )
                """)
                for date, values in stock_data.items():
                    try:
                        cursor.execute("""
                            INSERT INTO stock_prices_hourly 
                                (symbol, date, open, high, low, close, volume)
                            VALUES (%s, %s, %s, %s, %s, %s, %s)
                            ON CONFLICT (symbol, date) 
                            DO UPDATE SET 
                                open = EXCLUDED.open,
                                high = EXCLUDED.high,
                                low = EXCLUDED.low,
                                close = EXCLUDED.close,
                                volume = EXCLUDED.volume
                        """, (
                            symbol,
                            date,
                            values.get("1. open"),
                            values.get("2. high"),
                            values.get("3. low"),
                            values.get("4. close"),
                            values.get("5. volume")
                        ))
                    except Exception as row_error:
                        print(f"Skipping row {date} due to error: {row_error}")
        print(f"Hourly stock data for {symbol} inserted/updated successfully.")
    except Exception as e:
        print(f"Error storing data in DB: {e}")

# ----------------------------
# Main
# ----------------------------
if __name__ == "__main__":
    import sys
    symbol = sys.argv[1] if len(sys.argv) > 1 else "AAPL"
    stock_data = fetch_stock_data(symbol)
    store_in_db(symbol, stock_data)
