import os
import requests
import datetime
import time 

'''
Twitch.py encloses all methods to extract data from
the Twitch API pertaining to viewers per game and
viewers per game per country.

'''

# Load client ID and secret as environmental variables
client_id = os.environ.get("TWITCH_CLIENT_ID")
client_secret = os.environ.get("TWITCH_CLIENT_SECRET")


# Base URL for all requests
top_games_url = "https://api.twitch.tv/helix/games/top"
top_streams_url = "https://api.twitch.tv/helix/streams"


def get_access_token():

    '''
    get_access_token() returns a valid access token used
    to make HTTP requests to the Twitch API. 

    '''

    access_token = os.environ.get("TWITCH_ACCESS_TOKEN")
    valid_access_token = validate_access_token(access_token)
    if valid_access_token:
        return access_token
    return generate_access_token()

def generate_access_token():

    '''
    generate_access_token() generates a valid access token
    
    '''

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
    return os.environ.get("TWITCH_ACCESS_TOKEN")

def get_headers():

    '''
    get_headers() returns the access token and client ID
    used in the get HTTP requests for Twitch's API.
    
    '''

    headers = {
        "Authorization" : f"Bearer {get_access_token()}",
        "Client-ID" : client_id
    }

    return headers


def validate_access_token(access_token):

    '''
    validate_access_token() checks if the current acess token is valid. 
    If not generate_access_token() generates a new one. 

    Parameters
    ----------
    access_token : Str 
        Access token to validate
    
    '''

    # Validation URL and header
    validate_url = 'https://id.twitch.tv/oauth2/validate'
    validate_header = {"Authorization": f"OAuth {access_token}"
                    }
    
    try:
        validate_response = requests.get(url=validate_url, headers=validate_header)
        validate_response_json = validate_response.json()
        return validate_response.status_code == requests.codes.ok and validate_response_json['client_id'] == client_id # Succesful response => .status_code = 200. requests.codes.ok == 200
    except:
        return False
    
    

def non_games(non_game_names):

    '''
    non_games returns a dictionary of the name and ID
    of non-games such that I can remove them from 
    the get top_ggames request.

    Parameters
    ----------
    non_game_names : List 
        List of non-game names (strings)
    
    '''
    
    # Get top games name and id
    game_name, id = top_games()

    # Initiate empty list for ID of non-games
    id_non_games = []
    for name in non_game_names:
        id_non_game = id[game_name.index(name)]
        id_non_games.append(id_non_game)

    # Lists to dictionary
    dict = {}
    for name, id in zip(non_game_names, id_non_games):
        dict[name] = id
    
    return dict

    
def top_games(params = {'first' : 100}):

    '''
    top_games() returns two lists of the (default) 700 most popular 
    games as measured by number of viewers. The first list returns
    the name of the game while the second returns the game ID. 

    Parameters
    ----------
    params : Dictionary
        Specified paramters for the get HTTP request.
        Only the first parameter (# of hits per page)
        is required. I set it to 100 which is the max
        per page
    
    '''

    # Get request and parse from json to dictionary
    games_response = requests.get(url = top_games_url, params = params, headers = get_headers())
    games_response_json = games_response.json()
    

    # Lists of name and ID of games 
    game_name = [game["name"] for game in games_response_json["data"]]
    game_id = [game["id"] for game in games_response_json["data"]]

    # Get request for the following 6 pages 
    count = 0
    while bool(games_response_json["pagination"]) and count < 6:
        new_params = {'first' : 100, 'after' : games_response_json["pagination"]["cursor"]}
        games_response = requests.get(url = top_games_url, params = new_params, headers = get_headers())
        games_response_json = games_response.json()

        game_name_temp = [game["name"] for game in games_response_json["data"]]
        game_id_temp = [game["id"] for game in games_response_json["data"]]

        game_name.extend(game_name_temp)
        game_id.extend(game_id_temp)

        count += 1

    # Use the line below to get a list of game name and ID to filter out non-games
    # Make sure to return it in the bottom of the function
    # games = [(game["name"], game["id"]) for game in games_response_json["data"]]

    # Non-games to drop
    non_games_name = ["Just Chatting", "Sports", "Casino Slot Machine", "Talk Shows & Podcasts",
                      "Travel & Outdoors", "Music", "Art", "Slots", "ASMR", "Magic: The Gathering", 
                      "Chess", "Virtual Casino", "Poker", "Retro", "Politics", "I'm Only Sleeping",
                      "Crypto", "Software and Game Development", "Pools, Hot Tubs, and Beaches",
                      "Board Games", "Dating Simulator", "Games + Demos", "VRChat", "PowerWash Simulator",
                      "Marbles on Stream", "Dungeons & Dragons", "Animals, Aquariums, and Zoos", "UNO",
                      "Special Events", 'Food & Drink', 'Watch Parties', 'Always On', 'Live', 'Twitch Plays',
                      'The Casino: Roulette, Video Poker, Slot Machines, Craps, Baccarat', 'Casino Jackpot']
    non_games_id = ["509658", "518203", "1767487238", "417752", "509672", "26936", "509660", "498566", 
                    "509659", "2748", "743", "29452", "488190", "27284", "515214", "498592", "499634",
                    "1469308723", "116747788", "490413", "203542608", "66082", "499003",
                    "519103", "509511", "509577", "272263131", "11103", "509663", '509667', '515467', '499973',
                    '508402', '491180', '1967463137', '599619814']

    # Drop non-games 
    for name, id in zip(non_games_name, non_games_id):
        if name in game_name:
            game_name.remove(name)
            game_id.remove(id)

    return game_name, game_id

