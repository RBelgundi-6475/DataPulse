# DataPulse
This is an end-to-end real time data pipeline with Kafka, Docker, Streamlit and Microsoft SQL Server.

This project demonstrates how to stream Change Data Capture (CDC) data into a real-time dashboard using Streamlit. With Docker Compose, the setup includes a SQL Server instance for CDC, a Kafka pipeline for data streaming, and a Streamlit dashboard to visualize the data.

The project is ideal for data engineers and developers interested in working with real-time data pipelines, CDC, and interactive dashboards.

## Key Features

- **Change Data Capture (CDC)**: Captures changes in a SQL Server database using Debezium Connector and streams them to a Kafka topic.
- **Kafka Streaming**: Streams data in real-time using Kafka.
- **Streamlit Dashboard**: Visualizes the CDC data in an interactive and user-friendly dashboard.
- **Docker Compose**: Simplifies the setup by orchestrating all services in a single file.

## Prerequisites

Before you begin, ensure that you have the following tools installed on your local machine:

- [Docker](https://www.docker.com/get-started)
- [Docker Compose](https://docs.docker.com/compose/install/)
- [Python 3.x](https://www.python.org/downloads/) (for running Streamlit)

## Project Structure

```plaintext
.
├── docker-compose.yml      # Docker Compose file for orchestrating services
├── .env                    # Environment variables for configuration
├── streamlit_dashboard.py  # Streamlit app for data visualization
└── requirements.txt        # Python dependencies for Streamlit

