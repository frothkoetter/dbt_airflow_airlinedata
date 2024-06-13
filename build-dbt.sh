# Create a resource
./cde resource create --name dags 
./cde resource upload --name dags --local-path build_dbt.py 
./cde resource create --name requirements 
./cde resource upload --name requirements --local-path sample_requirements.txt
./cde resource create --name venvs 

# Create Job of “airflow” type and reference the DAG
./cde job delete --name build_venv
./cde job create --dag-file "build_dbt.py" --mount-1-resource dags --mount-2-resource requirements --airflow-file-mount-1-resource dags --airflow-file-mount-2-resource requirements --name build_venv --type airflow

#Trigger Airflow job to run
#./cde job run --name build_venv
