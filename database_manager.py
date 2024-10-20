import sqlite3

from database_types.student import Student

DATABASE_NAME = "school_permits.db"

USER_TYPE_STUDENT = 0
USER_TYPE_PARENT = 1
USER_TYPE_TEACHER = 2

USER_TABLE = "users"
USER_TABLE_FIELD_USER_ID = "user_id"
USER_TABLE_FIELD_EMAIL = "email"
USER_TABLE_FIELD_PASSWORD = "password"
USER_TABLE_FIELD_NAME = "name"
USER_TABLE_FIELD_TYPE = "type"

STUDENT_TABLE = "students"
STUDENT_TABLE_FIELD_USER_ID = "user_id"
STUDENT_TABLE_FIELD_PERMITS = "permits"
STUDENT_TABLE_FIELD_GROUPS = "groups"

TEACHER_TABLE = "teachers"
TEACHER_TABLE_FIELD_USER_ID = "user_id"

PARENT_TABLE = "parents"
PARENT_TABLE_FIELD_USER_ID = "user_id"
PARENT_TABLE_FIELD_CHILDREN_USER_IDS = "children"

PERMITS_TABLE = "permits"
PERMITS_TABLE_FIELD_PERMIT_ID = "permit_id"
PERMITS_TABLE_FIELD_TEACHER_USER_ID = "teacher_user_id"
PERMITS_TABLE_FIELD_PARENT_USER_ID = "parent_user_id"
PERMITS_TABLE_FIELD_PERMIT_TYPE = "permit_type"

SINGLE_USE_PERMITS_TABLE = "single_use_permits"
SINGLE_USE_PERMITS_TABLE_FIELD_PERMIT_ID = "permit_id"
SINGLE_USE_PERMITS_TABLE_FIELD_DATE = "date"
SINGLE_USE_PERMITS_TABLE_FIELD_TIME = "time"
SINGLE_USE_PERMITS_TABLE_FIELD_USED = "used"

RECURRING_PERMITS_TABLE = "recurring_permits"
RECURRING_PERMITS_TABLE_FIELD = "date"
RECURRING_PERMITS_TABLE_TIME = "time"
RECURRING_PERMITS_TABLE_VALID = "valid"

GROUP_TABLE = "groups"
GROUP_TABLE_FIELD_GROUP_ID = "group_id"
# Schedule?

