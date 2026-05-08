import pykx as kx
import pandas as pd
import time

class TickAnalytics:
    def __init__(self, host='localhost', port=5011):
        """Connects directly to the RDB (Port 5011) to query live intraday data."""
        try:
            self.q = kx.SyncQConnection(host=host, port=port)
            print(f"Connected to RDB on {host}:{port}")
        except Exception as e:
            print(f"Failed to connect to RDB: {e}")

    def get_vwap(self) -> pd.DataFrame:
        """
        Calculates Volume Weighted Average Price (VWAP).
        Notice we pass the heavy math down to KDB+ using q-sql.
        """
        query = """
        select vwap:size wavg price, total_vol:sum size by sym from trade
        """
        # Execute query and convert to Pandas DataFrame
        return self.q(query).pd()

    def get_trade_imbalance(self) -> pd.DataFrame:
        """
        Uses an 'as-of join' (aj) to join the latest quote to every trade
        to determine if the trade was buyer-initiated (trade price >= ask)
        or seller-initiated (trade price <= bid).
        """
        query = """
        / 1. Join quotes to trades as of the trade time
        enriched: aj[`sym`time; trade; quote];

        / 2. Classify direction and aggregate
        select
            buy_vol: sum size * price >= ask,
            sell_vol: sum size * price <= bid
        by sym from enriched
        """
        df = self.q(query).pd()

        # We can do the final signal math in Python
        df['imbalance_ratio'] = (df['buy_vol'] - df['sell_vol']) / (df['buy_vol'] + df['sell_vol'] + 1)
        return df

    def get_momentum_signal(self) -> pd.DataFrame:
        """
        Calculates simple intraday momentum using Q's mavg (moving average).
        """
        query = """
        select time, sym, price,
               fast_ma: 5 mavg price,
               slow_ma: 20 mavg price
        from trade where sym = `AAPL
        """
        df = self.q(query).pd()
        df['signal'] = df['fast_ma'] > df['slow_ma']
        return df.tail(10) # Return latest 10 ticks for display

if __name__ == "__main__":
    # Ensure tp.q, rdb.q, and feed.q are running before executing this
    analytics = TickAnalytics()

    print("\n--- Gathering Real-Time VWAP ---")
    print(analytics.get_vwap())

    print("\n--- Calculating Trade Imbalance via As-of Join ---")
    print(analytics.get_trade_imbalance())

    print("\n--- AAPL Momentum Signal ---")
    print(analytics.get_momentum_signal())
