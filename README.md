# Project Title

Cryptic:
Data inflow, schedulers and kafka services

### Details

Postgres:
Environment Variables in .env root
Init scripts in:
./docker_init/postgres_init/
-- initial db, schema and tables creation

---

PgAdmin:
Environment Variables in .env root
Init scripts in:
./docker_init/pgadmin_init/
-- .pgpass connection string to pghost
-- servers.json => details for pgadmin
-- wait-for-it.sh => waiting for postgres to setup

---

Perfect Server:
Environment variables in .env of root
\*Needs a copy of env inside the folder for db connection(setup in prepare_env.sh)
-- perfect_server/Dockerfile => Setting up pip install perfect => wait for postgres => run perfect server

---

---

Crypto_historic:
Environment variables => \*Needs a copy of env inside the folder for db connection(setup in prepare_env.sh)
--> update asset minute, hourly and daily -> see main func in crypto_historic.py
--> technical indicators in technical.py
--> other sources of data in misc.py (e.g fear greed)

## \*\*\* Long term kafka will replace lower timeframe

Forex_historic:
Same idea but not functional now.

---

Crypto_live:
ws streams of binance to kafka
.env copied from root folder
\*\* To get the historical data , aggregation functions on ws streams in kafka should be implented
=> Dockerfile to install kafka client and run entrypoint.sh => waiting for kafka connect service and run the main.py

### Deleting between project

docker rm -v -f $(docker ps -qa)

docker compose exec -it cryptic_kafka kafka-console-producer --broker-list cryptic_kafka:9092 --topic nys

docker compose exec -it cryptic_kafka kafka-topics --create --topic nys --partitions 1 --replication-factor 1 --bootstrap-server cryptic_kafka:9092
docker-compose exec cryptic_kafka kafka-console-producer --broker-list localhost:9092 --topic nys

docker-compose exec cryptic_kafka kafka-console-consumer --bootstrap-server localhost:9092 --topic nys --from-beginning



### ToDo:
fix kafka aggregation -> to timescale db
fix forex 
fix rest of technical and misc
- setting up data checks 
