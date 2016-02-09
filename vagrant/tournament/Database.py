import psycopg2


class Database():
    '''Create a psql database and execute the schema file'''

    def __init__(self, db_name, schema_file):
        self.db_name = db_name
        self.schema_file = schema_file
        conn = psycopg2.connect(dbname='postgres')
        conn.autocommit = True
        cursor = conn.cursor()
        cursor.execute("DROP DATABASE IF EXISTS " + db_name)
        cursor.execute("CREATE DATABASE " + db_name)
        cursor.close()
        conn.commit()
        conn.close()
        conn = psycopg2.connect("dbname="+db_name)
        cursor = conn.cursor()
        cursor.execute(open(self.schema_file, 'r').read())
        cursor.close()
        conn.commit()
        conn.close()


class Cursor(Database):
    '''Create a psycopg2 connection and cursor object

    Args: none

    Returns:
        An open cursor to the database "tournament".

    This class offers a context manager through __enter__ and __exit__ methods.
    Usage:
        with Cursor() as my_cursor:
            my_cursur.execute(some_sql)'''

    def __init__(self, database):
        self.db_name = database.db_name

    def __enter__(self):
        self.conn = psycopg2.connect("dbname=" + self.db_name)
        self.cursor = self.conn.cursor()
        return self.cursor

    def __exit__(self, exec_type, exec_val, exec_tb):
        self.conn.commit()
        self.cursor.close()
        self.conn.close()
