import streamlit as st

# --------- CSS for Background and Layout ---------
def set_bg_hack(bg_url):
    """
    A function to set a background image via CSS in Streamlit.
    """
    st.markdown(
         f"""
         <style>
         .stApp {{
             background: url("{bg_url}");
             background-size: cover;
             background-position: center;
             background-attachment: fixed;
         }}
         .css-18e3th9 {{
             background-color: rgba(0, 0, 0, 0.5); /* Add background transparency for sidebar */
         }}
         .css-1v0mbdj {{
             background-color: rgba(0, 0, 0, 0.7); /* Add background transparency for main content */
             border-radius: 10px;
             padding: 20px;
         }}
         h1, h2, h3, h4, h5, h6 {{
             color: white;  /* Ensure all headings are white for visibility */
         }}
         p {{
             color: white;  /* Ensure all text is white for visibility */
         }}
         </style>
         """,
         unsafe_allow_html=True
     )

# --------- Sidebar ---------
def sidebar():
    st.sidebar.title("🎧 Music Recommendation")
    
    # Authentication (simple mock-up)
    with st.sidebar.form("login_form"):
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        login_btn = st.form_submit_button("Login")
        if login_btn:
            st.sidebar.success(f"Welcome, {username}!")
    
    st.sidebar.subheader("Filters")
    
    # Genre filter
    genres = ['Pop', 'Rock', 'Hip-Hop', 'Classical', 'Jazz', 'Electronic']
    selected_genres = st.sidebar.multiselect("Select Genres", genres)

    # Artist filter
    artist_input = st.sidebar.text_input("Artist name")
    
    # Settings (e.g., dark mode)
    st.sidebar.subheader("Settings")
    dark_mode = st.sidebar.checkbox("Dark Mode", False)

    # Toggle dark mode (you need to implement CSS theme switch manually)
    if dark_mode:
        st.sidebar.write("Dark Mode is activated.")

# --------- Main Area ---------
def main_area():
    # Header Section
    st.title("🎵 Paigeonn Music Recommendation 🎶")
    st.subheader("Welcome back! Discover your next favorite song")
    
    # Search bar
    search_query = st.text_input("Search for a song, artist, or album")
    
    # Recommendation section (sample data here)
    st.subheader("Recommended for you")
    
    # Sample recommendation grid
    col1, col2, col3 = st.columns(3)
    
    # Song Card 1
    with col1:
        st.image("https://via.placeholder.com/150", caption="Song 1", use_column_width=True)
        if st.button("Play Song 1"):
            st.write("Playing Song 1")
    
    # Song Card 2
    with col2:
        st.image("https://via.placeholder.com/150", caption="Song 2", use_column_width=True)
        if st.button("Play Song 2"):
            st.write("Playing Song 2")
    
    # Song Card 3
    with col3:
        st.image("https://via.placeholder.com/150", caption="Song 3", use_column_width=True)
        if st.button("Play Song 3"):
            st.write("Playing Song 3")

    # Song Details section (hidden unless a song is clicked)
    with st.expander("Song Details", expanded=False):
        st.write("Here you can show detailed info about the song: lyrics, artist bio, album art, etc.")

# --------- Footer ---------
def footer():
    st.markdown("---")
    st.write("© 2024 Paigeonn Music • [Privacy Policy](#) • [About](#) • Follow us on [Twitter](#)")

# --------- Main App Function ---------
def main():
    # Set a music-themed background image from a URL
    set_bg_hack("https://example.com/music_background.jpg")
    
    sidebar()
    main_area()
    footer()

if __name__ == "__main__":
    main()