from airflow import DAG
from airflow.operators.dummy_operator import DummyOperator
from airflow.operators import StageToRedshiftOperator, LoadFactOperator, LoadDimensionOperator, QualityCheckOperator
from datetime import datetime, timedelta

default_args = {
    'owner': 'leesper',
    'start_date': datetime(2018, 11, 3),
    'depends_on_past': False,
    'retries': 3,
    'retry_delay': timedelta(minutes=5),
    'catchup': False,
    'email_on_retry': False,
}

dag = DAG('capstone_dag',
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
    s3_addr='s3://dend-capstone-lkj/versions-1.0.0-2017-06-15.csv',
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
    s3_addr='s3://dend-capstone-lkj/projects_with_repository_fields-1.0.0-2017-06-15.csv',
    task_id='Stage_projects',
    dag=dag
)

stage_stars_to_redshift = StageToRedshiftOperator(
    aws_conn_id='aws_credentials',
    redshift_conn_id='redshift',
    table='staging_stars',
    s3_addr='s3://dend-capstone-lkj/star.json',
    task_id='Stage_stars',
    dag=dag
)

load_repositories_fact_table = LoadFactOperator(
    redshift_conn_id='redshift',
    table='repositories',
    task_id='Load_repositories_fact_table',
    dag=dag
)

load_projects_dimension_table = LoadDimensionOperator(
    redshift_conn_id='redshift',
    table='projects',
    replace=True,
    task_id='Load_projects_dim_table',
    dag=dag
)

load_versions_dimension_table = LoadDimensionOperator(
    redshift_conn_id='redshift',
    table='versions',
    replace=True,
    task_id='Load_versions_dim_table',
    dag=dag
)

load_dependencies_dimension_table = LoadDimensionOperator(
    redshift_conn_id='redshift',
    table='dependencies',
    replace=True,
    task_id='Load_dependencies_dim_table',
    dag=dag
)

load_stars_dimension_table = LoadDimensionOperator(
    redshift_conn_id='redshift',
    table='stars',
    replace=True,
    task_id='Load_stars_dim_table',
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
        'staging_stars',
        'repositories', 
        'versions', 
        'dependencies', 
        'projects', 
        'stars',
    ]
)

end_operator = DummyOperator(task_id='Stop_execution',  dag=dag)

start_operator \
    >> [
        stage_versions_to_redshift, 
        stage_dependencies_to_redshift, 
        stage_projects_to_redshift, 
        stage_stars_to_redshift
    ] >> load_repositories_fact_table \
    >> [
        load_projects_dimension_table, 
        load_versions_dimension_table, 
        load_dependencies_dimension_table, 
        load_stars_dimension_table,
    ] >> run_quality_checks >> end_operator
                