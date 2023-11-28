import os
import pickle
import streamlit as st
import requests

# Function to fetch movie poster
def fetch_poster(movie_id):
    url = "https://api.themoviedb.org/3/movie/{}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US".format(movie_id)
    data = requests.get(url)
    data = data.json()
    poster_path = data['poster_path']
    full_path = "https://image.tmdb.org/t/p/w500/" + poster_path
    return full_path

# Function to recommend movies
def recommend(movie):
    index = movies[movies['title'] == movie].index[0]
    distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
    recommended_movie_names = []
    recommended_movie_posters = []
    for i in distances[1:6]:
        # fetch the movie poster
        movie_id = movies.iloc[i[0]].movie_id
        recommended_movie_posters.append(fetch_poster(movie_id))
        recommended_movie_names.append(movies.iloc[i[0]].title)

    return recommended_movie_names, recommended_movie_posters

# Header and loading data
st.header('🎬 Movie Recommender System')
movies = pickle.load(open(os.path.join('movie_list.pkl'), 'rb'))
similarity = pickle.load(open(os.path.join('similarity.pkl'), 'rb'))


# Movie selection dropdown
movie_list = movies['title'].values
selected_movie = st.selectbox(
    "Type or select a movie from the dropdown",
    movie_list
)

# Button to show recommendations with style adjustments
if st.button('Show Recommendations', key='recommendations_button', help='Click to get movie recommendations'):
    recommended_movie_names, recommended_movie_posters = recommend(selected_movie)
    
    # Display recommendations in two rows with three columns each
    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown(f"<p class='recommendation-name'><b>{recommended_movie_names[0]}</b></p>", unsafe_allow_html=True)
        st.image(recommended_movie_posters[0])

    with col2:
        st.markdown(f"<p class='recommendation-name'><b>{recommended_movie_names[1]}</b></p>", unsafe_allow_html=True)
        st.image(recommended_movie_posters[1])

    with col3:
        st.markdown(f"<p class='recommendation-name'><b>{recommended_movie_names[2]}</b></p>", unsafe_allow_html=True)
        st.image(recommended_movie_posters[2])

    col4, col5, col6 = st.columns(3)

    with col4:
        st.markdown(f"<p class='recommendation-name'><b>{recommended_movie_names[3]}</b></p>", unsafe_allow_html=True)
        st.image(recommended_movie_posters[3])

    with col5:
        st.markdown(f"<p class='recommendation-name'><b>{recommended_movie_names[4]}</b></p>", unsafe_allow_html=True)
        st.image(recommended_movie_posters[4])
