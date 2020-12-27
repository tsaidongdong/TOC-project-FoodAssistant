import sqlite3

class Database:
    def __init__(self):
        db = "diary.db"
        self.conn = sqlite3.connect(db)
        self.create_table()

    def create_table(self):
        cur = self.conn.cursor()
        cur.execute(
            '''CREATE TABLE IF NOT EXISTS diary
            ( 
                id INTEGER PRIMARY KEY AUTOINCREMENT ,
                date TEXT NOT NULL ,
                content TEXT NOT NULL 
            );'''
        )
        self.conn.commit()
    
    def read(self, date):
        cur = self.conn.cursor()
        cur.execute("SELECT * FROM diary WHERE date = ?", (date,))
        return cur.fetchall()

    def getSize(self, date):
        cur = self.conn.cursor()
        cur.execute("SELECT COUNT(*) AS 'size' FROM diary WHERE date = ?", (date,))
        return cur.fetchall()[0][0]

    def insert(self, new_data):
        cur = self.conn.cursor()
        cur.execute("INSERT INTO diary VALUES(?, ?, ?)", new_data)
        self.conn.commit()
        
    def update(self, date, new_content):
        cur = self.conn.cursor()
        cur.execute("UPDATE diary SET content = ? WHERE date = ?", (new_content, date))
        self.conn.commit()

    def drop(self):
        r = input("Drop table (Y/n)? ")
        if r == 'Y':
            cur = self.conn.cursor()
            cur.execute("DROP TABLE diary")

    def insert_with_check(self, new_data):
        if self.getSize(new_data[1]) == 0:
            self.insert(new_data)
        else:
            self.update(new_data[1], new_data[2])

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.conn.commit()
        self.conn.close()