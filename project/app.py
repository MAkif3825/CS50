import os

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.security import check_password_hash, generate_password_hash
from datetime import date, datetime, timedelta

from helpers import apology, login_required

# Configure application
app = Flask(__name__)


# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///project.db")


@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/")
@login_required
def index():
    events = db.execute("SELECT * FROM events WHERE user_id = ?", session["user_id"])
    tasks = db.execute("SELECT * FROM tasks WHERE user_id = ?", session["user_id"])
    habits = db.execute("SELECT * FROM habits WHERE user_id = ?", session["user_id"])
    todos = db.execute("SELECT * FROM todo WHERE user_id = ?", session["user_id"])

    today = datetime.now().date()
    todayy = today.strftime("%d %B %Y %A")

    formatted_events = []
    event_list = []
    formatted_tasks = []
    task_list = []
    formatted_habits = []
    habit_list = []

    for event in events:
        try:
            start = datetime.strptime(event["start"], "%Y-%m-%d")
            end = datetime.strptime(event["end"], "%Y-%m-%d")
        except ValueError:
            # Handle the case when the date-time format is "YYYY-MM-DDTHH:MM"
            start = datetime.strptime(event["start"], "%Y-%m-%dT%H:%M")
            end = datetime.strptime(event["end"], "%Y-%m-%dT%H:%M")

        if start.date() <= today < end.date():
            event_list.append(event)

        formatted_event = {
                'title': event['title'],
                'allDay': event['allDay'] == 'True',  # Convert 'True' string to boolean
                'start': event['start'],
                'end': event['end'],
                'backgroundColor': event['backgroundColor'],
            }
        formatted_events.append(formatted_event)

    for task in tasks:
        try:
            start = datetime.strptime(task["start"], "%Y-%m-%d")
            end = datetime.strptime(task["end"], "%Y-%m-%d")
        except ValueError:
            # Handle the case when the date-time format is "YYYY-MM-DDTHH:MM"
            start = datetime.strptime(task["start"], "%Y-%m-%dT%H:%M")
            end = datetime.strptime(task["end"], "%Y-%m-%dT%H:%M")

        if start.date() <= today < end.date():
            task_list.append(task)

        formatted_task = {
                'title': task['title'],
                'allDay': task['allDay'] == 'True',  # Convert 'True' string to boolean
                'start': task['start'],
                'end': task['end'],
                'backgroundColor': task['backgroundColor'],
                'extendedProps': {'isDone': task['status'] == 'True'},
            }
        formatted_tasks.append(formatted_task)


    for todo in todos:
        try:
            start = datetime.strptime(todo["start"], "%Y-%m-%d")
            end = datetime.strptime(todo["end"], "%Y-%m-%d")
        except ValueError:
            # Handle the case when the date-time format is "YYYY-MM-DDTHH:MM"
            start = datetime.strptime(todo["start"], "%Y-%m-%dT%H:%M")
            end = datetime.strptime(todo["end"], "%Y-%m-%dT%H:%M")

        if start.date() <= today < end.date():
            habit_list.append(todo)

    formatted_habits = [
        {
            'title': habit['title'],
            'allDay': habit['allDay'] == 'True',  # Convert 'True' string to boolean
            'startRecur': habit['start'],
            'endRecur': habit['end'],
            'backgroundColor': habit['backgroundColor'],
            'extendedProps': {'isDone': habit['status'] == 'True'},
            'daysOfWeek' : habit["daysOfWeek"].split(',')
        }
        for habit in habits
    ]

    user = db.execute("SELECT pp_img, pp_bg, name, surname FROM users WHERE id = ?", session["user_id"])[0]

    all_formatted = formatted_events + formatted_tasks + formatted_habits
    return render_template("index.html",all=all_formatted, events=event_list, tasks=task_list, habits=habit_list, user=user, today=todayy)


@app.route("/add_event", methods=["POST"])
@login_required
def add_event():
    if not request.form.get("title"):
        return apology("must provide title", 403)
    elif not request.form.get("start"):
        return apology("must provide start", 403)
    elif not request.form.get("end"):
        return apology("must provide end", 403)

    if request.form.get("eventType") == "allDay":
        isAllDay = "True"
        start = request.form.get("start")
        end = request.form.get("end")
    else:
        isAllDay = "False"
        startt = request.form.get("startTime")
        endt = request.form.get("endTime")
        start = request.form.get("start")
        end = request.form.get("end")
        start = start + "T" + startt
        end = end + "T" + endt

    db.execute("INSERT INTO events (user_id, title, allDay, start, end, backgroundColor) VALUES (?, ?, ?, ?, ?, ?)", session["user_id"], request.form.get("title"), isAllDay, start, end, request.form.get("backgroundColor1"))

    return redirect("/")

