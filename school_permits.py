from flask import Flask, render_template, request, redirect
from database_manager import DatabaseManager
import json

database = DatabaseManager()

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("login.html")

@app.route("/login", methods=["POST"])
def login():
    name = request.form["username"]
    password = request.form["password"]
    try:
        database.login(name, password)
        return render_template('index.html', user_name=name)
    except Exception as e:
        print(e)
        return redirect("/")

@app.route("/student_names")
def handle_student_names():
    student_name = request.args.get("name")

    students = database.get_students()

    similar_students = [i.get_full_name() for i in students if student_name in i.first_name + " " + i.last_name]

    return json.dumps(similar_students)
@app.route("/user_profile")
def user_profile():
    return "HI"
@app.route("/student_selected", methods=["GET", "POST"])
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
    app.run(debug=True)