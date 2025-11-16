from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python import PythonOperator


dag = DAG(
    dag_id='depends_on_past',
    default_args={'start_date': datetime.now() - timedelta(days=1)},
    schedule='0 21 * * *',
    catchup=False,
)

# Define tasks
task_a = PythonOperator(
    task_id="task_a",
    python_callable=lambda: print("Executing Task A"),
    dag=dag,
)

task_b = PythonOperator(
    task_id="task_b",
    python_callable=lambda: print("Executing Task B"),
    depends_on_past=True,
    dag=dag,
)

# Connect tasks
task_a >> task_b