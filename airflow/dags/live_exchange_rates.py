# Import
from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.operators.email import EmailOperator
from datetime import datetime, timedelta

# Define the DAG
dag = DAG(
    dag_id='live_exchange_rates',
    default_args={'start_date': datetime.now() - timedelta(days=1)},
    schedule='0 23 * * *',
    catchup=False
)

# Define the Tasks
fetch_exchange_rates = BashOperator(
    task_id='fetch_exchange_rates',
    bash_command="curl '{{ var.value.get('web_api_key') }}' -o xrate.json",
    cwd='/tmp',
    dag=dag,
)

send_email_task = EmailOperator(
    task_id='send_email',
    to="{{ var.value.get('support_email') }}",
    subject='Live Exchange Rate Download - Successful.',
    html_content='Live Exchange Rate data has been successfully downloaded.',
    dag=dag,
)



# Define the Dependencies
fetch_exchange_rates >> send_email_task