from flask import Flask, render_template, request
from application import app
from application.features_extraction import *
from application.model import *
import pandas as pd

song_df = pd.read_csv("./datafiles/songs_data2.csv")
complete_features = pd.read_csv("./datafiles/complete_feature_data4.csv")

#render the home page
@app.route("/")
def home():
   return render_template('home.html')

@app.route('/recommend', methods=['POST'])
def recommend_songs():
   #requesting the url form the HTML form
   url = request.form['URL']
   # Getting features from extract function
   df = extract_features(url)
   #get as many recommendations as the user requested
   top_reommendation = recommend_from_playlist(song_df, complete_features, df)
   number_of_records = int(request.form['number_of_records'])
   song_list = []
   for i in range(number_of_records):
      song_list.append([str(top_reommendation.iloc[i,1]) + ' - '+ '"'+str(top_reommendation.iloc[i,4])+'"',
       "https://open.spotify.com/track/"+ str(top_reommendation.iloc[i,-12]).split("/")[-1],
        str(top_reommendation.iloc[i,-1]), str(top_reommendation.iloc[i,7])])
   return render_template('results.html', songs= song_list)