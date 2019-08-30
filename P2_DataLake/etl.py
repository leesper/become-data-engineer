import configparser
from datetime import datetime
import os
from pyspark.sql import SparkSession
from pyspark.sql.functions import udf, col
from pyspark.sql.functions import year, month, dayofmonth, hour, weekofyear, date_format
from pyspark.sql.types import DoubleType


config = configparser.ConfigParser()

config.read('dl.cfg')
os.environ['AWS_ACCESS_KEY_ID']=config['AWS_ACCESS_KEY_ID']
os.environ['AWS_SECRET_ACCESS_KEY']=config['AWS_SECRET_ACCESS_KEY']


def create_spark_session():
    spark = SparkSession \
        .builder \
        .config("spark.jars.packages", "org.apache.hadoop:hadoop-aws:2.7.0") \
        .getOrCreate()
    return spark


def process_song_data(spark, input_data, output_data):
    # get filepath to song data file
    song_data = input_data + '/song-data/song_data/*/*/*/*.json'
    
    # read song data file
    df = spark.read.json(song_data)

    # extract columns to create songs table
    songs_table = df\
        .where("song_id is not null and song_id != ''")\
        .select('song_id', 'title', 'artist_id', 'year', 'duration')\
        .dropDuplicates(['song_id'])
    
    # write songs table to parquet files partitioned by year and artist
    songs_table.write.partitionBy('year', 'artist_id').parquet(output_data+'/songs')

    # extract columns to create artists table
    artists_table = df.where("artist_id != '' and artist_id is not null")\
        .select(
            col('artist_id'), 
            col('artist_name').alias('name'), 
            col('artist_location').alias('location'), 
            col('artist_latitude').alias('latitude'), 
            col('artist_longitude').alias('longitude'))
    
    # write artists table to parquet files
    artists_table.write.parquet(output_data+'/artists')


def process_log_data(spark, input_data, output_data):
    # get filepath to log data file
    log_data = input_data + '/log-data/*.json'

    # read log data file
    df = spark.read.json(log_data)
    
    # filter by actions for song plays
    df = df.where(df.page == 'NextSong')

    # extract columns for users table    
    users_table = df.select(
        col('userId').alias('user_id'), 
        col('firstName').alias('first_name'), 
        col('lastName').alias('last_name'), 
        'gender', 'level')
    
    # write users table to parquet files
    users_table.write.parquet(output_data+'/users')

    # create timestamp column from original timestamp column
    get_timestamp = udf(lambda ts: ts/1000.0, DoubleType())
    df = df.withColumn('timestamp', get_timestamp(df.ts).cast('timestamp'))
    
    # create datetime column from original timestamp column
    # get_datetime = udf()
    df = df.withColumn('start_time', date_format(df.timestamp, 'YYYY-MM-dd HH:mm:ss'))
    
    # extract columns to create time table
    time_table = df.select(
        'start_time', 
        hour(col('start_time')).alias('hour'), 
        dayofmonth(col('start_time')).alias('day'), 
        weekofyear(col('start_time')).alias('week'), 
        month(col('start_time')).alias('month'), 
        year(col('start_time')).alias('year'), 
        date_format(col('start_time'), 'u').cast('integer').alias('weekday'))
    
    # write time table to parquet files partitioned by year and month
    time_table.write.partitionBy('year', 'month').parquet(output_data+'/time')

    # read in song data to use for songplays table
    song_df = 

    # extract columns from joined song and log datasets to create songplays table 
    songplays_table = 

    # write songplays table to parquet files partitioned by year and month
    songplays_table


def main():
    spark = create_spark_session()
    # input_data = "s3a://udacity-dend/"
    input_data = "/vagrant"
    output_data = "/home/spark/output"
    
    process_song_data(spark, input_data, output_data)    
    process_log_data(spark, input_data, output_data)


if __name__ == "__main__":
    main()
