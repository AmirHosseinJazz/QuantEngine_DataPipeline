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

## -- Prefect Flows -- ##


@flow(log_prints=True)
def btc_daily():
    crypto_historic(symbol="BTCUSDT", interval="1d")


@flow(log_prints=True)
def btc_hourly():
    crypto_historic(symbol="BTCUSDT", interval="1h")


@flow(log_prints=True)
def btc_minutely():
    crypto_historic(symbol="BTCUSDT", interval="1m")


@flow(log_prints=True)
def btc_daily_update():
    crypto_update_latest(symbol="BTCUSDT", interval="1d")


@flow(log_prints=True)
def btc_hourly_update():
    crypto_update_latest(symbol="BTCUSDT", interval="1h")


@flow(log_prints=True)
def btc_minutely_update():
    crypto_update_latest(symbol="BTCUSDT", interval="1m")


@flow(log_prints=True)
def eth_daily():
    crypto_historic(symbol="ETHUSDT", interval="1d")


@flow(log_prints=True)
def eth_hourly():
    crypto_historic(symbol="ETHUSDT", interval="1h")


@flow(log_prints=True)
def eth_minutely():
    crypto_historic(symbol="ETHUSDT", interval="1m")


@flow(log_prints=True)
def eth_daily_update():
    crypto_update_latest(symbol="ETHUSDT", interval="1d")


@flow(log_prints=True)
def eth_hourly_update():
    crypto_update_latest(symbol="ETHUSDT", interval="1h")


@flow(log_prints=True)
def eth_minutely_update():
    crypto_update_latest(symbol="ETHUSDT", interval="1m")


########## -- Prefect Flows -- ##########
@flow(log_prints=True)
def btc_tech_daily():
    historical_technical(symbol="BTCUSDT", interval="1d")


@flow(log_prints=True)
def btc_tech_hourly():
    historical_technical(symbol="BTCUSDT", interval="1h")


@flow(log_prints=True)
def btc_tech_minutely():
    historical_technical(symbol="BTCUSDT", interval="1m")


@flow(log_prints=True)
def btc_tech_daily_update():
    update_technical(symbol="BTCUSDT", interval="1d")


@flow(log_prints=True)
def btc_tech_hourly_update():
    update_technical(symbol="BTCUSDT", interval="1h")


@flow(log_prints=True)
def btc_tech_minutely_update():
    update_technical(symbol="BTCUSDT", interval="1m")


@flow(log_prints=True)
def eth_tech_daily():
    historical_technical(symbol="ETHUSDT", interval="1d")


@flow(log_prints=True)
def eth_tech_hourly():
    historical_technical(symbol="ETHUSDT", interval="1h")


@flow(log_prints=True)
def eth_tech_minutely():
    historical_technical(symbol="ETHUSDT", interval="1m")


@flow(log_prints=True)
def eth_tech_daily_update():
    update_technical(symbol="ETHUSDT", interval="1d")


@flow(log_prints=True)
def eth_tech_hourly_update():
    update_technical(symbol="ETHUSDT", interval="1h")


@flow(log_prints=True)
def eth_tech_minutely_update():
    update_technical(symbol="ETHUSDT", interval="1m")


@flow(log_prints=True)
def fear_greed_flow():
    fear_greed()


@flow(log_prints=True)
def onchain_indicators_flow():
    onchain_indicators(symbol="BTCUSDT")


@flow(log_prints=True)
def event_update_flow():
    crypto_events()


@flow(log_prints=True)
def event_historic_flow():
    crypto_events_historic()


## -- Functions -- ##
def crypto_historic(symbol="BTCUSDT", interval="1m"):
    data = insert_klines(symbol=symbol, interval=interval)
    load_dotenv()
    if interval == "1m":
        db_table = f'"{symbol}"."kline_1M"'
    elif interval == "1h":
        db_table = f'"{symbol}"."kline_1H"'
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


def lastest_kline(symbol="BTCUSDT", interval="1m"):
    load_dotenv()
    if interval == "1m":
        db_table = f'"{symbol}"."kline_1M"'
    elif interval == "1h":
        db_table = f'"{symbol}"."kline_1H"'
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
    # Establish the database connection
    with psycopg2.connect(**conn_params) as conn:
        with conn.cursor() as cursor:
            query = f'SELECT * FROM {db_table} ORDER BY "CloseTime" DESC LIMIT 1'
            cursor.execute(query)
            data = cursor.fetchall()
            # cols
            cols = [desc[0] for desc in cursor.description]
    # get date from the data
    DF = pd.DataFrame(data=data, columns=cols)
    try:
        # Convert to date
        date = utility.unix_ts_to_date(DF["Opentime"].values[0], milli=True)
        # strint to date
        date_time_obj = datetime.strptime(date, "%Y-%m-%d %H:%M:%S")
        return date_time_obj
    except Exception as e:
        print(e)
        return None


