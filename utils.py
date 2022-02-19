import numpy as np
from datetime import datetime, timedelta

def readGidle():
    dex = np.recfromcsv("gidle.csv", encoding="utf-8")
    return dex

def getSong():
    today = str(datetime.date(datetime.now()-timedelta(hours=10)))
    dex = np.recfromcsv("daily.csv", encoding="utf-8")
    row = dex[dex['date'] == today]
    secret = row['gsong'][0]
    return secret

def getSongList():
    return list(readGidle().name)

def getDay(pkmn):
    dex = np.recfromcsv("daily.csv", encoding="utf-8")
    return list(dex['gsong']).index(pkmn)
    
def getSongInfo(gsong):
    dex = readGidle()
    return dex[dex['name']==gsong][0]

def getHint(guess_str, secret_str):
    try:
        guess = getSongInfo(guess_str)
        secret = getSongInfo(secret_str)
        hint = dict()
        hint['Name'] = '🟩' if guess["album"] == secret["album"] else '🟥'
        hint['Album'] = '🟩' if guess["album"] == secret["album"] else '🟥'
        hint['Release year'] = '🟩' if guess["year"] == secret["year"] else '🔼' if guess["year"] < secret["year"] else '🔽'
        hint['Song length'] = '🟩' if guess["song_length"] == secret["song_length"] else '🔼' if guess["song_length"] < secret["song_length"] else '🔽'
        hint['emoji'] = getHintMoji(hint)
        hint['name'] = 1 if guess_str == secret_str else 5
        hint['Guess'] = guess_str
        hint['songinfo'] = formatInfo(guess)
        return hint
    except:
        return False

def getHintMoji(hint):
    return "".join([val for x,val in hint.items()])

def formatInfo(gsong):
    txt = f"<b>Album:</b> {gsong['album']}<br>"
    txt += f"<b>Release year:</b> {gsong['year']}<br>"
    txt += f"<b>Song length:</b> {gsong['song_length']}<br>"
    return txt
