import streamlit as st
import pickle
import pandas as pd
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
    for member in cast_data.get('cast', [])[:5]:  
        cast_list.append({
            'name': member['name'],
            'profile': "https://image.tmdb.org/t/p/w500/" + member['profile_path'] if member.get('profile_path') else None
        })
    
    return poster_url, summary, cast_list

def fetch_posters(movie_id):
    response = requests.get(f'https://api.themoviedb.org/3/movie/{movie_id}?api_key=ab51797faa0023324ad58192ad117ae9&language=en-US')
    data = response.json()
    return "https://image.tmdb.org/t/p/w500/" + data['poster_path']
   
movies_dict = pickle.load(open('movies.pkl','rb'))
movies = pd.DataFrame(movies_dict)
similarity = pickle.load(open('similarity.pkl','rb'))

def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:10]

    recommended_movies = []
    recommended_movies_posters = []
    recommended_movies_ids = []  

    for i in movies_list:
        movie_id = movies.iloc[i[0]].id  
        recommended_movies.append(movies.iloc[i[0]].title)
        recommended_movies_posters.append(fetch_posters(movie_id))
        recommended_movies_ids.append(movie_id)  

    return recommended_movies, recommended_movies_posters, recommended_movies_ids  

st.title('Movie Recommender System')
st.subheader("Find your next favorite movie!")

selected_movie_name = st.selectbox(
    'Enter Name of Movie',  
    movies['title'].values)

if 'selected_movie_id' not in st.session_state:
    st.session_state.selected_movie_id = None

if 'recommendations' not in st.session_state:
    st.session_state.recommendations = None


if st.session_state.selected_movie_id:
    st.subheader("Movie Details")
    poster, summary, cast = fetch_movie_details(st.session_state.selected_movie_id)
    st.image(poster, use_column_width=True)
    st.write(summary)
    
    st.subheader("Top Cast:")
    cols = st.columns(5)
    for idx, actor in enumerate(cast):
        with cols[idx % 5]:  
            if actor['profile']:
                st.image(actor['profile'], width=100)
            st.write(actor['name'])

    if st.button("Back to Recommendations"):
        st.session_state.selected_movie_id = None
        st.rerun()
else:
    if st.button('Recommend'):
        names, posters, movie_ids = recommend(selected_movie_name)
        st.session_state.recommendations = (names, posters, movie_ids)

 
    if st.session_state.recommendations:
        names, posters, movie_ids = st.session_state.recommendations
        st.subheader("Recommended Movies:")
        for i in range(0, len(names), 5):  
            cols = st.columns(5)
            for j, col in enumerate(cols):
                if i + j < len(names):  
                    with col:
                        st.text(names[i + j])
                        st.image(posters[i + j])
                        if st.button(f"See Details ", key=f"details_{i+j}"):  
                            st.session_state.selected_movie_id = movie_ids[i + j]
                            st.rerun()

st.markdown(
    """
    <style>
    body {
        background-image: url("https://t3.ftcdn.net/jpg/10/25/57/76/360_F_1025577629_EPnzUsnnBYENn35cOWUomyTjqRzFbNKh.jpg");
        background-size: cover;
        background-repeat: no-repeat;
        background-attachment:fixed;
    }
    .stApp {
        background-color: rgba(0, 0, 0, 0.5);
    }
    </style>
    """,
    unsafe_allow_html=True  
)
