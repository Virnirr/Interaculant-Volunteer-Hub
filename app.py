import sqlite3
from sqlite3.dbapi2 import Timestamp
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash
from datetime import datetime

from helper import dict_factory
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
    return render_template("landing.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")
        
        # Query database for username
        con = sqlite3.connect("volunteer.db")
        con.row_factory = dict_factory
        db = con.cursor()

        rows = db.execute("SELECT * FROM users WHERE email=?", [email]).fetchall()

        # Ensure that email and password exist
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], password):
            con.close()
            flash("Invalid Email and/or Password", "danger")
            return redirect("/login")
        
        con.commit()
        con.close()

        # Forget any user_id
        session.clear()

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        flash("Login Successfully!", "info")
        return redirect("/services")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")

@app.route("/contact", methods=["GET", "POST"])
def contact():
    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        return redirect("/contact")


    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("contact.html")
    

@app.route("/logout")
def logout():
    """Log user out"""

    # Flash message for logout
    if "user_id" in session:
        user = session["user_id"]
        flash(f"You have been logged out, {user}", "info")

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
        
        # Logs user into database
        con = sqlite3.connect("volunteer.db")
        db = con.cursor()
        
        rows = db.execute("SELECT * FROM users WHERE username = ?", [username]).fetchall()
        email_check = db.execute("SELECT * FROM users WHERE email = ?", [email]).fetchall()

        if len(rows) != 0:
            con.close()
            flash("Username Already Taken!", "danger")
            return redirect("/register")
        
        if len(email_check) != 0:
            con.close()
            flash("Email Already Taken!", "danger")
            return redirect("/register")

        hashed_password = generate_password_hash(password, method='pbkdf2:sha256', salt_length=8)
        db.execute("INSERT INTO users(email, username, hash) VALUES(?, ?, ?)", 
                          [email, username, hashed_password])
        
        con.commit()
        con.close()

        # Reddirect user back to login page after registering
        
        flash("Register Successfully!", "success")
        return redirect("/login")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("register.html")

@app.route("/services", methods=["GET", "POST"])
def services():

    if request.method == "POST":
        # do something
        return redirect ("/")
    else:
        return render_template("services.html")

@app.route("/create_service", methods=["GET", "POST"])
def create_service():

    if request.method == "POST":
        # do something
        return redirect ("/")
    
    else:
        themes = [
            "Celebration",
            "Foodie",
            "Education"
        ]
        return render_template("create_service.html", themes=themes)