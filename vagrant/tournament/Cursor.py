import psycopg2


class Cursor():
    '''Create a psycopg2 connection and cursor object

    Args: none

    Returns:
        An open cursor to the database "tournament".

    This class offers a context manager through __enter__ and __exit__ methods.
    Usage:
        with Cursor() as my_cursor:
            my_cursur.execute(some_sql)'''

    def __init__(self):
        pass

    def __enter__(self):
        self.conn = psycopg2.connect("dbname=tournament")
        self.cursor = self.conn.cursor()
        return self.cursor

    def __exit__(self, exec_type, exec_val, exec_tb):
        self.conn.commit()
        self.cursor.close()
        self.conn.close()
