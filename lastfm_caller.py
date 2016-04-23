# lastfm-stats
# uverma

import urllib2
import hashlib
import json
import webbrowser
import time
import sys
import datetime, time

reload(sys)
sys.setdefaultencoding('utf-8')

# Desktop Authorization
# http://www.last.fm/api/desktopauth#6

API_KEY = ""
API_SECRET = ""
API_TOKEN = ""
API_SESSION = ""
REST_URL = "http://ws.audioscrobbler.com/2.0/"
JSON_REQ = "&format=json"
AUTH_FILENAME = 'authdata.json'
KEY_FILENAME = 'keydata.json'


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


def load_keys_from_disk():
    global API_KEY, API_SECRET
    keyfile = open(KEY_FILENAME, "r")
    data = json.load(keyfile)
    API_KEY = data['key']
    API_SECRET = data['secret']


# fetch new authorization token and session key, and save to disk
def get_new_auth():
    load_keys_from_disk()
    update_api_token()
    request_tokenauth_from_user()
    update_api_session()
    save_data_to_disk()


def get_ust_time(year, month, day):
    return int(time.mktime(datetime.datetime(year=year, month=month, day=day).timetuple()))


def get_recent_tracks():
    load_keys_from_disk()
    query_user = "uvcyclotron"
    query_numtracks = 200
    params = "&user=" + query_user + "&limit=" + query_numtracks.__str__()
    time_range = "&from="+get_ust_time(2015, 11, 21).__str__()+"&to="+get_ust_time(2015, 12, 1).__str__()
    url = REST_URL+"?method=user.getRecentTracks&api_key="+API_KEY+params+JSON_REQ
    webbrowser.open(url, new=2)
    response = urllib2.urlopen(url).read()
    json_data = json.loads(response)
    text_file = open('recent_tracks.txt', 'w')
    dump_file = open('recent_tracks_dump.json', 'w')
    # json.dump(response, open('recent_tracks_dump.json', 'w'))

    track_attr = json_data['recenttracks']['@attr']
    total_pages = track_attr['totalPages']
    print total_pages
    json_full_list = []
    for i in range(1, int(total_pages)):
        url_page = url+"&page="+i.__str__()
        response = urllib2.urlopen(url_page).read()
        json_data = json.loads(response)
        track_list = json_data['recenttracks']['track']
        for item in track_list:
            json_full_list.append(item)
            text = "Artist: "+item['artist']['#text']
            text += '\n'+"Track: "+item['name']
            text += '\n'+"Album: "+item['album']['#text']
            if 'date' in item:
                text += '\n'+"Date: "+item['date']['#text']
            else:
                text += '\n'+"Now Playing !"
            text += '\n\n'
            text_file.write(text)
    # write complete json dump to file
    json.dump(json_full_list, dump_file)


get_recent_tracks()