class DatabaseManager:
    def __init__(self):
        self.con = sqlite3.connect(DATABASE_NAME, check_same_thread=False)
        self.cur = self.con.cursor()

        self.create_tables()

    def create_tables(self):
        # lets go chatgpt
        # Create users table
        self.cur.execute(f"""
            CREATE TABLE IF NOT EXISTS {USER_TABLE} (
                {USER_TABLE_FIELD_USER_ID} INTEGER PRIMARY KEY,
                {USER_TABLE_FIELD_EMAIL} TEXT NOT NULL UNIQUE,
                {USER_TABLE_FIELD_PASSWORD} TEXT NOT NULL,
                {USER_TABLE_FIELD_NAME} TEXT NOT NULL,
                {USER_TABLE_FIELD_TYPE} INTEGER NOT NULL
            )
        """)

        # Create students table
        self.cur.execute(f"""
            CREATE TABLE IF NOT EXISTS {STUDENT_TABLE} (
                {STUDENT_TABLE_FIELD_USER_ID} INTEGER,
                {STUDENT_TABLE_FIELD_PERMITS} LIST,
                {STUDENT_TABLE_FIELD_GROUPS} LIST,
                FOREIGN KEY ({STUDENT_TABLE_FIELD_USER_ID}) REFERENCES {USER_TABLE}({USER_TABLE_FIELD_USER_ID})
            )
        """)

        # Create teachers table
        self.cur.execute(f"""
            CREATE TABLE IF NOT EXISTS {TEACHER_TABLE} (
                {TEACHER_TABLE_FIELD_USER_ID} INTEGER,
                FOREIGN KEY ({TEACHER_TABLE_FIELD_USER_ID}) REFERENCES {USER_TABLE}({USER_TABLE_FIELD_USER_ID})
            )
        """)

        # Create parents table
        self.cur.execute(f"""
            CREATE TABLE IF NOT EXISTS {PARENT_TABLE} (
                {PARENT_TABLE_FIELD_USER_ID} INTEGER,
                {PARENT_TABLE_FIELD_CHILDREN_USER_IDS} LIST,
                FOREIGN KEY ({PARENT_TABLE_FIELD_USER_ID}) REFERENCES {USER_TABLE}({USER_TABLE_FIELD_USER_ID})
            )
        """)

        # Create permits table
        self.cur.execute(f"""
            CREATE TABLE IF NOT EXISTS {PERMITS_TABLE} (
                {PERMITS_TABLE_FIELD_PERMIT_ID} INTEGER PRIMARY KEY,
                {PERMITS_TABLE_FIELD_TEACHER_USER_ID} INTEGER,
                {PERMITS_TABLE_FIELD_PARENT_USER_ID} INTEGER,
                {PERMITS_TABLE_FIELD_PERMIT_TYPE} TEXT,
                FOREIGN KEY ({PERMITS_TABLE_FIELD_TEACHER_USER_ID}) REFERENCES {USER_TABLE}({USER_TABLE_FIELD_USER_ID}),
                FOREIGN KEY ({PERMITS_TABLE_FIELD_PARENT_USER_ID}) REFERENCES {USER_TABLE}({USER_TABLE_FIELD_USER_ID})
            )
        """)

        # Create single-use permits table
        self.cur.execute(f"""
            CREATE TABLE IF NOT EXISTS {SINGLE_USE_PERMITS_TABLE} (
                {SINGLE_USE_PERMITS_TABLE_FIELD_PERMIT_ID} INTEGER,
                {SINGLE_USE_PERMITS_TABLE_FIELD_DATE} TEXT,
                {SINGLE_USE_PERMITS_TABLE_FIELD_TIME} TEXT,
                {SINGLE_USE_PERMITS_TABLE_FIELD_USED} INTEGER,
                FOREIGN KEY ({SINGLE_USE_PERMITS_TABLE_FIELD_PERMIT_ID}) REFERENCES {PERMITS_TABLE}({PERMITS_TABLE_FIELD_PERMIT_ID})
            )
        """)

        # Create recurring permits table
        self.cur.execute(f"""
            CREATE TABLE IF NOT EXISTS {RECURRING_PERMITS_TABLE} (
                {RECURRING_PERMITS_TABLE_FIELD} TEXT,
                {RECURRING_PERMITS_TABLE_TIME} TEXT,
                {RECURRING_PERMITS_TABLE_VALID} INTEGER,
                FOREIGN KEY ({RECURRING_PERMITS_TABLE_FIELD}) REFERENCES {PERMITS_TABLE}({PERMITS_TABLE_FIELD_PERMIT_ID})
            )
        """)

        # Create groups table
        self.cur.execute(f"""
            CREATE TABLE IF NOT EXISTS {GROUP_TABLE} (
                {GROUP_TABLE_FIELD_GROUP_ID} INTEGER PRIMARY KEY
            )
        """)
        #self.cur.execute(f"INSERT OR IGNORE INTO {USER_TABLE} ({USER_TABLE_FIELD_NAME}, {USER_TABLE_FIELD_PASSWORD}, {USER_TABLE_FIELD_TYPE}, {USER_TABLE_FIELD_EMAIL}) VALUES ('Daniel Roi', 12345, 0, 'danielr@pelech.ort.org.il')")
        # Commit the changes
        self.con.commit()

    def get_students(self):
        res = self.cur.execute(f"SELECT * FROM {USER_TABLE} WHERE {USER_TABLE_FIELD_TYPE} = {USER_TYPE_STUDENT}")
        res = res.fetchall()
        return [Student.from_db(val) for val in res]

    def add(self,name, u_type: int,email: str, password="123456"):
        self.cur.execute(f"INSERT OR IGNORE INTO {USER_TABLE} ({USER_TABLE_FIELD_NAME}, {USER_TABLE_FIELD_PASSWORD}, {USER_TABLE_FIELD_TYPE}, {USER_TABLE_FIELD_EMAIL}) VALUES (?, ?, ?, ?)",(name, password, u_type, email))
        self.con.commit()

    def login(self, email, password):
        res = self.cur.execute(f"SELECT * FROM users WHERE {USER_TABLE_FIELD_EMAIL} = ? AND {USER_TABLE_FIELD_PASSWORD} = ?", (email, password))
        res = res.fetchall()
        if len(res) > 0:
            return res[0]
        else:
            raise "Invalid name or password"
