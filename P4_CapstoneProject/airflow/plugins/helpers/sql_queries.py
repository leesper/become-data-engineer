class SqlQueries:
    repository_table_select = ("""
    INSERT INTO repository_fact
        (SELECT
            sp."repository id" AS repository_id,
            sp."repository stars count" AS stars,
            sp."repository forks count" AS forks,
            sp."repository watchers count" AS watchers,
            sp."repository contributors count" AS contributors,
            sp."repository size" AS size,
            sp."repository name with owner" AS repo,
            sv.id AS version_id,
            sv.project_id,
            sp."repository created timestamp" AS create_time,
            sd.id AS dependency_id
            FROM staging_projects sp
            JOIN staging_versions sv
            ON sp.id = sv.project_id
            JOIN staging_dependencies sd
            ON sp.id = sd."project id"
            WHERE sp."repository id" IS NOT NULL 
            AND TO_CHAR(sp."repository created timestamp", 'YYYY-MM-DD') = '{}')
    """)

    version_table_select = ("""
    INSERT INTO version_dim
        (SELECT
            sv.id AS version_id,
            sv.number,
            sv.published_timestamp
        FROM staging_versions sv
        JOIN staging_projects sp
        ON sv.project_id = sp.id
        WHERE TO_CHAR(sp."repository created timestamp", 'YYYY-MM-DD') = '{}')
    """)

    project_table_select = ("""
    INSERT INTO project_dim
        (SELECT
            id AS project_id,
            platform,
            name,
            "repository host type" AS host,
            language,
            licenses,
            status
        FROM staging_projects
        WHERE TO_CHAR("repository created timestamp", 'YYYY-MM-DD') = '{}')
    """)

    dependency_table_select = ("""
    INSERT into dependency_dim
        (SELECT
            id AS dependency_id,
            "Dependency Name" AS dependency_name,
            "Dependency Platform" AS dependency_platform,
            "Dependency Kind" AS dependency_kind
        FROM staging_dependencies)
    """)

    time_table_select = ("""
    INSERT INTO time_dim
        (SELECT
            "Repository Created Timestamp" AS create_time,
            EXTRACT(hour FROM create_time),
            EXTRACT(day FROM create_time),
            EXTRACT(month FROM create_time),
            EXTRACT(year FROM create_time),
            EXTRACT(dayofweek FROM create_time)
        FROM staging_projects
        WHERE TO_CHAR("repository created timestamp", 'YYYY-MM-DD') = '{}')
    """)