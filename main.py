import re
import base64
from flask import Flask, request, redirect
import requests

app = Flask(__name__)

client_id = 'dj0yJmk9SzgxeHBIOW4xc2NXJmQ9WVdrOVpVUnhhRXAzUW04bWNHbzlNQT09JnM9Y29uc3VtZXJzZWNyZXQmc3Y9MCZ4PTMw'
client_secret = 'b5513f001693afa6d7330adb782feb37062ac03e'
base_url = 'https://api.login.yahoo.com/'
redirect_uri = "https://c6cd0594e04f.ngrok-free.app"

@app.route("/send_to_consent")
def send_to_login():
    lang = re.split('[,;/ ]+', request.accept_languages.to_header())[0]
    code_url = f'oauth2/request_auth?client_id={client_id}&redirect_uri={redirect_uri}&response_type=code&scope=openid&language={lang}'
    url = base_url + code_url
    return redirect(url,code=302)

@app.route("/dashboard")
def get_tokens():
    code = request.args.get('code')
    encoded = base64.b64encode((client_id + ':' + client_secret).encode("utf-8"))
    headers = {
        'Authorization': f'Basic {encoded.decode("utf-8")}',
        'Content-Type': 'application/x-www-form-urlencoded'
    }
    data = {
        'grant_type': 'authorization_code',
        'redirect_uri': redirect_uri,
        'code': code
    }
    global response
    response = post(base_url + 'oauth2/get_token', headers=headers, data=data)
    response.ok
    return response.json()