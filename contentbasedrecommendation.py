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

def main_area():
  # Header Section
  st.title("🎵 Paigeonn Music Recommendation 🎶")
  st.subheader("Welcome back! Discover your next favorite song")
  text = st.selectbox('Select song you want recommendation for', 
                    music_df['name'].values)

  if st.button("Recommend"):
    df = content_based_recommendations(text)
    st.subheader("Recommended for you")
    # Sample recommendation grid
    col1, col2, col3, col4, col5 = st.columns(5)
    # Song Card 1
    with col1:
      st.image("music_11705439.png", caption="Song 1", use_column_width=True)
      st.write("Song 1")
      st.write("Name : " + df['name'][0])
      st.write("Artist : "+df['artists'][0])
      st.write("Popularity : "+str(df['popularity'][0]))
    
    # Song Card 2
    with col2:
      st.image("music_11705439.png", caption="Song 2", use_column_width=True)
      st.write("Song 2")
      st.write("Name : " + df.iloc[1]['name'])
      st.write("Artist : "+df.iloc[1]['artists'])
      st.write("popularity : "+str(df.iloc[1]['popularity']))
    
    # Song Card 3
    with col3:
      st.image("music_11705439.png", caption="Song 3", use_column_width=True)
      st.write("Song 3")
      st.write("Name : " + df.iloc[2]['name'])
      st.write("Artist : "+df.iloc[2]['artists'])
      st.write("popularity : "+str(df.iloc[2]['popularity']))
    
    # Song Card 4
    with col3:
      st.image("music_11705439.png", caption="Song 4", use_column_width=True)
      st.write("Song 4")
      st.write("Name : " + df.iloc[3]['name'])
      st.write("Artist : "+df.iloc[3]['artists'])
      st.write("popularity : "+str(df.iloc[3]['popularity']))

    # Song Card 5
    with col3:
      st.image("music_11705439.png", caption="Song 5", use_column_width=True)
      st.write("Song 5")
      st.write("Name : " + df.iloc[4]['name'])
      st.write("Artist : "+df.iloc[4]['artists'])
      st.write("popularity : "+str(df.iloc[4]['popularity']))

# --------- Footer ---------
def footer():
    st.markdown("---")
    st.write("© 2024 Paigeonn Music • [Privacy Policy](#) • [About](#) • Follow us on [Twitter](#)")


# --------- Main App Function ---------

main_area()
footer() 
