import sqlite3
from sqlite3.dbapi2 import Timestamp
from flask import Flask, flash, redirect, render_template, request, session, jsonify
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash
from datetime import datetime

from helper import dict_factory, login_required
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

        con = sqlite3.connect("volunteer.db")
        con.row_factory = dict_factory
        db = con.cursor()

        rows1 = db.execute("SELECT username FROM users WHERE id=?", [session["user_id"]]).fetchall()

        # Redirect user to home page
        flash("Login Successfully! Welcome " + rows1[0]['username'], "info")
        
        con.commit()
        con.close()

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
@login_required
def services():

    con = sqlite3.connect("volunteer.db")
    con.row_factory = dict_factory
    db = con.cursor()

    services = db.execute("SELECT * FROM services").fetchall()
    
    con.commit()
    con.close()

    return render_template("services.html", services=services)

@app.route("/availability", methods= ["POST"])
@login_required
def availability():

    spots = request.get_json()[0]['spots']
    service_id = request.get_json()[1]['server_id']

    con = sqlite3.connect("volunteer.db")
    db = con.cursor()


    try:
        db.execute("UPDATE services SET available=? WHERE id=?", (spots, service_id))
        results = {'processed': 'true'}
    except:
        results = {'processed': 'false'}
        
    con.commit()
    con.close()
    flash("Signed up Successfull!", "info")
    return jsonify(results)


@app.route("/create_service", methods=["GET", "POST"])
@login_required
def create_service():

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        
        # ALl input datas
        event_themes = request.form.get("event-theme")
        event_title = request.form.get("event_title")
        event_date = datetime.strptime(request.form.get("event_date"), '%Y-%m-%d').strftime('%A, %m/%d/%Y')
        start_time = datetime.strptime(request.form.get("start_time"), '%H:%M').strftime('%I:%M %p')
        end_time = datetime.strptime(request.form.get("end_time"), '%H:%M').strftime('%I:%M %p')
        event_location = request.form.get("location")
        total_volunteer = request.form.get("total_volunteer")
        instructions = request.form.get("instructions")
        
        # Database Query
        con = sqlite3.connect("volunteer.db")
        con.row_factory = dict_factory
        db = con.cursor()

        user_username = db.execute("SELECT username FROM users WHERE id =?", [session["user_id"]]).fetchall()
        user_email = db.execute("SELECT email FROM users WHERE id =?", [session["user_id"]]).fetchall()
        
        u_name= user_username[0]["username"]
        u_email =  user_email[0]["email"]

        # Insert all the data from the form into services database
        db.execute("INSERT INTO services (user_id, theme, title, host_username, host_email, date, start_time, end_time, location, total_volunteer, available, instruction) VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", 
        (session['user_id'], event_themes, event_title, u_name, u_email, event_date, start_time, end_time, event_location, total_volunteer, total_volunteer, instructions))
        
        con.commit()
        con.close()
        # Redirect to services page
        return redirect ("/services")
 
    # User reached route via GET (as by clicking a link or via redirect)
    else:
        themes = [
            "Celebration",
            "Foodie",
            "Education"
        ]
        return render_template("create_service.html", themes=themes)