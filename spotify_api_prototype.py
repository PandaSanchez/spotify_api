import requests
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import pandas as pd


def credentialize():
    # Handle OAuth and credentialization upfront:
    client_id = '480fceae19894c98b5d368a47916adcc'
    secret = 'c4ef40a7222b4508a00835bc8338dbcb'

    client_credentials_manager = SpotifyClientCredentials(client_id=client_id, client_secret=secret) 
    sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

    return sp


def get_artist_profile(sp):
    # Initialize empty master Dataframe:
    master_artist_profile_df = pd.DataFrame()

    # Search for the artist on Spotify API endpoint:
    artist_name = 'Band of Horses'
    artist_search_results_dict = sp.search(q='artist:' + artist_name, type='artist')
    artist_search_results_df = pd.DataFrame(artist_search_results_dict)

    # Get artist URI/ID details:
    artist_uri = artist_search_results_df['artists']['items'][0]['uri']

    """TODO: Get Artist Data"""
    # print(artist_search_results_df['artists'])
    artist_profile_dict = artist_search_results_df['artists']['items'][0]

    artist_profile_url = artist_profile_dict['external_urls']['spotify']
    artist_total_followers = artist_profile_dict['followers']['total']
    artist_followers_href = artist_profile_dict['followers']['href']
    artist_genre_lst = artist_profile_dict['genres']
    artist_api_endpoint = artist_profile_dict['href']
    artist_id = artist_profile_dict['id']
    artist_image_url = artist_profile_dict['images'][0]['url']
    artist_name = artist_profile_dict['name']
    artist_popularity = artist_profile_dict['popularity']
    artist_type = artist_profile_dict['type']
    artist_uri = artist_profile_dict['uri']

    artist_profile_df = pd.DataFrame({'artist_id': artist_id,
                                      'artist_name': artist_name,
                                      'artist_profile_page': artist_profile_url,
                                      'artist_total_followers': artist_total_followers,
                                      'artist_followers_href': artist_followers_href,
                                      'artist_genres': str(artist_genre_lst).replace('[', '').replace(']', '').replace("'", ""),
                                      'artist_api_endpoint': artist_api_endpoint,
                                      'artist_image_url': artist_image_url,
                                      'artist_popularity': artist_popularity,
                                      'artist_type': artist_type,
                                      'artist_uri': artist_uri}, index=[0])

    master_artist_profile_df = master_artist_profile_df.append(artist_profile_df, ignore_index=True)

    master_artist_profile_df.to_csv('/Users/richie/Client Engagements - 2019/Epic Seats/SEO Projects/Artist Profiles - Spotify API/artist_profile_test.csv', encoding='utf-8', index=False)

    print("\n")
    print(master_artist_profile_df)

    return artist_uri


def get_artist_top_tracks(artist_uri, sp):
    """NOTE: GET ARTIST'S TOP TRACKS (one row at a time)"""
    artist_top_track_results = sp.artist_top_tracks(artist_uri)
    artist_top_track_results_df = pd.DataFrame(artist_top_track_results['tracks'])

    top_tracks_master_df = pd.DataFrame()
    for i in list(range(len(artist_top_track_results_df))):
        # Build Track Objects:
        track_api_endpoint = artist_top_track_results_df.iloc[i]['href']
        track_id = artist_top_track_results_df.iloc[i]['id']
        track_name = artist_top_track_results_df.iloc[i]['name']
        track_popularity = artist_top_track_results_df.iloc[i]['popularity']
        track_number = artist_top_track_results_df.iloc[i]['track_number']
        track_preview_url = artist_top_track_results_df.iloc[i]['preview_url']
        track_uri = artist_top_track_results_df.iloc[i]['uri']
        explicit_track = artist_top_track_results_df.iloc[i]['explicit']

        # Build Artist Objects:
        artist_id = artist_top_track_results_df.iloc[i]['artists'][0]['id']
        artist_name = artist_top_track_results_df.iloc[i]['artists'][0]['name']
        artist_profile_url = artist_top_track_results_df.iloc[i]['artists'][0]['external_urls']['spotify']
        artist_api_endpoint = artist_top_track_results_df.iloc[i]['artists'][0]['href']

        # Build Album Objects:
        album_type = artist_top_track_results_df.iloc[i]['album']['album_type']
        album_profile_url = artist_top_track_results_df.iloc[i]['external_urls']['spotify']
        album_api_endoint = artist_top_track_results_df.iloc[i]['album']['href']
        album_id = artist_top_track_results_df.iloc[i]['album']['id']
        album_image = artist_top_track_results_df.iloc[i]['album']['images'][0]['url']
        album_name = artist_top_track_results_df.iloc[i]['album']['name']
        album_no_of_discs = artist_top_track_results_df.iloc[i]['disc_number']
        album_duration_ms = artist_top_track_results_df.iloc[i]['duration_ms']

        # Dataframe Top Track Results for One Row:
        top_track_row_result_df = pd.DataFrame({'track_id': track_id,
                                                'track_name': track_name,
                                                'track_popularity': track_popularity,
                                                'track_number': track_number,
                                                'track_preview': track_preview_url,
                                                'explicit': explicit_track,
                                                'track_uri': track_uri,
                                                'track_api_endpoint': track_api_endpoint,
                                                'artist_id': artist_id,
                                                'artist_name': artist_name,
                                                'artist_profile_page': artist_profile_url,
                                                'artist_api_endpoint': artist_api_endpoint,
                                                'album_id': album_id,
                                                'album_name': album_name,
                                                'album_type': album_type,
                                                'album_number_of_discs': album_no_of_discs,
                                                'album_duration_ms': album_duration_ms,
                                                'album_profile_page': album_profile_url,
                                                'album_image': album_image,
                                                'album_api_endpoint': album_api_endoint}, index=[0])

        top_tracks_master_df = top_tracks_master_df.append(top_track_row_result_df, ignore_index=True)

    print(top_tracks_master_df)

    top_tracks_master_df.to_csv('/Users/richie/Client Engagements - 2019/Epic Seats/SEO Projects/Artist Profiles - Spotify API/artist_top_tracks_test.csv', encoding='utf-8', index=False)


def main():
    try:
        tokenized_sp_object = credentialize()
        artist_uri = get_artist_profile(tokenized_sp_object)
        get_artist_top_tracks(artist_uri, tokenized_sp_object)

    except Exception as e:
        print("An artist on your list did not return results from the Spotify API.")
        pass


if __name__ == "__main__":
    main()
