#antal = input("Hur många tecken?")
#svårighet = input("1-5, hur svårt")

#easy[] = {a,b,c,d,e,f,g}
#medium[] = {'1','2','3','4','5'}
#hard[] = {'@','!','#','€','$','%'}

from cs50 import SQL #Ta bort
from flask import Flask, flash, jsonify, redirect, render_template, request, session
from flask_session import Session

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///passwords.db") #Ändra

passwords = {}

# Configure session
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

INVALIDCREDENTIALS = "Wrong password or username"


@app.route("/")
def index():
    name = "Oliver" # db
    if not session.get("name"):
        return redirect("/login")
    #passwords = db.execute("SELECT address, username, password FROM password JOIN user ON user.id = password.id WHERE id = id")
    return render_template("index.html", name=name)


@app.route("/login", methods = ["GET", "POST"])
def login():
    if session.get("name"):
        return redirect("/")
    if request.method == "POST":
        if request.form.get("password") == "123": #db.execute("SELECT password"):
            session["name"] = request.form.get("username") + request.form.get("password")
            return redirect("/")
        else:
            return render_template("login.html", errorText = INVALIDCREDENTIALS)
    return render_template("login.html")

@app.route("/logout")
def logout():
    session["name"] = None
    return redirect("/login")

@app.route("/register", methods = ["GET", "POST"])
def register():
    if request.method == "POST":
        if request.form.get("password") == request.form.get("password2"):
            name = request.form.get("name")
            username = request.form.get("username")
            password = request.form.get("password")
            db.execute("INSERT INTO user (name, username, password) VALUES (?, ?, ?)", name, username, password)
            session["name"] = request.form.get("username") + request.form.get("password")
            return redirect("/")
        else:
            return render_template("register.html", errorText = INVALIDCREDENTIALS)
    elif request.method == "GET":
        return render_template("register.html")
    return render_template("index.html")
