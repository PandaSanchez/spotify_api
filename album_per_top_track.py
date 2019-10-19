import requests
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import pandas as pd


def get_album_tracks(album_id, incoming_track_name):
    # Handle OAuth and credentialization upfront:
    client_id = '480fceae19894c98b5d368a47916adcc'
    secret = 'c4ef40a7222b4508a00835bc8338dbcb'

    client_credentials_manager = SpotifyClientCredentials(client_id=client_id, client_secret=secret) 
    sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

    album_tracks_dict = sp.album_tracks(album_id, limit=50, offset=0)
    album_tracks_df = pd.DataFrame(album_tracks_dict)

    master_album_tracks_df = pd.DataFrame()
    for ind, row in album_tracks_df.iterrows():
        album_api_endpoint = row['href']
        album_artist_profile_url = row['items']['artists'][0]['external_urls']['spotify']
        album_artist_api_endpoint = row['items']['artists'][0]['href']
        album_artist_id = row['items']['artists'][0]['id']
        album_artist_name = row['items']['artists'][0]['name']
        album_artist_type = row['items']['artists'][0]['type']
        album_artist_uri = row['items']['artists'][0]['uri']
        album_artist_available_markets = str(row['items']['available_markets']).replace('[', '').replace(']', '').replace("'", "")
        album_disc_number = row['items']['disc_number']
        album_duration_ms = row['items']['duration_ms']

        track_explicit = row['items']['explicit']
        track_url = row['items']['external_urls']['spotify']
        track_api_endpoint = row['items']['href']
        track_id = row['items']['id']
        track_is_local = row['items']['is_local']
        track_name = row['items']['name']
        track_preview_url = row['items']['preview_url']
        track_number = row['items']['track_number']
        track_type = row['items']['type']
        track_uri = row['items']['uri']

        album_tracks_df = pd.DataFrame({'track_id': track_id,
                                        'track_name': track_name,
                                        'track_number': track_number,
                                        'track_explicit': track_explicit,
                                        'track_url': track_url,
                                        'track_preview_url': track_preview_url,
                                        'track_api_endpoint': track_api_endpoint,
                                        'track_uri': track_uri,
                                        'track_type': track_type,
                                        'track_is_local': track_is_local,
                                        'album_id': album_id,
                                        'album_api_endpoint': album_api_endpoint,
                                        'album_artist_profile_url': album_artist_profile_url,
                                        'album_artist_api_endpoint': album_artist_api_endpoint,
                                        'album_artist_id': album_artist_id,
                                        'album_artist_name': album_artist_name,
                                        'album_artist_type': album_artist_type,
                                        'album_artist_uri': album_artist_uri,
                                        'album_artist_available_markets': album_artist_available_markets,
                                        'album_disc_number': album_disc_number,
                                        'album_duration_ms': album_duration_ms}, index=[0])

        master_album_tracks_df = master_album_tracks_df.append(album_tracks_df, ignore_index=True)

    master_album_tracks_df['top_track'] = incoming_track_name

    print(f"\nHere's an album associated with one of the artist's top track, {incoming_track_name}:\n")
    print(master_album_tracks_df)
    # master_album_tracks_df.to_csv('/Users/richie/Client Engagements - 2019/Epic Seats/SEO Projects/Artist Profiles - Spotify API/master_album_tracks_example.csv', encoding='utf-8', index=False)
