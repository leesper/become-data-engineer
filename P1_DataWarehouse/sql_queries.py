import configparser


# CONFIG
config = configparser.ConfigParser()
config.read('dwh.cfg')
IAM_ROLE_ARN = config.get('IAM_ROLE', 'ARN')
LOG_DATA = config.get('S3', 'LOG_DATA')
LOG_JSON_PATH = config.get('S3', 'LOG_JSONPATH')
SONG_DATA = config.get('S3', 'SONG_DATA')

# DROP TABLES

staging_events_table_drop = "DROP TABLE IF EXISTS staging_events"
staging_songs_table_drop = "DROP TABLE IF EXISTS staging_songs"
songplay_table_drop = "DROP TABLE IF EXISTS songplays"
user_table_drop = "DROP TABLE IF EXISTS users"
song_table_drop = "DROP TABLE IF EXISTS songs"
artist_table_drop = "DROP TABLE IF EXISTS artists"
time_table_drop = "DROP TABLE IF EXISTS time"

# CREATE TABLES

staging_events_table_create= ("""
CREATE TABLE IF NOT EXISTS staging_events (
    artist VARCHAR(512),
    auth VARCHAR(64),
    firstName VARCHAR(32),
    gender VARCHAR(2),
    itemInSession INT,
    lastName VARCHAR(32),
    length NUMERIC,
    level VARCHAR(8),
    location VARCHAR(512),
    method VARCHAR(8),
    page VARCHAR(16),
    registration NUMERIC,
    sessionId INT,
    song VARCHAR(512),
    status INT,
    ts BIGINT,
    userAgent VARCHAR(256),
    userId INT);
""")

staging_songs_table_create = ("""
CREATE TABLE IF NOT EXISTS staging_songs (
    num_songs INT,
    artist_id VARCHAR(32),
    artist_latitude NUMERIC,
    artist_longitude NUMERIC,
    artist_location VARCHAR(512),
    artist_name VARCHAR(512),
    song_id VARCHAR(32),
    title VARCHAR(512),
    duration NUMERIC,
    year INT);
""")

songplay_table_create = ("""
CREATE TABLE IF NOT EXISTS songplays (
    songplay_id INT IDENTITY(0,1) PRIMARY KEY, 
    start_time TIMESTAMP NOT NULL sortkey, 
    user_id INT NOT NULL,
    level VARCHAR(8),
    song_id VARCHAR(32),
    artist_id VARCHAR(32) distkey,
    session_id INT,
    location VARCHAR(512),
    user_agent VARCHAR(256));
""")

user_table_create = ("""
CREATE TABLE IF NOT EXISTS users (
    user_id INT PRIMARY KEY,
    first_name VARCHAR(32),
    last_name VARCHAR(32),
    gender CHAR(1),
    level VARCHAR(8))
diststyle all;
""")

song_table_create = ("""
CREATE TABLE IF NOT EXISTS songs (
    song_id VARCHAR PRIMARY KEY sortkey,
    title VARCHAR(512),
    artist_id VARCHAR(32),
    year INT,
    duration NUMERIC);
""")

artist_table_create = ("""
CREATE TABLE IF NOT EXISTS artists (
    artist_id VARCHAR PRIMARY KEY sortkey distkey,
    name VARCHAR(512),
    location VARCHAR(512),
    latitude NUMERIC,
    longitude NUMERIC);
""")

time_table_create = ("""
CREATE TABLE IF NOT EXISTS time (
    start_time TIMESTAMP PRIMARY KEY sortkey,
    hour INT,
    day INT,
    week INT,
    month INT,
    year INT,
    weekday INT);
""")

# STAGING TABLES

staging_events_copy = ("""
COPY staging_events FROM '{}'
CREDENTIALS 'aws_iam_role={}'
REGION 'us-west-2'
JSON '{}';
""").format(LOG_DATA, IAM_ROLE_ARN, LOG_JSON_PATH)

staging_songs_copy = ("""
COPY staging_songs FROM '{}'
CREDENTIALS 'aws_iam_role={}'
REGION 'us-west-2'
JSON 'auto';
""").format(SONG_DATA, IAM_ROLE_ARN)

# FINAL TABLES

songplay_table_insert = ("""
INSERT INTO songplays (
    start_time, 
    user_id, 
    level, 
    song_id, 
    artist_id, 
    session_id, 
    location, 
    user_agent)
    SELECT TIMESTAMP 'epoch' + ts/1000 * interval '1 second' AS start_time, 
    userId, 
    level, 
    song_id, 
    artist_id, 
    sessionId, 
    location, 
    userAgent 
    FROM staging_events se
    JOIN staging_songs ss
    ON se.song = ss.title 
    AND se.length = ss.duration 
    AND se.artist = ss.artist_name
    AND se.page = 'NextSong';
""")

user_table_insert = ("""
INSERT INTO users (
    user_id,
    first_name,
    last_name,
    gender,
    level)
    SELECT DISTINCT userId, 
    firstName, 
    lastName, 
    gender, 
    level 
    FROM staging_events
    WHERE page = 'NextSong';
""")

song_table_insert = ("""
INSERT INTO songs (
    song_id,
    title,
    artist_id,
    year,
    duration)
    SELECT DISTINCT song_id, 
    title, 
    artist_id, 
    year, 
    duration 
    FROM staging_events se
    JOIN staging_songs ss
    ON se.song = ss.title
    AND se.artist = ss.artist_name
    AND se.page = 'NextSong';
""")

artist_table_insert = ("""
INSERT INTO artists (
    artist_id,
    name,
    location,
    latitude,
    longitude)
    SELECT DISTINCT artist_id, 
    artist_name, 
    artist_location, 
    artist_latitude, 
    artist_longitude
    FROM staging_songs;
""")

time_table_insert = ("""
INSERT INTO time (
    start_time,
    hour,
    day,
    week,
    month,
    year,
    weekday)
    SELECT DISTINCT TIMESTAMP 'epoch' + ts/1000 * interval '1 second' AS start_time, 
    EXTRACT(HOUR FROM start_time),
    EXTRACT(DAY FROM start_time),
    EXTRACT(WEEK FROM start_time),
    EXTRACT(MONTH FROM start_time),
    EXTRACT(YEAR FROM start_time),
    EXTRACT(DOW FROM start_time)
    FROM staging_events
    WHERE page = 'NextSong';
""")

# QUERY LISTS

create_table_queries = [staging_events_table_create, staging_songs_table_create, songplay_table_create, user_table_create, song_table_create, artist_table_create, time_table_create]
drop_table_queries = [staging_events_table_drop, staging_songs_table_drop, songplay_table_drop, user_table_drop, song_table_drop, artist_table_drop, time_table_drop]
copy_table_queries = [staging_events_copy, staging_songs_copy]
insert_table_queries = [songplay_table_insert, user_table_insert, song_table_insert, artist_table_insert, time_table_insert]
