## Udacity - Data Engineering - 3
# Data Warehouse with AWS and Redshift

## About / Synopsis

In this project, I apply what I've learned on data warehouses and AWS to build an ETL pipeline for a database hosted on Redshift. To complete the project, I need to define fact and dimension tables for a star schema, choose distribution styles, and write an ETL pipeline that transfers data from files on S3 into these tables in Redshift using Python and SQL.

## Table of Contents
* [Project Datasets](#project-datasets)
    - [Song Dataset](#song-dataset)
    - [Log Dataset](#log-dataset)
* [Schema for Song Play Analysis](#schema-for-song-play-analysis)
    - [Fact Table](#fact-table)
    - [Dimension Tables](#dimension-tables)
* [Files in the Project](#files-in-the-project)
* [Running the Project](#running-the-project)
* [What I Have Learned](#what-i-have-learned)
* [Author](#author)

## Project Datasets

I'll be working with two datasets that reside in S3. Here are the S3 links for each:
* Song data: `s3://udacity-dend/song_data`
* Log data: `s3://udacity-dend/log_data`
    - Log data json path: `s3://udacity-dend/log_json_path.json`

### Song Dataset

The first dataset is a subset of real data from the [Million Song Dataset](https://labrosa.ee.columbia.edu/millionsong/). Each file is in JSON format and contains metadata about a song and the artist of that song. The files are partitioned by the first three letters of each song's track ID. For example, `song_data/A/B/C/TRABCEI128F424C983.json`

### Log Dataset

The second dataset consists of log files in JSON format generated by this [event simulator](https://github.com/Interana/eventsim) based on the songs in the dataset above. These simulate activity logs from a music streaming app based on specified configurations. The log files in the dataset are partitioned by year and month. For example, `log_data/2018/11/2018-11-12-events.json`.

## Schema for Song Play Analysis

Using the song and log datasets, I will create a star schema optimized for queries on song play analysis. This includes the following tables.

![Schema ERD](../media/schema.png?raw=true)

In `dwh_test.ipynb` I elaborate on the choice of tables distribution style.

### Fact Table

* **songplays** - records in log data associated with song plays i.e. records with page `NextSong`
    - *songplay_id, start_time, user_id, level, song_id, artist_id, session_id, location, user_agent*
    - distribution style: KEY distribution key *start_time*

### Dimension Tables

* **users** - users in the app
    - *user_id, first_name, last_name, gender, level*
    - distribution style: ALL
* **songs** - songs in music database
    - *song_id, title, artist_id, year, duration*
    - distribution style: ALL
* **artists** - artists in music database
    - *artist_id, name, location, latitude, longitude*
    - distribution style: ALL
* **time** - timestamps of records in songplays broken down into specific units
    - *start_time, hour, day, week, month, year, weekday*
    - distribution style: KEY distribution key *start_time*

## Files in the Project

- `dwh.cfg` is a configuration file with cluster parameters, which you need to complete with your AWS keys and database password.
- `dwh_iac.ipynb` contains IAC instructions to create, run, and delete the Redshift cluster.
- `dwh_test.ipynb` tests all ETL queries following the procedure step by step.
- `create_tables.py` drops and creates tables. Run this file to reset your tables before each time you run your ETL scripts.
- `etl.py` reads and processes files from `song_data` and `log_data` and loads them into DWH tables.
- `sql_queries.py` contains all SQL queries, and is imported into the last three files above.
- `README.md` provides the project description you are now reading.

## Running the Project

1) Open `dwh.cfg` and fill in your AWS keys, `aws_key` and `aws_secret`, and your Redshift database password, `db_password`.
1) Open `dwh_iac.ipynb` and follow IAC instructions to create and run the Redshift cluster.
1) When the cluster is running you can either run `create_tables.py` and then `etl.py` to create and populate the database, or
1) You can run `dwh_test.ipynb` to test the ETL procedure step by step.
1) Should you wish to delete your Redshift cluster, return to `dwh_iac.ipynb` and run its ending cells.

## What I Have Learned

Through the implementation of this project, while solving the project's core tasks, I've learned:

1) Setting up and accessing the Redshift cluster using IAC.
1) Data modeling for Redshift, including the choice of table distribution style.
1) COPY from S3 into Redshift.
1) SQL to SQL ETL on Redshift and that [INSERT on Redshift](https://docs.aws.amazon.com/redshift/latest/dg/r_INSERT_30.html) is not offering upsert control with ON CONFLICT clause.
1) Designed string (for WHERE condition) and floating point (for aggregations) attributes for the song length.

## Author

Andrii Dzugaiev, [in:dzugaev](https://www.linkedin.com/in/dzugaev/)