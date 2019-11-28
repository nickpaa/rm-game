import sqlite3
from sqlite3 import Error
import numpy as np


db_file = 'results.db'

sqlite3.register_adapter(np.int64, lambda val: int(val))


def create_connection(db_file):
    """ create a database connection to the SQLite database
        specified by db_file
    :param db_file: database file
    :return: Connection object or None
    """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except Error as e:
        print(e)
 
    return conn


def create_table(conn, create_table_sql):
    """ create a table from the create_table_sql statement
    :param conn: Connection object
    :param create_table_sql: a CREATE TABLE statement
    :return:
    """
    try:
        c = conn.cursor()
        c.execute(create_table_sql)
    except Error as e:
        print(e)


create_string = """
CREATE TABLE IF NOT EXISTS results (
    id integer PRIMARY KEY,
    name text NOT NULL,
    location text NOT NULL,
    game text NOT NULL,
    revenue integer NOT NULL,
    gametime text
);
"""


def main():
    db_file = 'results.db'

    conn = create_connection(db_file)
    if conn:
        create_table(conn, create_string)
    else:
        print('Error - can\'t create database connection')


def insert_results(conn, result):
    sql = """ INSERT INTO results(name, location, game, revenue, gametime)
        VALUES(?,?,?,?,?);"""
    cur = conn.cursor()
    cur.execute(sql, result)
    conn.commit()


def drop_results(conn):
    pass


if __name__ == '__main__':
    main()