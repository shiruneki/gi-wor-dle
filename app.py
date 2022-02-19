import json
from utils import *
from flask import Flask, request, render_template, make_response, url_for, redirect
from datetime import datetime, timedelta, date
import requests
import os

app = Flask(__name__)

GIWORDLE_KEY = os.environ['GIWORDLE_KEY']

def getCookieData():
    prefix = ""
    try:
        secret = request.cookies.get(prefix+'secret')
        attempts = int(request.cookies.get(prefix+'attempts'))
        previousGuesses = request.cookies.get(prefix+'game_record')
        previousGuesses = json.loads(previousGuesses)
        gameOver = 1 if len(previousGuesses) > 0 and previousGuesses[-1]["name"] == 1 else 2 if attempts <= 0 else 0
    except:
        previousGuesses = []
        gameOver = 0
        attempts = 5

    return previousGuesses, gameOver, secret, attempts

@app.route("/")
def index():
    if 'clear' in request.args or not 'secret' in request.cookies:
        album = int(request.args['album'])
        resp = make_response(redirect(url_for('index')))
        resp.set_cookie('game_record', "[]")
        resp.set_cookie('secret', getSong(album=album))
        resp.set_cookie('attempts', '5')
        resp.set_cookie('total_attempts', '5')
        return resp

    previousGuesses, gameOver, secret, attempts = getCookieData()
    mosaic = "\n".join([x['emoji'] for x in previousGuesses])
    return render_template("index.html", data=previousGuesses, gameOver=gameOver, gsong=getSongList(), secret=secret, error=False, mosaic=mosaic, attempts=attempts)

@app.route("/", methods=['POST'])
def guess():
    previousGuesses, gameOver, secret, attempts = getCookieData()

    if(not gameOver):
        hint = getHint(request.form['guess'], secret)
        if (hint):
            previousGuesses.append(getHint(request.form['guess'], secret))
            attempts -= 1
        else:
            mosaic = "\n".join([x['emoji'] for x in previousGuesses])
            return render_template('index.html', data=previousGuesses, gameOver=gameOver, gsong=getSongList(), secret=secret, error=True, mosaic=mosaic, attempts=attempts)

        gameOver = 1 if previousGuesses[-1]["name"] == 1 else 2 if attempts <= 0 else 0
        if(gameOver):
            handleGameOver(previousGuesses, gameOver, secret, attempts, False)

    total_attempts = request.cookies.get('total_attempts')
    guesses = len(previousGuesses) if gameOver == 1 else 'X'
    mosaic = f"(G)I-DLE song {guesses}/{total_attempts}\\n\\n" +"\\n".join([x['emoji'] for x in previousGuesses])
    resp = make_response(render_template('index.html', data=previousGuesses, gameOver=gameOver, gsong=getSongList(), secret=secret, error=False, mosaic=mosaic, attempts=attempts))
    resp.set_cookie('game_record', json.dumps(previousGuesses))
    resp.set_cookie('attempts', str(attempts))

    return resp

if __name__ == "__main__":
    app.run(debug=True, use_reloader=True)