def top_games_old(params = {'first' : 100}):

    '''
    top_games() returns two lists of the (default) 50 most popular 
    games as measured by number of viewers. The first list returns
    the name of the game while the second returns the game ID. 

    Parameters
    ----------
    params : Dictionary
        Specified paramters for the get HTTP request.
        Only the first parameter (# of hits per page)
        is required. I set it to 70 to still have 50
        games after filtering out non-games.
    
    '''

    # Get request and parse from json to dictionary
    games_response = requests.get(url = top_games_url, params = params, headers = get_headers())
    games_response_json = games_response.json()
    

    # Lists of name and ID of games 
    game_name = [game["name"] for game in games_response_json["data"]]
    game_id = [game["id"] for game in games_response_json["data"]]

    # Use the line below to get a list of game name and ID to filter out non-games
    # Make sure to return it in the bottom of the function
    # games = [(game["name"], game["id"]) for game in games_response_json["data"]]

    # Non-games to drop
    non_games_name = ["Just Chatting", "Sports", "Casino Slot Machine", "Talk Shows & Podcasts",
                      "Travel & Outdoors", "Music", "Art", "Slots", "ASMR", "Magic: The Gathering", 
                      "Chess", "Virtual Casino", "Poker", "Retro", "Politics", "I'm Only Sleeping",
                      "Crypto", "Software and Game Development", "Pools, Hot Tubs, and Beaches",
                      "Board Games", "Dating Simulator", "Games + Demos", "VRChat", "PowerWash Simulator",
                      "Marbles on Stream", "Dungeons & Dragons", "Animals, Aquariums, and Zoos", "UNO",
                      "Special Events"]
    non_games_id = ["509658", "518203", "1767487238", "417752", "509672", "26936", "509660", "498566", 
                    "509659", "2748", "743", "29452", "488190", "27284", "515214", "498592", "499634",
                    "1469308723", "116747788", "490413", "203542608", "66082", "499003",
                    "519103", "509511", "509577", "272263131", "11103", "509663"]

    for name, id in zip(non_games_name, non_games_id):
        if name in game_name:
            game_name.remove(name)
            game_id.remove(id)

    # Return 50 most popular games 
    return game_name[:50], game_id[:50]


def get_streams(params = {'first' : 100}):

    '''
    get_streams() returns a dictionary of one page of
    response bodies of various streams. The number
    of streams, the chosen game, and the page number
    is determined by the parameters.

    Parameters
    ----------
    params : Dictionary
        Specified paramters for the get HTTP request. 
        The parameters are elaborated on below. 

        game_id : Str / Int
            Filters the get request to only the specified
            games. In my setup, I go one game at a time.

        first : Str
            Sets the amounts of hits per page. 100 is maximum

        after : Str
            Returns the next page of hits. This is left blank
            in the first run (first page)
    
    '''

    # Get HTTP request to get streams and parse from json to dictionary
    time.sleep(0.01)
    streams_response = requests.get(url = top_streams_url, params = params, headers = get_headers())
    while streams_response.status_code != requests.codes.ok:
        print("Fejl i get request. Fik response:" f'{streams_response}. Vi prøver igen')
        streams_response = requests.get(url = top_streams_url, params = params, headers = get_headers())

    streams_response_json = streams_response.json()

    return streams_response_json


