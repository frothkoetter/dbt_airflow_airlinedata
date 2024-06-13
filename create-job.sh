# Create a resource
./cde resource create --name dags 
./cde resource upload --name dags --local-path dbt_airlinedata.py 
#./cde resource create --name projects 
#./cde resource upload-archive --name projects --local-path dbt_airlinedata.zip

# Create Job of “airflow” type and reference the DAG
./cde job delete --name dbt_airlinedata 
./cde job create --dag-file "dbt_airlinedata.py" --mount-1-resource dags --mount-2-resource venvs --mount-3-resource projects --airflow-file-mount-1-resource dags --airflow-file-mount-2-resource venvs --airflow-file-mount-3-resource projects --name dbt_airlinedata --type airflow

#Trigger Airflow job to run
#./cde job run --name dbt_airlinedata
