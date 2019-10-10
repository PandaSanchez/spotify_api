import requests
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import pandas as pd

# Handle OAuth and credentialization upfront:
client_id = '480fceae19894c98b5d368a47916adcc'
secret = 'c4ef40a7222b4508a00835bc8338dbcb'

client_credentials_manager = SpotifyClientCredentials(client_id=client_id, client_secret=secret) 
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

# Kid A album example:
example_album_id = '19RUXBFyM4PpmrLRdtqWbp'

album_tracks_dict = sp.album_tracks(example_album_id, limit=50, offset=0)

album_api_endpoint = album_tracks_dict['href']
album_artist_profile_url = album_tracks_dict['items'][0]['artists'][0]['external_urls']['spotify']
album_artist_api_endpoint = album_tracks_dict['items'][0]['artists'][0]['href']
album_artist_id = album_tracks_dict['items'][0]['artists'][0]['id']
album_artist_name = album_tracks_dict['items'][0]['artists'][0]['name']
album_artist_type = album_tracks_dict['items'][0]['artists'][0]['type']
album_artist_uri = album_tracks_dict['items'][0]['artists'][0]['uri']
album_artist_available_markets = album_tracks_dict['items'][0]['artists']['available_markets']

print(album_api_endpoint)
print(album_artist_profile_url)
print(album_artist_api_endpoint)
print(album_artist_id)
print(album_artist_name)
print(album_artist_type)
print(album_artist_uri)
print(album_artist_available_markets)
quit()

album_tracks_df = pd.DataFrame(album_tracks_dict)

print(album_tracks_df)

album_tracks_df.to_csv('/Users/richie/Client Engagements - 2019/Epic Seats/SEO Projects/Artist Profiles - Spotify API/album_tracks_example.csv', encoding='utf-8', index=False)
