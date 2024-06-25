from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from airflow.utils.dates import days_ago
from datetime import timedelta

def load_and_process_data():
    from scripts.data_processing import load_and_process_data
    df = load_and_process_data()
    df.show()

def analyze_categories():
    from scripts.category_analysis import analyze_categories
    from scripts.data_processing import load_and_process_data
    df = load_and_process_data()
    top_categories = analyze_categories(df)
    top_categories.show()

def send_notifications():
    from scripts.notification_sender import send_notifications
    from scripts.category_analysis import analyze_categories
    from scripts.data_processing import load_and_process_data
    df = load_and_process_data()
    top_categories = analyze_categories(df)
    send_notifications(top_categories)

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': days_ago(1),
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

dag = DAG(
    'data_pipeline_dag',
    default_args=default_args,
    description='A simple data pipeline DAG',
    schedule_interval=timedelta(days=1),
)

t1 = PythonOperator(
    task_id='load_and_process_data',
    python_callable=load_and_process_data,
    dag=dag,
)

t2 = PythonOperator(
    task_id='analyze_categories',
    python_callable=analyze_categories,
    dag=dag,
)

t3 = PythonOperator(
    task_id='send_notifications',
    python_callable=send_notifications,
    dag=dag,
)

t1 >> t2 >> t3
