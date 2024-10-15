import sqlite3

from student import Student, Teacher

DATABASE_NAME = "school_permits.db"

class DatabaseManager:
    def __init__(self):
        self.con = sqlite3.connect(DATABASE_NAME, check_same_thread=False)
        self.cur = self.con.cursor()

        self.cur.execute("CREATE TABLE IF NOT EXISTS students(name TEXT, password TEXT)")
        self.cur.execute("CREATE TABLE IF NOT EXISTS teachers(name TEXT, password TEXT)")
        self.cur.execute("INSERT OR IGNORE INTO teachers (name, password) VALUES ('Doron Lopez', '12345')")
        self.con.commit()
    def convert_to_student(self, data_base_entry):
        return Student(data_base_entry[0], data_base_entry[1])

    def convert_to_teacher(self, data_base_entry):
        return Teacher(data_base_entry[0], data_base_entry[1])

    def get_students(self):
        res = self.cur.execute("SELECT * FROM students")
        res = res.fetchall()

        students = [Student(student[0], student[1]) for student in res]
        return students
    def add(self,name,is_student: bool, password="123456"):
        self.cur.execute(f"INSERT OR IGNORE INTO {"students" if is_student else "teachers"} (name, password) VALUES ('{name}', '{password}')")
        self.con.commit()
    def login(self, name, password):
        res = self.cur.execute("SELECT * FROM students WHERE name = ? AND password = ?", (name, password))
        res = res.fetchall()
        if len(res) > 0:
            return self.convert_to_student(res[0])

        res = self.cur.execute("SELECT * FROM teachers WHERE name = ? AND password = ?", (name, password))
        res = res.fetchall()
        if len(res) > 0:
            return self.convert_to_teacher(res[0])
        else:
            raise "Invalid name or password"
