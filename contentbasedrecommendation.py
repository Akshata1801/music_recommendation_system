import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler
from datetime import datetime
from sklearn.metrics.pairwise import cosine_similarity
import streamlit as st

music_df = pd.read_csv("data.csv")
music_df = music_df.fillna(0)

# Normalize the music features using Min-Max scaling
scaler = MinMaxScaler()
music_features = music_df[['danceability',
                           'energy', 
                           'key', 
                           'loudness',
                           'mode',
                           'speechiness',
                           'acousticness',
                           'instrumentalness',
                           'liveness', 
                           'valence',
                           'tempo']].values
music_features_scaled = scaler.fit_transform(music_features)
music_features_scaled[np.isnan(music_features_scaled)]=0

# Function to calculate weighted popularity scores based on given factors by user
def calculate_weighted_popularity(value,factor):
    if factor == 'loudness':
      avg = music_df.loc[:, 'loudness'].mean()
    elif factor == 'tempo':
      avg = music_df.loc[:, 'tempo'].mean()
    else:
      avg = music_df.loc[:, 'danceability'].mean()

    abs_value = abs(avg - value)
    weight = 1 / (abs_value)
    return weight

def content_based_recommendations(input_song_name, num_recommendations=5):
    if input_song_name not in music_df['name'].values:
        print(f"'{input_song_name}' not found in the dataset. Please enter a valid song name.")
        return
    else:
      print("found")  


    # Get the index of the input song in the music DataFrame
    input_song_index = music_df[music_df['name'] == input_song_name].index[0]
    

    # Calculate the similarity scores based on music features (cosine similarity)
    similarity_scores = cosine_similarity([music_features_scaled[input_song_index]], music_features_scaled)

    # Get the indices of the most similar songs
    similar_song_indices = similarity_scores.argsort()[0][::-1][1:num_recommendations + 1]

    # Get the names of the most similar songs based on content-based filtering
    content_based_recommendations = music_df.iloc[similar_song_indices][['name',
                                                                         'artists',
                                                                         'release_date',
                                                                         'popularity']]

    return content_based_recommendations

# a function to get hybrid recommendations based on weighted popularity
def hybrid_recommendations(input_song_name, factor, num_recommendations=5, alpha=0.5):
    if input_song_name not in music_df['name'].values:
        print(f"'{input_song_name}' not found in the dataset. Please enter a valid song name.")
        return

    # Get content-based recommendations
    content_based_rec = content_based_recommendations(input_song_name, num_recommendations)

    # Get the popularity score of the input song
    popularity_score = music_df.loc[music_df['name'] == input_song_name, 'popularity'].values[0]

    # Calculate the weighted popularity score
    weighted_popularity_score = popularity_score * calculate_weighted_popularity(music_df.loc[music_df['name'] == input_song_name, factor].values[0],factor)

    # Combine content-based and popularity-based recommendations based on weighted popularity
    hybrid_recommendations = content_based_rec
    hybrid_recommendations = pd.concat([hybrid_recommendations, pd.DataFrame([{
        'name': input_song_name,
        'artists': music_df.loc[music_df['name'] == input_song_name, 'artists'].values[0],
        'release_date': music_df.loc[music_df['name'] == input_song_name, 'release_date'].values[0],
        'popularity': weighted_popularity_score
    }])], ignore_index=True)

    print(len(hybrid_recommendations))

    # Sort the hybrid recommendations based on weighted popularity score
    hybrid_recommendations = hybrid_recommendations.sort_values(by='popularity', ascending=False)

    # Remove the input song from the recommendations
    hybrid_recommendations = hybrid_recommendations[hybrid_recommendations['name'] != input_song_name]
    print("after removing input song "+str(len(hybrid_recommendations)))

    return hybrid_recommendations

def main_area():
  # Header Section
  st.title("🎵 Paigeonn Music Recommendation 🎶")
  st.subheader("Welcome back! Discover your next favorite song")
  text = st.selectbox('Select song you want recommendation for', 
                    music_df['name'].values)
  text_other = st.selectbox('Select on what basis, you would prefer song recommendation', 
                     ("tempo", "danceability", "loudness"))

  if st.button("Recommend"):
    df = hybrid_recommendations(text,text_other)
    print(len(df))
    print(df)
    st.subheader("Recommended for you")

    if len(df) == 0:
      st.subheader("There are no recommendations, Please try another song or another factor")
    else:
      ncol = len(df)
      cols = st.columns(ncol)
      wcol = 5
      for i in range(ncol):
        col = cols[i%wcol]
        with col:
          st.image("music_11705439.png", caption="Song", use_column_width=True)
          st.write("Song "+str(i+1))
          st.write("Name : " + df.iloc[i]['name'])
          st.write("Artist : "+df.iloc[i]['artists'])
          st.write("Popularity : "+str(df.iloc[i]['popularity']))


# --------- Footer ---------
def footer():
    st.markdown("---")
    st.write("© 2024 Paigeonn Music • [Privacy Policy](#) • [About](#) • Follow us on [Twitter](#)")


# --------- Main App Function ---------

main_area()
footer() 