def crypto_update_latest(symbol="BTCUSDT", interval="1m"):
    last_update = lastest_kline(symbol=symbol, interval=interval)
    if last_update is None:
        print("No historic data in the database")
        return
    data = update_klines(
        symbol=symbol,
        interval=interval,
        startyear=last_update.year,
        startmonth=last_update.month,
        startday=last_update.day,
        start_hour=last_update.hour,
        start_minute=last_update.minute,
    )
    load_dotenv()
    if interval == "1m":
        db_table = f'"{symbol}"."kline_1M"'
    elif interval == "1h":
        db_table = f'"{symbol}"."kline_1H"'
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


######## Technical Analysis ########
def historical_technical(symbol="BTCUSDT", interval="1d"):
    load_dotenv()
    if interval == "1m":
        db_table = f'"{symbol}"."kline_1M"'
        db_table_tech = f'"{symbol}"."technical_1M"'
    elif interval == "1h":
        db_table = f'"{symbol}"."kline_1H"'
        db_table_tech = f'"{symbol}"."technical_1H"'
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


def update_technical(symbol="BTCUSDT", interval="1d"):
    load_dotenv()
    if interval == "1m":
        db_table = f'"{symbol}"."kline_1M"'
        db_table_tech = f'"{symbol}"."technical_1M"'
    elif interval == "1h":
        db_table = f'"{symbol}"."kline_1H"'
        db_table_tech = f'"{symbol}"."technical_1H"'
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
        with conn.cursor() as cursor:
            query = f"""select "Opentime" from {db_table}
            where "CloseTime" > (select DISTINCT "CloseTime" from {db_table_tech} order by "CloseTime" desc limit 1 )
            order by "Opentime" asc
            limit 1"""
            cursor.execute(query)
            data = cursor.fetchall()
            # cols
            cols = [desc[0] for desc in cursor.description]
    # get date from the data
    try:
        OpenTime = pd.DataFrame(data=data, columns=cols).iloc[-1][0]
    except:
        print("No data to update")
        return

    with psycopg2.connect(**conn_params) as conn:
        with conn.cursor() as cur:
            cur.execute(
                f"""
            SELECT * from  {db_table} where "Opentime" in ((select DISTINCT("Opentime") from {db_table} where "Opentime" <= {OpenTime} order by "Opentime" desc  limit 300)	UNION
            (select DISTINCT("Opentime") from {db_table} where "Opentime" >= {OpenTime} order by "Opentime" desc ))
            """
            )
            rows = cur.fetchall()
            columns = [desc[0] for desc in cur.description]
            data = pd.DataFrame(rows, columns=columns)
            try:
                Technical = technical.technial_indicators(data)
            except Exception as e:
                print(e)
                return
            for i in tqdm(range(len(Technical.columns))):
                InDF = Technical.iloc[:, i]
                InDF = InDF.reset_index()
                InDF["Item"] = Technical.columns[i]
                InDF.columns = ["CloseTime", "Value", "Item"]
                InDF.dropna(subset=["Value"], inplace=True)
                tuples = [tuple(x) for x in InDF.to_numpy()]
                cols = ",".join([f'"{i}"' for i in InDF.columns.tolist()])
                query = f"INSERT INTO {db_table_tech} ({cols}) VALUES %s ON CONFLICT "
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


####
def fear_greed():
    load_dotenv()
    db_name = os.getenv("DATABASE")
    db_user = os.getenv("POSTGRES_USER")
    db_pass = os.getenv("POSTGRES_PASSWORD")
    db_host = os.getenv("POSTGRES_HOST")
    db_table = "general.feargreed"
    conn_params = {
        "dbname": db_name,
        "user": db_user,
        "password": db_pass,
        "host": db_host,
    }
    with psycopg2.connect(**conn_params) as conn:
        with conn.cursor() as cur:
            DF = misc.fear_greed()
            tuples = [tuple(x) for x in DF.to_numpy()]
            cols = ",".join([f'"{i}"' for i in DF.columns.tolist()])
            query = f"INSERT INTO {db_table} ({cols}) VALUES %s ON CONFLICT DO NOTHING"
            try:
                execute_values(cur, query, tuples)
                conn.commit()
                print(f"Data inserted into {db_table} successfully.")
            except Exception as e:
                print("Error: ", e)
                conn.rollback()
    print(f"Data inserted into {db_table} successfully.")


