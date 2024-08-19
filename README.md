# QuantEngine_DataPipeline

QuantEngine_DataPipeline is the data engineering component of the QuantEngine project, focused on the automated ingestion, cleaning, and storage of financial data, particularly Bitcoin (BTC). This repository manages the entire data pipeline, ensuring that high-quality, up-to-date data is available for financial modeling and analysis.

## Features

- **Data Ingestion:** Automatically retrieves BTC data on multiple timeframes (1m, 5m, 1h, 1d) and additional indicators (e.g., Fear and Greed Index).
- **Data Cleaning:** Processes raw data to remove inconsistencies and fill gaps, ensuring the integrity of the data used in analysis.
- **Data Storage:** Utilizes TimescaleDB for efficient time series data storage and querying.
- **Scheduling:** Uses Perfect-server to schedule data retrieval at specific intervals, ensuring that the data pipeline remains current.
- **Docker Compose:** Manages services such as PostgreSQL, pgAdmin, Redis, TimescaleDB, Kafka (experimental), and Perfect-server using a custom Docker Compose setup.

## Project Structure

QuantEngine_DataPipeline/
│
├── docker-compose.yml # Docker Compose file for managing services
└── README.md # Project documentation

## Getting Started

### Services

- Docker and Docker Compose
- PostgreSQL and TimescaleDB
- Perfect-Server
- TimeScaleDB
- Redis, RedisInsight
- Kafka, KafkaConnect,Zookeeper

<!-- ### Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/yourusername/QuantEngine_DataPipeline.git
   cd QuantEngine_DataPipeline
   ```

2. Set up environment variables:

   ```bash
   cp .env.example .env
   ```

3. Start the data pipeline services:

   ```bash
   docker-compose up -d
   ``` -->

Access services:
   - **pgAdmin:** `http://localhost:8888`
   - **Perfect-server:** `http://localhost:4200`

### Usage

- **Data Ingestion:** Scheduled tasks automatically retrieve and process data according to the configuration.
- **Data Monitoring:** Use pgAdmin to monitor the database and ensure data integrity.

### Future Enhancements

- **Enhanced Data Processing:** Additional data cleaning and transformation pipelines.
- **Real-time Data Streaming:** Re-enable Kafka for real-time data ingestion and processing.
- **Expanded Data Sources:** Incorporate additional cryptocurrency and financial data sources.

