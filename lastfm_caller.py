# lastfm-stats
# uverma

import urllib2
import hashlib
import json
import webbrowser
import time
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

# Desktop Authorization
# http://www.last.fm/api/desktopauth#6

API_KEY = "7b870ce78aeba2a1b40449e1b5bddf98"
API_SECRET = "4578360352884baec863838a0ad2c667"
REST_URL = "http://ws.audioscrobbler.com/2.0/"
JSON_REQ = "&format=json"
API_TOKEN = ""
API_SESSION = ""
AUTH_FILENAME = 'authdata.json'


# Step 2 : fetch request token
def update_api_token():
    global API_TOKEN
    auth_token_string = "api_key"+API_KEY+"methodauth.getToken"
    request_sign = hashlib.md5(auth_token_string.encode('utf-8')).hexdigest()
    url_token = REST_URL+'?method=auth.getToken&api_key='+API_KEY+'&api_sig='+request_sign+JSON_REQ
    print "token request: "+url_token
    response = urllib2.urlopen(url_token).read()
    json_data = json.loads(response)
    API_TOKEN = json_data['token']


# Step 3 : request auth from user
def request_tokenauth_from_user():
    url_user_auth = 'http://www.last.fm/api/auth/?api_key='+API_KEY+'&token='+API_TOKEN
    print "user auth url: "+url_user_auth  # open link in browser and allow access to application
    webbrowser.open(url_user_auth, new=2, autoraise=True)  # open in a new tab (2), and raise focus
    time.sleep(10)  # wait for auth from user


# Step 4 : fetch a web service session
def update_api_session():
    global API_SESSION
    auth_token_string = "api_key"+API_KEY+"methodauth.getSessiontoken"+API_TOKEN+API_SECRET
    session_sign = hashlib.md5(auth_token_string.encode('utf-8')).hexdigest()
    url_session_auth = REST_URL+'?method=auth.getSession&api_key='+API_KEY+'&api_sig='+session_sign+'&token='+API_TOKEN+JSON_REQ
    # print auth_token_string
    # print session_sign
    print "session url: "+url_session_auth
    response = urllib2.urlopen(url_session_auth).read()
    print "session response: "+response
    json_data = json.loads(response)
    API_SESSION = json_data['session']['key']


def save_data_to_disk():
    authfile = open(AUTH_FILENAME, "w")
    auth_data_list = dict()
    auth_data_list['token'] = API_TOKEN
    auth_data_list['session'] = API_SESSION
    json.dump(auth_data_list, authfile)


# load previosly fetched auth info from disk
def load_data_from_disk():
    global API_SESSION, API_TOKEN
    authfile = open(AUTH_FILENAME, "r")
    data = json.load(authfile)
    API_SESSION = data['session']
    API_TOKEN = data['token']


# fetch new authorization token and session key, and save to disk
def get_new_auth():
    update_api_token()
    request_tokenauth_from_user()
    update_api_session()
    save_data_to_disk()


def get_recent_tracks():
    user = "uvcyclotron"
    url = REST_URL+"?method=user.getRecentTracks&api_key="+API_KEY+"&user="+user+JSON_REQ
    webbrowser.open(url, new=2)
    response = urllib2.urlopen(url).read()
    json.dump(response, open('recent_tracks_dump.json', 'w'))
    json_data = json.loads(response)
    tfile = open('recent_tracks.txt', 'w')
    track_list = json_data['recenttracks']['track']
    for item in track_list:
        text = "Artist: "+item['artist']['#text']
        text += '\n'+"Track: "+item['name']
        text += '\n'+"Album: "+item['album']['#text']
        if 'date' in item:
            text += '\n'+"Date: "+item['date']['#text']
        else:
            text += '\n'+"Now Playing !"
        text += '\n\n'
        tfile.write(text)

load_data_from_disk()
get_recent_tracks()


