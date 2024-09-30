import sqlite3 as lite

class dbsqlite:
    def __init__(self):        
        self.banco = 'exped.db'
        self.con = None
        self.cur = None
        self.setup_db_connection()

    def setup_db_connection(self):
        try:
            self.con = lite.connect(self.banco)
            self.cur = self.con.cursor()
        except Exception as e:
            print(f"Error setting up database connection: {e}")

    def close_db_connection(self):
        try:
            if self.cur:
                self.cur.close()
            if self.con:
                self.con.close()
        except Exception as e:
            print(f"Error closing database connection: {e}")
