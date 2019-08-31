# Purpose

Sparkify is a startup who recently pushed out a brand-new online music streaming app。The app collected data about songs and user activity and store them in the format of JSON, in different directoies.

The analytics team is particularly interested in the data and wants to better understand what songs the users are listening to, aiming at providing more valued-added services. As data engineers, we must design a suitable database schema and ETL pipeline. By extracting, transforming and loading from JSON files into relational models. We provide conveniences for the team to do analysis about user behaviors.

# Design

The raw data are divided into two categories: log data and music data. **Log data** is about user activities, it contains information about the users, such as name, gender and location; about the songs, such as artist, song name and length; and about the session, such as session ID, method and user agent.**Music data** is metadata about songs, such as the location, latitude, longitude, title, year and duration about the songs. We load the data from S3 into Spark, and then wrangling the data into one fact table and several dimension tables, and then write them back into S3 as parquet files partitioned if necessary.

## Fact

From this point, we can construct out data model as star schema. A fact table is built based on the log data containing these fields:

1. songplay_id
2. start_time
3. user_id
4. level
5. song_id
6. artist_id
7. session_id
8. location
9. user_agent

## Dimension

We set up four dimensions for the fact table: by user, by song, by artists and by time.

### User Dimension

1. user_id
2. first_name
3. last_name
4. gender
5. Level

### Song Dimension

1. song_id
2. title
3. artist_id
4. year
5. duration

### Artist Dimension

1. artist_id
2. name
3. location
4. latitude
5. longitude

### Time Dimension

1. start_time
2. hour
3. day
4. week
5. month
6. year
7. weekday

# Howto

This project contains following files:

- README.md: specifications about the project(this file)
- etl.py: an ETL script running on Spark

## Step 1: Get Access and Secret Key

Go to the AWS website, from "My Security Credentials" on the right top of the page, copy and paste the access key and secret access key into dl.cfg.

## Step 2: Create an S3 bucket for output

Go to the AWS S3 service, create a bucket called datalake-project.

## Step 3: Activate the ETL processing

Upload the etl.py to the cluster, then run `python etl.py` at the main node. Or you can create a jupyter notebook, copy and paste all content in etl.py and run it interatively in notebook.