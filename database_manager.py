import sqlite3

from student import User

DATABASE_NAME = "school_permits.db"

class DatabaseManager:
    def __init__(self):
        self.con = sqlite3.connect(DATABASE_NAME, check_same_thread=False)
        self.cur = self.con.cursor()

        self.cur.execute("CREATE TABLE IF NOT EXISTS users(name TEXT, password TEXT, type INT)")
        self.cur.execute("INSERT OR IGNORE INTO users (name, password, type) VALUES ('Doron Lopez', '12345', 2)")
        self.con.commit()


    def get_students(self):
        res = self.cur.execute("SELECT name FROM users WHERE type = 0")
        res = res.fetchall()
        return res
    def add(self,name,type: int, password="123456"):
        self.cur.execute(f"INSERT OR IGNORE INTO users (name, password, type) VALUES (?, ?, ?)",(name, password, type))
        self.con.commit()
    def login(self, name, password):
        res = self.cur.execute("SELECT * FROM users WHERE name = ? AND password = ?", (name, password))
        res = res.fetchall()
        if len(res) > 0:
            return res[0]
        else:
            raise "Invalid name or password"
