import requests
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import pandas as pd


def get_all_artist_albums(artist_uri):
    # Handle OAuth and credentialization upfront:
    client_id = '480fceae19894c98b5d368a47916adcc'
    secret = 'c4ef40a7222b4508a00835bc8338dbcb'

    client_credentials_manager = SpotifyClientCredentials(client_id=client_id, client_secret=secret) 
    sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

    results_dict = sp.artist_albums(artist_uri, limit=50, album_type='album')
    artist_albums_df = pd.DataFrame(results_dict)

    # artist_albums_df = pd.DataFrame(artist_albums_dict)
    # artist_albums_df.to_csv('/Users/richie/Client Engagements - 2019/Epic Seats/SEO Projects/Artist Profiles - Spotify API/artist_albums_test.csv', encoding='utf-8', index=False)
    
    master_artist_albums_df = pd.DataFrame()
    for i, r in artist_albums_df.iterrows():
        album_id = r['items']['id']
        album_name = r['items']['name']
        album_release_date = r['items']['release_date']
        album_release_date_precision = r['items']['release_date_precision']
        album_total_tracks = r['items']['total_tracks']
        album_group = r['items']['album_group']
        album_api_endpoint = r['items']['href']
        album_uri = r['items']['uri']
        album_image = r['items']['images'][0]['url']
        album_type = r['items']['album_type']
        artist_url = r['items']['artists'][0]['external_urls']['spotify']
        artist_api_endpoint = r['items']['artists'][0]['href']
        artist_id = r['items']['artists'][0]['id']
        artist_name = r['items']['artists'][0]['name']
        artist_type = r['items']['artists'][0]['type']
        artist_uri = r['items']['artists'][0]['uri']
        album_available_markets = str(r['items']['available_markets']).replace('[', '').replace(']', '').replace("'", "")

        artist_album_df = pd.DataFrame({'albumid': album_id,
                                        'albumname': album_name,
                                        'albumreleasedate': album_release_date,
                                        'albumreleasedateprecision': album_release_date_precision,
                                        'albumtotaltracks': album_total_tracks,
                                        'albumgroup': album_group,
                                        'albumapiendpoint': album_api_endpoint,
                                        'albumuri': album_uri,
                                        'albumimage': album_image,
                                        'albumtype': album_type,
                                        'artisturl': artist_url,
                                        'artistapiendpoint': artist_api_endpoint,
                                        'artistid': artist_id,
                                        'artistname': artist_name,
                                        'artisttype': artist_type,
                                        'artisturi': artist_uri,
                                        'albumavailablemarkets': album_available_markets}, index=[0])

        master_artist_albums_df = master_artist_albums_df.append(artist_album_df, ignore_index=True)
    
    print("\nAll of the artist's albums:\n")
    print(master_artist_albums_df)


def main():
    # Test URI:
    artist_uri = 'spotify:artist:0OdUWJ0sBjDrqHygGUXeCF'
    get_all_artist_albums(artist_uri)


if __name__ == "__main__":
    main()
