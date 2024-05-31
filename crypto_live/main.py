from confluent_kafka.avro import AvroProducer
from confluent_kafka import avro
import time
from dotenv import load_dotenv
import os
import asyncio
import websockets
import json


async def binance_socket(avro_agg_trade, avro_trade, avro_kline):
    uri = "wss://stream.binance.com:9443/stream?streams=btcusdt@trade/btcusdt@aggTrade/btcusdt@kline_1m"

    while True:  # Continuously attempt to reconnect
        try:
            # Connect to the WebSocket server without automatic ping handling
            async with websockets.connect(uri, ping_interval=None) as websocket:
                print("Opened connection")

                # Handle incoming messages
                async for message in websocket:
                    if isinstance(message, bytes) and len(message) == 0:
                        # Manual handling of ping messages (if needed)
                        await websocket.pong()  # Respond with pong
                    else:
                        message_data = json.loads(message)
                        stream = message_data["stream"]
                        data = message_data["data"]

                        if stream == "btcusdt@aggTrade":
                            process_aggtrade(data, avro_agg_trade)
                        elif stream == "btcusdt@trade":
                            process_trade(data, avro_trade)
                        elif stream == "btcusdt@kline_1m":
                            process_kline(data, avro_kline)
        except websockets.exceptions.ConnectionClosed as e:
            print(f"Connection closed with error: {e}, reconnecting...")
            await asyncio.sleep(10)


def create_avro_producer_aggtrade(
    kafka_host, kafka_port, schema_reg_host, schema_reg_port
):
    value_schema_str = """{
      "type": "record",
      "name": "AggregateTrade",
      "namespace": "com.example.binance",
      "fields": [
        {"name": "eventType", "type": "string"},
        {"name": "eventTime", "type": "long"},
        {"name": "symbol", "type": "string"},
        {"name": "aggTradeId", "type": "long"},
        {"name": "price", "type": "string"},
        {"name": "quantity", "type": "string"},
        {"name": "firstTradeId", "type": "long"},
        {"name": "lastTradeId", "type": "long"},
        {"name": "tradeTime", "type": "long"},
        {"name": "isBuyerMaker", "type": "boolean"},
        {"name": "ignore", "type": "boolean"}
      ]
    }"""
    value_schema = avro.loads(value_schema_str)

    avro_producer = AvroProducer(
        {
            "bootstrap.servers": f"{kafka_host}:{kafka_port}",
            "schema.registry.url": f"http://{schema_reg_host}:{schema_reg_port}",
        },
        default_value_schema=value_schema,
    )

    return avro_producer


def create_avro_producer_trade(
    kafka_host, kafka_port, schema_reg_host, schema_reg_port
):
    value_schema_str = """{
      "type": "record",
      "name": "Trade",
      "namespace": "com.example.binance",
      "fields": [
        {"name": "eventType", "type": "string"},
        {"name": "eventTime", "type": "long"},
        {"name": "symbol", "type": "string"},
        {"name": "tradeId", "type": "long"},
        {"name": "price", "type": "string"},
        {"name": "quantity", "type": "string"},
        {"name": "buyerOrderId", "type": "long"},
        {"name": "sellerOrderId", "type": "long"},
        {"name": "tradeTime", "type": "long"},
        {"name": "isBuyerMaker", "type": "boolean"},
        {"name": "ignore", "type": "boolean"}
      ]
    }"""
    value_schema = avro.loads(value_schema_str)

    avro_producer = AvroProducer(
        {
            "bootstrap.servers": f"{kafka_host}:{kafka_port}",
            "schema.registry.url": f"http://{schema_reg_host}:{schema_reg_port}",
        },
        default_value_schema=value_schema,
    )

    return avro_producer


