import requests
import random
import json
import pandas as pd
import time
from tqdm import tqdm
from datetime import datetime

endpoints = [
    "https://api.binance.com",
    "https://api1.binance.com",
    "https://api2.binance.com",
    "https://api3.binance.com",
    "https://api4.binance.com",
]
data_endpoints = ["https://data.binance.com/"]


def run_api(command="/api/v3/ping", data_endPoint=False, **params):
    ### Runs API ping command
    try:
        if data_endPoint:
            cmd = "{url}{command}".format(
                url=random.choice(data_endpoints), command=command
            )
        else:
            cmd = "{url}{command}".format(url=random.choice(endpoints), command=command)
        if len(params) == 0:
            r = requests.get(cmd)
        else:
            r = requests.get(cmd, params=params)
        return r
    except Exception as E:
        return "Error: " + str(E)

def server_time():
    ### Returns server time in milliseconds
    return json.loads(run_api(command="/api/v3/time").text)["serverTime"]

def get_depth(symbol="BTCUSDT"):
    ### returns order book
    return json.loads(run_api("/api/v3/depth", symbol=symbol).text)
def get_trades(symbol="BTCUSDT"):
    ### returns recent trades
    return json.loads(run_api("/api/v3/trades", symbol=symbol).text)
def get_klines(symbol="BTCUSDT", interval="1m", startTime="1672587540000", limit=1000):
    try:
        return json.loads(
            run_api(
                "/api/v3/klines",
                symbol=symbol,
                interval=interval,
                startTime=startTime,
                limit=limit,
            ).text
        )
    except:
        return "Data Retreival Error..."
def get_historic_klines(
    start="1672527600000",
    end="1672647480000",
    interval="1m",
    symbol="BTCUSDT",
    limit=1000,
):
    if interval == "1m":
        multiplier = 1
    elif interval == "5m":
        multiplier = 5
    elif interval == "15m":
        multiplier = 15
    elif interval == "30m":
        multiplier = 30
    elif interval == "1h":
        multiplier = 60
    elif interval == "2h":
        multiplier = 120
    elif interval == "4h":
        multiplier = 240
    elif interval == "6h":
        multiplier = 360
    elif interval == "8h":
        multiplier = 480
    elif interval == "12h":
        multiplier = 720
    elif interval == "1d":
        multiplier = 1440
    elif interval == "1w":
        multiplier = 10080
    else:
        raise Exception("Invalid interval")
    All = []
    for start in tqdm(range(int(start), int(end), int(60000 * multiplier * limit))):
        r = get_klines(symbol=symbol, interval=interval, startTime=start, limit=limit)
        for t in r:
            All.append(t)
        if start == All[-1][0]:
            break
        start = All[-1][0]
        time.sleep(2)
    df = pd.DataFrame(
        All,
        columns=[
            "Opentime",
            "Open",
            "High",
            "Low",
            "Close",
            "Volume",
            "CloseTime",
            "QuoteAssetVolume",
            "NumberOfTrades",
            "TakerBuyBaseAssetVolume",
            "TakerBuyQuoteAssetVolume",
            "Un",
        ],
    )
    return df

def get_historic_aggtrades(
    start="1672527600000", end="1672647480000", symbol="BTCUSDT", limit=1000
):
    All = []
    for time in tqdm(range(int(start), int(end), 600000)):
        r = get_aggtrades(
            symbol=symbol, startTime=str(time), endTime=str(time + 600000), limit=limit
        )
        for t in r:
            All.append(t)
    df = pd.DataFrame(All)
    df.columns = [
        "aggtradeID",
        "price",
        "quantity",
        "firsttradeID",
        "lasttradeID",
        "timestamp",
        "buyermaker",
        "bestpriceMatch",
    ]
    return df

def get_latest_klines_dataframe(symbol="BTCUSDT", interval="1m", limit="1000"):
    res = json.loads(
        run_api("/api/v3/klines", symbol=symbol, interval=interval, limit=limit).text
    )
    df = pd.DataFrame(
        res,
        columns=[
            "Opentime",
            "Open",
            "High",
            "Low",
            "Close",
            "Volume",
            "CloseTime",
            "QuoteAssetVolume",
            "NumberOfTrades",
            "TakerBuyBaseAssetVolume",
            "TakerBuyQuoteAssetVolume",
            "Un",
        ],
    )
    df["Time"] = df["Opentime"].apply(
        lambda x: datetime.utcfromtimestamp(x / 1000).strftime("%Y-%m-%d %H:%M:%S")
    )
    df["High"] = df["High"].astype(float)
    df["Low"] = df["Low"].astype(float)
    df["Close"] = df["Close"].astype(float)
    df["Open"] = df["Open"].astype(float)
    df["Volume"] = df["Volume"].astype(float)
    return df

def get_24h_ticker_price_change(symbol="BTCUSDT"):
    return json.loads(run_api("/api/v3/ticker/24hr", symbol=symbol).text)

def get_symbol_price_ticker(symbol="BTCUSDT"):
    return json.loads(run_api("/api/v3/ticker/price", symbol=symbol).text)

def get_symbol_orderbook_ticker(symbol="BTCUSDT"):
    return json.loads(run_api("/api/v3/ticker/bookTicker", symbol=symbol).text)

def get_rollin_window_price_change(symbol="BTCUSDT",window_size='1m'):
    return json.loads(run_api("/api/v3/ticker", symbol=symbol, windowSize=window_size).text)
