import os
import time
import shutil
import zipfile
import pandas as pd
import utility
import binance
from datetime import datetime
####### Kline data ########
def insert_klines(
    startyear="2020",
    startmonth="01",
    startday="01",
    symbol="BTCUSDT",
    endyear="",
    endmonth="",
    endday="",
    interval="1m",
):
    start = str(utility.unix_ts(year=startyear, month=startmonth, day=startday))
    ##
    if endyear == "":
        today = time.strftime("%Y-%m-%d")
        today = today.split("-")
        today_year = today[0]
        today_month = today[1]
        today_day = today[2]
        end = str(utility.unix_ts(year=today_year, month=today_month, day=today_day))
    else:
        end = str(utility.unix_ts(year=endyear, month=endmonth, day=endday))
    ##
    print("Fetching data from Binance API...")
    print(f"Start: {start} | End: {end}")
    df = binance.get_historic_klines(start=start, end=end, symbol=symbol, interval=interval)
    print("# of rows: ", len(df))
    return df

def update_klines(startyear="2024",
    startmonth="04",
    startday="15",
    start_hour="00",
    start_minute="00",
    symbol="BTCUSDT",
    endyear="",
    endmonth="",
    endday="",
    end_hour="",
    end_minute="",
    interval="1m",):
    start = str(utility.unix_ts(year=startyear, month=startmonth, day=startday))
    ##
    if endyear == "":
        today = datetime.now()
        today_year= str(today.year)
        today_month = str(today.month)
        today_day = str(today.day)
        today_hour = str(today.hour)
        today_minute = str(today.minute)
      
        end = str(utility.unix_ts(year=today_year, month=today_month, day=today_day, hour=today_hour, minute=today_minute))
    else:
        end = str(utility.unix_ts(year=endyear, month=endmonth, day=endday, hour=end_hour, minute=end_minute))
    df = binance.get_historic_klines(start=start, end=end, symbol=symbol, interval=interval)
    print("# of rows: ", len(df))
    return df

