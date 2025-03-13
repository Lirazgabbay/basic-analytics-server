# Basic Analytics Server

## Overview
This project is a basic analytics/log server built using **FastAPI** and hosted on **Azure**. The server is designed to receive and store event logs in an SQLite database and provide reports based on user activity within a given time frame.

## Features
- **Event Processing**: Accepts events via HTTP POST requests and stores them in an SQLite database.
- **Event Reporting**: Retrieves events for a specific user that occurred within a given timeframe.
- **Unit Testing**: Ensures proper data insertion and retrieval.
- **Dockerized Deployment**: The application is containerized and deployed on Azure.
- **Automated Load Testing**: A Python client generates random events in parallel using `joblib`.
- **CI/CD with GitHub Actions**: Automates the build and deployment process to Azure.

---
## Setup & Installation
### Prerequisites
- **Python 3.8+**
- **FastAPI & Dependencies**
- **SQLite**
- **Docker**
- **Azure Account**

## CI/CD with GitHub Actions
Triggers on Git Push: Automates Docker build and deployment to Azure.


