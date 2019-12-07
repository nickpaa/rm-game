from sqlite3 import register_adapter, connect
from numpy import int64
from pandas import read_sql_query


class GameDB():

    def __init__(self, db_file):
        self.db_file = db_file
        register_adapter(int64, lambda val: int(val))

    def create_connection(self):
        conn = connect(self.db_file)
        return conn

    def create_table(self):
        conn = self.create_connection()
        cur = conn.cursor()
        cur.execute("""
            CREATE TABLE IF NOT EXISTS results (
                id integer PRIMARY KEY,
                name text NOT NULL,
                location text NOT NULL,
                game text NOT NULL,
                revenue integer NOT NULL,
                gametime text
            );
        """)
        conn.close()

    def insert_results(self, result):
        conn = self.create_connection()
        cur = conn.cursor()
        cur.execute("""
            INSERT INTO results(
                name, location, game, revenue, gametime)
            VALUES(?,?,?,?,?)
            ;
            """, result)
        conn.commit()
        conn.close()

    def get_all_results(self):
        conn = self.create_connection()
        return read_sql_query('SELECT * FROM results ORDER BY revenue desc, gametime desc', conn)

    def get_some_results(self, which_game):
        conn = self.create_connection()
        return read_sql_query(f"SELECT * FROM results where game = '{which_game}' ORDER BY revenue desc, gametime desc", conn)

    def get_todays_results(self):
        conn = self.create_connection()
        return read_sql_query("SELECT * FROM results where gametime >= date('now') ORDER BY revenue desc, gametime desc", conn)

    def get_some_of_todays_results(self, which_game):
        conn = self.create_connection()
        return read_sql_query(f"SELECT * FROM results where game = '{which_game}' and gametime >= date('now') ORDER BY revenue desc, gametime desc", conn)

    def drop_results(self):
        conn = self.create_connection()
        cur = conn.cursor()
        cur.execute(""" DELETE FROM results; """)
        conn.commit()
        conn.close()


if __name__ == '__main__':
    test = GameDB('test.db')
