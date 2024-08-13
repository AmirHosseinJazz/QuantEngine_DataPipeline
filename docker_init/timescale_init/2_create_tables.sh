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


# psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname "$DATABASE" <<-EOSQL

#         CREATE TABLE IF NOT EXISTS "general"."feargreed"
#     (
#         "Item" character varying COLLATE pg_catalog."default" NOT NULL,
#         "DateTime" character varying COLLATE pg_catalog."default" NOT NULL,
#         "Value" double precision NOT NULL,
#         CONSTRAINT fear_greed_pkey PRIMARY KEY ("Item", "DateTime")
#     )

#     TABLESPACE pg_default;

#     ALTER TABLE IF EXISTS "general"."feargreed"
#     OWNER TO $POSTGRES_USER;
# EOSQL

# psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname "$DATABASE" <<-EOSQL

#         CREATE TABLE IF NOT EXISTS "news"."crypto_events"
#         (
#         event_id bigint NOT NULL,
#         date character varying COLLATE pg_catalog."default",
#         "time" character varying COLLATE pg_catalog."default",
#         "Impact" character varying COLLATE pg_catalog."default",
#         title character varying COLLATE pg_catalog."default",
#         details character varying COLLATE pg_catalog."default",
#         actual character varying COLLATE pg_catalog."default",
#         forecast character varying COLLATE pg_catalog."default",
#         previous character varying COLLATE pg_catalog."default",
#         CONSTRAINT crypto_events_pkey PRIMARY KEY (event_id)
#         )
#     TABLESPACE pg_default;

#     ALTER TABLE IF EXISTS "news"."crypto_events"
#     OWNER TO $POSTGRES_USER;
# EOSQL


# psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname "$DATABASE" <<-EOSQL

#         CREATE TABLE IF NOT EXISTS "news"."cryptofactory_news"
#         (
#         datetime character varying COLLATE pg_catalog."default" NOT NULL,
#         title character varying COLLATE pg_catalog."default",
#         href character varying COLLATE pg_catalog."default",
#         CONSTRAINT cryptofactory_news_pkey PRIMARY KEY (datetime)
#         )
#     TABLESPACE pg_default;

#     ALTER TABLE IF EXISTS "news"."cryptofactory_news_detailed"
#     OWNER TO $POSTGRES_USER;
# EOSQL

# psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname "$DATABASE" <<-EOSQL

#         CREATE TABLE IF NOT EXISTS "news"."cryptofactory_news_detailed"
#         (
#         datetime character varying COLLATE pg_catalog."default" NOT NULL,
#         text text COLLATE pg_catalog."default" NOT NULL,
#         CONSTRAINT cryptofactory_news_detailed_pkey PRIMARY KEY (datetime)
#         )
#     TABLESPACE pg_default;

#     ALTER TABLE IF EXISTS "news"."cryptofactory_news_detailed"
#     OWNER TO $POSTGRES_USER;
# EOSQL

# psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname "$DATABASE" <<-EOSQL

#         CREATE TABLE IF NOT EXISTS "general"."money_index"
#         (
#         "Item" character varying COLLATE pg_catalog."default" NOT NULL,
#         "DateTime" character varying COLLATE pg_catalog."default" NOT NULL,
#         "Value" double precision,
#         CONSTRAINT money_index_pkey PRIMARY KEY ("Item", "DateTime")
#         )
#     TABLESPACE pg_default;

#     ALTER TABLE IF EXISTS "general"."money_index"
#     OWNER TO $POSTGRES_USER;
# EOSQL