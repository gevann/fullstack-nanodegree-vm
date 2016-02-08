import psycopg2


class Cursor():
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
