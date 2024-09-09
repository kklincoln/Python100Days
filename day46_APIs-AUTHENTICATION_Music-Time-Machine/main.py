import os
import requests
from bs4 import BeautifulSoup #beautifulSoup version 4
import pprint
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from dotenv import load_dotenv


#---GET SECRET KEYS FROM .ENV FILE----#
load_dotenv()
#replace spotify_display_name with username
SPOTIFY_DISPLAY_NAME = input("What is your spotify display name?:") #"Tndfr3q"
SPOTIFY_CLIENT_ID = os.environ.get("SPOTIFY_CLIENT_ID")
SPOTIFY_CLIENT_SECRET = os.environ.get("SPOTIFY_CLIENT_SECRET")
URL_REDIRECT = "https://example.com"
OAUTH_AUTHORIZE_URL= 'https://accounts.spotify.com/authorize'
OAUTH_TOKEN_URL= 'https://accounts.spotify.com/api/token'

#----------------------PROMPT USER AND SCRAPE THE TOP 100 TRACKS FROM BILLBOARD.COM ---------------------------------#
# Create an input() prompt that asks what year you would like to travel to in YYY-MM-DD format. e.g.
# URL of the chart on a historical date: https://www.billboard.com/charts/hot-100/2000-08-26
user_date = input("What year would you like to travel to? Enter the date in the following format, YYYY-MM-DD: ")

#Connect to the billboard page for parsing top 100 songs
response = requests.get(url="https://www.billboard.com/charts/hot-100/"+ user_date)
billboard_list = response.text

# scrape the top 100 song titles on that date into a Python List.
soup = BeautifulSoup(billboard_list, "html.parser")
song_name_spans = soup.select("li ul li h3")
song_names = [song.getText().strip() for song in song_name_spans] #Strips the whitespace and returns just the song name

print(song_names)

#----------------------AUTHENTICATE WITH SPOTIFY  ------------------------------------#


sp = spotipy.Spotify(
    auth_manager=SpotifyOAuth(
        client_id=SPOTIFY_CLIENT_ID,
        client_secret=SPOTIFY_CLIENT_SECRET,
        redirect_uri=URL_REDIRECT,
        scope = "playlist-modify-private",
        cache_path="token.txt",
        username=SPOTIFY_DISPLAY_NAME
        )
)
user = sp.current_user() #gathers the information about the userID that linked the URL from redirect page
print(user)
user_id = sp.current_user()["id"] #xpandurmind

#----------------------CREATE LIST OF BILLBOARD TOP 100 SONGS WITH SPOTIFY URI  ------------------------------------#
# HINT 1: You can use the query format "track: {name} year: {YYYY}" to narrow down on a track name from a particular year.
# URI: The resource identifier that you can enter, for example, in the Spotify Desktop client’s search box
            # to locate an artist, album, or track. Example:spotify:track:6rqhFgbbKwnb9MLmUQDhG6
            #URL  Example: http://open.spotify.com/track/6rqhFgbbKwnb9MLmUQDhG6
            #Spotify ID: 6rqhFgbbKwnb9MLmUQDhG6

song_uris =[]
year = user_date.split("-")[0]
for song in song_names:
    result = sp.search(q=f"track:{song} year:{year}", type="track")
    print(result)
    try:
        uri = result["tracks"]["items"][0]["uri"]
        song_uris.append(uri)
    except IndexError:
        print(f"{song} doesn't exist in Spotify. Skipped.")

#---------------------Step 4 - Creating and Adding to Spotify Playlist------------------------#
playlist = sp.user_playlist_create(
    user=user_id,
    name=f"{user_date} Billboard Top 100",
    public=False
)
# print(playlist)
#take the list of song URIs above, add them to the playlist created above, referencing the [id] key:value pair
sp.playlist_add_items(playlist_id=playlist["id"], items=song_uris)


