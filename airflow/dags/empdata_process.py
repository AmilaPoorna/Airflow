import os
from airflow import DAG
from datetime import datetime, timedelta
from airflow.sensors.python import PythonSensor
from airflow.operators.python import PythonOperator
from airflow.providers.snowflake.hooks.snowflake import SnowflakeHook
from airflow.providers.snowflake.transfers.copy_into_snowflake import CopyFromExternalStageToSnowflakeOperator

LOCAL_FILE_PATH = "/opt/airflow/data/employee_details.csv"

dag = DAG(
    dag_id='local_to_snowflake_dag', 
    default_args={'start_date': datetime.now() - timedelta(days=1)},
    schedule='0 23 * * *',
    catchup=False
)

def check_local_file():
    return os.path.exists(LOCAL_FILE_PATH)

wait_file = PythonSensor(
    task_id='wait_for_local_file',
    python_callable=check_local_file,
    poke_interval=10,
    timeout= 60 * 60 * 5,
    soft_fail=True,
    mode='reschedule',
    dag=dag
)

def upload_local_file():
    hook = SnowflakeHook(snowflake_conn_id="snowflake_conn")
    hook.run(
        f"PUT file://{LOCAL_FILE_PATH} @AIRFLOW.L1_LANDING.MY_LOCAL_STAGE AUTO_COMPRESS=TRUE",
        autocommit=True
    )

upload_file = PythonOperator(
    task_id="upload_local_file_to_stage",
    python_callable=upload_local_file,
    dag=dag
)

# Load the file from local to Snowflake
load_table = CopyFromExternalStageToSnowflakeOperator(
    task_id="load_local_file_to_table",
    snowflake_conn_id="snowflake_conn",
    files=["employee_details.csv.gz"],
    table="AIRFLOW.L1_LANDING.employee_details", 
    stage='AIRFLOW.L1_LANDING.MY_LOCAL_STAGE',
    file_format="(type = 'CSV',field_delimiter = ',', skip_header = 1)",
    dag=dag
)

# Set the dependencies
wait_file >> upload_file >> load_table