def create_avro_producer_kline(
    kafka_host, kafka_port, schema_reg_host, schema_reg_port
):
    value_schema_str = """{
        "type": "record",
        "name": "KlineEvent",
        "namespace": "com.example.binance",
        "fields": [
            {"name": "eventType", "type": "string"},
            {"name": "eventTime", "type": "long"},
            {"name": "symbol", "type": "string"},
            {"name": "startTime", "type": "long"},
            {"name": "closeTime", "type": "long"},
            {"name": "interval", "type": "string"},
            {"name": "firstTradeId", "type": "int"},
            {"name": "lastTradeId", "type": "int"},
            {"name": "openPrice", "type": "string"},
            {"name": "closePrice", "type": "string"},
            {"name": "highPrice", "type": "string"},
            {"name": "lowPrice", "type": "string"},
            {"name": "baseAssetVolume", "type": "string"},
            {"name": "numberOfTrades", "type": "int"},
            {"name": "isKlineClosed", "type": "boolean"},
            {"name": "quoteAssetVolume", "type": "string"},
            {"name": "takerBuyBaseAssetVolume", "type": "string"},
            {"name": "takerBuyQuoteAssetVolume", "type": "string"},
            {"name": "ignore", "type": "string"}
            
        ]
        }"""
    value_schema = avro.loads(value_schema_str)

    avro_producer = AvroProducer(
        {
            "bootstrap.servers": f"{kafka_host}:{kafka_port}",
            "schema.registry.url": f"http://{schema_reg_host}:{schema_reg_port}",
        },
        default_value_schema=value_schema,
    )

    return avro_producer


def process_aggtrade(data, avro_producer_agg_trade):
    # Prepare the message according to the schema
    message = {
        "eventType": data["e"],
        "eventTime": data["E"],
        "symbol": data["s"],
        "aggTradeId": data["a"],
        "price": data["p"],
        "quantity": data["q"],
        "firstTradeId": data["f"],
        "lastTradeId": data["l"],
        "tradeTime": data["T"],
        "isBuyerMaker": data["m"],
        "ignore": data["M"],
    }

    # Produce the message to Kafka
    avro_producer_agg_trade.produce(topic="btcaggtrade", value=message)
    avro_producer_agg_trade.flush()


def process_trade(data, avro_producer_trade):
    # Prepare the message according to the schema
    message = {
        "eventType": data["e"],
        "eventTime": data["E"],
        "symbol": data["s"],
        "tradeId": data["t"],
        "price": data["p"],
        "quantity": data["q"],
        "buyerOrderId": data["b"],
        "sellerOrderId": data["a"],
        "tradeTime": data["T"],
        "isBuyerMaker": data["m"],
        "ignore": data["M"],
    }

    # Produce the message to Kafka
    avro_producer_trade.produce(topic="btctrade", value=message)
    avro_producer_trade.flush()


def process_kline(data, avro_producer_kline):
    # Prepare the message according to the schema
    kline_data = data["k"]

    # Assemble the message according to the Avro schema
    message = {
        "eventType": data["e"],
        "eventTime": data["E"],
        "symbol": data["s"],
        "startTime": kline_data["t"],
        "closeTime": kline_data["T"],
        "interval": kline_data["i"],
        "firstTradeId": kline_data["f"],
        "lastTradeId": kline_data["L"],
        "openPrice": kline_data["o"],
        "closePrice": kline_data["c"],
        "highPrice": kline_data["h"],
        "lowPrice": kline_data["l"],
        "baseAssetVolume": kline_data["v"],
        "numberOfTrades": kline_data["n"],
        "isKlineClosed": kline_data["x"],
        "quoteAssetVolume": kline_data["q"],
        "takerBuyBaseAssetVolume": kline_data["V"],
        "takerBuyQuoteAssetVolume": kline_data["Q"],
        "ignore": kline_data["B"],
    }
    # Produce the message to Kafka
    avro_producer_kline.produce(topic="btcklineonemin", value=message)
    avro_producer_kline.flush()


async def main(avro_agg_trade, avro_trade, avro_kline):
    await binance_socket(avro_agg_trade, avro_trade, avro_kline)


if __name__ == "__main__":
    load_dotenv()
    schema_reg_host = os.getenv("SCHEMA_REGISTRY_HOST_NAME")
    schema_reg_port = os.getenv("LOCAL_SCHMEA_REGISTRY_PORT")
    kafka_host = os.getenv("KAFKA_HOST_NAME")
    kafka_port = os.getenv("LOCAL_KAFKA_PORT1")
    avro_agg_trade = create_avro_producer_aggtrade(
        kafka_host, kafka_port, schema_reg_host, schema_reg_port
    )
    avro_trade = create_avro_producer_trade(
        kafka_host, kafka_port, schema_reg_host, schema_reg_port
    )
    avro_kline = create_avro_producer_kline(
        kafka_host, kafka_port, schema_reg_host, schema_reg_port
    )
    asyncio.run(main(avro_agg_trade, avro_trade, avro_kline))
