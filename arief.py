import sqlite3
from sqlite3 import Error
def create_connection():
    db = None
    try:
        db = sqlite3.connect(r"volleyball.db")
        print("connection success")
    except Error as e:
        print(e)
    return db

def create_table(connection, create_table_sql):
    cursor = connection.cursor()
    cursor.execute(create_table_sql)

def insert_user(connection, user):
    sql = """ INSERT INTO users(username,password) VALUES(?,?)"""
    cursor = connection.cursor()
    cursor.execute(sql, user)

def get_users(connection):
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM users")
    users = cursor.fetchall()
    return users

def get_usernames(connection):
    cursor = connection.cursor()
    cursor.execute("SELECT username FROM users")
    usernames = cursor.fetchall()
    username_list = []
    for username in usernames:
        username_list.append(username[0])
    return username_list

def get_teams(connection,user_id):
    cursor = connection.cursor()
    cursor.execute("SELECT team_name FROM teams WHERE id = ?", (user_id,))
    teams = cursor.fetchall()
    team_list = []
    for team in teams:
        team_list.append(team[0])
    return team_list
def get_players(connection,team_name):
    cursor = connection.cursor()
    cursor.execute("SELECT name FROM players WHERE team_name = ?", (team_name,))
    players = cursor.fetchall()
    player_list = []
    for player in players:
        player_list.append(player[0])
    return player_list

def get_player_info(connection,team_name):
    cursor = connection.cursor()
    cursor.execute("SELECT name, position FROM players WHERE team_name = ?", (team_name,))
    players = cursor.fetchall()
    player_info = {}
    for player in players:
        player_info.update({player[0]:player[1]})
    return player_info

def insert_team(connection, user_id, team_name):
    cursor = connection.cursor()
    cursor.execute("INSERT INTO teams(id,team_name) VALUES(?,?)",(user_id, team_name))

def insert_player(connection, team_name, player_name, position):
    cursor = connection.cursor()
    cursor.execute("INSERT INTO players(team_name, name, position) VALUES(?,?,?)",(team_name, player_name, position,))

def search_usernames(users, username):
    for i, user in enumerate(users):
        if user[1] == username:
            return (i + 1)
    return False
