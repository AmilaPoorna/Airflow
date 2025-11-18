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

## exchange_rate_pipeline
Automates a simple ETL pipeline that runs daily at 22:00 between October 1, 2025, and December 31, 2025. It consists of three tasks.
1. Downloads exchange rate csv data and saves it to `/tmp`.
2. Runs a custom Python function clean_data from `clean_data.py` located in plugins folder which reads the csv, fills missing values with deafult values and saves the cleansed csv data to the data folder.
3. Sends a notification email upon success.

## git_repo_dag
Runs daily at 21:00. Uses `GithubOperator` to call GitHub’s `get_repo` method for `apache/airflow` repository and logs the repository tags.

## live_exchange_rates
Runs daily at 23:00. Downloads live exchange rate data and sends a notification email upon success. Here `web_api_key` and `support_email` are variables defined in Airflow UI.

## profit_uk
Runs daily at 21:00. Uses `profit_uk.sql` in the sqls folder within the DAGs folder to create or replace a table named `profit_uk` in the `L1_LANDING` schema of the `AIRFLOW` repository, based on the `sales_uk` table in the same schema and repository in Snowflake. Upon success, a notification email is sent. Here the sales date range (`process_interval`) is defined as a variable and Snowflake connection (`snowflake_conn`) is defined as a connection in the Airflow UI.

**Note:** You can start a 30-day free Snowflake trial, which includes $400 of free usage, if you don’t already have a Snowflake account.

## empdata_process
Runs daily at 23:00. Uses a sensor that waits for the file, poking every 10 seconds for up to 5 hours. When the employee_details.csv file exists in the data folder, it uploads the local file to the AIRFLOW.L1_LANDING.MY_LOCAL_STAGE stage in Snowflake. In the original tutorial, the DAG checked for the file in an S3 bucket on AWS.

## xrate_to_local
This DAG runs daily at 23:00. It automatically downloads the exchange rate data as a JSON file and stores it in the fetched_xrates folder, then uploads it to the uploaded_xrates folder inside the data folder.

## trigger_rules
Defines three upstream tasks (`task_a`, `task_b`, `task_c`) that simulate failures, a downstream `task_d` configured with `trigger_rule='all_failed'` which runs only when all upstream tasks fail, and a final `task_e` that runs after `task_d`.

## conditional_branching
Checks the file size of `source_file_extrat.dat` in the tmp folder inside the dags folder. If the file size is greater than approximately 10.74B, it branches to the parallel transformation/load path; otherwise, it branches to the serial transformation/load path.

## setup_teardown
Creates a resource (`create_cluster`), runs several query tasks, and then deletes the resource via a teardown (`delete_cluster`) linked to the setup task.

## LatestOnly
Ensures that a notification email is sent on success only for the latest DAG run, while a notification email is always sent on failure.

## DependsOnPast
One task (`task_b`) is configured with `depends_on_past=True`, causing it to wait for the previous DAG run’s corresponding task instance to succeed before running in the current schedule.