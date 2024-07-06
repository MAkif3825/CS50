import os

from cs50 import SQL
from flask import Flask, flash, jsonify, redirect, render_template, request, session

from datetime import datetime

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///birthdays.db")

# Define years
start_year = 1900
current_year = datetime.now().year
years = list(range(start_year, current_year +1))

# Define months
months = list(range(1, 13))

# Define days
days = list(range(1, 32))



@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":

        # TODO: Add the user's entry into the database
        name = request.form.get("name")
        month = request.form.get("month")
        day = request.form.get("day")
        db.execute("INSERT INTO birthdays (name, month, day) VALUES (?, ?, ?)", name, month, day)
        return redirect("/" )

    else:

        # TODO: Display the entries in the database on index.html
        table = db.execute("SELECT * FROM birthdays")

        return render_template("index.html" , table=table, years=years , months=months, days=days)