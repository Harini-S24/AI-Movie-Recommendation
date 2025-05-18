import streamlit as st
import pickle
import pandas as pd
import requests

# Load the data
movies = pickle.load(open('movies.pkl', 'rb'))
similarity = pickle.load(open('similarity.pkl', 'rb'))

# TMDB API to fetch posters safely
def fetch_poster(movie_id):
    api_key = "YOUR_TMDB_API_KEY"  # Replace with your actual TMDB API key
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={api_key}&language=en-US"
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        poster_path = data.get('poster_path')
        if poster_path:
            return "https://image.tmdb.org/t/p/w500/" + poster_path
    except:
        pass
    return "https://via.placeholder.com/500x750?text=No+Image"

# Recommend movies
def recommend(movie):
    if movie not in movies['title'].values:
        return [], []
    
    index = movies[movies['title'] == movie].index[0]
    distances = similarity[index]
    movie_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]

    recommended_titles = []
    recommended_posters = []
    for i in movie_list:
        movie_id = movies.iloc[i[0]].movie_id
        recommended_titles.append(movies.iloc[i[0]].title)
        recommended_posters.append(fetch_poster(movie_id))
    return recommended_titles, recommended_posters

# Streamlit UI
st.title('Movie Recommender System')

selected_movie = st.selectbox("Type or select a movie", movies['title'].values)

if st.button('Show Recommendation'):
    names, posters = recommend(selected_movie)
    
    if not names:
        st.error("No recommendations found for the selected movie.")
    else:
        cols = st.columns(len(names))
        for i in range(len(names)):
            with cols[i]:
                st.text(names[i])
                st.image(posters[i])
