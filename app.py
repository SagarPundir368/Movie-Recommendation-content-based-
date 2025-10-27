import streamlit as st
import pandas as pd
import pickle
import requests

## DEFINE A FUNCTION TO FETCH THE POSTER
def fetch_poster(movie_id):
    response = requests.get('https://api.themoviedb.org/3/movie/{}?api_key=6343ed906199013864ff3cbb0fb6c32e&language=en-US'.format(movie_id))
    data = response.json()
    return "https://image.tmdb.org/t/p/w500/" + data['poster_path']

## DEFINE A FUNCTION WHICH WILL RECOMMEND US THE FIVE MOVIE WHEN WE GIVE IT A MOVIE NAME
def recommender(movie_name):
    movie = movie_name.lower()
    movie_index = df[df['title'] == movie].index[0]
    if movie_index is not None:
        distance = similarity[movie_index]
        enumerate_list = list(enumerate(distance))
        recommender_list = sorted(enumerate_list, reverse=True, key=lambda x: x[
            1])  ## key element help us to sort it on the basis of similarity score not index

        recommended_movie = []
        recommended_movie_poster = []
        for m_index, sim_score in recommender_list[1:6]:
            recommended_movie.append(df.iloc[m_index].title.title())
            recommended_movie_poster.append(fetch_poster(df.iloc[m_index].movie_id))
        return recommended_movie, recommended_movie_poster
    else:
        return "SORRY WE HAVE NO RECOMMENDATION FOR THIS ONE, HOPE YOU DON'T MIND!!🥺🥺🥺"

similarity = pickle.load(open('similarity.pkl','rb'))
st.title('Movie Recommender System')

df = pd.read_csv('movies.csv')
Movie_list = df['title'].apply(lambda x: x.title()).values

Query_movie = st.selectbox('Select Movie Name', Movie_list)

if st.button('Recommend me some Similar movies'):
    recommendations,poster = recommender(Query_movie)
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        st.text(recommendations[0])
        st.image(poster[0])

    with col2:
        st.text(recommendations[1])
        st.image(poster[1])

    with col3:
        st.text(recommendations[2])
        st.image(poster[2])

    with col4:
        st.text(recommendations[3])
        st.image(poster[3])

    with col5:
        st.text(recommendations[4])
        st.image(poster[4])


