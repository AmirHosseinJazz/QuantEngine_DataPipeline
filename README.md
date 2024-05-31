# Project Title

A docker compose with bash scripts to setup a postgres server, configured with prefect for orchestration, fast api for endpoint and pgadmin for viusal inspection

## Installation

execute by running ./run_docker



### Deleting between project
docker rm -v -f $(docker ps -qa)


docker compose exec -it cryptic_kafka kafka-console-producer --broker-list cryptic_kafka:9092 --topic nys


docker compose exec -it cryptic_kafka kafka-topics --create --topic nys --partitions 1 --replication-factor 1 --bootstrap-server cryptic_kafka:9092
docker-compose exec cryptic_kafka kafka-console-producer --broker-list localhost:9092 --topic nys


docker-compose exec cryptic_kafka kafka-console-consumer --bootstrap-server localhost:9092 --topic nys --from-beginning
