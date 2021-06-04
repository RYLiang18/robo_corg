from flask import Flask, request
import requests
import json
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get("messenger_key_1")

@app.route('/', methods=["GET", "POST"])
def home():
    return 'HOME'

@app.route('/webhook', methods=["GET", "POST"])
def index():
    # >>> authentication stuff >>>
    VERIFY_TOKEN = os.environ.get("messenger_verify_token")

    if 'hub.mode' in request.args:
        mode = request.args.get('hub.mode')
        print(mode)
    if 'hub.verify_token' in request.args:
        token = request.args.get('hub.verify_token')
        print(token)
    if 'hub.challenge' in request.args:
        challenge = request.args.get('hub.challenge')
        print(challenge)


    if 'hub.mode' in request.args and 'hub.verify_token' in request.args:
        mode = request.args.get('hub.mode')
        token = request.args.get('hub.verify_token')

        if mode == 'subscribe' and token == VERIFY_TOKEN:
            print('WEBHOOK VERIFIED')
            challenge = request.args.get('hub.challenge')
            return challenge, 200
        else:
            return 'ERROR', 403
    # <<<<<<<<<<<<<<<<<<<<<<<<<<<<<

    # TODO

if __name__ == '__main__':
    app.run(host='localhost', port='8888', debug=True)