# Dockerized Stock Data Pipeline (Airflow + PostgreSQL)

This project sets up a **data pipeline** using **Apache Airflow** (inside Docker) to fetch stock market data from **Alpha Vantage** API and store it into a **PostgreSQL database**.

---

## Features
- Fetches stock data every hour (`IBM` symbol, 5min interval).
- Stores data in `stock_data` table (Postgres).
- Uses Airflow for scheduling.
- Uses Docker Compose for easy setup.
- Handles errors gracefully.

---

##  Project Structure
