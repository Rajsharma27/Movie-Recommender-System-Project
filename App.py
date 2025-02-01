import streamlit as st
import pickle
import pandas as pd
import os
import requests

def fetch_movie_details(movie_id):
    api_key = "ab51797faa0023324ad58192ad117ae9"
    movie_url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={api_key}&language=en-US"
    cast_url = f"https://api.themoviedb.org/3/movie/{movie_id}/credits?api_key={api_key}&language=en-US"
    
    movie_data = requests.get(movie_url).json()
    cast_data = requests.get(cast_url).json()
    
    poster_url = "https://image.tmdb.org/t/p/w500/" + movie_data['poster_path']
    summary = movie_data.get('overview', 'No summary available')
    
    cast_list = []
    for member in cast_data.get('cast', [])[:5]:  # Show top 5 cast members
        cast_list.append({
            'name': member['name'],
            'profile': "https://image.tmdb.org/t/p/w500/" + member['profile_path'] if member.get('profile_path') else None
        })
    
    return poster_url, summary, cast_list

def fetch_posters(movie_id):
   response = requests.get('https://api.themoviedb.org/3/movie/{}?api_key=ab51797faa0023324ad58192ad117ae9&language=en-US '.format(movie_id))
   data = response.json()
   return " https://image.tmdb.org/t/p/w500/" +  data['poster_path']
   

movies_dict = pickle.load(open('movies.pkl','rb'))
movies = pd.DataFrame(movies_dict)
similarity = pickle.load(open('similarity.pkl','rb'))

directors_dict = pickle.load(open('director.pkl', 'rb'))

def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)),reverse=True,key=lambda x:x[1])[1:20]

    recommended_movies = []
    recommended_movies_posters = []
    recommended_movies_directors = []
    for i in movies_list:
        movie_id = movies.iloc[i[0]].id 
        recommended_movies.append(movies.iloc[i[0]].title)
        recommended_movies_posters.append(fetch_posters(movie_id))

    return recommended_movies,recommended_movies_posters



st.title('Movie Recommender System ')
st.subheader("Find your next favorite movie!")
selected_movie_name = st.selectbox(
    'Enter Name of Movie',  
    movies['title'].values)

if st.button('Recommend'):
    names, posters = recommend(selected_movie_name)

    for i in range(0, len(names), 5):  
        cols = st.columns(5)
        for j, col in enumerate(cols):
            if i + j < len(names):  
                with col:
                    st.text(names[i + j])
                    
                    st.image(posters[i + j])

if 'selected_movie' in st.session_state:
    movie_details = fetch_movie_details(st.session_state['selected_movie']['id'])
    st.subheader(st.session_state['selected_movie']['title'])
    st.image(movie_details[0], width=300)
    st.write(movie_details[1])
    st.subheader("Cast:")
    for cast in movie_details[2]:
        col1, col2 = st.columns([1, 3])
        with col1:
            if cast['profile']:
                st.image(cast['profile'], width=100)
        with col2:
            st.write(cast['name'])








st.markdown(
    """
    <style>
    body {
        background-image: url("https://t3.ftcdn.net/jpg/10/25/57/76/360_F_1025577629_EPnzUsnnBYENn35cOWUomyTjqRzFbNKh.jpg");
        background-size: cover;
        background-repeat: no-repeat;
        background-attachment: fixed;
    }
    .stApp {
        background-color: rgba(0, 0, 0, 0.5); /* Optional: Add transparency for contrast */
    }
    </style>
    """,
    unsafe_allow_html=True
)