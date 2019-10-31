# fixme
class SqlQueries:
    repository_table_select = ("""
        SELECT
            sp."Repository ID" AS repository_id,
            sp."Repository Stars Count" AS stars,
            sp."Repository Forks Count" AS forks,
            sp."Repository Watchers Count" AS watchers,
            sp."Repository Contributors Count" AS contributors,
            sv.ID AS version_id,
            sv."Project ID"AS project_id,
            sp."Repository Created Timestamp" AS create_time,
            sd.ID AS dependency_id,
            sp."Repository Size" AS size,
            ss.repo AS repo
            FROM staging_projects sp
            JOIN staging_versions sv
            ON sp.ID = sv."Project ID"
            JOIN staging_dependencies sd
            ON sp.ID = sd."Project ID"
            JOIN staging_stars ss
            ON sp."Repository Name with Owner" = ss.repo
            WHERE sp."Repository Host Type" = "GitHub"
    """)

    version_table_select = ("""
        SELECT
            sv.ID AS version_id,
            sv.Number AS number,
            sv."Published Timestamp" AS publish_time
        FROM staging_versions sv
        JOIN staging_projects sp
        ON sv."Project ID" = sp.ID
        WHERE sp."Repository Host Type" = "GitHub"
    """)

    project_table_select = ("""
        SELECT
            ID AS project_id,
            Platform AS platform,
            Name AS name,
            "Repository Host Type" AS host,
            Language AS language,
            Licenses AS license,
            Status AS status
        FROM staging_projects
        WHERE "Repository Host Type" = "GitHub"
    """)

    dependency_table_select = ("""
        SELECT
            ID AS dependency_id,
            "Dependency Name" AS dependency_name,
            "Dependency Platform" AS dependency_platform,
            "Dependency Kind" AS dependency_kind
        FROM staging_dependencies
    """)

    star_table_select = ("""
        SELECT
            repo,
            starred_at,
            login,
            html_url,
            type,
            site_admin
        FROM staging_stars
    """)

    time_table_select = ("""
        SELECT
            "Repository Created Timestamp" AS create_time,
            CONVERT(timestamp, create_time) AS tts,
            EXTRACT(day from tts),
            EXTRACT(month from tts),
            EXTRACT(year from tts),
            EXTRACT(dayofweek from tts)
        FROM staging_projects
    """)

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