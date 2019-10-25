# fixme
class SqlQueries:
    repository_table_select = ("""
        SELECT
            "Repository ID" AS repository_id,
            "Repository Stars Count" AS stars,
            "Repository Forks Count" AS forks,
            AS watchers,
            AS contributors,
            AS version_id,
            AS project_id,
            AS create_time,
            AS dependency_id,
            AS star_id,
            AS size,
            AS repo,
    """)
    version_table_select = ("""""")
    project_table_select = ("""""")
    dependency_table_select = ("""""")
    star_table_select = ("""""")
    time_table_select = ("""""")
    songplay_table_insert = ("""
        SELECT
                md5(events.sessionid || events.start_time) songplay_id,
                events.start_time, 
                events.userid, 
                events.level, 
                songs.song_id, 
                songs.artist_id, 
                events.sessionid, 
                events.location, 
                events.useragent
                FROM (SELECT TIMESTAMP 'epoch' + ts/1000 * interval '1 second' AS start_time, *
            FROM staging_events
            WHERE page='NextSong') events
            LEFT JOIN staging_songs songs
            ON events.song = songs.title
                AND events.artist = songs.artist_name
                AND events.length = songs.duration
    """)

    user_table_insert = ("""
        SELECT distinct userid, firstname, lastname, gender, level
        FROM staging_events
        WHERE page='NextSong'
    """)

    song_table_insert = ("""
        SELECT distinct song_id, title, artist_id, year, duration
        FROM staging_songs
    """)

    artist_table_insert = ("""
        SELECT distinct artist_id, artist_name, artist_location, artist_latitude, artist_longitude
        FROM staging_songs
    """)

    time_table_insert = ("""
        SELECT start_time, extract(hour from start_time), extract(day from start_time), extract(week from start_time), 
               extract(month from start_time), extract(year from start_time), extract(dayofweek from start_time)
        FROM songplays
    """)