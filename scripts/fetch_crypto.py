import requests
import pandas as pd
import sqlite3
from datetime import datetime
import time

while True:
    try:
        url = "https://api.coingecko.com/api/v3/simple/price"

        params = {
            "ids": "bitcoin,ethereum",
            "vs_currencies": "usd",
            "include_market_cap": "true",
            "include_24hr_vol": "true"
        }

        response = requests.get(url, params=params)
        data = response.json()

        records = []

        for coin in data:
            records.append({
                "timestamp": datetime.now(),
                "coin": coin,
                "price": data[coin]["usd"],
                "market_cap": data[coin]["usd_market_cap"],
                "volume": data[coin]["usd_24h_vol"]
            })

        df = pd.DataFrame(records)

        conn = sqlite3.connect("database/crypto.db")

        df.to_sql("crypto_data", conn, if_exists="append", index=False)

        conn.close()

        print("Data inserted at:", datetime.now())

    except Exception as e:
        print("Error:", e)

    # Wait 5 minutes (300 seconds)
    time.sleep(300)