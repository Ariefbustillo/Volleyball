from flask import Flask, render_template, request, redirect, url_for, session
from os import path, walk
import os
from functools import wraps
import sqlite3
from sqlite3 import Error

from arief import *

extra_dirs = [
    "./static",
]
extra_files = extra_dirs[:]
for extra_dir in extra_dirs:
    for dirname, dirs, files in walk(extra_dir):
        for filename in files:
            filename = path.join(dirname, filename)
            if path.isfile(filename):
                extra_files.append(filename)


app = Flask(__name__)
app.debug = True

# Secret key for sessions
app.secret_key = os.getenv("SECRET_KEY")

# ensures user is logged in, wrapper
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session["logged_in"]:
            return redirect(url_for("index"))
        return f(*args, **kwargs)

    return decorated_function


# main page
@app.route("/")
def index():
    if "logged_in" not in session:
        session["logged_in"] = False
        session["user_id"] = None
        session["teams"] = []
    if not session["logged_in"]:
        return render_template("login.html")
    db = create_connection()
    session["teams"] = get_teams(db, session["user_id"])
    return render_template("index.html", teams=session["teams"])


# log out button
@app.route("/logout")
def logout():
    session["logged_in"] = False
    return render_template("logged_out.html")


# create account button
@app.route("/signup")
def signup():
    return render_template("create_account.html")


# Goes to team page, from index
@app.route("/team_rotations", methods=["post"])
def team_rotations():
    team = request.form.get("team_name")
    db = create_connection()
    players = get_players(db, team)
    print("PLAYERS", players)

    return render_template("team_rotations.html", players=players, team=team)


# Create team button
@app.route("/create_team")
@login_required
def create_team():

    return render_template("create_team.html")


# Adds team to database, back to home page
@app.route("/new_team", methods=["post"])
def new_team():
    team_name = request.form.get("team_name")
    db = create_connection()
    with db:
        insert_team(db, session["user_id"], team_name)
    return redirect(url_for("index"))


# Create player button
@app.route("/create_player", methods=["post"])
@login_required
def create_player():
    team_name = request.form.get("team_name")
    return render_template("create_player.html", team_name=team_name)


# Adds player to databse, return to team page
@app.route("/new_player", methods=["post"])
def new_player():
    name = request.form.get("name")
    position = request.form.get("position")
    team = request.form.get("team_name")
    db = create_connection()
    with db:
        insert_player(db, team, name, position)
    db = create_connection()
    players = get_players(db, team)
    return render_template("team_rotations.html", players=players, team=team)


# Get player info from database, to player info page
@app.route("/player_info", methods=["post"])
@login_required
def player_info():
    name = request.form.get("name")
    team = request.form.get("team")
    player_id = request.form.get("player_id")
    db = create_connection()
    player_info = get_player_info(db, player_id)

    return render_template(
        "player_info.html",
        name=name,
        team=team,
        position=player_info.position,
        player_id=player_id,
    )


# Removes player from database, back to home page
@app.route("/remove_player", methods=["post"])
def remove_player():
    player_id = int(request.form.get("player_id"))
    db = create_connection()
    with db:
        delete_player(db, player_id)
    return redirect(url_for("index"))


# Creates new account
@app.route("/create_account", methods=["post"])
def create_account():
    db = create_connection()
    username = request.form.get("username")
    password = request.form.get("password")
    with db:
        user = (username, password)
        insert_user(db, user)
    return render_template("login.html")


# Login authentification
@app.route("/login", methods=["POST", "GET"])
def login():
    # session["username"] = request.form.get("username")
    user_name = request.form.get("username")
    password = request.form.get("password")
    db = create_connection()
    users = get_users(db)

    # Checks for inputted info in database
    if search_usernames(users, user_name) != False:
        if users[(search_usernames(users, user_name) - 1)][2] == password:

            session["logged_in"] = True
            session["user_id"] = users[(search_usernames(users, user_name) - 1)][0]
            session["username"] = user_name
            return redirect(url_for("index"))
        else:
            return render_template("failed_login.html")
    else:
        return render_template("failed_login.html")


if __name__ == "__main__":
    app.run(extra_files=extra_files)
