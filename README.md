# Stock Pipeline

This project implements a Dockerized stock data pipeline using **Apache Airflow**. It automates fetching stock data, storing it in a database, and provides a web-based interface for scheduling, monitoring, and managing workflows.

---

## Prerequisites

Before running the project, make sure you have the following installed:

- **Docker Desktop**  
- **Docker Compose**  
- **PowerShell** (Windows) or **Terminal** (Linux/macOS)  

Ensure Docker Desktop is running, as all containers depend on it.

---

## Setup and Installation

### 1. Build Docker Images

The stock fetcher service requires building a custom Docker image:

```powershell
docker-compose build stock_fetcher
