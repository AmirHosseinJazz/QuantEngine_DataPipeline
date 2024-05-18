import os
import psycopg2
from psycopg2.extras import execute_values
from dotenv import load_dotenv
from forex_histdata import *

def get_all_assets():
    load_dotenv()
    asset_list=os.getenv("FOREX_ASSETS").split(',')
    for k in asset_list[:1]:
        try:
            asset_with_forward_slash=k[:3]+'/'+k[3:]
            print('Downloading data for '+asset_with_forward_slash)
            forex_historical_metaTrader(asset=asset_with_forward_slash)
        except Exception as e:
            print('Error downloading data for '+k)
            print(e)
            continue

def forex_historical_metaTrader(asset='EUR/USD'):
    data=get_asset_history(asset)
    load_dotenv()
    db_table="kline_1M"
    db_name=os.getenv("DATABASE")
    db_user=os.getenv("POSTGRES_USER")
    db_pass=os.getenv("POSTGRES_PASSWORD")
    db_host=os.getenv("POSTGRES_HOST")
    conn_params = {
        'dbname': db_name,
        'user': db_user,
        'password': db_pass,
        'host': db_host
    }

    # Establish the database connection
    with psycopg2.connect(**conn_params) as conn:
        with conn.cursor() as cursor:
            for _dataframe in data:
                # Create a list of tuples from the dataframe values
                tuples = [tuple(x) for x in _dataframe.to_numpy()]
                
                # Comma-separated _dataframeframe columns
                cols = ','.join(list(_dataframe.columns))
                
                # SQL query to execute
                query = f"""
                        INSERT INTO "{asset.replace('/','')}"."{db_table}" (
                            datetime, open, high, low, close, volume
                        ) VALUES %s
                        ON CONFLICT (datetime) DO UPDATE SET
                            open = EXCLUDED.open,
                            high = EXCLUDED.high,
                            low = EXCLUDED.low,
                            close = EXCLUDED.close,
                            volume = EXCLUDED.volume;
                        """
                try:
                    execute_values(cursor, query, tuples)
                    
                    conn.commit()
                    print(f"Data inserted into {asset.replace('/','')}.'{db_table}' successfully.")
                except Exception as e:
                    print("Error: ", e)
                    conn.rollback()


if __name__ == "__main__":
    # get_all_assets()
    pass
    ####
    # flow_fhistorical_source1=get_all_assets.to_deployment(name='forex_history',cron='0 0 1 * *')
    # serve(flow_fhistorical_source1)