def onchain_indicators(symbol="BTCUSDT"):
    load_dotenv()
    db_name = os.getenv("DATABASE")
    db_user = os.getenv("POSTGRES_USER")
    db_pass = os.getenv("POSTGRES_PASSWORD")
    db_host = os.getenv("POSTGRES_HOST")
    db_table = f'"{symbol}"."onchain_indicators"'
    conn_params = {
        "dbname": db_name,
        "user": db_user,
        "password": db_pass,
        "host": db_host,
    }
    with psycopg2.connect(**conn_params) as conn:
        with conn.cursor() as cur:
            DF = misc.onchain_indicators()
            tuples = [tuple(x) for x in DF.to_numpy()]
            cols = ",".join([f'"{i}"' for i in DF.columns.tolist()])
            query = f"INSERT INTO {db_table} ({cols}) VALUES %s ON CONFLICT DO NOTHING"
            try:
                execute_values(cur, query, tuples)
                conn.commit()
                print(f"Data inserted into {db_table} successfully.")
            except Exception as e:
                print("Error: ", e)
                conn.rollback()
    print(f"Data inserted into {db_table} successfully.")


def money_index():
    load_dotenv()
    db_name = os.getenv("DATABASE")
    db_user = os.getenv("POSTGRES_USER")
    db_pass = os.getenv("POSTGRES_PASSWORD")
    db_host = os.getenv("POSTGRES_HOST")
    db_table = f'"general"."money_index"'
    conn_params = {
        "dbname": db_name,
        "user": db_user,
        "password": db_pass,
        "host": db_host,
    }
    with psycopg2.connect(**conn_params) as conn:
        with conn.cursor() as cur:
            DF = misc.money_index_data()
            tuples = [tuple(x) for x in DF.to_numpy()]
            cols = ",".join([f'"{i}"' for i in DF.columns.tolist()])
            query = f"INSERT INTO {db_table} ({cols}) VALUES %s ON CONFLICT DO NOTHING"
            try:
                execute_values(cur, query, tuples)
                conn.commit()
                print(f"Data inserted into {db_table} successfully.")
            except Exception as e:
                print("Error: ", e)
                conn.rollback()
    print(f"Data inserted into {db_table} successfully.")


###
def crypto_events():
    load_dotenv()
    db_name = os.getenv("DATABASE")
    db_user = os.getenv("POSTGRES_USER")
    db_pass = os.getenv("POSTGRES_PASSWORD")
    db_host = os.getenv("POSTGRES_HOST")
    db_table = f'"news"."crypto_events"'
    conn_params = {
        "dbname": db_name,
        "user": db_user,
        "password": db_pass,
        "host": db_host,
    }
    with psycopg2.connect(**conn_params) as conn:
        with conn.cursor() as cur:
            DF = misc.update_crypto_calendar()
            tuples = [tuple(x) for x in DF.to_numpy()]
            cols = ",".join([f'"{i}"' for i in DF.columns.tolist()])
            query = f"INSERT INTO {db_table} ({cols}) VALUES %s ON CONFLICT DO NOTHING"
            try:
                execute_values(cur, query, tuples)
                conn.commit()
                print(f"Data inserted into {db_table} successfully.")
            except Exception as e:
                print("Error: ", e)
                conn.rollback()
    print(f"Data inserted into {db_table} successfully.")


def crypto_events_historic():
    load_dotenv()
    db_name = os.getenv("DATABASE")
    db_user = os.getenv("POSTGRES_USER")
    db_pass = os.getenv("POSTGRES_PASSWORD")
    db_host = os.getenv("POSTGRES_HOST")
    db_table = f'"news"."crypto_events"'
    conn_params = {
        "dbname": db_name,
        "user": db_user,
        "password": db_pass,
        "host": db_host,
    }
    with psycopg2.connect(**conn_params) as conn:
        with conn.cursor() as cur:
            DF = misc.all_crypto_calendar()
            tuples = [tuple(x) for x in DF.to_numpy()]
            cols = ",".join([f'"{i}"' for i in DF.columns.tolist()])
            query = f"INSERT INTO {db_table} ({cols}) VALUES %s ON CONFLICT DO NOTHING"
            try:
                execute_values(cur, query, tuples)
                conn.commit()
                print(f"Data inserted into {db_table} successfully.")
            except Exception as e:
                print("Error: ", e)
                conn.rollback()
    print(f"Data inserted into {db_table} successfully.")


