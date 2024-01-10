from cs50 import SQL # To be removed
from flask import Flask, flash, jsonify, redirect, render_template, request, session
from flask_session import Session
from functools import wraps
import rsa
from werkzeug.security import check_password_hash, generate_password_hash
from cryptography.fernet import Fernet

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///passwords.db") #Ändra

# Configure session
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

#publicKey, privateKey = rsa.newkeys(2048)
#key = Fernet.generate_key()
#fernet = Fernet(key)

# Define login_required
def login_required(f):
    """
    Decorate routes to require login.

    http://flask.pocoo.org/docs/0.12/patterns/viewdecorators/
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)
    return decorated_function


@app.route("/")
@login_required
def index():
    # Get username
    name = db.execute("SELECT username FROM users WHERE id = ?",
    session["user_id"])[0]['username']
    # Get passwords
    passwords = db.execute("SELECT website, username, password FROM passwords WHERE id = ?", session["user_id"])
    if len(passwords) == 0:
        return render_template("index.html")

    return render_template("index.html", username=name, passwords=passwords)#, decrypted=decrypted) #TODO: Handle Decryption

@app.route("/create", methods = ["GET", "POST"])
@login_required
def create():
    if request.method == "GET":
        return render_template("create.html")
    else:
        # If website was not submitted
        if not request.form.get("website"):
            return render_template("create.html", errorText = "Need to enter website")
        # If username not submitted
        if not request.form.get("username"):
            return render_template("create.html", errorText = "Need to enter username")
        # If username not submitted
        elif not request.form.get("password"):
            return render_template("create.html", errorText = "Need to enter password")

        if 0 != len(db.execute("SELECT * FROM passwords WHERE website = ? AND id = ?", request.form.get("website"), session["user_id"])):
            return render_template("create.html", errorText = "Password for this website already registered")
        #TODO: Time

        # Insert new password to
        db.execute("INSERT INTO passwords (id, username, website, password)VALUES (?, ?, ?, ?)",
            session["user_id"],
            request.form.get("username"),
            request.form.get("website"),
            request.form.get("password")
            #rsa.encrypt(request.form.get("password").encode(), publicKey)
            #fernet.encrypt(request.form.get("password").encode())
            )

        return redirect("/")

@app.route("/change", methods = ["GET", "POST"])
@login_required
def change():
    if request.method == "GET":
        return redirect("/")
    else:
        # Check if value is correct
        if len(db.execute("SELECT * FROM passwords WHERE website = ? AND id = ?", request.form["change_button"], session["user_id"])) != 1:
            return redirect("/")

        return render_template("change.html", website=request.form["change_button"])

@app.route("/changed", methods = ["GET", "POST"])
@login_required
def changed():
    if request.method == "GET":
        return redirect("/")
    else:
        # If website was not submitted
        if not request.form.get("website"):
            return render_template("create.html", errorText = "Need to enter website")
        # If username not submitted
        if not request.form.get("username"):
            return render_template("create.html", errorText = "Need to enter username")
        # If username not submitted
        elif not request.form.get("password"):
            return render_template("create.html", errorText = "Need to enter password")

        # Make sure it exists
        if len(db.execute("SELECT * FROM passwords WHERE website = ? AND id = ?", request.form.get("website"), session["user_id"])) != 1:
            return render_template("create.html", errorText = "Incorrect") #TODO: Handle correct

        # Change
        db.execute("UPDATE passwords SET username = ?, password = ? WHERE website = ? AND id = ?",
                   request.form.get("username"),
                   request.form.get("password"), #TODO: Encrypt
                   #rsa.encrypt(request.form.get("password").encode(), publicKey),
                   #fernet.encrypt(request.form.get("password").encode()),
                   request.form.get("website"),
                   session['user_id'])
        return redirect("/")

#@app.route("/decrypt", methods = ["GET", "POST"])
#@login_required
#def decrypt():
    #if request.method == "GET":
        #return redirect("/")
    #else:
        #return render_template("index.html",)


@app.route("/login", methods = ["GET", "POST"])
def login():
    session.clear()

    if request.method == "GET":
        return render_template("login.html")
    else:
        # If username not submitted
        if not request.form.get("username"):
            return render_template("login.html", errorText = "Need to enter username")
        # If username not submitted
        elif not request.form.get("password"):
            return render_template("login.html", errorText = "Need to enter password")
        # Get user details
        users = db.execute(
            "SELECT * FROM users WHERE username = ?",
            request.form.get("username")
        )
        # Check if user exists and password is correct
        if len(users) != 1 or not check_password_hash(users[0]["password"], request.form.get("password")):
            return render_template("login.html", errorText="invalid username and/or password")

        # Start session for user
        session["user_id"] = users[0]["id"]

        return redirect("/")


@app.route("/logout")
def logout():
    session["user_id"] = None
    return redirect("/login")


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "GET":
        return render_template("register.html")
    else:
        # If not username is submitted
        if not request.form.get("username"):
            return render_template("register.html", errorText = "Need to enter username")

        # If not password was submitted
        elif not request.form.get("password"):
            return render_template("register.html", errorText = "Need to enter password")

        # If password was not submitted
        elif not request.form.get("password2"):
            return render_template("register.html", errorText = "Need to enter password confirmation")

        # If any credentials are too long
        elif ( len(request.form.get("password")) > 20 or len(request.form.get("username")) > 15 ):
            return render_template("register.html", errorText = "Password or Username is too long.")

        # Ensure the password and confirmation is the same
        elif request.form.get("password") != request.form.get("password2"):
            return render_template("register.html", errorText = "The passwords are not identical")

        # Ensure the username is unique
        elif (
            len(db.execute("SELECT * FROM users WHERE username = ?",
                    request.form.get("username"),)) > 0 ):
            return render_template("register.html", errorText = "Username already taken, choose another")

        # Save user to the database
        db.execute("INSERT INTO users (username, password)VALUES (?, ?)",
            request.form.get("username"),
            #hash
            #argon2.hash_password(bytes(request.form.get("password"),"utf-8")),)
            generate_password_hash(request.form.get("password")))

        # Get the users credentials
        rows = db.execute(
            "SELECT * FROM users WHERE username = ?", request.form.get("username")
        )
        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")
