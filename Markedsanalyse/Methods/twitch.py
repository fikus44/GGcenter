import os
import requests
import time

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
    

def top_games(params = {'first' : 50}):

    games_response = requests.get(url = top_games_url, params = params, headers = get_headers())
    games_response_json = games_response.json()

    game_name = [game["name"] for game in games_response_json["data"]]
    game_id = [game["id"] for game in games_response_json["data"]]

    return game_name, game_id


def get_streams(params):

    streams_response = requests.get(url = top_streams_url, params = params, headers = get_headers())
    streams_response_json = streams_response.json()

    return streams_response_json

def update_params(stream_response, game_id):

    params = {'game_id' : f'{game_id}', 'first' : 100, 'after' : f'{stream_response["pagination"]["cursor"]}'}

    return params


def loop_through_pages(params, game_id):

    result = []
    stream_response = get_streams(params)
    result.extend(stream_response["data"])

    while bool(stream_response["pagination"]): # Dict evaluates to True as long as there is another page 
        new_params = update_params(stream_response, game_id)
        stream_response = get_streams(new_params)
        result.extend(stream_response["data"])        

    return result


def viewers_per_game(params, game_id):

    stream_response = loop_through_pages(params, game_id)
    viewers_per_game = [game["viewer_count"] for game in stream_response]

    top10_lang = ["en", "es", "ko", "fr", "zh", "ru", "de", "it", "pt", "ja"]

    en_viewers_per_game = sum([game["viewer_count"] if game["language"] == 'en' else 0 for game in stream_response])
    sp_viewers_per_game = sum([game["viewer_count"] if game["language"] == 'es' else 0 for game in stream_response])
    ko_viewers_per_game = sum([game["viewer_count"] if game["language"] == 'ko' else 0 for game in stream_response])
    fr_viewers_per_game = sum([game["viewer_count"] if game["language"] == 'fr' else 0 for game in stream_response])
    ch_viewers_per_game = sum([game["viewer_count"] if game["language"] == 'zh' else 0 for game in stream_response])
    ru_viewers_per_game = sum([game["viewer_count"] if game["language"] == 'ru' else 0 for game in stream_response])
    de_viewers_per_game = sum([game["viewer_count"] if game["language"] == 'de' else 0 for game in stream_response])
    it_viewers_per_game = sum([game["viewer_count"] if game["language"] == 'it' else 0 for game in stream_response])
    pt_viewers_per_game = sum([game["viewer_count"] if game["language"] == 'pt' else 0 for game in stream_response])
    ja_viewers_per_game = sum([game["viewer_count"] if game["language"] == 'ja' else 0 for game in stream_response])
    ot_viewers_per_game = sum([game["viewer_count"] if game["language"] not in top10_lang else 0 for game in stream_response])

    country_viewers_per_game = {"en" : en_viewers_per_game, "sp" : sp_viewers_per_game, "pt" : pt_viewers_per_game, "de" : de_viewers_per_game,
                                "ru" : ru_viewers_per_game, "fr" : fr_viewers_per_game, "ko" : ko_viewers_per_game, "ja" : ja_viewers_per_game,
                                "ch" : ch_viewers_per_game, "it" : it_viewers_per_game, "ot" : ot_viewers_per_game}

    return sum(viewers_per_game), country_viewers_per_game

def country_viewers_per_game(params, game_id):

    stream_response = loop_through_pages(params, game_id)
    country_viewers_per_game = []

    return None 



'''
In Helix, there doesn’t appear to be a way to easily get a games viewer count, currently you would have to page through the streams 
endpoint https://dev.twitch.tv/docs/api/reference/#get-streams 262 using the game_id param to limit it to that specific game, and sum the viewer count 
from each stream object returned.

et call med top 50 games eller lignende og så for hver af dem et kald med streamers som jeg så lægger sammen. Hvad med trendning games? -- de skal være i top 50 ellers er de ikke
spændende alligevel, så der kan jeg nok fange dem ved så bare at lave noget databehandling som viser hvis der er nogle spil som lige pludseilg kommer frem 
'''


def send_twitch_request(url, body, params, method = "GET", headers = get_headers()):
    response = requests.request(method = method, url = url, body = body, headers = headers, params = params)

    return response.json()