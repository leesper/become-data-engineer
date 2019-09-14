from datetime import datetime, timedelta
import os
from airflow import DAG
from airflow.operators.dummy_operator import DummyOperator
from airflow.operators import (StageToRedshiftOperator, LoadFactOperator,
                                LoadDimensionOperator, DataQualityOperator)
from helpers import SqlQueries

# AWS_KEY = os.environ.get('AWS_KEY')
# AWS_SECRET = os.environ.get('AWS_SECRET')

default_args = {
    'owner': 'udacity',
    'start_date': datetime(2019, 1, 12),
    'depends_on_past': False,
    'retries': 3,
    'retry_delay': timedelta(minutes=5),
    'catchup': False,
    'email_on_retry': False,
}

dag = DAG('udac_example_dag',
          default_args=default_args,
          description='Load and transform data in Redshift with Airflow',
          schedule_interval='@hourly'
        )

start_operator = DummyOperator(task_id='Begin_execution',  dag=dag)

stage_events_to_redshift = StageToRedshiftOperator(
    aws_conn_id='aws_credentials',
    redshift_conn_id='redshift',
    table='staging_events',
    s3_addr='s3://udacity-dend/log_data',
    task_id='Stage_events',
    provide_context=True,
    dag=dag
)

stage_songs_to_redshift = StageToRedshiftOperator(
    aws_conn_id='aws_credentials',
    redshift_conn_id='redshift',
    table='staging_songs',
    s3_addr='s3://udacity-dend/song_data',
    task_id='Stage_songs',
    dag=dag
)

load_songplays_table = LoadFactOperator(
    redshift_conn_id='redshift',
    table='songplays',
    task_id='Load_songplays_fact_table',
    dag=dag
)

load_user_dimension_table = LoadDimensionOperator(
    redshift_conn_id='redshift',
    table='users',
    replace=True,
    task_id='Load_user_dim_table',
    dag=dag
)

load_song_dimension_table = LoadDimensionOperator(
    redshift_conn_id='redshift',
    table='songs',
    replace=True,
    task_id='Load_song_dim_table',
    dag=dag
)

load_artist_dimension_table = LoadDimensionOperator(
    redshift_conn_id='redshift',
    table='artists',
    replace=True,
    task_id='Load_artist_dim_table',
    dag=dag
)

load_time_dimension_table = LoadDimensionOperator(
    redshift_conn_id='redshift',
    table='time',
    replace=True,
    task_id='Load_time_dim_table',
    dag=dag
)

run_quality_checks = DataQualityOperator(
    task_id='Run_data_quality_checks',
    dag=dag,
    redshift_conn_id='redshift',
    tables=['staging_events', 'staging_songs', 'users', 'songs', 'artists', 'time']
)

end_operator = DummyOperator(task_id='Stop_execution',  dag=dag)

start_operator \
    >> [stage_events_to_redshift, stage_songs_to_redshift] \
    >> load_songplays_table \
    >> [
        load_song_dimension_table, 
        load_user_dimension_table, 
        load_artist_dimension_table, 
        load_time_dimension_table
    ] >> run_quality_checks >> end_operator
