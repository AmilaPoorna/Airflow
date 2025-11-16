from airflow import DAG
from airflow.providers.standard.operators.python import PythonOperator
from datetime import datetime, timedelta
import requests

def print_welcome():
    print('Welcome to Airflow!')

def print_date():
    print(f"Today is {datetime.today().date()}")

def print_random_quote():
    response = requests.get('https://zenquotes.io/api/random', timeout=10)
    data = response.json()
    quote = data[0]['q']
    author = data[0]['a']
    print(f'Quote of the day: "{quote}" — {author}')

dag = DAG(
    dag_id='welcome_dag',
    start_date=datetime.now() - timedelta(days=1),
    schedule='0 23 * * *',
    catchup=False
)

print_welcome_task = PythonOperator(
    task_id='print_welcome',
    python_callable=print_welcome,
    dag=dag
)

print_date_task = PythonOperator(
    task_id='print_date',
    python_callable=print_date,
    dag=dag
)

print_random_quote = PythonOperator(
    task_id='print_random_quote',
    python_callable=print_random_quote,
    dag=dag
)

# Set the dependencies between the tasks
print_welcome_task >> print_date_task >> print_random_quote