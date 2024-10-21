import sqlite3

from database_types.student import Student

import sqlite3

from database_types.user import User

DATABASE_NAME = "school_permits.db"

USER_TYPE_STUDENT = 1
USER_TYPE_PARENT = 2
USER_TYPE_TEACHER = 0

USER_TABLE = "users"
USER_TABLE_FIELD_USER_ID = "user_id"
USER_TABLE_FIELD_EMAIL = "email"
USER_TABLE_FIELD_PASSWORD = "password"
USER_TABLE_FIELD_NAME = "name"
USER_TABLE_FIELD_TYPE = "type"

STUDENT_TABLE = "students"
STUDENT_TABLE_FIELD_USER_ID = "user_id"
STUDENT_TABLE_FIELD_PARENT1_ID = "parent1_id"
STUDENT_TABLE_FIELD_PARENT2_ID = "parent2_id"

PERMITS_TABLE = "single_use_permits"
PERMITS_TABLE_FIELD_PERMIT_ID = "permit_id"
PERMITS_TABLE_FIELD_TEACHER_USER_ID = "teacher_user_id"
PERMITS_TABLE_FIELD_PARENT_USER_ID = "parent_user_id"
PERMITS_TABLE_FIELD_STUDENT_USER_ID = "student_user_id"
PERMITS_TABLE_FIELD_PERMIT_TYPE = "permit_type"
PERMITS_TABLE_FIELD_DATE = "date"
PERMITS_TABLE_FIELD_TIME = "time"
PERMITS_TABLE_FIELD_USED = "used"
PERMITS_TABLE_FIELD_CONFIRMED = "confirmed"

STUDENTS_GROUPS_TABLE = "students_groups"
STUDENTS_GROUPS_FIELD_STUDENT_ID = "student_id"
STUDENTS_GROUPS_FIELD_GROUP_ID = "group_id"

GROUP_TABLE = "groups"
GROUP_TABLE_FIELD_GROUP_ID = "group_id"


