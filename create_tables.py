import configparser
import psycopg2
from sql_queries import create_table_queries, drop_table_queries


def drop_tables(cur, conn):
    """
    Drops all DWH tables.
    """
    for query in drop_table_queries:
        cur.execute(query)
        conn.commit()


def create_tables(cur, conn):
    """
    Creates all DWH tables.
    """
    for query in create_table_queries:
        cur.execute(query)
        conn.commit()


def main():
    """
    Drops and creates all DWH tables.
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

    drop_tables(cur, conn)
    create_tables(cur, conn)

    conn.close()


if __name__ == "__main__":
    main()