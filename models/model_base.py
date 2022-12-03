import os
from sklearn.metrics.pairwise import cosine_similarity
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

client_id = os.environ.get('CLIENT_ID')
client_secret = os.environ.get('CLIENT_SECRET')

#Soptify credentials to call API
client_credentials_manager = SpotifyClientCredentials(client_id=client_id,client_secret=client_secret)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

# Convert users playlist into single vector
# parameter: (feature_set: dataframe of spotify songs, df: playlist dataframe)
# return: (single vector feature of playlist)
def generate_feature(feature_set, df):
    # features in the playlist
    feature_set_playlist = feature_set[feature_set['id'].isin(df['id'].values)]
    # non-playlist song features
    feature_set_nonplaylist = feature_set[~feature_set['id'].isin(df['id'].values)]
    final_feature_set_playlist = feature_set_playlist.drop(columns = "id")
    return final_feature_set_playlist.sum(axis = 0), feature_set_nonplaylist

# parameter: (df: dataframe, features: single playlist vector, non playlist features: songs not in the playlist)
# return: Top recommendation
def generate_recommendation(df, features, non_playlist_features):    
    df_non_playlist = df[df['track_uri'].isin(non_playlist_features['id'].values)]
    # Compare the cosine similarity of the playlist and the entire collection of songs
    df_non_playlist['sim'] = cosine_similarity(non_playlist_features.drop('id', axis = 1).values, features.values.reshape(1, -1))[:,0]
    top_non_playlist_df = df_non_playlist.sort_values('sim', ascending = False).head(40)
    top_non_playlist_df['url'] = top_non_playlist_df['track_uri'].apply(lambda x: sp.track(x)['album']['images'][1]['url'])
    return top_non_playlist_df

def recommend_from_playlist(songDF, complete_feature_set, playlistDF_test):
    complete_feature_set_playlist_vector, complete_feature_set_nonplaylist = generate_feature(complete_feature_set, playlistDF_test)
    # Generate recommendation
    top_recommendation = generate_recommendation(songDF, complete_feature_set_playlist_vector, complete_feature_set_nonplaylist)
    return top_recommendation
