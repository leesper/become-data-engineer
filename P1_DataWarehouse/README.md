# Purpose

Sparkify is a startup who recently pushed out a brand-new online music streaming app。The app collected data about songs and user activity and store them in the format of JSON, in different directoies.

The analytics team is particularly interested in the data and wants to better understand what songs the users are listening to, aiming at providing more valued-added services. As data engineers, we must design a suitable database schema and ETL pipeline. By extracting, transforming and loading from JSON files into relational models. We provide conveniences for the team to do analysis about user behaviors.

# Design

The raw data are divided into two categories: log data and music data. **Log data** is about user activities, it contains information about the users, such as name, gender and location; about the songs, such as artist, song name and length; and about the session, such as session ID, method and user agent.**Music data** is metadata about songs, such as the location, latitude, longitude, title, year and duration about the songs.

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
5. Longitude

### Time Dimension

1. start_time
2. hour
3. day
4. week
5. month
6. year
7. Weekday(0-monday, 6-sunday)

# Howto

This project contains following files:

- README.md: specifications about the project(this file)
- create_tables.py: functions to drop and create tables from scratch
- etl.py: an ETL script
- sql_queries.py: All SQL statements are written here

## Step 1: Creating Tables

Run this command to create table:

```shell
python create_tables.py
```

## Step 2: Performing ETLs

Run the ETL process:

```shell
python etl.py
```

# Example Queries

Do users like to pay for the music or listen for free?

```sql
SELECT level, COUNT(*) FROM songplays GROUP BY level;
```

```
level | count
-------+-------
 free  |  1206
 paid  |  5507
```

More people are likely to pay for the music, so which gender is more likely to pay?

```sql
SELECT gender, songplays.level, COUNT(*) FROM songplays JOIN users ON songplays.user_id = users.user_id GROUP BY gender, songplays.level;
```

```
gender | level | count
--------+-------+-------
 F      | free  |   585
 F      | paid  |  4225
 M      | free  |   621
 M      | paid  |  1282
```

Both of the gender are willing to pay, females are more generous. Do people listen to music in workday or weekend?

```sql
SELECT CASE WHEN weekday=0 OR weekday=6 THEN 'weekend' ELSE 'workday' END AS day_type, COUNT(*)
FROM songplays sp
JOIN time t 
ON sp.start_time=t.start_time
GROUP BY day_type
ORDER BY 2 DESC;
```

```
day_type | count
-------+-------
 workday  |  5702
 weekend  |  1011
```

So people listen to music in workday more often.