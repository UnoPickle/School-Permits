import sqlite3

from student import Student

DATABASE_NAME = "school_permits.db"

class DatabaseManager:
    def __init__(self):
        self.con = sqlite3.connect(DATABASE_NAME, check_same_thread=False)
        self.cur = self.con.cursor()

        self.cur.execute("CREATE TABLE IF NOT EXISTS students(first_name TEXT, last_name TEXT)")

    def convert_to_student(self, data_base_entry):
        return Student(data_base_entry[0], data_base_entry[1])

    def get_students(self):
        res = self.cur.execute("SELECT * FROM students")
        res = res.fetchall()

        students = [Student(student[0], student [1]) for student in res]
        return students
