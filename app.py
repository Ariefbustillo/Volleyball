from flask import Flask, render_template, request, redirect, url_for
from os import path, walk
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


# USERS = {
#     'arief': 'password',
#     'luthfi': 'passwordBetter',
#     'murtado': 'contrasena'
# }

LOGGED_IN = False


def login_required(f):
   

    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not LOGGED_IN:
            return redirect(url_for('index'))
        return f(*args, **kwargs)
    return decorated_function


@app.route("/")
def index():
    global LOGGED_IN
    global USER_ID
    if not LOGGED_IN: 
        print(LOGGED_IN)
        return render_template("login.html")
    db = create_connection()
    teams = get_teams(db, USER_ID)
    return render_template("index.html", teams=teams)


@app.route("/logout")
def logout():
    global LOGGED_IN
    LOGGED_IN = False
    return render_template("logged_out.html")

@app.route("/signup")
def signup():
    return render_template("create_account.html")

@app.route("/team_rotations", methods=["post"])
def team_rotations():
    team = request.form.get("team_name")
    db = create_connection()
    players = get_players(db, team)
    return render_template("team_rotations.html", players=players, team=team)

@app.route("/create_team")
@login_required
def create_team():
    
    return render_template("create_team.html")

@app.route("/new_team", methods=["post"])
def new_team():
    # global USER_ID
    team_name = request.form.get("team_name")
    db = create_connection()
    with db:
        insert_team(db, USER_ID, team_name)
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
    db = create_connection()
    players_info = get_player_info(db,team)
    position = players_info[name]
    return render_template("player_info.html", name=name, team=team, position=position)



@app.route("/create_account", methods=["post"])
def create_account():
    db = create_connection()
    username = request.form.get("username")
    password = request.form.get("password")
    with db:
        user = (username, password)
        insert_user(db,user)
    # user = (username,password)
    # insert_user(db, user)
    return (render_template("login.html"))


@app.route("/login", methods=["POST", "GET"])
def login():
    user_name = request.form.get("username")
    password = request.form.get("password")
    db = create_connection()
    users = get_users(db)
    print(search_usernames(users,user_name))
    print(users[1][2])
    if search_usernames(users,user_name) != False:        
        if users[(search_usernames(users,user_name) - 1)][2] == password:
            global LOGGED_IN
            LOGGED_IN = True
            global USER_ID
            USER_ID = search_usernames(users,user_name)
            print("true")
            return redirect(url_for('index'))
        else: return render_template("failed_login.html")
    else:
        print("loser")
        return render_template("failed_login.html")

    # if username in USERS.keys() and password == USERS[username]:
    #     global LOGGED_IN
    #     LOGGED_IN = True
    #     print("Here")
    #     return redirect(url_for('index'))
    # else:
    #     return render_template("failed_login.html")

@app.route("/rotate", methods=["POST"])
def rotate():
    players = [None] * 6
    teamsheets =[]
    players[1] = request.form.get("playerOne")
    players[2] = request.form.get("playerTwo")
    players[3] = request.form.get("playerThree")
    players[4] = request.form.get("playerFour")
    players[5] = request.form.get("playerFive")
    players[0] = request.form.get("playerSix")


    for i, player in enumerate(players):
        newArr = []
        newArr.append(players[(i + 1) % 6])
        newArr.append(players[(i + 6) % 6]) 
        newArr.append(players[(i + 5) % 6])
        newArr.append(players[(i + 2) % 6])
        newArr.append(players[(i + 3) % 6])
        newArr.append(players[(i + 4) % 6])
        teamsheets.append(newArr)


    return render_template("rotations.html", teamsheets=teamsheets)

if __name__ == "__main__":
  app.run(extra_files=extra_files)