# Spotify-Music-Recommendation-System

https://drive.google.com/file/d/1Xt4i6-yC5HpocDP7E3RxCRy5HCDVGzdI/view?usp=sharing

## Description
This project's objective is to develop a recommendation system that will enable users to find new music based on a playlist or song that they already like. To make sure the model will continue to function successfully in the future, this project starts with data collecting and a self-growing dataset. It then moves on to model deployment.

## Data
For this project, I'm using the Million Playlist Dataset, which, as its name implies, consists of one million playlists. contains a number of songs, and some metadata is included as well, such as the name of the playlist, duration, number of songs, number of artists, etc.



Check out the dataset [here](https://www.aicrowd.com/challenges/spotify-million-playlist-dataset-challenge)

## Data extraction
Getting keys to use will be the first step. For this, we will want a [Spotify for developers](https://developer.spotify.com) account. This equates to having a Spotify account and is not required to have Spotify Premium. Choose "create an app" from the dashboard by going there. The public and private keys needed to use the API are now available to us.

We can obtain a client ID and client secret for this app now that we have one. Both of these serve as a form of username and password for the application and will be needed to login with the Spotify web API for our application. It is best practice to avoid sharing either of these, but avoid sharing the client secret key in particular. To avoid this, we can keep it in a different file that should be Gitignored if you're using Git for version management.

Spotify credentials should be stored the in the a `Spotify.yaml` file with the first line as the **credential id** and the second line as the **secret key**:
```python
Client_id : ************************
client_secret : ************************
```
To access this credentials, please use the following code:
```python
stream= open("Spotify/Spotify.yaml")
spotify_details = yaml.safe_load(stream)
auth_manager = SpotifyClientCredentials(client_id=spotify_details['Client_id'],
                                        client_secret=spotify_details['client_secret'])
sp = spotipy.client.Spotify(auth_manager=auth_manager)
```
## Code
### Data Extraction.ipynb
- This notebook reads the main.json files containing the playlists in order to train the model and generate recommendations.
- The loop_slices() function will go through as many slices as desired to extract the unique track URIs from the playlists for the content-based recommendation system.
- Using the Spotify API for Feature Extraction **(Audio Features, Track Release Date, Track Popularity, Artist Popularity, Artist Genres)** and Saving Results to a CSV Files and Errors to a Log File
```python
f = open('data/audio_features.csv','a')
e=0
for i in tqdm(range(0,len(t_uri),100)):
    try:
     track_feature = sp.audio_features(t_uri[i:i+100])
     track_df = pd.DataFrame(track_feature)
     csv_data = track_df.to_csv(header=False,index=False)
     f.write(csv_data)
    except Exception as error:
        e+=1
        r = open("audio_features_log.txt", "a")
        r.write(datetime.datetime.now().strftime("%d.%b %Y %H:%M:%S")+": "+str(error)+'\n')
        r.close()
        time.sleep(3)
        continue
r = open("audio_features_log.txt", "a")
r.write(datetime.datetime.now().strftime("%d.%b %Y %H:%M:%S")+" _________________________ "+"Total Number Of Errors : "+str(e)+" _________________________ "+'\n')
r.close()
f.close()
```

### Data Preprocessing.ipynb
- This notebook reads the extracted features and merges them into one dataframe.
- Handling missing extraction features and dropping duplicated and irrelevant columns
- Create five point buckets for track and artist popularity and 50 point buckets for the track release date.
```python
df['Track_release_date'] = df['Track_release_date'].apply(lambda x: int(x/50))
```
If I'm listening to music from the 1950s, I'd like the model to recommend music from the same era. 

### Recommendation System.ipynb
- Repeating the extraction features and preprocessing steps for the user's playlist (input)
- If a track from the user's playlist is missing from the dataset, it will be added automatically. 
- TfidfVectorizer was used for the Artist Genres (TF-IDF automatically assigns weights to metadata based on how frequently they appear). 

<img width="1017" alt="tfidf_4" src="https://user-images.githubusercontent.com/107134115/201203710-c1a48e8b-1365-4cc3-bba4-58a1102bafde.png">

- I was first using OneHotEncoder for **Track_release_date, Track_pop, Artist_pop** but I found no difference in the final result other than high memory usage.
- Converting a user playlist to a single vector 
- Cosine similarity is used to compare playlist vectors to song vectors to generate recommendations.

![image](https://user-images.githubusercontent.com/107134115/201203569-6bcd14fd-6704-4ad7-9577-44095bd65f74.png)

- I decided to go with three models. 

 **Model 1** which gives the genera more weight than the audio features

 **Model 2**  which gives equal weight to all features (as a result, playlist languages and genres are ignored)
 
 **Spotify Model**, which is available through the Spotify API

### Reference
- https://medium.com/analytics-vidhya/music-recommender-system-part-2-ff4c3f54cba3
- https://github.com/madhavthaker/spotify-recommendation-system
- https://spotipy.readthedocs.io/en/master/