from flask import Flask, request, jsonify
from flask_cors import CORS
import yahoo_fantasy_api as yfa
from yahoo_oauth import OAuth2
import sqlite3
import pandas as pd
import numpy as np
import re


#Connect to sqlite table
connection = sqlite3.connect("player_stats_2024.db")
c = connection.cursor()

c.execute("""SELECT p.NAME, p.TEAM, p.POSITION, p.PASSING_YARDS, p.PASSING_TOUCHDOWNS, r.RUSHING_YARDS, r.RUSHING_TOUCHDOWNS, rc.RECEIVING_YARDS, rc.RECEIVING_TOUCHDOWNS 
          FROM passing p 
          LEFT JOIN rushing r ON p.NAME = r.NAME 
          LEFT JOIN receiving rc ON p.NAME = rc.NAME
          """)
rows = c.fetchall()

# c.execute("SELECT id, NAME, TEAM, POSITION FROM rushing WHERE rushing.POSITION = 'QB'")
# rows = c.fetchall()

#count = 0
# print("Players:\n")
players = []
for row in rows:
    data = [row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8]]
    players.append(data)
    #count += 1
    #print(count)
    #print(f"Player ID: {row[0]}, Name: {row[1]}, Team: {row[2]}, Position: {row[3]}, Passing Yards: {row[4]}, Passing Touchdowns: {row[5]}, Rushing Yards: {row[6]}, Rushing Touchdowns: {row[7]}, Receiving Yards: {row[8]}, Receicing Touchdowns: {row[9]}")

df = pd.DataFrame(players)
df = df.fillna(0)
# for i in range(100):
#     for j in range(8):
#         if isinstance(df.iloc[i, j], np.floating):
#             df.iloc[i, j] = np.int64(np.round(df.iloc[i, j]))
#             print(type(df.iloc[i, j]))

print(df)

# print("Players:\n")
# for row in rows:
#     print(f"Player ID: {row[0]}, Name: {row[1]}, Team: {row[2]}, Position: {row[3]}")


# app = Flask(__name__)
# CORS(app)

# client_id = 'dj0yJmk9SzgxeHBIOW4xc2NXJmQ9WVdrOVpVUnhhRXAzUW04bWNHbzlNQT09JnM9Y29uc3VtZXJzZWNyZXQmc3Y9MCZ4PTMw'
# client_secret = 'b5513f001693afa6d7330adb782feb37062ac03e'
# base_url = 'https://api.login.yahoo.com/'
# redirect_uri = "https://c6cd0594e04f.ngrok-free.app"

# #Authentication
# oauth = OAuth2(None, None, from_file="oauth2.json")

# gm = yfa.Game(oauth, "nfl")

# league = gm.to_league("461.l.341550")

# teams = league.teams()

# userTeamId = league.team_key()

# userNickname = teams[userTeamId]['managers'][0]['manager']['nickname']

# roster = league.to_team(userTeamId).roster()

# print(league.player_stats('33389', season=2025))

# for i in range(len(roster)):
#     print(roster[i])

# @app.route("/")
# def userName():
#     return userNickname

# def projectedPoints():
#     return

# def currentPoints():
#     return



# if __name__ == "__main__":
#     app.run(host="0.0.0.0", port=5000)


#Prints the name of team
#print(teams['461.l.341550.t.1']['name'])

#Prints the nickname of the user
#print(teams[userTeamId]['managers'][0]['manager']['nickname'])

#Prints the team key before printing the list of players
# for i in teams.keys():
#     roster = league.to_team(teams[i]['team_key']).roster()
#     teamName = teams[i]['name']
#     print("\n" + teamName + ":")
#     for j in range(len(roster)):
#         print(roster[j]['name'])

#roster = league.to_team("461.l.341550.t.1").roster()

#Prints the roster of a team
#for i in range(len(roster)):
#    print(roster[i]['name'])
