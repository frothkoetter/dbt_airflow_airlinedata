from datetime import datetime
from airflow import DAG
from airflow.operators.bash_operator import BashOperator

VENV_RESOURCE_NAME = "venvs"
VENV_REQUIREMENTS_RESOURCE_NAME = "requirements"
VENV_REQUIREMENTS_FILENAME = "sample_requirements.txt"
CDE_API_HOST = "{{ conn.cde_runtime_api.host }}"
CDE_API_PORT = "{{ conn.cde_runtime_api.port }}"
CDE_API_SCHEMA = "{{ conn.cde_runtime_api.schema }}"

default_args = {
    'owner': 'cloud_era',
    'depends_on_past': False,
    'start_date': datetime(2024, 5, 22, 12, 30),
}

dag = DAG(
    'build_venv',
    default_args=default_args,
    catchup=False,
    is_paused_upon_creation=False,
)

build_venv = BashOperator(
    task_id='BUILD_VENV',
    bash_command=(
        'export PIP_USER=false && cd /home/airflow && python -m venv venv && source /home/airflow/venv/bin/activate && '
        f'python -m pip install -r /app/mount/{VENV_REQUIREMENTS_RESOURCE_NAME}/{VENV_REQUIREMENTS_FILENAME} && '
        'zip -r venv.zip venv && '
        f'response=$(curl -X PUT {CDE_API_SCHEMA}://{CDE_API_HOST}:{CDE_API_PORT}/api/v1/resources/{VENV_RESOURCE_NAME} -F \'file=@/home/airflow/venv.zip;type=application/zip\') &&'
        'if echo "$response" | grep -q \'"status":"error"\'; then '
        '  echo "Upload failed with response: $response"; '
        '  exit 1; '
        'fi'
    ), dag=dag)

build_venv
