"""
This is an example dag for using the KubernetesPodOperator.
"""
import logging
import os

from airflow import DAG
from airflow.providers.cncf.kubernetes.operators.kubernetes_pod import \
    KubernetesPodOperator
from airflow.operators.dummy_operator import DummyOperator
from datetime import datetime, timedelta
try:
   from src.models.initial_model_functions import load_preprocess, fit_model
except:
   print("import failed1")

try:
   from .src.models.initial_model_functions import load_preprocess, fit_model
except:
   print("import failed2")

print(os.getcwd())

# log = logging.getLogger(__name__)


default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime.utcnow(),
    'email': ['airflow@example.com'],
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5)
}

dag = DAG(
    'kubernetes_sample', default_args=default_args,
    schedule_interval=timedelta(minutes=10), tags=['debug'])

start = DummyOperator(task_id='debug_task', dag=dag)

python_task = KubernetesPodOperator(namespace='default',
                                    image="python:3.6",
                                    cmds=["python", "-c"],
                                    arguments=["import time; print('sleeping for 1500sec'); time.sleep(1500)"],
                                    labels={"foo": "bar"},
                                    name="passing-python",
                                    task_id="passing-task-python",
                                    get_logs=True,
                                    dag=dag
                                    )

python_task.set_upstream(start)
