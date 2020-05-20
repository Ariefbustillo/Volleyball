from flask import Flask, render_template, request, redirect, url_for, session
from os import path, walk
import os
from functools import wraps
import sqlite3
from sqlite3 import Error

from arief import *



extra_dirs = ['./static',]
extra_files = extra_dirs[:]
for extra_dir in extra_dirs:
    for dirname, dirs, files in walk(extra_dir):
        for filename in files:
            filename = path.join(dirname, filename)
            if path.isfile(filename):
                extra_files.append(filename)


app = Flask(__name__)
app.debug = True
app.secret_key = os.getenv("SECRET_KEY")


def login_required(f):
   

    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session['logged_in']:
            return redirect(url_for('index'))
        return f(*args, **kwargs)
    return decorated_function


@app.route("/")
def index():
    if 'logged_in' not in session:
        session['logged_in'] = False
        session['user_id'] = None
        session['teams'] = []
    if not session['logged_in']: 
        return render_template("login.html")
    db = create_connection()
    session['teams'] = get_teams(db, session['user_id'])
    return render_template("index.html", teams=session['teams'])


@app.route("/logout")
def logout():
    session['logged_in'] = False
    return render_template("logged_out.html")

@app.route("/signup")
def signup():
    return render_template("create_account.html")

@app.route("/team_rotations", methods=["post"])
def team_rotations():
    team = request.form.get("team_name")
    db = create_connection()
    players = get_players(db, team)
    print('PLAYERS', players)

    return render_template("team_rotations.html", players=players, team=team)

@app.route("/create_team")
@login_required
def create_team():
    
    return render_template("create_team.html")

@app.route("/new_team", methods=["post"])
def new_team():
    team_name = request.form.get("team_name")
    db = create_connection()
    with db:
        insert_team(db, session['user_id'], team_name)
    return redirect(url_for('index'))

@app.route("/create_player", methods=["post"])
@login_required
def create_player():
    team_name = request.form.get("team_name")
    return render_template("create_player.html", team_name = team_name)

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
    return render_template("team_rotations.html",players=players, team=team)

@app.route("/player_info", methods=["post"])
@login_required
def player_info():
    name = request.form.get("name")
    team = request.form.get("team")
    player_id = request.form.get("player_id")
    db = create_connection()
    player_info = get_player_info(db,player_id)

    return render_template("player_info.html", name=name, team=team, position=player_info.position, player_id=player_id)

@app.route("/remove_player", methods=["post"])
def remove_player():
    player_id = int(request.form.get("player_id"))
    db = create_connection()
    with db:
        delete_player(db, player_id)
    return redirect(url_for('index'))

@app.route("/create_account", methods=["post"])
def create_account():
    db = create_connection()
    username = request.form.get("username")
    password = request.form.get("password")
    with db:
        user = (username, password)
        insert_user(db,user)
    return (render_template("login.html"))


@app.route("/login", methods=["POST", "GET"])
def login():
    session['username'] = request.form.get("username")
    user_name = request.form.get("username")
    password = request.form.get("password")
    db = create_connection()
    users = get_users(db)

    if search_usernames(users,user_name) != False:        
        if users[(search_usernames(users,user_name) - 1)][2] == password:
            
            session['logged_in'] = True
            session['user_id'] = users[(search_usernames(users,user_name) - 1)][0]
            session['username'] = user_name
            return redirect(url_for('index'))
        else: return render_template("failed_login.html")
    else:
        return render_template("failed_login.html")


# @app.route("/rotate", methods=["POST"])
# def rotate():
#     players = [None] * 6
#     teamsheets =[]
#     players[1] = request.form.get("playerOne")
#     players[2] = request.form.get("playerTwo")
#     players[3] = request.form.get("playerThree")
#     players[4] = request.form.get("playerFour")
#     players[5] = request.form.get("playerFive")
#     players[0] = request.form.get("playerSix")


#     for i, player in enumerate(players):
#         newArr = []
#         newArr.append(players[(i + 1) % 6])
#         newArr.append(players[(i + 6) % 6]) 
#         newArr.append(players[(i + 5) % 6])
#         newArr.append(players[(i + 2) % 6])
#         newArr.append(players[(i + 3) % 6])
#         newArr.append(players[(i + 4) % 6])
#         teamsheets.append(newArr)


#     return render_template("rotations.html", teamsheets=teamsheets)

if __name__ == "__main__":
  app.run(extra_files=extra_files)