@app.route("/add_task", methods=["POST"])
@login_required
def add_task():
    if not request.form.get("title"):
        return apology("must provide title", 403)
    elif not request.form.get("start"):
        return apology("must provide start", 403)
    elif not request.form.get("end"):
        return apology("must provide end", 403)


    if request.form.get("taskType") == "allDay":
        isAllDay = "True"
        start = request.form.get("start")
        end = request.form.get("end")
    else:
        isAllDay = "False"
        startt = request.form.get("startTimee")
        endt = request.form.get("endTimee")
        start = request.form.get("start")
        end = request.form.get("end")
        start = start + "T" + startt
        end = end + "T" + endt

    db.execute("INSERT INTO tasks (user_id, title, allDay, start, end, backgroundColor, status) VALUES (?, ?, ?, ?, ?, ?, 'false')", session["user_id"], request.form.get("title"), isAllDay, start, end, request.form.get("backgroundColor2"))

    return redirect("/")

@app.route("/add_habit", methods=["POST"])
@login_required
def add_habit():
    if not request.form.get("title"):
        return apology("must provide title", 403)
    elif not request.form.get("start"):
        return apology("must provide start", 403)
    elif not request.form.get("end"):
        return apology("must provide end", 403)

    date1_str = request.form.get("start")
    date2_str = request.form.get("end")

    habit_id = db.execute("SELECT habit_id FROM habit_id WHERE user_id = ?",session["user_id"])
    if not  habit_id:
        habit_id = 1
        db.execute("INSERT INTO habit_id (user_id, habit_id) VALUES (?, ?)", session["user_id"], habit_id)
    else:
        habit_id = habit_id[0]["habit_id"]

    # Convert date strings to date objects
    date1 = date.fromisoformat(date1_str)
    date2 = date.fromisoformat(date2_str)

    # Calculate the difference in days
    number_of_days = (date2.toordinal() - date1.toordinal())

    days = request.form.getlist("days")
    days_string = ','.join(days)
    habit_day = 1

    if request.form.get("habitType") == "timeRangeee":
        isAllDay = "False"
        startt = request.form.get("startTimeee")
        endt = request.form.get("startTimeee")
        start = request.form.get("start")
        end = request.form.get("end")
        startwt = start + "T" + startt
        endwt = end + "T" + endt

        db.execute("INSERT INTO habits (user_id, habit_id, title, allDay, start, end, daysOfWeek, backgroundColor, status) VALUES (?, ?, ?, ?, ?, ?, ?, ?, 'false')", session["user_id"], habit_id, request.form.get("title"), isAllDay, startwt, endwt, days_string, request.form.get("backgroundColor3"))

        day_names_dict = {0: 'Sunday', 1: 'Monday', 2: 'Tuesday', 3: 'Wednesday', 4: 'Thursday', 5: 'Friday', 6: 'Saturday'}

        day_names = [
            day_names_dict[int(day)]
            for day in days
            ]


        for _ in range(number_of_days):
            pseudo_date = datetime.strptime(start, "%Y-%m-%d")
            day_name = pseudo_date.strftime("%A")


            if day_name in day_names:
                db.execute("INSERT INTO todo (user_id, habit_id, title, start, end, backgroundColor, status, habit_day) VALUES (?, ?, ?, ?, ?, ?, 'false', ?)", session["user_id"], habit_id, request.form.get("title"), startwt, startwt, request.form.get("backgroundColor3"), habit_day)
                habit_day +=1

            # Convert date string to datetime object
            date3 = datetime.strptime(start, "%Y-%m-%d")

            # Calculate the date one day later
            one_day_later = date3 + timedelta(days=1)

            # Format the result as YYYY-MM-DD
            start = one_day_later.strftime("%Y-%m-%d")

            startwt = start + "T" + startt


    else:
        isAllDay = "True"
        start = request.form.get("start")
        end = request.form.get("end")

        db.execute("INSERT INTO habits (user_id, habit_id, title, allDay, start, end, daysOfWeek, backgroundColor, status) VALUES (?, ?, ?, ?, ?, ?, ?, ?, 'false')", session["user_id"], habit_id, request.form.get("title"), isAllDay, start, end, days_string, request.form.get("backgroundColor3"))

        day_names_dict = {0: 'Sunday', 1: 'Monday', 2: 'Tuesday', 3: 'Wednesday', 4: 'Thursday', 5: 'Friday', 6: 'Saturday'}

        day_names = [
            day_names_dict[int(day)]
            for day in days
            ]

        for _ in range(number_of_days):
            pseudo_date = datetime.strptime(start, "%Y-%m-%d")
            day_name = pseudo_date.strftime("%A")

            if day_name in day_names:
                db.execute("INSERT INTO todo (user_id, habit_id, title, start, end, backgroundColor, status, habit_day) VALUES (?, ?, ?, ?, ?, ?, 'false', ?)", session["user_id"], habit_id, request.form.get("title"), start, start, request.form.get("backgroundColor3"), habit_day)
                habit_day += 1

            # Convert date string to datetime object
            date3 = datetime.strptime(start, "%Y-%m-%d")

            # Calculate the date one day later
            one_day_later = date3 + timedelta(days=1)

            # Format the result as YYYY-MM-DD
            start = one_day_later.strftime("%Y-%m-%d")

    habit_id += 1
    db.execute("UPDATE habit_id SET habit_id = ? WHERE user_id = ?", habit_id, session["user_id"])
    return redirect("/")

