import configparser

# CONFIG
dwh_cfg = configparser.ConfigParser()
dwh_cfg.read('dwh.cfg')

IAM_ROLE_ARN = dwh_cfg.get('IAM', 'IAM_ROLE_ARN')
S3_LOG_DATA  = dwh_cfg.get('S3', 'LOG_DATA')
S3_LOG_JSON  = dwh_cfg.get('S3', 'LOG_JSON')
S3_SONG_DATA = dwh_cfg.get('S3', 'SONG_DATA')

# DROP TABLES
staging_events_table_drop = "DROP TABLE IF EXISTS staging_events;"
staging_songs_table_drop = "DROP TABLE IF EXISTS staging_songs;"
songplay_table_drop = "DROP TABLE IF EXISTS songplays;"
user_table_drop = "DROP TABLE IF EXISTS users;"
song_table_drop = "DROP TABLE IF EXISTS songs;"
artist_table_drop = "DROP TABLE IF EXISTS artists;"
time_table_drop = "DROP TABLE IF EXISTS time;"

# CREATE TABLES

staging_events_table_create= ("""
CREATE TABLE IF NOT EXISTS staging_events (
    artist varchar,
    auth varchar,
    firstName varchar,
    gender varchar,
    itemInSession int,
    lastName varchar,
    length varchar,
    level varchar,
    location varchar,
    method varchar,
    page varchar,
    registration varchar,
    sessionId varchar,
    song varchar,
    status varchar,
    ts timestamp,
    userAgent varchar,
    userId int
);
""")

staging_songs_table_create = ("""
CREATE TABLE IF NOT EXISTS staging_songs (
    num_songs int,
    artist_id varchar,
    artist_latitude varchar,
    artist_longitude varchar,
    artist_location varchar,
    artist_name varchar,
    song_id varchar,
    title varchar,
    duration varchar,
    year smallint
);
""")

songplay_table_create = ("""
CREATE TABLE IF NOT EXISTS songplays (
    songplay_id bigint identity(0,1) PRIMARY KEY,
    start_time timestamp NOT NULL,
    user_id int NOT NULL,
    level varchar NOT NULL,
    song_id varchar,
    artist_id varchar,
    session_id varchar,
    location varchar,
    user_agent varchar
) DISTSTYLE KEY DISTKEY (start_time) SORTKEY (start_time);
""")

user_table_create = ("""
CREATE TABLE IF NOT EXISTS users (
    user_id int PRIMARY KEY,
    first_name varchar,
    last_name varchar,
    gender varchar,
    level varchar NOT NULL
) DISTSTYLE ALL SORTKEY (user_id);
""")

song_table_create = ("""
CREATE TABLE IF NOT EXISTS songs (
    song_id varchar PRIMARY KEY,
    title varchar,
    artist_id varchar,
    year smallint,
    duration_str varchar,
    duration_real real
) DISTSTYLE ALL SORTKEY (song_id);
""")

artist_table_create = ("""
CREATE TABLE IF NOT EXISTS artists (
    artist_id varchar PRIMARY KEY,
    name varchar,
    location varchar,
    latitude real,
    longitude real
) DISTSTYLE ALL SORTKEY (artist_id);
""")

time_table_create = ("""
CREATE TABLE IF NOT EXISTS time (
    start_time timestamp PRIMARY KEY,
    hour smallint NOT NULL,
    day smallint NOT NULL,
    week smallint NOT NULL,
    month smallint NOT NULL,
    year smallint NOT NULL,
    weekday varchar NOT NULL    
) DISTSTYLE KEY DISTKEY (start_time) SORTKEY (start_time);
""")

# STAGING TABLES

staging_events_copy = ("""
COPY staging_events FROM {s3_bucket}
    credentials 'aws_iam_role={role_arn}'
    region 'us-west-2'
    format as JSON {log_json}
    timeformat as 'epochmillisecs';
""").format(s3_bucket = S3_LOG_DATA, role_arn = IAM_ROLE_ARN, log_json = S3_LOG_JSON)

staging_songs_copy = ("""
COPY staging_songs FROM {s3_bucket}
    credentials 'aws_iam_role={role_arn}'
    region 'us-west-2' format as JSON 'auto';
""").format(s3_bucket = S3_SONG_DATA, role_arn = IAM_ROLE_ARN)

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
SELECT DISTINCT
    event.ts           as start_time, 
    event.userId       as user_id,
    event.level        as level, 
    song.song_id       as song_id, 
    song.artist_id     as artist_id, 
    event.sessionId    as session_id, 
    event.location     as location, 
    event.userAgent    as user_agent
FROM staging_events    as event
JOIN staging_songs     as song
    ON  event.song      = song.title
    AND event.artist    = song.artist_name
WHERE   event.page      = 'NextSong'
    AND event.ts       is NOT NULL
    AND event.userId   is NOT NULL
    AND event.level    is NOT NULL
""")

user_table_insert = ("""
INSERT INTO users (user_id, first_name, last_name, gender, level)
SELECT DISTINCT    userId,  firstName,  lastName,  gender, level
FROM staging_events
WHERE   userId is NOT NULL
    AND level  is NOT NULL;
""")

song_table_insert = ("""
INSERT INTO songs (song_id, title, artist_id, year, duration_str, duration_real)
SELECT DISTINCT    song_id, title, artist_id, year, duration,     duration::real
FROM staging_songs
WHERE song_id is NOT NULL;
""")

artist_table_insert = ("""
INSERT INTO artists (artist_id, name, location, latitude, longitude)
SELECT DISTINCT      artist_id, artist_name, artist_location, artist_latitude::real, artist_longitude::real
FROM staging_songs
WHERE artist_id is NOT NULL
AND     song_id is NOT NULL;
""")

time_table_insert = ("""
INSERT INTO time (start_time, hour, day, week, month, year, weekday)
SELECT DISTINCT
    start_time                         as start_time,
    extract(hour      from start_time) as hour,
    extract(day       from start_time) as day,
    extract(week      from start_time) as week,
    extract(month     from start_time) as month,
    extract(year      from start_time) as year,
    extract(dayofweek from start_time) as weekday
FROM songplays;
""")

# QUERY LISTS

create_table_queries = [staging_events_table_create, staging_songs_table_create, songplay_table_create, user_table_create, song_table_create, artist_table_create, time_table_create]
drop_table_queries = [staging_events_table_drop, staging_songs_table_drop, songplay_table_drop, user_table_drop, song_table_drop, artist_table_drop, time_table_drop]
copy_table_queries = [staging_events_copy, staging_songs_copy]
insert_table_queries = [songplay_table_insert, user_table_insert, song_table_insert, artist_table_insert, time_table_insert]
