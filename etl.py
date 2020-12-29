import configparser
import psycopg2
from sql_queries import copy_table_queries, insert_table_queries


def load_staging_tables(cur, conn):
    """
    Populates the staging tables with CPOY from S3 buckets.
    """
    for query in copy_table_queries:
        cur.execute(query)
        conn.commit()


def insert_tables(cur, conn):
    """
    Performs SQL to SQL ETL from staging tables into fact and dimension tables.
    """
    for query in insert_table_queries:
        cur.execute(query)
        conn.commit()


def main():
    """
    Populates all DWH tables. Caters for the tables created.
    """
    dwh_cfg = configparser.ConfigParser()
    dwh_cfg.read('dwh.cfg')
    
    conn_values = (dwh_cfg.get('DB','DB_USER'),
                   dwh_cfg.get('DB','DB_PASSWORD'),
                   dwh_cfg.get('DB','DB_ENDPOINT'),
                   dwh_cfg.get('DB','DB_PORT'),
                   dwh_cfg.get('DB','DB_NAME'))
    
    conn = psycopg2.connect("user={} password={} host={} port={} dbname={}".format(*conn_values))
    cur = conn.cursor()
    
    load_staging_tables(cur, conn)
    insert_tables(cur, conn)

    conn.close()


if __name__ == "__main__":
    main()