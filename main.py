import re
import base64
from flask import Flask, request, redirect
import requests

app = Flask(__name__)

client_id = 'dj0yJmk9SzgxeHBIOW4xc2NXJmQ9WVdrOVpVUnhhRXAzUW04bWNHbzlNQT09JnM9Y29uc3VtZXJzZWNyZXQmc3Y9MCZ4PTMw'
client_secret = 'b5513f001693afa6d7330adb782feb37062ac03e'
base_url = 'https://api.login.yahoo.com/'
redirect_uri = "https://c6cd0594e04f.ngrok-free.app"
