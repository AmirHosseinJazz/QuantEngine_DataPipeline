import asyncio
import websockets


async def binance_socket():
    uri = "wss://stream.binance.com:9443/stream?streams=btcusdt@aggTrade"

    async with websockets.connect(
        uri, ping_interval=180, ping_timeout=600
    ) as websocket:
        print("Opened connection")

        async for message in websocket:
            print("Received message:")
            print(message)


async def main():
    await binance_socket()


if __name__ == "__main__":
    asyncio.run(main())
