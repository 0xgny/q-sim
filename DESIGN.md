# Design Document: Q/PyKX Tick Infrastructure

## 1. Overview
This project simulates a real-time tick data infrastructure. It consists of a Q/KDB+ data layer (Tickerplant, Real-Time Database, Feedhandler) and a Python/PyKX analytics layer. The goal is to capture high-frequency trading data, make it immediately queryable in memory, and perform complex temporal calculations.

## 2. Technical Structure
The architecture follows the classic publish-subscribe (pub/sub) pattern standard in KDB+ environments:
* **Feedhandler (`feed.q`):** Simulates market data (Trades and Quotes). In a real environment, this connects to an exchange API (e.g., Polygon.io, FIX engines) and parses data into Q tables.
* **Tickerplant (`tp.q`):** A lightweight router. It receives updates from the feedhandler, pushes them to a log file (for disaster recovery - omitted in this basic mock), and publishes them to subscribers.
* **Real-Time Database (`rdb.q`):** Subscribes to the Tickerplant. It stores intraday data in memory, allowing for microsecond-latency queries. At the end of the day, it flushes this data to disk as a partitioned Historical Database (HDB).
* **Analytics Client (`analytics.py`):** Uses PyKX via Inter-Process Communication (IPC) to query the RDB, pushing aggregations down to the Q process and pulling results into Pandas DataFrames for complex signal generation.

## 3. Abstraction Philosophy
* **Data Gravity (Pushing compute to data):** Operations that reduce data volume—like calculating Volume Weighted Average Price (VWAP) or temporal joins (`aj`)—are written in `q-sql` and executed on the KDB+ server. Moving millions of rows over a network to Python is an anti-pattern.
* **Pythonic Surface:** The PyKX layer abstracts the Q-IPC connections so quantitative researchers can trigger KDB+ analytics using familiar Python syntax and receive standard Pandas DataFrames.
* **Separation of Concerns:** The tickerplant does absolutely no calculations. Its only job is routing. The RDB handles storage and read-queries. Python handles mathematical modeling.

## 4. Schema Decisions
* **`trade`**: `(time; sym; price; size)`
* **`quote`**: `(time; sym; bid; ask; bsize; asize)`
* Both tables use `timespan` for microsecond precision and `symbol` types for tickers, as symbol interning in KDB+ allows for O(1) string comparisons.
