import os

from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash
from datetime import datetime

# My app
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Ensure responses aren't cached
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

@app.route("/")
def home():
    return "Hello, Flask!"

@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()
    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")
        
        # Query database for username
        con = sqlite3.connect("volunteer.db")
        db = con.cursor()
        rows = db.execute("SELECT * FROM users WHERE = :email", email=email)

        # Ensure that email and password exist
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return redirect("/")
        
        con.commit()
        con.close()

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

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
    """Register user"""
    
    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        username = request.form.get("username")
        email = request.form.get("email")
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")
        
        if not password or password != confirmation:
            return render_template("password_mistake_html")
        
        # Logs user into database
        con = sqlite3.connect("volunteer.db")
        db = con.cursor()
        rows = db.execute("INSERT INTO users(email, username, hash) VALUES(?, ?, ?)", 
                          email, username, generate_password_hash( password, method='pbkdf2:sha256', salt_length=8))
        
        con.commit()
        con.close()

        # Reddirect user back to login page after registering
        return redirect("login.html")
    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("register.html")


# Error Handler
def errorhandler(e):
    """Handle error"""
    if not isinstance(e, HTTPException):
        e = InternalServerError()
    return render_template("error.html")


# Listen for errors
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)
