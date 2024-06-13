from airflow import DAG
from airflow.decorators import dag, task
from airflow.operators.bash import BashOperator
from datetime import datetime

default_args = {
    'owner': 'cloud_era',
    'depends_on_past': False,
    'start_date':  datetime(2022, 8, 22, 12, 30),
}

dag = DAG(
    'dbt_airlinedata',
    default_args=default_args,
    catchup=False,
    is_paused_upon_creation=False,
)

dbt_version = BashOperator(
        task_id="dbt_version",
        bash_command="cp /app/mount/venvs/venv/ /home/airflow/venv -r && source /home/airflow/venv/bin/activate && dbt --version",
        env={"PATH_TO_DBT_VENV": "/app/mount/venvs/venv/"},
	dag=dag,
	trigger_rule="dummy"
	)

dbt_debug = BashOperator(
        task_id="dbt_debug",
        bash_command="cp /app/mount/venvs/venv/ /home/airflow/venv -r && source /home/airflow/venv/bin/activate && dbt debug",
        env={"PATH_TO_DBT_VENV": "/app/mount/venvs/venv/"},
	dag=dag,
	trigger_rule="dummy"
	)

dbt_test = BashOperator(
        task_id="dbt_test",
        bash_command="cp /app/mount/venvs/venv/ /home/airflow/venv -r && source /home/airflow/venv/bin/activate && cp /app/mount/projects/dbt_airlinedata/ /home/airflow/dbt_airlinedata -r && cd /home/airflow/dbt_airlinedata && dbt test",
        env={"PATH_TO_DBT_VENV": "/app/mount/venvs/venv/"},
	dag=dag,
	trigger_rule="dummy"
	)

dbt_run = BashOperator(
        task_id="dbt_run",
        bash_command="cp /app/mount/venvs/venv/ /home/airflow/venv -r && source /home/airflow/venv/bin/activate && cp /app/mount/projects/dbt_airlinedata/ /home/airflow/dbt_airlinedata -r && cd /home/airflow/dbt_airlinedata && dbt test",
        env={"PATH_TO_DBT_VENV": "/app/mount/venvs/venv/"},
	dag=dag,
	trigger_rule="dummy"
	)

dbt_version >> dbt_debug >> dbt_test >> dbt_run
