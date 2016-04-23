# lastfm-stats
# uverma
import collections
import json
import sys
import operator
import bokeh
from bokeh.charts.utils import show

reload(sys)
sys.setdefaultencoding('utf-8')


def fetch_artist_freq():
    data_file = open("recent_tracks_dump.json", "r")
    freq_file = open("artist_freq_data.json", "w")
    json_data = json.load(data_file)
    c = 0
    artist_freq = {}
    for item in json_data:
        artist = item['artist']['#text']
        if artist in artist_freq:
            # found, increment counter
            artist_freq[artist] += 1
        else:
            # not found. add to list
            artist_freq[artist] = 1
        c += 1
        if c == 30:
            break

    # print artist_freq
    # json.dump(artist_freq, freq_file)
    artist_list_sorted = sorted(artist_freq.items(), key=operator.itemgetter(1), reverse=True)
    artists_list = [str(seq[0]) for seq in artist_list_sorted]
    print artist_list_sorted
    print artists_list
    # json.dump(artist_list_sorted, freq_file)
    al = {"a": 2, "b": 5, "d": 7}
    aal = sorted(al.items(), key=operator.itemgetter(1), reverse=True)
    # [seq[0] for seq in aal]
    al = collections.OrderedDict(aal)
    bl = ["d", "b", "a"]
    # print aal
    # print al
    # vplot = bokeh.charts.Bar(artist_list_sorted, artists_list, title="Artist Frequency")
    # vplot = bokeh.charts.Bar(al, bl, title="Artist Frequency")
    # show(vplot)


def fetch_album_freq():
    data_file = open("recent_tracks_dump.json", "r")
    freq_file = open("album_freq_data.json", "w")
    json_data = json.load(data_file)
    c = 0
    album_freq = {}
    for item in json_data:
        album = item['album']['#text']
        if album in album_freq:
            # found, increment counter
            album_freq[album] += 1
        else:
            # not found. add to list
            album_freq[album] = 1
        # c += 1
        # if c == 30:
        #     break

    album_list_sorted = sorted(album_freq.items(), key=operator.itemgetter(1), reverse=True)
    json.dump(album_list_sorted, freq_file)


def fetch_track_freq():
    data_file = open("recent_tracks_dump.json", "r")
    freq_file = open("track_freq_data.json", "w")
    json_data = json.load(data_file)
    c = 0
    track_freq = {}
    for item in json_data:
        track = item['name']
        if track in track_freq:
            # found, increment counter
            track_freq[track] += 1
        else:
            # not found. add to list
            track_freq[track] = 1
        # c += 1
        # if c == 30:
        #     break

    track_list_sorted = sorted(track_freq.items(), key=operator.itemgetter(1), reverse=True)
    json.dump(track_list_sorted, freq_file)


fetch_artist_freq()