@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        # Check if name is blank
        if not request.form.get("name"):
            return apology("must provide a name")

        # Check if surname is blank
        if not request.form.get("surname"):
            return apology("must provide a surname")

        # Check if useranme is blank
        if not request.form.get("username"):
            return apology("must provide a username")

        # Check if password is blank
        elif not request.form.get("password"):
            return apology("password cannot be blank")

        # Check if confirmation is blank
        elif not request.form.get("confirmation"):
            return apology("confirmation cannot be blank")

        # Check the passwords
        elif not request.form.get("password") == request.form.get("confirmation"):
            return apology("Confitmation has to be same with password.")

        else:
            # Check if there is a same username in database
            check = db.execute(
                "SELECT username FROM users WHERE username = (?);",
                request.form.get("username"),
            )
            if check:
                return apology("Username is already taken.")

            # Provide security and insert the user info in database
            phash = generate_password_hash(request.form.get("password"))
            db.execute(
                "INSERT INTO users (name, surname, username, hash) VALUES (?, ?, ?, ?)",
                request.form.get("name"),
                request.form.get("surname"),
                request.form.get("username"),
                phash,
            )

            # Keep the user logged in
            session["user_id"] = db.execute(
                "SELECT id FROM users WHERE username = (?);",
                request.form.get("username"),
            )[0]["id"]

            # Redirect user to home page
            return redirect("/")

    else:
        return render_template("register.html")

@app.route("/settings", methods=["GET", "POST"])
@login_required
def settings():
    if request.method == "POST":
        #Confirm the password
        if not check_password_hash(db.execute("SELECT hash FROM users WHERE id=?", session["user_id"])[0]["hash"], request.form.get("confirm")):
            return apology("Wrong password.")
        else:
            #Check for name
            name = request.form.get("name")
            if name:
                db.execute("UPDATE users SET name = ? WHERE id= ?", name, session["user_id"])

            #Check for surname
            surname = request.form.get("surname")
            if surname:
                db.execute("UPDATE users SET surname = ? WHERE id= ?", surname, session["user_id"])

            #Check for avatar
            avatar = request.form.get("avatar")
            if avatar:
                db.execute("UPDATE users SET pp_img = ? WHERE id= ?", avatar, session["user_id"])

            #Check for bg
            color = request.form.get("color")
            if not color == "#000000":
                db.execute("UPDATE users SET pp_bg = ? WHERE id= ?", color, session["user_id"])

            #Check for username
            username = request.form.get("username")
            if username:
                db.execute("UPDATE users SET username = ? WHERE id= ?", username, session["user_id"])

            #Check for password
            password = request.form.get("password")
            if password:
                hashed = generate_password_hash(request.form.get("password"))
                db.execute("UPDATE users SET hash = ? WHERE id= ?", hashed, session["user_id"])

            return redirect("/")

    else:
        user = db.execute("SELECT * FROM users WHERE id = ?", session["user_id"])[0]
        return render_template("settings.html", user=user)

