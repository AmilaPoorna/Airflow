from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.models import Variable
import subprocess
import shutil

TARGET_DIR = "/opt/airflow/data"

dag = DAG(
    dag_id='xrate_to_local',
    default_args={'start_date': datetime.now() - timedelta(days=1)},
    schedule='0 23 * * *',
    catchup=False
)

def fetch_xrate_fn(ti):
    xrate_filename = f'xrate_{datetime.now().strftime("%Y-%m-%d-%H-%M-%S")}.json'
    local_path = f'{TARGET_DIR}/fetched_xrates/{xrate_filename}'
    curl_command = ["curl", Variable.get('web_api_key'), "-o", local_path]
    subprocess.run(curl_command, check=True)
    ti.xcom_push(key='xrate_file', value=xrate_filename)

fetch_xrate = PythonOperator(
    task_id='fetch_xrate',
    python_callable=fetch_xrate_fn,
    dag=dag
)

def upload_xrate_fn(ti):
    filename = ti.xcom_pull(task_ids='fetch_xrate', key='xrate_file')
    src_path = f"{TARGET_DIR}/fetched_xrates/{filename}"
    dst_path = f"{TARGET_DIR}/uploaded_xrates/{filename}"
    shutil.copy(src_path, dst_path)

upload_xrate = PythonOperator(
    task_id='copy_to_local',
    python_callable=upload_xrate_fn,
    dag=dag
)

# Define Dependencies
fetch_xrate >> upload_xrate