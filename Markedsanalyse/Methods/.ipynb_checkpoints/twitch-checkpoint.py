import os
import requests
import json

# Load client ID and secret as environmental variables
client_id = os.environ.get("TWITCH_CLIENT_ID")
client_secret = os.environ.get("TWITCH_CLIENT_SECRET")


# Base URL for all top games
top_games_url = "https://api.twitch.tv/helix/games/top"
top_streams_url = "https://api.twitch.tv/helix/streams"


def get_access_token():
    # get_access_token returnerer et valid access_token, som vi skal bruge til Twitch API

    access_token = os.environ.get("TWITCH_ACCESS_TOKEN")
    valid_access_token = validate_access_token(access_token)
    if valid_access_token:
        return access_token
    return generate_access_token()

def generate_access_token():
    # generate_access_token genererer et access token, hvis det nuværende er invalid

    # Generate body for HTTP post 
    auth_body = {"client_id": client_id,
                 "client_secret": client_secret,
                 "grant_type": "client_credentials"
                 }

    auth_response = requests.post(
        url="https://id.twitch.tv/oauth2/token", json=auth_body)

    # Set up headers for future requests
    auth_response_json = auth_response.json()

    # Set Environment Variables and return token
    os.environ["TWITCH_ACCESS_TOKEN"] = auth_response_json['access_token']
    return os.environ.get("TWTICH_ACCESS_TOKEN")

def get_headers():
    # get_headers returnerer de headers vi skal bruge i get requesten for at få data ud fra twitch API

    headers = {
        "Authorization" : f"Bearer {get_access_token()}",
        "Client-ID" : client_id
    }

    return headers


def validate_access_token(access_token):
    "validate_access_token tjekker om access token er valid, ellers får vi en ny i get_access_token"

    validate_url = 'https://id.twitch.tv/oauth2/validate'
    validate_header = {"Authorization": f"OAuth {access_token}"
                       }
    
    try:
        validate_response = requests.get(url=validate_url, headers=validate_header)
        validate_response_json = validate_response.json()
        return validate_response.status_code == requests.codes.ok and validate_response_json['client_id'] == client_id # Succesful response => .status_code = 200. requests.codes.ok == 200
    except:
        return False
    
def send_twitch_request(url, body, params, method = "GET", headers = get_headers()):
    response = requests.request(method = method, url = url, body = body, headers = headers, params = params)

    return response.json()
    
def top_games(): # Jeg skal tilføje argumenter til denne, så jeg kan gøre den dynamisk, hvis jeg skal have forskellige træk

    games_response = requests.get(url = top_games_url, headers = get_headers())
    games_response_json = games_response.json()

    return games_response_json

def get_streams():
    
    streams_response = requests.get(url = top_streams_url, headers = get_headers())
    streams_response_json = streams_response.json()

    return streams_response_json


# Jeg får ikke viewer data når jeg trækker fra top_games så skal trække fra stream og så lægge sammen inden for hver kategori. Jeg har trækket vist nok inde i jupyter
# Jeg ved ikke om jeg bare kan trække samtlige streams på twtich (evt alle streams med mere end et min antal viewers). Ellers kan jeg bruge top games til at få top X antal games
# og så ud fra kun de games kan jeg få viewers. 

'''
In Helix, there doesn’t appear to be a way to easily get a games viewer count, currently you would have to page through the streams 
endpoint https://dev.twitch.tv/docs/api/reference/#get-streams 262 using the game_id param to limit it to that specific game, and sum the viewer count 
from each stream object returned.

et call med top 50 games eller lignende og så for hver af dem et kald med streamers som jeg så lægger sammen. Hvad med trendning games? -- de skal være i top 50 ellers er de ikke
spændende alligevel, så der kan jeg nok fange dem ved så bare at lave noget databehandling som viser hvis der er nogle spil som lige pludseilg kommer frem 
'''