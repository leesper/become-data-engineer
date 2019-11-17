from airflow import DAG
from airflow.operators.dummy_operator import DummyOperator
from operators import StageToRedshiftOperator, LoadFactOperator, LoadDimensionOperator, QualityCheckOperator
from datetime import datetime, timedelta

default_args = {
    'owner': 'leesper',
    'start_date': datetime(2018, 11, 3),
    'depends_on_past': False,
    'retries': 3,
    'retry_delay': timedelta(minutes=3),
    'catchup': False,
    'email_on_retry': False,
}

dag = DAG('dend_dag',
          default_args=default_args,
          description='Load and transform repository data in Redshift with Airflow',
          schedule_interval='@hourly',
          max_active_runs=1
        )

start_operator = DummyOperator(task_id='Begin_execution',  dag=dag)

stage_versions_to_redshift = StageToRedshiftOperator(
    aws_conn_id='aws_credentials',
    redshift_conn_id='redshift',
    table='staging_versions',
    s3_addr='s3://dend-capstone-lkj/versions.json',
    task_id='Stage_versions',
    provide_context=True,
    dag=dag
)

stage_dependencies_to_redshift = StageToRedshiftOperator(
    aws_conn_id='aws_credentials',
    redshift_conn_id='redshift',
    table='staging_dependencies',
    s3_addr='s3://dend-capstone-lkj/dependencies-1.0.0-2017-06-15.csv',
    task_id='Stage_dependencies',
    dag=dag
)

stage_projects_to_redshift = StageToRedshiftOperator(
    aws_conn_id='aws_credentials',
    redshift_conn_id='redshift',
    table='staging_projects',
    s3_addr='s3://dend-capstone-lkj/projects_with_repository.csv',
    task_id='Stage_projects',
    dag=dag
)

load_repositories_fact_table = LoadFactOperator(
    redshift_conn_id='redshift',
    table='repository_fact',
    task_id='Load_repositories_fact_table',
    dag=dag
)

load_projects_dimension_table = LoadDimensionOperator(
    redshift_conn_id='redshift',
    table='project_dim',
    replace=True,
    task_id='Load_projects_dim_table',
    dag=dag
)

load_versions_dimension_table = LoadDimensionOperator(
    redshift_conn_id='redshift',
    table='version_dim',
    replace=True,
    task_id='Load_versions_dim_table',
    dag=dag
)

load_dependencies_dimension_table = LoadDimensionOperator(
    redshift_conn_id='redshift',
    table='dependency_dim',
    replace=True,
    task_id='Load_dependencies_dim_table',
    dag=dag
)

load_time_dimension_table = LoadDimensionOperator(
    redshift_conn_id='redshift',
    table='time_dim',
    replace=True,
    task_id='Load_time_dim_table',
    dag=dag
)

run_quality_checks = QualityCheckOperator(
    task_id='Run_data_quality_checks',
    dag=dag,
    redshift_conn_id='redshift',
    tables=[
        'staging_versions', 
        'staging_dependencies', 
        'staging_projects', 
        'repository_fact', 
        'version_dim', 
        'dependency_dim', 
        'project_dim', 
        'time_dim'
    ]
)

end_operator = DummyOperator(task_id='Stop_execution',  dag=dag)

start_operator \
    >> [
        stage_versions_to_redshift, 
        stage_dependencies_to_redshift, 
        stage_projects_to_redshift 
    ] >> load_repositories_fact_table \
    >> [
        load_projects_dimension_table, 
        load_versions_dimension_table, 
        load_dependencies_dimension_table, 
        load_time_dimension_table
    ] >> run_quality_checks >> end_operator
                