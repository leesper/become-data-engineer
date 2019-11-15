class SqlQueries:
    repository_table_select = ("""
        SELECT
            sp."repository id" AS repository_id,
            sp."repository stars count" AS stars,
            sp."repository forks count" AS forks,
            sp."repository watchers count" AS watchers,
            sp."repository contributors count" AS contributors,
            sv.id AS version_id,
            sv."project id"AS project_id,
            sp."repository created timestamp" AS create_time,
            sd.id AS dependency_id,
            sp."repository size" AS size,
            sp."repository name with owner" AS repo
            FROM staging_projects sp
            JOIN staging_versions sv
            ON sp.id = sv."project id"
            JOIN staging_dependencies sd
            ON sp.id = sd."project id"
    """)

    version_table_select = ("""
        SELECT
            sv.id AS version_id,
            sv.number AS number,
            sv."published timestamp" AS publish_time
        FROM staging_versions sv
        JOIN staging_projects sp
        ON sv."project id" = sp.id
    """)

    project_table_select = ("""
        SELECT
            id AS project_id,
            platform,
            name,
            "repository host type" AS host,
            language,
            licenses,
            status
        FROM staging_projects
    """)

    dependency_table_select = ("""
        SELECT
            id AS dependency_id,
            "Dependency Name" AS dependency_name,
            "Dependency Platform" AS dependency_platform,
            "Dependency Kind" AS dependency_kind
        FROM staging_dependencies
    """)

    time_table_select = ("""
        SELECT
            "Repository Created Timestamp" AS create_time,
            EXTRACT(hour FROM create_time),
            EXTRACT(day FROM create_time),
            EXTRACT(month FROM create_time),
            EXTRACT(year FROM create_time),
            EXTRACT(dayofweek FROM create_time)
        FROM staging_projects
    """)