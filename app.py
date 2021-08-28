import sqlite3
from sqlite3.dbapi2 import Timestamp
from flask import Flask, flash, redirect, render_template, request, session, jsonify
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash
from datetime import datetime
from flask_mail import Mail, Message
from helper import dict_factory, login_required
import os
from dotenv import load_dotenv
load_dotenv()

# My app
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Configure emails
app.config["MAIL_DEFAULT_SENDER"] = os.getenv("MAIL_DEFAULT_SENDER")
app.config["MAIL_PASSWORD"] = os.getenv("MAIL_PASSWORD")
app.config["MAIL_USERNAME"] = os.getenv("MAIL_USERNAME")
app.config["MAIL_PORT"] = 587
app.config["MAIL_SERVER"] = "smtp.gmail.com"
app.config["MAIL_USE_TLS"] = True
mail = Mail(app)

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

@app.route("/logout")
def logout():
    """Log user out"""
    con = sqlite3.connect("volunteer.db")
    con.row_factory = dict_factory
    db = con.cursor()

    user = db.execute("SELECT username FROM users WHERE id=?", [session["user_id"]]).fetchall()

    con.commit()
    con.close()
    # Forget any user_id
    session.clear()

    # Flash message for logout
    flash("You have been logged out, " + user[0]['username'], "success")

    # Redirect user to login form
    return redirect("/")

@app.route("/contact", methods=["GET", "POST"])
def contact():
    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        
        full_name = request.form.get("full_name")
        email = request.form.get("email")
        subject = request.form.get("subject")
        message = request.form.get("message")

        msg = Message(subject, recipients=[os.getenv("MAIL_HOME")])
        msg.html = f"<p><b>{full_name} - {email} sent you this message.</b></p> <p>{message}</p>"
        mail.send(msg)

        flash("Successfully sent Message. We will get back to you as soon as possible", "success")
        return redirect("/contact")


    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("contact.html")
        
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
        flash("Service Successfully Made!", "success")
        return redirect ("/services")
 
    # User reached route via GET (as by clicking a link or via redirect)
    else:
        themes = [
            "Celebration",
            "Foodie",
            "Education"
        ]
        return render_template("create_service.html", themes=themes)

@app.route("/availability", methods= ["POST"])
@login_required
def availability():

    spots = request.get_json()[0]['spots']
    sev_id = request.get_json()[0]['server_id']

    con = sqlite3.connect("volunteer.db")
    con.row_factory = dict_factory
    db = con.cursor()

    volunteer = db.execute("SELECT services_id FROM volunteers WHERE user_id = ? AND services_id=?", (session["user_id"], sev_id)).fetchall()

    if len(volunteer) != 0:
        con.close()
        flash("Already Signed Up for that Service", "danger")
        results = {'processed': 'false'}
        return jsonify(results)

    if spots < 0:
        con.close()
        flash("No more available spots for this service", "danger")
        results = {'processed': 'false'}
        return jsonify(results)

    user_username = db.execute("SELECT username FROM users WHERE id =?", [session["user_id"]]).fetchall()
    user_email = db.execute("SELECT email FROM users WHERE id =?", [session["user_id"]]).fetchall()
    service_title = db.execute("SELECT title FROM services WHERE id=?", (sev_id)).fetchall()
    service_date = db.execute("SELECT date FROM services WHERE id=?", (sev_id)).fetchall()
    service_start = db.execute("SELECT start_time FROM services WHERE id=?", (sev_id)).fetchall()
    service_end = db.execute("SELECT end_time FROM services WHERE id=?", (sev_id)).fetchall()
    service_location = db.execute("SELECT location FROM services WHERE id=?", (sev_id)).fetchall()
        
    u_name = user_username[0]["username"]
    u_email =  user_email[0]["email"]
    sev_title = service_title[0]["title"]
    sev_date = service_date[0]["date"]
    sev_start = service_start[0]["start_time"]
    sev_end = service_end[0]["end_time"]
    sev_location = service_location[0]["location"]

    try:
        db.execute("INSERT INTO volunteers (services_id, user_id, volunteer_username, volunteer_email, title, date, start_time, end_time, location) VALUES(?, ?, ?, ?, ?, ?, ?, ?, ? )",
                    (sev_id, session["user_id"], u_name, u_email, sev_title, sev_date, sev_start, sev_end, sev_location))
        db.execute("UPDATE services SET available=? WHERE id=?", (spots, sev_id))
        results = {'processed': 'true'}
        flash("Signed up Successfull!", "success")
    except:
        flash("Something went wrong", "danger")
        results = {'processed': 'false'}
        
    con.commit()
    con.close()

    return jsonify(results)

@app.route("/service_management", methods = ["GET"])
@login_required
def service_management():

    con = sqlite3.connect("volunteer.db")
    con.row_factory = dict_factory
    db = con.cursor()

    services_created = db.execute("SELECT id, title, date, start_time, end_time, location, total_volunteer, available FROM services WHERE user_id = ?", [session["user_id"]]).fetchall()
    volunteer = db.execute("SELECT services_id, volunteer_username, volunteer_email FROM volunteers WHERE user_id = ?", [session["user_id"]]).fetchall()

    con.commit()
    con.close()

    return render_template("service_management.html", services_created = services_created, volunteers = volunteer)


@app.route("/service_joined", methods=["GET", "POST"])
@login_required
def service_joined():

    # if you receive a post request
    if request.method == "POST":
        
        service_id = request.get_json()[0]['service_id']
        user_id = request.get_json()[0]['user_id']

        con = sqlite3.connect("volunteer.db")
        con.row_factory = dict_factory
        db = con.cursor()

        # Delete the service from from volunteer
        try:
            db.execute("DELETE FROM volunteers WHERE services_id = ? AND user_id = ?", (service_id, user_id))
            results = {'processed': 'true'}
            db.execute("UPDATE services SET available = available+1 WHERE id =?", (service_id))
            flash("Successfully Removed!", "success")
        except:
            flash("Something went wrong", "danger")
            results = {'processed': 'false'}
        
        con.commit()
        con.close()

        return jsonify(results)

    # if you receive a get request
    else: 
        con = sqlite3.connect("volunteer.db")
        con.row_factory = dict_factory
        db = con.cursor()

        joined = db.execute("SELECT services_id, user_id, title, date, start_time, end_time, location from volunteers WHERE user_id =?", [session["user_id"]]).fetchall()
    
        con.commit()
        con.close()

        return render_template("services_joined.html", joined = joined)
