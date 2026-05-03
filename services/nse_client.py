import yfinance as yf
import pandas as pd

def get_1y_history(symbol):
    try:
        ticker = symbol.replace("-EQ", "") + ".NS"
        print(f"Fetching Yahoo Finance: {ticker}")

        df = yf.download(ticker, period="1y")

        if df is None or df.empty:
            print(f"No data for {symbol}")
            return None

        print(f"SUCCESS {symbol}: {len(df)} rows")
        return df

    except Exception as e:
        print(f"ERROR: {e}")
        return None
