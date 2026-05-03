import yfinance as yf
import pandas as pd


class NSEClient:

    def _to_yfinance_symbol(self, symbol: str) -> str:
        """
        Convert:
        RELIANCE-EQ → RELIANCE.NS
        """
        base = symbol.replace("-EQ", "").strip()
        return f"{base}.NS"

    # -----------------------------
    # STOCK QUOTE
    # -----------------------------
    def get_quote(self, symbol):
        try:
            ticker = self._to_yfinance_symbol(symbol)
            data = yf.Ticker(ticker).info

            return {
                "symbol": symbol,
                "price": data.get("regularMarketPrice"),
                "open": data.get("open"),
                "high": data.get("dayHigh"),
                "low": data.get("dayLow"),
                "volume": data.get("volume"),
                "marketCap": data.get("marketCap"),
            }

        except Exception as e:
            print(f"Quote error for {symbol}: {e}")
            return None

    # -----------------------------
    # 1 YEAR HISTORY
    # -----------------------------
    def get_1y_history(self, symbol):
        try:
            ticker = self._to_yfinance_symbol(symbol)
            print(f"\nFetching: {ticker}")

            df = yf.download(ticker, period="1y", interval="1d", auto_adjust=False)

            # ---------------- DEBUG ----------------
            print(f"RAW ROWS: {len(df)}")

            if df is None or df.empty:
                print(f"No data for {symbol}")
                return None

            # ---------------- FIX: MultiIndex issue ----------------
            if isinstance(df.columns, pd.MultiIndex):
                df.columns = df.columns.get_level_values(0)

            # ---------------- STANDARDIZE ----------------
            df = df.reset_index()

            # Ensure required column exists
            if "Close" not in df.columns:
                if "Adj Close" in df.columns:
                    df["Close"] = df["Adj Close"]
                else:
                    print(f"Missing Close for {symbol}. Columns: {df.columns}")
                    return None

            # Convert safely
            df["Close"] = pd.to_numeric(df["Close"], errors="coerce")
            df = df.dropna(subset=["Close"])

            print(f"SUCCESS {symbol}: {len(df)} rows")
            print(f"COLUMNS: {list(df.columns)}")

            return df

        except Exception as e:
            print(f"ERROR for {symbol}: {e}")
            return None
