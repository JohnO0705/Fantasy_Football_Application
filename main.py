import re
import base64
from flask import Flask, request, redirect
import requests
import yahoo_fantasy_api as yfa
from yahoo_oauth import OAuth2

app = Flask(__name__)

client_id = 'dj0yJmk9SzgxeHBIOW4xc2NXJmQ9WVdrOVpVUnhhRXAzUW04bWNHbzlNQT09JnM9Y29uc3VtZXJzZWNyZXQmc3Y9MCZ4PTMw'
client_secret = 'b5513f001693afa6d7330adb782feb37062ac03e'
base_url = 'https://api.login.yahoo.com/'
redirect_uri = "https://c6cd0594e04f.ngrok-free.app"

#Authentication
oauth = OAuth2(None, None, from_file="oauth2.json")

gm = yfa.Game(oauth, "nfl")

league = gm.to_league("461.l.341550")

teams = league.teams()

#Prints the team key
for i in teams.keys():
    roster = league.to_team(teams[i]['team_key']).roster()
    print(i)
    for j in range(len(roster)):
        print(roster[j]['name'])

#roster = league.to_team("461.l.341550.t.1").roster()

#Prints the roster of a team
#for i in range(len(roster)):
#    print(roster[i]['name'])
