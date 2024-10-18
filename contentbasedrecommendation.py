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
print("music features scaled")
print(music_features_scaled)
music_features_scaled = music_features_scaled.fillna(0)

def content_based_recommendations(input_song_name, num_recommendations=5):
    if input_song_name not in music_df['name'].values:
        print(f"'{input_song_name}' not found in the dataset. Please enter a valid song name.")
        return
    else:
      print("found")  


    # Get the index of the input song in the music DataFrame
    input_song_index = music_df[music_df['name'] == input_song_name].index[0]
    print("found matches")
    print(music_features_scaled[input_song_index])
    print(music_features_scaled)
    

    # Calculate the similarity scores based on music features (cosine similarity)
    similarity_scores = cosine_similarity([music_features_scaled[input_song_index]], music_features_scaled,nan_policy='propagate')

    # Get the indices of the most similar songs
    similar_song_indices = similarity_scores.argsort()[0][::-1][1:num_recommendations + 1]

    # Get the names of the most similar songs based on content-based filtering
    content_based_recommendations = music_df.iloc[similar_song_indices][['name',
                                                                         'artists',
                                                                         'relase_date',
                                                                         'popularity']]

    return content_based_recommendations

st.header("Content-Type")
text = st.selectbox('Select song you want recommendation for', 
                    music_df['name'].values)

if st.button("Recommend"):
    df = content_based_recommendations(text)
    st.dataframe(df)