CREATE TABLE IF NOT EXISTS public.repository_fact (
    repository_id INT4 NOT NULL,
    stars INT4,
    forks INT4,
    watchers INT4,
    contributors INT4,
    size INT4,
    repo VARCHAR(256),
    version_id INT4,
    project_id INT4,
    create_time TIMESTAMP,
    dependency_id INT4,
    PRIMARY KEY(repository_id)
);

CREATE TABLE IF NOT EXISTS public.version_dim (
    version_id INT4 NOT NULL,
    number VARCHAR(256),
    publish_time TIMESTAMP,
    PRIMARY KEY(version_id)
);

CREATE TABLE IF NOT EXISTS public.project_dim (
    project_id INT4 NOT NULL,
    platform VARCHAR(256),
    name VARCHAR(256),
    host VARCHAR(256),
    language VARCHAR(256),
    license VARCHAR(256),
    status VARCHAR(256),
    PRIMARY KEY(project_id)
);

CREATE TABLE IF NOT EXISTS public.dependency_dim (
    dependency_id INT4 NOT NULL,
    dependency_name VARCHAR(256),
    dependency_platform VARCHAR(256),
    dependency_kind VARCHAR(256),
    PRIMARY KEY(dependency_id)
);

CREATE TABLE IF NOT EXISTS public.time_dim (
    create_time TIMESTAMP NOT NULL,
    "hour" INT4,
	"day" INT4,
	"month" VARCHAR(256),
	"year" INT4,
	weekday VARCHAR(256),
    PRIMARY KEY(create_time)
);

CREATE TABLE IF NOT EXISTS public.staging_dependencies (
    ID INT4,
    Platform VARCHAR(256),
    "Project Name" VARCHAR(256),
    "Project ID" INT4,
    "Version Number" VARCHAR(256),
    "Version ID" INT4,
    "Dependency Name" VARCHAR(256),
    "Dependency Platform" VARCHAR(256),
    "Dependency Kind" VARCHAR(256),
    "Optional Dependency" VARCHAR(256),
    "Dependency Requirements" VARCHAR(1024),
    "Dependency Project ID" INT4
);

CREATE TABLE IF NOT EXISTS public.staging_projects (
    ID INT4,
    Platform VARCHAR(256),
    Name VARCHAR(256),
    "Created Timestamp" TIMESTAMP,
    "Updated Timestamp" TIMESTAMP,
    Description VARCHAR(4096),
    Keywords VARCHAR(8192),
    "Homepage URL" VARCHAR(1024),
    Licenses VARCHAR(256),
    "Repository URL" VARCHAR(1024),
    "Versions Count" INT4,
    SourceRank INT4,
    "Latest Release Publish Timestamp" TIMESTAMP,
    "Latest Release Number" VARCHAR(256),
    "Package Manager ID" INT4,
    "Dependent Projects Count" INT4,
    Language VARCHAR(256),
    Status VARCHAR(256),
    "Last synced Timestamp" TIMESTAMP,
    "Dependent Repositories Count" INT4,
    "Repository ID" INT4,
    "Repository Host Type" VARCHAR(256),
    "Repository Name with Owner" VARCHAR(256),
    "Repository Description" VARCHAR(4096),
    "Repository Fork?" VARCHAR(16),
    "Repository Created Timestamp" TIMESTAMP,
    "Repository Updated Timestamp" TIMESTAMP,
    "Repository Last pushed Timestamp" TIMESTAMP,
    "Repository Homepage URL" VARCHAR(1024),
    "Repository Size" INT4,
    "Repository Stars Count" INT4,
    "Repository Language" VARCHAR(256),
    "Repository Issues enabled?" VARCHAR(16),
    "Repository Wiki enabled?" VARCHAR(16),
    "Repository Pages enabled?" VARCHAR(16),
    "Repository Forks Count" INT4,
    "Repository Mirror URL" VARCHAR(1024),
    "Repository Open Issues Count" INT4,
    "Repository Default branch" VARCHAR(256),
    "Repository Watchers Count" INT4,
    "Repository UUID" VARCHAR(256),
    "Repository Fork Source Name with Owner" VARCHAR(256),
    "Repository License" VARCHAR(256),
    "Repository Contributors Count" INT4,
    "Repository Readme filename" VARCHAR(256),
    "Repository Changelog filename" VARCHAR(256),
    "Repository Contributing guidelines filename" VARCHAR(256),
    "Repository License filename" VARCHAR(256),
    "Repository Code of Conduct filename" VARCHAR(256),
    "Repository Security Threat Model filename" VARCHAR(256),
    "Repository Security Audit filename" VARCHAR(256),
    "Repository Status" VARCHAR(256),
    "Repository Last Synced Timestamp" TIMESTAMP,
    "Repository SourceRank" INT4,
    "Repository Display Name" VARCHAR(256),
    "Repository SCM type" VARCHAR(256),
    "Repository Pull requests enabled?" VARCHAR(16),
    "Repository Logo URL" VARCHAR(1024),
    "Repository Keywords" VARCHAR(8192)
);

CREATE TABLE IF NOT EXISTS public.staging_versions (
    id INT4,
    platform VARCHAR(256),
    project_name VARCHAR(256),
    project_id INT4,
    "number" VARCHAR(256),
    published_timestamp TIMESTAMP,
    created_timestamp TIMESTAMP,
    updated_timestamp TIMESTAMP
);
