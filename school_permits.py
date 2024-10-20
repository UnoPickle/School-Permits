from flask import Flask, render_template, request, redirect, session, url_for
from database_manager import DatabaseManager
import json
from functools import wraps

database = DatabaseManager()

app = Flask(__name__)
TYPES = {"student": 0, "parent": 1, "teacher": 2}


def check_session(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        # check session
        print(session)
        if "name" in session:
            return func(*args, **kwargs)
        # no session, go to log in
        return redirect(url_for("index"))

    return wrapper


@app.route("/")
def index():
    return render_template("login.html")


@app.route("/login", methods=["POST"])
def login():
    name = request.form["username"]
    password = request.form["password"]
    try:
        user = database.login(name, password)
        session["name"] = name
        session["type"] = user[2]
        return redirect(url_for("find_student"))
    except Exception as e:
        print(e)
        return redirect("/")

@app.route("/find_student")
@check_session
def find_student():
    return render_template('find_student.html', user_name=session["name"])

@app.route('/admin/add', methods=['GET', 'POST'])
@check_session
def add_person():
    if request.method == 'POST':
        name = request.form['name']
        role = request.form['role']
        if role in TYPES:
            database.add(name, TYPES[role])

    return render_template('add_user.html', user_name=session["name"])


@app.route("/student_names")
@check_session
def handle_student_names():
    student_name = request.args.get("name")

    students = database.get_students()
    print(students)
    similar_students = [i[0] for i in students if student_name in i[0]]

    return json.dumps(similar_students)


@app.route("/user_profile")
@check_session
def user_profile():
    return "HI"


@app.route("/student_selected", methods=["GET", "POST"])
@check_session
def select_student():
    #student_name = request.args.get("name")
    return render_template(
        'student.html',
        student_name="student_name",
        class_grade="9th (3)",
        permit_today_time="10:00",
        permit_status="Unused",
        permit_date="10/10/2024",
        permit_time="10:00",
        future_permit_date="19/10/2024",
        future_permit_time="10:00",
        teacher_name="Yakir",
        parental_approval="Yes"
    )


if __name__ == "__main__":
    app.secret_key = 'zDasmcnaslfdkas;daKNCSDLKFN34223&ESF'
    app.run(debug=True)
