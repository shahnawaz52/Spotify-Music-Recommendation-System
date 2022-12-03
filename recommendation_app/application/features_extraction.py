import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import os
import pandas as pd

def extract_features(URL):
    client_id = os.environ.get('CLIENT_ID')
    client_secret = os.environ.get('CLIENT_SECRET')

    #Soptify credentials to call API
    client_credentials_manager = SpotifyClientCredentials(client_id=client_id,client_secret=client_secret)
    sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)
    
    # split the url to get the playlist ID
    playlist_id = URL.split("/")[4].split("?")[0]
    playlist_tracks_data = sp.playlist_tracks(playlist_id)

    tracks_id = []
    tracks_titles = []
    playlist_tracks_artists = []
    playlist_tracks_first_artists = []

    for track in playlist_tracks_data['items']:
        tracks_id.append(track['track']['id'])
        tracks_titles.append(track['track']['name'])
        artist_list = []
        for artist in track['track']['artists']:
            artist_list.append(artist['name'])
        playlist_tracks_artists.append(artist_list)
        playlist_tracks_first_artists.append(artist_list[0])

    #create a dataframe
    features = sp.audio_features(tracks_id)
    features_df = pd.DataFrame(data=features, columns=features[0].keys())
    features_df['first_artist'] = playlist_tracks_first_artists
    features_df['all_artists'] = playlist_tracks_artists
    features_df['title'] = tracks_titles
    features_df = features_df[['id', 'title', 'first_artist', 'all_artists', 'danceability', 'energy', 'key', 'loudness',
                                'mode', 'acousticness', 'instrumentalness', 'liveness', 'valence', 'tempo',
                                'duration_ms', 'time_signature']]
    return features_df