class DatabaseManager:
    def __init__(self):
        self.con = sqlite3.connect(DATABASE_NAME, check_same_thread=False)
        self.cur = self.con.cursor()
        self.create_tables()

    def create_tables(self):
        # Create users table
        self.cur.execute(f"""
            CREATE TABLE IF NOT EXISTS {USER_TABLE} (
                {USER_TABLE_FIELD_USER_ID} INTEGER PRIMARY KEY AUTOINCREMENT,
                {USER_TABLE_FIELD_EMAIL} TEXT NOT NULL UNIQUE,
                {USER_TABLE_FIELD_PASSWORD} TEXT NOT NULL,
                {USER_TABLE_FIELD_NAME} TEXT NOT NULL,
                {USER_TABLE_FIELD_TYPE} INTEGER NOT NULL
            )
        """)

        # Create students table
        self.cur.execute(f"""
            CREATE TABLE IF NOT EXISTS {STUDENT_TABLE} (
                {STUDENT_TABLE_FIELD_USER_ID} INTEGER PRIMARY KEY,
                {STUDENT_TABLE_FIELD_PARENT1_ID} INTEGER,
                {STUDENT_TABLE_FIELD_PARENT2_ID} INTEGER,
                FOREIGN KEY ({STUDENT_TABLE_FIELD_USER_ID}) REFERENCES {USER_TABLE}({USER_TABLE_FIELD_USER_ID}) ON DELETE CASCADE,
                FOREIGN KEY ({STUDENT_TABLE_FIELD_PARENT1_ID}) REFERENCES {USER_TABLE}({USER_TABLE_FIELD_USER_ID}) ON DELETE SET NULL,
                FOREIGN KEY ({STUDENT_TABLE_FIELD_PARENT2_ID}) REFERENCES {USER_TABLE}({USER_TABLE_FIELD_USER_ID}) ON DELETE SET NULL
            )
        """)

        # Create groups table
        self.cur.execute(f"""
            CREATE TABLE IF NOT EXISTS {GROUP_TABLE} (
                {GROUP_TABLE_FIELD_GROUP_ID} INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL UNIQUE
            )
        """)

        # Create students_groups table
        self.cur.execute(f"""
            CREATE TABLE IF NOT EXISTS {STUDENTS_GROUPS_TABLE} (
                {STUDENTS_GROUPS_FIELD_GROUP_ID} INTEGER NOT NULL,
                {STUDENTS_GROUPS_FIELD_STUDENT_ID} INTEGER NOT NULL,
                FOREIGN KEY ({STUDENTS_GROUPS_FIELD_STUDENT_ID}) REFERENCES {STUDENT_TABLE} ({STUDENT_TABLE_FIELD_USER_ID}) ON DELETE CASCADE,
                FOREIGN KEY ({STUDENTS_GROUPS_FIELD_GROUP_ID}) REFERENCES {GROUP_TABLE} ({GROUP_TABLE_FIELD_GROUP_ID}) ON DELETE CASCADE,
                PRIMARY KEY ({STUDENTS_GROUPS_FIELD_GROUP_ID}, {STUDENTS_GROUPS_FIELD_STUDENT_ID})
            )
        """)

        # Create permits table
        self.cur.execute(f"""
            CREATE TABLE IF NOT EXISTS {PERMITS_TABLE} (
                {PERMITS_TABLE_FIELD_PERMIT_ID} INTEGER PRIMARY KEY AUTOINCREMENT,
                {PERMITS_TABLE_FIELD_TEACHER_USER_ID} INTEGER NOT NULL,
                {PERMITS_TABLE_FIELD_STUDENT_USER_ID} INTEGER NOT NULL,
                {PERMITS_TABLE_FIELD_PARENT_USER_ID} INTEGER,
                {PERMITS_TABLE_FIELD_PERMIT_TYPE} TEXT NOT NULL,
                {PERMITS_TABLE_FIELD_DATE} TEXT NOT NULL,
                {PERMITS_TABLE_FIELD_TIME} TEXT NOT NULL,
                {PERMITS_TABLE_FIELD_CONFIRMED} BOOLEAN NOT NULL DEFAULT 0,
                {PERMITS_TABLE_FIELD_USED} BOOLEAN NOT NULL DEFAULT 0,
                FOREIGN KEY ({PERMITS_TABLE_FIELD_TEACHER_USER_ID}) REFERENCES {USER_TABLE}({USER_TABLE_FIELD_USER_ID}) ON DELETE CASCADE,
                FOREIGN KEY ({PERMITS_TABLE_FIELD_STUDENT_USER_ID}) REFERENCES {USER_TABLE}({USER_TABLE_FIELD_USER_ID}) ON DELETE CASCADE,
                FOREIGN KEY ({PERMITS_TABLE_FIELD_PARENT_USER_ID}) REFERENCES {USER_TABLE}({USER_TABLE_FIELD_USER_ID}) ON DELETE SET NULL
            )
        """)

        # Insert default admin user
        self.cur.execute(f"""
            INSERT OR IGNORE INTO {USER_TABLE} (
                {USER_TABLE_FIELD_NAME},
                {USER_TABLE_FIELD_PASSWORD},
                {USER_TABLE_FIELD_TYPE},
                {USER_TABLE_FIELD_EMAIL}
            ) VALUES ('Admin', '12345', {USER_TYPE_TEACHER}, 'admin@example.com')
        """)

        # Commit the changes
        self.con.commit()

    def get_students(self):
        res = self.cur.execute(f"SELECT * FROM {USER_TABLE} WHERE {USER_TABLE_FIELD_TYPE} = {USER_TYPE_STUDENT}")
        res = res.fetchall()
        return [User.from_db(val) for val in res]

    def add_user(self, name, u_type: int, email: str, password="123456", parents=None):
        self.cur.execute(f"""
                        INSERT INTO {USER_TABLE} (
                            {USER_TABLE_FIELD_EMAIL},
                            {USER_TABLE_FIELD_PASSWORD},
                            {USER_TABLE_FIELD_NAME},
                            {USER_TABLE_FIELD_TYPE}
                        ) VALUES (?, ?, ?, ?)
                    """, (email, password, name, u_type))

        # Get the user_id of the newly inserted user
        user_id = self.cur.lastrowid

        # If the user is a student, insert into the students table
        if u_type == USER_TYPE_STUDENT:
            self.cur.execute(f"""
                            INSERT INTO {STUDENT_TABLE} (
                                {STUDENT_TABLE_FIELD_USER_ID},
                                {STUDENT_TABLE_FIELD_PARENT1_ID},
                                {STUDENT_TABLE_FIELD_PARENT2_ID}
                            ) VALUES (?, ?, ?)
                        """, (user_id, *parents))

        self.con.commit()
        return user_id

    def add_parent_to_student(self, parent_id, student_id):
        user = self.get_student_by_id(student_id)
        print(student_id)
        if user:
            print(user)
            if not user[1]:
                self.cur.execute(f"""UPDATE {STUDENT_TABLE} SET {STUDENT_TABLE_FIELD_PARENT1_ID} = {parent_id}""")
                # Commit the changes
                self.con.commit()
                return True
            elif not user[2]:
                self.cur.execute(f"""UPDATE {STUDENT_TABLE} SET {STUDENT_TABLE_FIELD_PARENT2_ID} = {parent_id}""")
                # Commit the changes
                self.con.commit()
                return True
        return False
    def login(self, email, password):
        res = self.cur.execute(
            f"SELECT * FROM users WHERE {USER_TABLE_FIELD_EMAIL} = ? AND {USER_TABLE_FIELD_PASSWORD} = ?",
            (email, password))
        res = res.fetchall()
        if len(res) > 0:
            return res[0]
        else:
            raise "Invalid name or password"

    def get_user_by_id(self, id):
        res = self.cur.execute(f"SELECT * FROM {USER_TABLE} WHERE {USER_TABLE_FIELD_USER_ID} = {id}")
        res = res.fetchone()
        return res[0]
    def get_student_by_id(self, id):
        res = self.cur.execute(f"SELECT * FROM {STUDENT_TABLE} WHERE {STUDENT_TABLE_FIELD_USER_ID} = {id}")
        res = res.fetchone()
        return res
    def get_user_by_email(self, email):
        res = self.cur.execute(f"SELECT * FROM {USER_TABLE} WHERE {USER_TABLE_FIELD_EMAIL} = '{email}'")
        res = res.fetchone()
        return res
