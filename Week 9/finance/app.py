import os

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required, lookup, usd

# Configure application
app = Flask(__name__)

# Custom filter
app.jinja_env.filters["usd"] = usd

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///finance.db")


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
    table = db.execute(
        "SELECT * FROM stock_index WHERE user_id = ?", session["user_id"]
    )
    cash = float(
        db.execute("SELECT cash FROM users WHERE id = ?", session["user_id"])[0]["cash"]
    )
    total = cash
    for row in table:
        addition = lookup(row["stock_symbol"])
        row["price"] = addition["price"]
        row["name"] = addition["name"]
        row["total"] = float(row["price"]) * int(row["quantity"])
        total += row["total"]

    return render_template("index.html", table=table, total=total, cash=cash)
    """Show portfolio of stocks"""


@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    """Buy shares of stock"""
    if request.method == "POST":
        # Check the presence of stock
        table = lookup(request.form.get("symbol"))
        if table == None:
            return apology("Stock Not found")

        # Check the validation of number
        shares = request.form.get("shares")
        try:
            shares = int(request.form.get("shares"))
        except ValueError:
            return apology("You should type a number!")
        if shares < 1:
            return apology("You cannot buy less than 1!")

        # Check if the user can afford it
        cash = float(
            db.execute("SELECT cash FROM users WHERE id = ?", session["user_id"])[0][
                "cash"
            ]
        )
        price = shares * table["price"]
        if cash - price < 0:
            return apology("You cannot afford it :/")

        # Buy
        db.execute(
            "INSERT INTO transactions (user_id, stock_symbol, quantity, price, total, type, date) VALUES (?, ?, ?, ?, ?, 'BUY', date('now'))",
            session["user_id"],
            table["symbol"],
            shares,
            table["price"],
            price,
        )
        current = cash - price
        db.execute(
            "UPDATE users SET cash = ? WHERE id = ?", current, session["user_id"]
        )

        check = db.execute(
            "SELECT * FROM stock_index WHERE user_id = ? AND stock_symbol = ?;",
            session["user_id"],
            table["symbol"],
        )
        if check:
            check = check[0]
            last_quantity = int(check["quantity"]) + shares
            db.execute(
                "UPDATE stock_index set quantity = ? WHERE user_id = ? AND stock_symbol = ?;",
                last_quantity,
                session["user_id"],
                table["symbol"],
            )
        else:
            db.execute(
                "INSERT INTO stock_index (user_id, stock_symbol, quantity) VALUES (?, ?, ?)",
                session["user_id"],
                table["symbol"],
                shares,
            )

        return redirect("/")

    else:
        return render_template("buy.html")


@app.route("/history")
@login_required
def history():
    """Show history of transactions"""
    table = db.execute(
        "SELECT * FROM transactions WHERE user_id = ?", session["user_id"]
    )
    return render_template("history.html", table=table)


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
        rows = db.execute(
            "SELECT * FROM users WHERE username = ?", request.form.get("username")
        )

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(
            rows[0]["hash"], request.form.get("password")
        ):
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


@app.route("/quote", methods=["GET", "POST"])
@login_required
def quote():
    if request.method == "POST":
        table = lookup(request.form.get("symbol"))

        # Check the stock
        if table == None:
            return apology("Not found")

        return render_template("quoted.html", table=table)

    else:
        table = db.execute("SELECT * FROM fav WHERE user_id = ?", session["user_id"])
        if table:
            for row in table:
                row["price"] = lookup(row["stock_symbol"])["price"]

    return render_template("quote.html", table=table)


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
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
                "INSERT INTO users (username, hash) VALUES (?, ?)",
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


@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    """Sell shares of stock"""
    if request.method == "POST":
        symbol = request.form.get("symbol")
        table = lookup(symbol)

        # Check the validation of number
        shares = request.form.get("shares")
        try:
            shares = int(request.form.get("shares"))
        except ValueError:
            return apology("You should type a number!")
        if shares < 1:
            return apology("You cannot sell less than 1!")
        # Check if the user can afford it
        result = db.execute(
            "SELECT quantity FROM stock_index WHERE user_id = ? AND stock_symbol = ?",
            session["user_id"],
            table["symbol"],
        )
        if result:
            result = result[0]

        presence = int(result["quantity"])
        if presence < shares:
            return apology("You don't have that much!")

        price = shares * table["price"]
        cash = float(
            db.execute("SELECT cash FROM users WHERE id = ?", session["user_id"])[0][
                "cash"
            ]
        )
        current = cash + price
        last_quantity = presence - shares

        db.execute(
            "UPDATE stock_index set quantity = ? WHERE user_id = ? AND stock_symbol = ?;",
            last_quantity,
            session["user_id"],
            table["symbol"],
        )

        if last_quantity == 0:
            db.execute("DELETE FROM stock_index WHERE quantity = 0;")

        db.execute(
            "INSERT INTO transactions (user_id, stock_symbol, quantity, price, total, type, date) VALUES (?, ?, ?, ?, ?, 'SELL', date('now'))",
            session["user_id"],
            table["symbol"],
            shares,
            table["price"],
            price,
        )
        db.execute(
            "UPDATE users SET cash = ? WHERE id = ?", current, session["user_id"]
        )

        return redirect("/")
        # Sell

    else:
        data = db.execute(
            "SELECT * FROM stock_index WHERE user_id = ?", session["user_id"]
        )
        return render_template("sell.html", data=data)


@app.route("/fav", methods=["POST"])
@login_required
def fav():
    stock = request.form.get("symbol")
    check = db.execute(
        "SELECT * FROM fav WHERE user_id = ? AND stock_symbol = ?",
        session["user_id"],
        stock,
    )
    if check:
        return apology("It has been added already.")
    else:
        db.execute(
            "INSERT INTO fav (user_id, stock_symbol) VALUES (?,?)",
            session["user_id"],
            stock,
        )
    return redirect("/quote")


@app.route("/rmm", methods=["POST"])
@login_required
def rmm():
    stock = request.form.get("symbol")
    db.execute(
        "DELETE FROM fav WHERE user_id=? AND stock_symbol=?", session["user_id"], stock
    )
    return redirect("/quote")
