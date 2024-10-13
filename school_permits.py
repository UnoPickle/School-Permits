from flask import Flask, render_template, request
import database_manager
from database_manager import DatabaseManager
import json

database = DatabaseManager()

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("login.html")

@app.route("/student_names")
def handle_student_names():
    student_name = request.args.get("name")

    students = database.get_students()

    similar_students = list()

    for i in students:
        if student_name in i.first_name + " " + i.last_name:
            similar_students.append(i)

    return json.dumps([str(i) for i in similar_students])