@app.route("/overview", methods=["GET", "POST"])
@login_required
def overview():
    today = datetime.now().date()

    events = db.execute("SELECT * FROM events WHERE user_id = ?", session["user_id"])
    tasks = db.execute("SELECT * FROM tasks WHERE user_id = ?", session["user_id"])
    habits = db.execute("SELECT * FROM habits WHERE user_id = ?", session["user_id"])

    current_events = []
    current_tasks = []
    current_habits = []

    past_events = []
    past_tasks = []
    past_habits = []

    for event in events:
        try:
            end = datetime.strptime(event["end"], "%Y-%m-%d")
        except ValueError:
            end = datetime.strptime(event["end"], "%Y-%m-%dT%H:%M")

        if end.date() < today:
            past_events.append(event)
        else:
            current_events.append(event)
    print(past_events)

    for task in tasks:
        if task["status"] == 'false':
            task["status"] = 'Not completed'
        else:
            task["status"] = 'Completed'

        try:
            end = datetime.strptime(task["end"], "%Y-%m-%d")
        except ValueError:
            end = datetime.strptime(task["end"], "%Y-%m-%dT%H:%M")

        if end.date() < today:
            past_tasks.append(task)
        else:
            current_tasks.append(task)

    for habit in habits:
        try:
            end = datetime.strptime(habit["end"], "%Y-%m-%d")
        except ValueError:
            end = datetime.strptime(habit["end"], "%Y-%m-%dT%H:%M")

        numerator = 0
        data = db.execute("SELECT status FROM todo WHERE user_id = ? AND habit_id = ?", session["user_id"], habit["habit_id"])
        for element in data:
            if element["status"] == 'true':
                numerator += 1

        habit["details"] = db.execute("SELECT * FROM todo WHERE user_id = ? AND habit_id = ?", session["user_id"], habit["habit_id"])

        success = numerator/len(data)*100
        habit["success"] = "{:.2f}".format(success)

        if end.date() < today:
            past_habits.append(habit)
        else:
            current_habits.append(habit)

    return render_template("overview.html", cevents=current_events, pevents=past_events, ctasks=current_tasks, ptasks=past_tasks, chabits=current_habits, phabits=past_habits)


@app.route("/task_status", methods=["POST"])
@login_required
def task_status():
    if request.form.get("task_status") == "false":
        db.execute("UPDATE tasks SET status = 'false' WHERE user_id = ? AND task_id = ?", session["user_id"], request.form.get("task_id"))
    else:
        db.execute("UPDATE tasks SET status = 'true' WHERE user_id = ? AND task_id = ?", session["user_id"], request.form.get("task_id"))

    """Get stock quote."""
    return redirect("/")

@app.route("/task_statuso", methods=["POST"])
@login_required
def task_statuso():
    if request.form.get("task_status") == "false":
        db.execute("UPDATE tasks SET status = 'false' WHERE user_id = ? AND task_id = ?", session["user_id"], request.form.get("task_id"))
    else:
        db.execute("UPDATE tasks SET status = 'true' WHERE user_id = ? AND task_id = ?", session["user_id"], request.form.get("task_id"))

    """Get stock quote."""
    return redirect("overview")

@app.route("/habit_status", methods=["POST"])
@login_required
def habit_status():
    if request.form.get("habit_status") == "false":
        db.execute("UPDATE todo SET status = 'false' WHERE user_id = ? AND start = ? AND habit_id = ?", session["user_id"], request.form.get("start"), request.form.get("habit_id"))
    else:
        db.execute("UPDATE todo SET status = 'true' WHERE user_id = ? AND start = ? AND habit_id = ?", session["user_id"], request.form.get("start"), request.form.get("habit_id"))

    """Get stock quote."""
    return redirect("/")

@app.route("/habit_statuso", methods=["POST"])
@login_required
def habit_statuso():
    if request.form.get("habit_status") == "false":
        db.execute("UPDATE todo SET status = 'false' WHERE user_id = ? AND start = ? AND habit_id = ?", session["user_id"], request.form.get("start"), request.form.get("habit_id"))
    else:
        db.execute("UPDATE todo SET status = 'true' WHERE user_id = ? AND start = ? AND habit_id = ?", session["user_id"], request.form.get("start"), request.form.get("habit_id"))

    """Get stock quote."""
    return redirect("overview")

@app.route("/del_event", methods=["POST"])
@login_required
def del_event():
    db.execute("DELETE FROM events WHERE user_id = ? AND event_id = ?", session["user_id"], request.form.get("event_id"))
    return redirect("overview")

@app.route("/del_task", methods=["POST"])
@login_required
def del_task():
    db.execute("DELETE FROM tasks WHERE user_id = ? AND task_id = ?", session["user_id"], request.form.get("task_id"))
    return redirect("overview")

@app.route("/del_habit", methods=["POST"])
@login_required
def del_habit():
    db.execute("DELETE FROM habits WHERE user_id = ? AND habit_id = ?", session["user_id"], request.form.get("habit_id"))
    db.execute("DELETE FROM todo WHERE user_id = ? AND habit_id = ?", session["user_id"], request.form.get("habit_id"))
    return redirect("overview")