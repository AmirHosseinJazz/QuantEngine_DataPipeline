import os
import psycopg2
from psycopg2 import sql
from psycopg2.extras import execute_values
from dotenv import load_dotenv
from crypto_histdata import *
from prefect import flow, serve, get_client
from datetime import datetime
import technical
import utility
import misc

import pandas as pd

from tqdm import tqdm

def crypto_historic(symbol="BTCUSDT", interval="1m"):
    data = insert_klines(symbol=symbol, interval=interval)
    load_dotenv()
    if interval == "1m":
        db_table = f'"{symbol}"."kline_1M"'
    elif interval=='15m':
        db_table = f'"{symbol}"."kline_15M"'
    elif interval == "1h":
        db_table = f'"{symbol}"."kline_1H"'
    elif interval == "4h":
        db_table = f'"{symbol}"."kline_4H"'
    elif interval == "1d":
        db_table = f'"{symbol}"."kline_1D"'
    db_name = os.getenv("DATABASE")
    db_user = os.getenv("POSTGRES_USER")
    db_pass = os.getenv("POSTGRES_PASSWORD")
    db_host = os.getenv("POSTGRES_HOST")
    conn_params = {
        "dbname": db_name,
        "user": db_user,
        "password": db_pass,
        "host": db_host,
    }
    print(db_table)
    # Establish the database connection
    with psycopg2.connect(**conn_params) as conn:
        with conn.cursor() as cursor:
            data = data.drop_duplicates()
            tuples = [tuple(x) for x in data.to_numpy()]

            cols = ",".join(f'"{col}"' for col in data.columns)
            # SQL query to execute, corrected for placeholders
            query = """
                INSERT INTO {table} ({fields}) VALUES %s
                ON CONFLICT ("Opentime", "CloseTime") DO UPDATE
                SET "Open" = EXCLUDED."Open", "High" = EXCLUDED."High", "Low" = EXCLUDED."Low", 
                    "Close" = EXCLUDED."Close", "Volume" = EXCLUDED."Volume", 
                    "QuoteAssetVolume" = EXCLUDED."QuoteAssetVolume", "NumberOfTrades" = EXCLUDED."NumberOfTrades", 
                    "TakerBuyBaseAssetVolume" = EXCLUDED."TakerBuyBaseAssetVolume",
                    "TakerBuyQuoteAssetVolume" = EXCLUDED."TakerBuyQuoteAssetVolume", "Un" = EXCLUDED."Un"
            """.format(
                table=db_table, fields=cols
            )

            # Execute the query with placeholders correctly mapped
            try:
                execute_values(cursor, query, tuples)
                conn.commit()
                print(f"Data inserted into {db_table} successfully.")
            except Exception as e:
                print("Error: ", e)
                conn.rollback()

def historical_technical(symbol="BTCUSDT", interval="1d"):
    load_dotenv()
    if interval == "1m":
        db_table = f'"{symbol}"."kline_1M"'
        db_table_tech = f'"{symbol}"."technical_1M"'
    elif interval == "15m":
        db_table = f'"{symbol}"."kline_15M"'
        db_table_tech = f'"{symbol}"."technical_15M"'

    elif interval == "1h":
        db_table = f'"{symbol}"."kline_1H"'
        db_table_tech = f'"{symbol}"."technical_1H"'
    elif interval == "4h":
        db_table = f'"{symbol}"."kline_4H"'
        db_table_tech = f'"{symbol}"."technical_4H"'

    elif interval == "1d":
        db_table = f'"{symbol}"."kline_1D"'
        db_table_tech = f'"{symbol}"."technical_1D"'
    else:
        print("Invalid interval")
        return
    db_name = os.getenv("DATABASE")
    db_user = os.getenv("POSTGRES_USER")
    db_pass = os.getenv("POSTGRES_PASSWORD")
    db_host = os.getenv("POSTGRES_HOST")
    conn_params = {
        "dbname": db_name,
        "user": db_user,
        "password": db_pass,
        "host": db_host,
    }
    with psycopg2.connect(**conn_params) as conn:
        with conn.cursor() as cur:
            cur.execute(f"SELECT * FROM {db_table}")
            rows = cur.fetchall()
            columns = [desc[0] for desc in cur.description]
            data = pd.DataFrame(rows, columns=columns)
    Technical = technical.technial_indicators(data)
    with psycopg2.connect(**conn_params) as conn:
        with conn.cursor() as cur:
            for i in tqdm(range(len(Technical.columns))):
                InDF = Technical.iloc[:, i]
                InDF = InDF.reset_index()
                InDF["Item"] = Technical.columns[i]
                InDF.columns = ["CloseTime", "Value", "Item"]
                InDF.dropna(subset=["Value"], inplace=True)
                tuples = [tuple(x) for x in InDF.to_numpy()]
                cols = ",".join([f'"{i}"' for i in InDF.columns.tolist()])
                query = (
                    f"INSERT INTO {db_table}_technical ({cols}) VALUES %s ON CONFLICT "
                )
                query = """
                INSERT INTO {table} ({fields}) VALUES %s
                ON CONFLICT ("Item", "CloseTime") DO UPDATE
                SET "Value" = EXCLUDED."Value"
                """.format(
                    table=db_table_tech, fields=cols
                )
                try:
                    execute_values(cur, query, tuples)
                    conn.commit()
                except Exception as e:
                    print("Error: ", e)
                    conn.rollback()
    print(f"Data inserted into {db_table_tech} successfully.")


if __name__=="__main__":
    # crypto_historic(symbol="BTCUSDT", interval="15m")
    historical_technical(symbol="BTCUSDT", interval="15m")
    historical_technical(symbol="BTCUSDT", interval="4h")