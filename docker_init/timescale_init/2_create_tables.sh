#!/bin/bash
set -e

# Assuming ASSETS is a comma-separated list of asset names
IFS=',' read -ra ADDR <<< "$FOREX_ASSETS"
IFS=',' read -ra ADDR2 <<< "$CRYPTO_ASSETS"


export PGPASSWORD=$POSTGRES_PASSWORD

# for asset in "${ADDR[@]}"
# do
# modified_asset="${asset//\//}"



# psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname "$DATABASE" <<-EOSQL
    # CREATE TABLE "$modified_asset"."kline_1M"
#     (
#         datetime character varying COLLATE pg_catalog."default" NOT NULL,
#         open double precision NOT NULL,
#         high double precision NOT NULL,
#         low double precision NOT NULL,
#         close double precision NOT NULL,
#         volume double precision NOT NULL,
#         CONSTRAINT "kline_1M_pkey" PRIMARY KEY (datetime)
#     )

#     TABLESPACE pg_default;

#     ALTER TABLE IF EXISTS "$modified_asset"."kline_1M"
#     OWNER TO $POSTGRES_USER;
# EOSQL
# done 

for asset in "${ADDR2[@]}"
do 

psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname "$TIMESCALE_DATABASE" <<-EOSQL
    CREATE TABLE IF NOT EXISTS "$asset"."strategy_metrics"
    (
        time TIMESTAMPTZ PRIMARY KEY,
        close FLOAT,
        position INT,
        cash FLOAT,
        value FLOAT

    )

    TABLESPACE pg_default;

    ALTER TABLE IF EXISTS "$asset"."strategy_metrics"
    OWNER TO $POSTGRES_USER; 
EOSQL

psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname "$TIMESCALE_DATABASE" <<-EOSQL
    CREATE TABLE IF NOT EXISTS "$asset"."strategy_trades"
    (
        time TIMESTAMPTZ PRIMARY KEY,
        trade_type TEXT,
        price FLOAT,
        pnl FLOAT,
        pnlcomm FLOAT
    )

    TABLESPACE pg_default;

    ALTER TABLE IF EXISTS "$asset"."strategy_trades"
    OWNER TO $POSTGRES_USER;
EOSQL




done


psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname "$TIMESCALE_DATABASE" <<-EOSQL

        CREATE TABLE IF NOT EXISTS "public"."strategy_metrics"
    (
       test_name character varying COLLATE pg_catalog."default" NOT NULL,
        "time" timestamp with time zone NOT NULL,
        close double precision,
        "position" integer,
        cash double precision,
        value double precision,
        CONSTRAINT strategy_metrics_pkey PRIMARY KEY (test_name, "time")
    )

    TABLESPACE pg_default;

    ALTER TABLE IF EXISTS "public"."strategy_metrics"
    OWNER TO $POSTGRES_USER;
EOSQL

psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname "$TIMESCALE_DATABASE" <<-EOSQL

        CREATE TABLE IF NOT EXISTS "public"."strategy_trades"
    (
        test_name character varying COLLATE pg_catalog."default" NOT NULL,
        "time" timestamp with time zone NOT NULL,
        trade_type text COLLATE pg_catalog."default",
        price double precision,
        pnl double precision,
        pnlcomm double precision,
        CONSTRAINT strategy_trades_pkey PRIMARY KEY (test_name, "time")
    )

    TABLESPACE pg_default;

    ALTER TABLE IF EXISTS "public"."strategy_trades"
    OWNER TO $POSTGRES_USER;
EOSQL


psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname "$TIMESCALE_DATABASE" <<-EOSQL

        CREATE TABLE IF NOT EXISTS "public"."timeseries_metrics"
    (
        id SERIAL PRIMARY KEY,              
        test_name VARCHAR(255) NOT NULL,    
        metric_name VARCHAR(255) NOT NULL,  
        timestamp DATE NOT NULL,            
        metric_value FLOAT8,                
        created_at TIMESTAMPTZ DEFAULT NOW()    )

    TABLESPACE pg_default;

    ALTER TABLE IF EXISTS "public"."timeseries_metrics"
    OWNER TO $POSTGRES_USER;
EOSQL


psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname "$TIMESCALE_DATABASE" <<-EOSQL

        CREATE TABLE IF NOT EXISTS "public"."single_metrics"
    (
         id SERIAL PRIMARY KEY,              -- Automatically incrementing ID
    test_name VARCHAR(255) NOT NULL,    -- Test name (up to 255 characters)
    metric_name VARCHAR(255) NOT NULL,  -- Metric name (up to 255 characters)
    metric_value FLOAT8,                -- Metric value as a double precision float
    created_at TIMESTAMPTZ DEFAULT NOW()    )

    TABLESPACE pg_default;

    ALTER TABLE IF EXISTS "public"."single_metrics"
    OWNER TO $POSTGRES_USER;
EOSQL
