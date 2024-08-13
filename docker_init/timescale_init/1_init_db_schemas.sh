#!/bin/bash
set -e

psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname "postgres" -c "CREATE DATABASE backtrader;"
# psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname "postgres" -c "CREATE DATABASE \"$TIMESCALE_DATABASE\";"


# IFS=',' read -ra ADDR <<< "$FOREX_ASSETS"

# for asset in "${ADDR[@]}"; do
#     modified_asset="${asset//\//}"
#     psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname "$DATABASE" -c "CREATE SCHEMA \"$modified_asset\";"
# done

IFS=',' read -ra ADDR2 <<< "$CRYPTO_ASSETS"
for asset in "${ADDR2[@]}"; do
    psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname "$TIMESCALE_DATABASE" -c "CREATE SCHEMA \"$asset\";"
done
# psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname "$DATABASE" -c "CREATE SCHEMA news;"

# psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname "$DATABASE" -c "CREATE SCHEMA economic;"

# psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname "$DATABASE" -c "CREATE SCHEMA sentiment;"

# psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname "$DATABASE" -c "CREATE SCHEMA general;"