def update_params(stream_response, game_id):

    '''
    update_params() updates the params variable used
    in the get_streams() method such that when called
    get_streams() returns the next page of streams

    Parameters
    ----------
    stream_response : Dictionary
        Output from get_streams() method. Using f-
        formatting the parameters are then updated

    game_id : Str / Int
        Filters the parameters to only pertain to
        the specified game

    '''

    # Params variable for subsequent stream requests
    params = {'game_id' : f'{game_id}', 'first' : 100, 'after' : f'{stream_response["pagination"]["cursor"]}'}

    return params


def loop_through_pages(params, game_id):

    '''
    loop_through_pages() loops through all
    pages of the HTTP get request and returns
    all response bodies in a list

    Parameters
    ----------
    params : Dictionary
        Specified paramters for the get HTTP request. 
        The parameters are elaborated on below. 

        game_id : Str / Int
            Filters the get request to only the specified
            games. In my setup, I go one game at a time.

        first : Str
            Sets the amounts of hits per page. 100 is maximum

        after : Str
            Returns the next page of hits. DO NOT SPECIFY IT!
            The reason being that we specify the first run in
            the params variable. The next pages are generated
            using the update_params() method which generates
            the params variable with the after parameter 
            itself. 
        
    game_id : Str / Int
        Filters the parameters to only pertain to
        the specified game
    
    '''

    # Initialize holder as well as first page of stream response bodies
    result = []
    stream_response = get_streams(params)
    try:
        result.extend(stream_response["data"])
    except: 
        print(stream_response)


    # While there are new pages we keep requesting them and adding them to the holder
    while bool(stream_response["pagination"]): # Dict evaluates to True as long as there is another page 
        new_params = update_params(stream_response, game_id)
        stream_response = get_streams(new_params)
        try:
            result.extend(stream_response["data"]) 
        except:
            print(stream_response)
              

    return result


def viewers_per_game(params, game_id):

    '''
    viewers_per_game() returns a list of live viewers
    for the specified game as well as a dictionary of
    the number of viewers from each of the 10 most
    popular countries

    Parameters
    ----------
    params : Dictionary
        Specified paramters for the get HTTP request. 
        The parameters are elaborated on below. 

        game_id : Str / Int
            Filters the get request to only the specified
            games. In my setup, I go one game at a time.

        first : Str
            Sets the amounts of hits per page. 100 is maximum

        after : Str
            Returns the next page of hits. DO NOT SPECIFY IT!
            The reason being that we specify the first run in
            the params variable. The next pages are generated
            using the update_params() method which generates
            the params variable with the after parameter 
            itself. 
    
    game_id : Str / Int
        Filters the parameters to only pertain to
        the specified game

    '''

    # Loop through pages pertaining to the specifc game and sum viewers
    stream_response = loop_through_pages(params, game_id)
    viewers_per_game = [game["viewer_count"] for game in stream_response]

    # Filter our big streamers if they have at least 1.000 viewers and
    # one of the following three 1) more than 70% of all viewers for 
    # the specific game, 2) more than 10 times as many viewers as the
    # second largest streamer or 3) the three biggest streamers 
    # account for more than 95% of all viewers (multiple big streamers)
    big = True
    if len(viewers_per_game) >= 3:
        while big == True:
            if viewers_per_game[0] >= 250 and len(viewers_per_game) >= 3 and (viewers_per_game[0] >= 0.7 * sum(viewers_per_game) or 
                                    viewers_per_game[0] > 10 * viewers_per_game[1] or sum(viewers_per_game[:3]) >= 0.95 * sum(viewers_per_game)):
                stream_response.pop(0)
            big = False

    # Recreate viewers per game post filtering 
    viewers_per_game = [game["viewer_count"] for game in stream_response]


    # 10 most popular languages on twitch
    top10_lang = ["en", "es", "ko", "fr", "zh", "ru", "de", "it", "pt", "ja"]

    # Viewers pertaining to each of the 10 most popular countries
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


def loop_through_games():

    '''
    loop_through_games() returns two dictionaries. The 
    first dictionary encloses the viewer number of the first
    X most popular games as specified by top_games() method.
    The second dictionary partitions the total number of 
    viewers by language. 

    '''

    game_name, game_id = top_games() # params = {"first" : 10}
    viewers = dict.fromkeys(game_name)
    country_viewers = dict.fromkeys(game_name)

    for name, id in zip(game_name, game_id):

        viewers_temp, country_viewers_temp = viewers_per_game(params = {'game_id' : f'{id}', 'first' : 100}, game_id = id)
        viewers[name] = viewers_temp
        country_viewers[name] = country_viewers_temp

    # Timestamp of data
    dt_long = datetime.datetime.now()
    dt = datetime.datetime(dt_long.year,dt_long.month,dt_long.day,dt_long.hour)

    return dt, viewers, country_viewers
