import requests
import pandas as pd
from datetime import datetime

URL = "https://api.wise.com/v1/rates?source=EUR&target=BRL"

response = requests.get(URL)
rate = response.json()[0]["rate"]

data = {
    "date": [datetime.now()],
    "price": [rate]
}

try:
    df = pd.read_csv("euro.csv")
    df = pd.concat([df, pd.DataFrame(data)], ignore_index=True)
except FileNotFoundError:
    df = pd.DataFrame(data)

df["avg_14"] = df["price"].rolling(14).mean()

df.to_csv("euro.csv", index=False)

price_now = df.iloc[-1]["price"]
avg = df.iloc[-1]["avg_14"]

if pd.notna(avg) and price_now < avg * 0.99:
    print(f"🚨 ALERTA: Euro barato! €1 = R${price_now:.2f}")
else:
    print(f"Sem oportunidade. €1 = R${price_now:.2f}")
