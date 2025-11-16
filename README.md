# Airflow

## What is Apache Airflow?

Apache Airflow is an open-source workflow orchestration platform designed to programmatically author, schedule, and monitor data pipelines. This repository contains various DAGs (Directed Acyclic Graphs) that demonstrate different Airflow concepts and patterns that I have created by following the [Apache Airflow Complete Tutorial](https://www.youtube.com/playlist?list=PLc2EZr8W2QIAI0cS1nZGNxoLzppb7XbqM) YouTube playlist by **SleekData**. All demonstrations were performed using Apache Airflow on Windows Docker.

## General Instructions

1. **Install Docker on your system if it is not already installed.**

2. **Install Windows Subsystem for Linux using:**
   ```bash
   wsl --update
   ```

3. **Install VS Code on your system if it is not already installed, and from there install Python and Docker extensions.**

4. **Clone the repository using:**
   ```bash
   git clone https://github.com/AmilaPoorna/Airflow.git
   ```

5. **Build image using dockerfile and compose up using docker-compose.yml**

## welcome_dag
A simple DAG that runs daily at 23:00 which prints a welcome message, today's date and fetches a random quote using an API respectively.

## exchange_rate_pipeline.py
Automates a simple ETL pipeline that runs daily at 22:00 between October 1, 2025, and December 31, 2025. It consists of three tasks.
1. Downloads exchange rate csv data and saves it to `/tmp`.
2. Runs a custom Python function clean_data from `clean_data.py` located in plugins folder which reads the csv, fills missing values with deafult values and saves the cleansed csv data to the data folder.
3. Sends a notification email upon success.

## git_repo_dag.py
Runs daily at 21:00. Uses `GithubOperator` to call GitHub’s `get_repo` method for `apache/airflow` repository and logs the repository tags.

## live_exchange_rates.py
Runs daily at 23:00. Downloads live exchange rate data and sends a notification email upon success. Here `web_api_key` and `support_email` are variables defined in Airflow UI.

## profit_uk.py
