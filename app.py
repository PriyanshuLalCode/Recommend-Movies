import streamlit as st
import pickle
import pandas as pd
import requests # This library allows us to talk to the TMDB website

# 1. FETCH POSTER FUNCTION
def fetch_poster(movie_id):
    # This is the "Door Key" to get data from TMDB
    # REPLACE 'YOUR_API_KEY_HERE' WITH THE KEY YOU COPIED FROM THE WEBSITE!
    api_key = "d5c8af53173f216f30b4671d5f12eaf8" 
    
    # We ask TMDB for the movie details
    response = requests.get(f'https://api.themoviedb.org/3/movie/{movie_id}?api_key={api_key}&language=en-US')
    data = response.json()
    
    # We build the full path to the image
    # 'w500' means we want the image to be 500 pixels wide
    return "https://image.tmdb.org/t/p/w500/" + data['poster_path']

# 2. LOAD DATA
try:
    movies_dict = pickle.load(open('movies.pkl', 'rb'))
    movies = pd.DataFrame(movies_dict)
    similarity = pickle.load(open('similarity.pkl', 'rb'))
except FileNotFoundError:
    st.error("⚠️ Error: Model files not found. Run main.py first!")
    st.stop()

# 3. RECOMMENDATION FUNCTION (Updated to return names AND posters)
# 3. RECOMMENDATION FUNCTION
def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]
    
    recommended_movies = []
    recommended_posters = []
    
    for i in movies_list:
        movie_id = movies.iloc[i[0]].id
        
        # Get the title
        recommended_movies.append(movies.iloc[i[0]].title)
        
        # Get the poster
        try:
            # Try to fetch the real poster
            poster_url = fetch_poster(movie_id)
            recommended_posters.append(poster_url)
        except:
            # If it fails, use this "No Image" picture from Wikipedia (It works everywhere)
            recommended_posters.append("https://upload.wikimedia.org/wikipedia/commons/1/14/No_Image_Available.jpg")
            
    return recommended_movies, recommended_posters
# 4. THE WEBSITE UI
st.title('🎬 Movie Recommender AI')
st.markdown("Select a movie you like, and the AI will recommend 5 similar ones.")

selected_movie_name = st.selectbox(
    'Which movie did you like?',
    movies['title'].values
)

if st.button('Get Recommendations'):
    # Create a loading spinner while fetching images
    with st.spinner('Asking the AI and fetching posters...'):
        names, posters = recommend(selected_movie_name)
        
        st.success(f"Because you liked **{selected_movie_name}**:")
        
        # Create 5 columns to show images side-by-side
        col1, col2, col3, col4, col5 = st.columns(5)
        
        with col1:
            st.text(names[0])
            st.image(posters[0])
        with col2:
            st.text(names[1])
            st.image(posters[1])
        with col3:
            st.text(names[2])
            st.image(posters[2])
        with col4:
            st.text(names[3])
            st.image(posters[3])
        with col5:
            st.text(names[4])
            st.image(posters[4])