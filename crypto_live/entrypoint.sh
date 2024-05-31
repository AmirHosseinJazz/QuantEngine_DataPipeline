#!/bin/bash
set -e

# Function to wait for Kafka Connect to be ready
wait_for_kafka_connect() {
    echo "Waiting for Kafka Connect to be ready..."
    while ! curl -s http://kafka-connect:8085/connectors | grep -q "timescale"; do
      echo "Waiting for Kafka Connect..."
      sleep 30
    done
    echo "Kafka Connect is ready!"
}

# Call the function to ensure Kafka Connect is ready
wait_for_kafka_connect

# Execute the Python script
python main.py