if __name__ == "__main__":

    historic_btc_daily = btc_daily.to_deployment(
        name="btc_historic_daily", cron="10 0 1 * *"
    )
    historic_btc_hourly = btc_hourly.to_deployment(
        name="btc_historic_hourly", cron="15 0 1 * *"
    )
    historic_btc_minutely = btc_minutely.to_deployment(
        name="btc_historic_minute", cron="20 0 1 * *"
    )

    update_btc_daily = btc_daily_update.to_deployment(
        name="btc_daily_update", cron="1 10 * * *"
    )
    update_btc_hourly = btc_hourly_update.to_deployment(
        name="btc_hourly_update", cron="1 */5 * * *"
    )
    update_btc_minutely = btc_minutely_update.to_deployment(
        name="btc_minute_update", cron="*/5 * * * *"
    )

    # historic_eth_daily=eth_daily.to_deployment(name='eth_historic_daily',cron='10 1 1 * *')
    # historic_eth_hourly=eth_hourly.to_deployment(name='eth_historic_hourly',cron='15 1 1 * *')
    # historic_eth_minutely=eth_minutely.to_deployment(name='eth_historic_minute',cron='20 1 1 * *')

    # update_eth_daily=eth_daily_update.to_deployment(name='eth_daily_update',cron='1 10 * * *')
    # update_eth_hourly=eth_hourly_update.to_deployment(name='eth_hourly_update',cron='1 */5 * * *')
    # update_eth_minutely=eth_minutely_update.to_deployment(name='eth_minute_update',cron='*/5 * * * *')

    btc_tech_daily = btc_tech_daily.to_deployment(
        name="btc_tech_daily", cron="10 3 1 * *"
    )
    btc_tech_hourly = btc_tech_hourly.to_deployment(
        name="btc_tech_hourly", cron="15 3 1 * *"
    )
    btc_tech_minutely = btc_tech_minutely.to_deployment(
        name="btc_tech_minute", cron="20 3 1 * *"
    )

    btc_tech_daily_update = btc_tech_daily_update.to_deployment(
        name="btc_tech_daily_update", cron="1 10 * * *"
    )
    btc_tech_hourly_update = btc_tech_hourly_update.to_deployment(
        name="btc_tech_hourly_update", cron="1 */5 * * *"
    )
    btc_tech_minutely_update = btc_tech_minutely_update.to_deployment(
        name="btc_tech_minute_update", cron="*/5 * * * *"
    )

    # eth_tech_daily=eth_tech_daily.to_deployment(name='eth_tech_daily',cron='10 4 1 * *')
    # eth_tech_hourly=eth_tech_hourly.to_deployment(name='eth_tech_hourly',cron='15 4 1 * *')
    # eth_tech_minutely=eth_tech_minutely.to_deployment(name='eth_tech_minute',cron='20 4 1 * *')

    # eth_tech_daily_update=eth_tech_daily_update.to_deployment(name='eth_tech_daily_update',cron='1 10 * * *')
    # eth_tech_hourly_update=eth_tech_hourly_update.to_deployment(name='eth_tech_hourly_update',cron='1 */5 * * *')
    # eth_tech_minutely_update=eth_tech_minutely_update.to_deployment(name='eth_tech_minute_update',cron='*/5 * * * *')

    fear_greed_daily = fear_greed_flow.to_deployment(
        name="fear_greed", cron="0 7 * * *"
    )
    onchain_daily = onchain_indicators_flow.to_deployment(
        name="onchain_indicators", cron="0 8 * * *"
    )
    crypto_event_update_flow = event_update_flow.to_deployment(
        name="event_update", cron="10 */6 * * *"
    )
    crypto_event_historical_flow = event_historic_flow.to_deployment(
        name="event_historic", cron="0 6 1 * *"
    )

    serve(
        historic_btc_daily,
        historic_btc_hourly,
        historic_btc_minutely,
        update_btc_daily,
        update_btc_hourly,
        update_btc_minutely,
        # historic_eth_daily,
        # historic_eth_hourly,
        # historic_eth_minutely,
        # update_eth_daily,
        # update_eth_hourly,
        # update_eth_minutely,
        btc_tech_daily,
        btc_tech_hourly,
        btc_tech_minutely,
        btc_tech_daily_update,
        btc_tech_hourly_update,
        btc_tech_minutely_update,
        # eth_tech_daily,
        # eth_tech_hourly,
        # eth_tech_minutely,
        # eth_tech_daily_update,
        # eth_tech_hourly_update,
        # eth_tech_minutely_update,
        fear_greed_daily,
        onchain_daily,
        crypto_event_update_flow,
        # crypto_event_historical_flow,
    )
