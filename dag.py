from datetime import timedelta, datetime
from airflow import DAG
from airflow.operators.python_operator import PythonOperator
import tasks
import configs

client, filename = configs.config()

default_args = {
    'owner': 'airflow',
    'start_date': datetime(2020, 6, 3),
    'depends_on_past': False,
    'email': ['airflow@example.com'],
    'retries': 1,
    'retry_delay': timedelta(minutes=2),
}
dag = DAG(dag_id='corona',
          default_args=default_args,
          description="Collecting  data",
          schedule_interval=timedelta(days=1),
          )

t1 = PythonOperator(task_id="fetch_data", python_callable=tasks.get_covidDdata, dag=dag)
t2 = PythonOperator(task_id="creating_dataset", python_callable=tasks.create_dataset, dag=dag)
t3 = PythonOperator(task_id="creating_newTable", python_callable=tasks.create_new_table, dag=dag)
t4 = PythonOperator(task_id="inserting_data", python_callable=tasks.insert_data, dag=dag)


t1 >> t2 >> t3 >> t4

