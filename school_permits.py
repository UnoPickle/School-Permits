from flask import Flask, render_template, request, redirect, session, url_for, flash
from database_manager import DatabaseManager
import json
from functools import wraps
import secrets
from email_manager import send_change_password
database = DatabaseManager()

app = Flask(__name__)
TYPES = {"teacher": 0, "student": 1, "parent": 2}


def check_session(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        # check session
        if "name" in session:
            return func(*args, **kwargs)
        # no session, go to log in
        return redirect(url_for("index"))

    return wrapper


@app.route("/")
def index():
    if "name" in session:
        return f"HI {session["name"]}"
    return render_template("login.html")


@app.route("/logout")
def logout():
    session.clear()
    return render_template("login.html")


@app.route("/login", methods=["POST"])
def login():
    email = request.form["username"]
    password = request.form["password"]
    try:
        user = database.login(email, password)
        session["name"] = user[3]
        session["type"] = user[4]
        return redirect(url_for("find_student"))
    except Exception as e:
        return redirect("/")


@app.route("/find_student")
@check_session
def find_student():
    return render_template('find_student.html', user_name=session["name"])


@app.route('/add', methods=['GET', 'POST'])
@check_session
def add_person():
    if session.get("type") != TYPES.get("teacher"):
        return render_template("permission_error.html")

    if request.method == 'POST':
        name = request.form['name']
        role = request.form['role']
        email = request.form['email']

        if role in TYPES:
            if role == "student":
                # Get parent data from form
                parent_names = request.form.getlist('parent_name[]')
                parent_emails = request.form.getlist('parent_email[]')

                # Validate that at least one parent is provided
                if not parent_names or not parent_emails or len(parent_names) < 1 or len(parent_emails) < 1:
                    flash('At least one parent profile is required when adding a student.')
                    return redirect(url_for('add_person'))

                parents_ids = []
                # Loop through parent profiles and add them
                for p_name, p_email in zip(parent_names, parent_emails):
                    # Check if parent already exists
                    parent = database.get_user_by_email(p_email)
                    if not parent:
                        # Add new parent
                        parent_id = database.add_user(p_name, TYPES['parent'], p_email)
                    else:
                        print(parent)
                        parent_id = parent[0]
                    parents_ids.append(parent_id)

                # if only 1 parent was submitted, the second is none
                if len(parents_ids) == 1:
                    parents_ids.append(None)

                database.add_user(name, TYPES["student"], email, parents=parents_ids)
                flash('Student and parent(s) added successfully.')
                return render_template('add_user.html', user_name=session["name"])

            elif role == "parent":
                # Get the student's email
                student_email = request.form.get('student_email')
                if not student_email:
                    flash('Student\'s email is required when adding a parent.')
                    return redirect(url_for('add_person'))

                # Find the student in the database
                student = database.get_user_by_email(student_email)
                print(student)
                if not student or student[4] != TYPES['student']:
                    flash('No student found with the provided email.')
                    return redirect(url_for('add_person'))

                # Add the parent to the database
                parent_id = database.add_user(name, TYPES[role], email)

                # Link the parent to the student
                database.add_parent_to_student(parent_id, student[0])

                return redirect(url_for('add_person'))  # Replace with your success page

            else:
                # For 'teacher' or other roles
                database.add_user(name, TYPES[role], email)
                flash('Person added successfully.')
                return redirect(url_for('add_person'))  # Replace with your success page
        else:
            flash('Invalid role selected.')
            return redirect(url_for('add_person'))
    else:
        # Handle GET request by rendering the form
        return render_template('add_user.html', user_name=session["name"])


@app.route("/reset_password", methods=["GET", "POST"])
def reset_password():
    if request.method == "GET":
        return render_template("reset_password.html")
    else:
        if not ("secret_token" in session and "wanted_email" in session):
            redirect(url_for("index"))
        code = request.form.get("code")
        if not code:
            return redirect(url_for("forgot_password"))
        if code == session["secret_token"]:
            del session["secret_token"]
            database.change_password_by_email(session["wanted_email"], session["new_password"])
            del session["wanted_email"]
            return "Your password has been reseted to the deafult password"
        else:
            #didnt succeed
            return redirect(url_for("forgot_password"))


@app.route("/forgot_password", methods=["GET", "POST"])
def forgot_password():
    if request.method == "GET":
        return render_template("forgot_password.html")
    else:
        email = request.form.get("email")
        if not email or not database.get_user_by_email(email):
            print("email does not in database")
            return render_template("forgot_password.html")
        token = secrets.token_hex(16)
        session["secret_token"] = token
        session["wanted_email"] = email
        send_change_password(email, token)
        return redirect(url_for("reset_password"))

@app.route("/student_names")
@check_session
def handle_student_names():
    student_name = request.args.get("name")

    students = database.get_students()
    similar_students = [i.get_name() for i in students if student_name in i.get_name()]

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
