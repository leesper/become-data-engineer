# Purpose

Sparkify is a startup who recently pushed out a brand-new online music streaming app。The app collected data about songs and user activity and store them in the format of JSON, in different directoies.

The analytics team is particularly interested in the data and wants to better understand  what songs the users are listening to, aiming at providing more valued-added services. As data engineers, we must design a suitable database schema and ETL pipeline. By extracting, transforming and loading from JSON files into relational models. We provide conveniences for the team to do analysis about user behaviors.

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

* README.md: specifications about the project(this file)
* create_tables.py: functions to drop and create tables from scratch
* data: a directory contains log and song data
* etl.ipynb: jupyter notebook about the ETL operations
* etl.py: an ETL script written based on etl.ipynb
* sql_queries.py: All SQL statements are written here
* test.ipynb: jupyter notebook for all the test utilities

## Step 1: Setting up environment

First installing PostgreSQL on your computer, under MacOS:

```brew install postgresql```

Start it immediately and configure it to start every time your computer starts up:

```pg_ctl -D /usr/local/var/postgres start && brew services start postgresql```

Check PostgreSQL's verion:

```postgres -V```

Use `psql`utility to add user `student`:

```sql
CREATE ROLE student WITH LOGIN PASSWORD 'student'
```

Grant the user `student` a right to create database:

```sql
ALTER ROLE student CREATEDB
```

Use psql as user `student`:

```sql
psql postgres -U student
```

Create database `studentdb`:

```sql
CREATE DATABASE studentdb
```

You can refer this [document](https://www.codementor.io/engineerapart/getting-started-with-postgresql-on-mac-osx-are8jcopb) for more detail.

## Step 2: Dropping and creating tables

Dropping and creating tables from scratch:

```shell
python create_tables.py
```

## Step 3: Performing ETLs

Run all the ETL operations:

```shell
python etl.py
```

All the data will be stored in the fact and dimension tables above.

# Example Queries

Do users like to pay for the music or just listen for free?

```sql
select level, count(*) from songplays group by level;
```

```
 level | count
-------+-------
 free  |  1229
 paid  |  5591
```

More people are likely to pay for the music, so which gender is more likely to pay?

```sql
select gender, songplays.level, count(*) from songplays join users on songplays.user_id = users.user_id group by gender, songplays.level;
```

```
 gender | level | count
--------+-------+-------
 M      | free  |   636
 F      | paid  |  4294
 F      | free  |   593
 M      | paid  |  1297
```

Both of the gender are willing to pay, females are more generous.