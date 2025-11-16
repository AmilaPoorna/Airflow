from airflow import DAG
from datetime import datetime, timedelta
from airflow.operators.email import EmailOperator
from airflow.providers.common.sql.operators.sql import SQLExecuteQueryOperator

# Define the DAG
dag = DAG(
    dag_id='load_profit_uk',
    default_args={'start_date': datetime.now() - timedelta(days=1)},
    schedule='0 21 * * *',
    catchup=False
)

# Define the Task
load_table = SQLExecuteQueryOperator(
    task_id='load_table',
#    sql='./sqls/profit_uk.sql',
    sql='select 1',
    conn_id='snowflake_conn',
    dag=dag
)

send_email = EmailOperator(
    task_id='send_email',
    to="{{ var.value.get('support_email') }}",
    subject='UK profit table load - Successful',
    html_content='UK Sales table to Profit table Load Completed',
    dag=dag,
)


# Define the Dependencies
load_table >> send_email