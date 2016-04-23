#lastFM-stats

A simple tool to connect to the last.fm server and fetch a user's play history data. 
Collected data is dumped to json files, which can be parsed to produce top N results. Further parsing and processing programs can be built to work with the data.


### One-time Auth Setup
Use the `lastfm_caller.py` to first setup authorization. 

+   Get your own API authorization keys by registering from the [last.fm API site](http://www.last.fm/api/authentication).
+   Put key and secret in `keydata.json` file using the provided template.
+   Use `update_api_token()` to get a token from the service. This uses your provided auth key.
+   Call `request_tokenauth_from_user()` right after getting the previous step to authorize this token. Opens a window in web browser for authorization from the user.
+   Call `update_api_session()` to fetch a session ID.
+   Store token and session data in `authdata.json` file using the `save_data_to_disk()`
+   You're done with the auth setup!


### Fetch data

 Use `get_recent_tracks()` to get recently played tracks by a user. Modify `query_user` and `query_numtracks` accordingly. Modify the params for the query URL as per need. Refer the online [API docs](http://www.last.fm/api/intro) for more info on how to build REST style query URLs.


### Parsing data
 
 Use `fetch_artist_freq()` to generate a frequency table of the artists from the fetched data. Final list can be printed to console output, or dumped out to a json file (uncomment the appropriate command).
 
 Similar methods exist to create frequency table for album and tracks. 
