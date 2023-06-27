import os
import requests

# Load client ID and secret as environmental variables
client_id = os.environ.get("TWITCH_CLIENT_ID")
client_secret = os.environ.get("TWITCH_CLIENT_SECRET")


# Base URL for all top games
top_games_url = "https://api.twitch.tv/helix/games/top"


def get_access_token():
    "get_access_token returnerer et access_token, som vi skal bruge til Twitch API"

    access_token = os.environ.get("TWITCH_ACCESS_TOKEN")
    if access_token:
        return access_token

    # Generate access token
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


def validate_auth(access_token):
    "validate_auth tjekker om access token er valid, ellers får vi en ny i get_access_token"
