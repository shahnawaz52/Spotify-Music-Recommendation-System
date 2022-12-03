import pandas as pd
import json

#Convert the playlist json data to pandas dataframe
def convert_json_to_raw():
    challenge_json_data = json.loads(open('../music_recommendation_app/data/challenge_set.json').read())
    playlists = challenge_json_data['playlists']
    playlists_df = pd.json_normalize(playlists, record_path=['tracks'], meta=['name'], errors='ignore')
    playlists_df.to_csv('../music_recommendation_app/data/playlist_raw_data.csv')

if __name__ == "__main__":
    convert_json_to_raw()